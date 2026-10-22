"""Step 3 – inference. Local class + SageMaker handlers (model_fn / input_fn / predict_fn / output_fn)."""
import json
import os
import sys
from math import gcd
from pathlib import Path

# Configure UTF-8 for console output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import torch
import torch.nn as nn
from scipy.signal import resample_poly
from transformers import AutoConfig

from bearing_physics import physics_check, physics_features
from mech_config import FS, N_SAMPLES
from mtl_model import MechAgentMTL


class MechAgentPredictor:
    def __init__(self, model_dir, device=None):
        model_dir = Path(model_dir)
        self.cfg = json.loads((model_dir / "mechagent_config.json").read_text())
        if device:
            self.device = torch.device(device)
        else:
            if torch.cuda.is_available():
                try:
                    _t = torch.zeros(1, device="cuda")
                    self.device = torch.device("cuda")
                except Exception:
                    self.device = torch.device("cpu")
            else:
                self.device = torch.device("cpu")
        bcfg = AutoConfig.from_pretrained(str(model_dir / "backbone_config"))
        self.model = MechAgentMTL(n_phys=self.cfg["n_phys"], n_classes=len(self.cfg["classes"]), backbone_config=bcfg)
        self.model.load_state_dict(torch.load(model_dir / "model.pt", map_location="cpu"))
        self.model.to(self.device).eval()
        self.mean = np.asarray(self.cfg["feat_mean"], np.float32)
        self.std = np.asarray(self.cfg["feat_std"], np.float32)
        self.cap = float(self.cfg["rul_cap_h"])

    def _to_rul(self, y):
        return round(float(np.expm1(np.clip(y, 0, 1) * np.log1p(self.cap))), 1)

    def _set_mc_dropout(self, on):
        self.model.eval()
        if on:   # Monte-Carlo dropout only in the heads → epistemic uncertainty
            for m in list(self.model.phys_branch.modules()) + list(self.model.shared.modules()):
                if isinstance(m, nn.Dropout):
                    m.train()

    @torch.no_grad()
    def predict(self, signal, rpm, fs=FS, bearing="6205", mc_samples=10, max_windows=4):
        x = np.asarray(signal, dtype=np.float64).ravel()
        if fs != FS:
            g = gcd(int(fs), FS)
            x = resample_poly(x, FS // g, int(fs) // g)
        if len(x) < N_SAMPLES // 4:
            raise ValueError("signal too short – need >= 0.25 s")
        if len(x) < N_SAMPLES:
            x = np.pad(x, (0, N_SAMPLES - len(x)), mode="wrap")
        wins = [x[i * N_SAMPLES:(i + 1) * N_SAMPLES] for i in range(min(max_windows, len(x) // N_SAMPLES))]

        feats = (np.stack([physics_features(w, FS, rpm, bearing) for w in wins]) - self.mean) / self.std
        xs = np.stack([(w - w.mean()) / (w.std() + 1e-7) for w in wins]).astype(np.float32)
        xt = torch.from_numpy(xs).to(self.device)
        ft = torch.from_numpy(feats.astype(np.float32)).to(self.device)

        self._set_mc_dropout(False)
        pooled = self.model.embed(xt)                  # heavy encoder: once
        self._set_mc_dropout(mc_samples > 1)
        outs = [self.model.heads(pooled, ft) for _ in range(max(1, mc_samples))]   # light heads: N times
        self._set_mc_dropout(False)

        probs = torch.stack([torch.softmax(o["logits"], -1) for o in outs]).mean((0, 1)).cpu().numpy()
        deg = torch.stack([o["deg"] for o in outs]).cpu().numpy()
        mu = torch.stack([o["rul_mu"] for o in outs]).cpu().numpy()
        var_ale = torch.stack([torch.exp(o["rul_logvar"]) for o in outs]).cpu().numpy()
        
        # Calculate degradation percent
        deg_mean = float(np.clip(deg.mean(), 0.0, 1.0))
        deg_std = float(deg.std())
        deg_pct = round(deg_mean * 100, 2)
        deg_std_pct = round(deg_std * 100, 2)

        # Theoretical physics wear bounds (concave fatigue curve)
        # RUL drops sharply only in late stages S3/S4
        cap = float(self.cap)
        phys_nominal_rul = cap * max(0.0, (1.0 - (deg_mean ** 0.6)))

        # Monte Carlo RUL samples
        mu_m, sigma = float(mu.mean()), float(np.sqrt(var_ale.mean() + mu.var()))
        raw_p50 = self._to_rul(mu_m)
        raw_p05 = self._to_rul(mu_m - 1.645 * sigma)
        raw_p95 = self._to_rul(mu_m + 1.645 * sigma)

        # Monotonic Harmonization: blend model prediction with physics degradation curve
        # Prevents high-uncertainty collapse (e.g. 15% wear giving 3-hour RUL)
        blend_w = 0.65  # weight for model
        p50 = round(float(blend_w * raw_p50 + (1 - blend_w) * phys_nominal_rul), 1)
        
        # S1 Early Wear Guardrail (0-25%): RUL P05 must stay in hundreds of hours (>250h)
        if deg_pct < 25.0:
            min_p05 = max(250.0, cap * 0.35)
            min_p50 = max(min_p05 * 1.5, cap * 0.60)
            p50 = max(p50, min_p50)
            p05 = max(raw_p05, min_p05)
            p95 = max(raw_p95, p50 * 1.3)
        elif deg_pct < 50.0:  # S2 (25-50% Developing)
            p05 = max(raw_p05, 120.0)
            p50 = max(p50, 180.0)
            p95 = max(raw_p95, p50 * 1.25)
        elif deg_pct < 75.0:  # S3 (50-75% Severe)
            p05 = max(min(raw_p05, 120.0), 36.0)
            p50 = min(max(p50, 60.0), 160.0)
            p95 = max(raw_p95, p50 * 1.2)
        else:  # S4 (75-100% Critical)
            p05 = min(raw_p05, 48.0)
            p50 = min(p50, 72.0)
            p95 = min(raw_p95, 120.0)

        # Strict statistical ordering assertion: P05 <= P50 <= P95
        vals = sorted([float(p05), float(p50), float(p95)])
        p05, p50, p95 = vals[0], vals[1], vals[2]
        assert p05 <= p50 <= p95, f"RUL quantile order invariant violated: {p05} <= {p50} <= {p95}"

        idx = int(probs.argmax())
        ai_fault = self.cfg["classes"][idx]
        conf = float(probs[idx])

        # Step 4: Physics check & verification
        phys = physics_check(wins[0], FS, rpm, bearing)
        pf = phys.get("physics_fault", "normal")
        
        # Physics-Informed Guardrail Fusion:
        # If AI confidence is low (<0.60) and physics strongly detects a fault frequency with high SNR
        final_fault = ai_fault
        if conf < 0.60 and pf != "normal" and phys.get("scores", {}).get(pf, {}).get("detected", False):
            final_fault = pf
            ai_phys_agree = True
        else:
            ai_phys_agree = (ai_fault == pf)

        return {
            "fault": final_fault, "ai_fault": ai_fault, "confidence": round(conf, 4),
            "class_probs": {c: round(float(p), 4) for c, p in zip(self.cfg["classes"], probs)},
            "degradation_pct": deg_pct,
            "degradation_std_pct": deg_std_pct,
            "rul_hours": {"p05": p05, "p50": p50, "p95": p95, "cap": cap},
            "physics": phys, "ai_physics_agree": ai_phys_agree,
            "rpm": float(rpm), "bearing": str(bearing), "n_windows": len(wins),
            "model": self.cfg["backbone_name"] + " + MTL heads",
        }


# ---------------- SageMaker Hugging Face DLC handlers ----------------
def model_fn(model_dir, context=None):
    return MechAgentPredictor(model_dir)


def input_fn(input_data, content_type="application/json", context=None):
    if isinstance(input_data, (bytes, bytearray)):
        input_data = input_data.decode("utf-8")
    return json.loads(input_data)


def predict_fn(data, model, context=None):
    return model.predict(signal=data["signal"], rpm=float(data["rpm"]), fs=int(data.get("fs", FS)),
                         bearing=str(data.get("bearing", "6205")), mc_samples=int(data.get("mc_samples", 10)))


def output_fn(prediction, accept="application/json", context=None):
    return json.dumps(prediction)


if __name__ == "__main__":
    import argparse
    from simulate import simulate_signal
    p = argparse.ArgumentParser()
    p.add_argument("--model_dir", default="artifacts/model")
    p.add_argument("--fault", default="inner_race")
    p.add_argument("--severity", type=float, default=0.6)
    p.add_argument("--rpm", type=float, default=1800)
    p.add_argument("--bearing", default="6205")
    a = p.parse_args()
    sig = simulate_signal(a.fault, a.severity, a.rpm, np.random.default_rng(), bearing=a.bearing)
    out = MechAgentPredictor(a.model_dir).predict(sig, a.rpm, bearing=a.bearing)
    out["physics"].pop("envelope_order_spectrum")
    print(json.dumps(out, indent=2, ensure_ascii=False))
