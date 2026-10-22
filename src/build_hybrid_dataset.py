"""Build hybrid training dataset combining:
1. Real CWRU lab dataset (.mat)
2. Real XJTU-SY lab dataset (.csv)
3. Simulated physics dataset
Output saved to data_hybrid/train.npz and data_hybrid/val.npz
"""
import os
import sys
from pathlib import Path
import json
import numpy as np
import scipy.io as sio
from scipy.signal import resample
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mech_config import FS, N_SAMPLES, CLASSES, RUL_CAP_H
from bearing_physics import physics_features
import simulate

CWRU_DIR = Path("real_dataset_from_lab/CWRU")
XJTU_DIR = Path("real_dataset_from_lab/XJTU-SY/XJTU-SY_Bearing_Datasets")

def extract_cwru_samples():
    """Extract 16,000-sample windows from CWRU .mat files."""
    records = {k: [] for k in ["signals", "feats", "cls", "deg", "rul", "rpm", "bearing"]}
    if not CWRU_DIR.exists():
        print("CWRU directory not found, skipping...")
        return records

    cwru_files = sorted(list(CWRU_DIR.glob("*.mat")))
    print(f"Processing {len(cwru_files)} CWRU files...")

    for fpath in cwru_files:
        fname = fpath.stem
        # Determine fault class and severity
        if fname.startswith("Normal"):
            fault_cls = "normal"
            deg = 0.05
            rul = 350.0
        elif fname.startswith("IR"):
            fault_cls = "inner_race"
            sev_code = fname[2:5]
            deg = 0.35 if "007" in sev_code else (0.65 if "014" in sev_code else 0.90)
            rul = max(10.0, 150.0 * (1.0 - deg))
        elif fname.startswith("OR"):
            fault_cls = "outer_race"
            sev_code = fname[2:5]
            deg = 0.35 if "007" in sev_code else (0.65 if "014" in sev_code else 0.90)
            rul = max(10.0, 150.0 * (1.0 - deg))
        elif fname.startswith("B"):
            fault_cls = "ball"
            sev_code = fname[1:4]
            deg = 0.35 if "007" in sev_code else (0.65 if "014" in sev_code else 0.90)
            rul = max(10.0, 150.0 * (1.0 - deg))
        else:
            continue

        try:
            mat = sio.loadmat(str(fpath))
            de_keys = [k for k in mat.keys() if "DE_time" in k]
            if not de_keys:
                de_keys = [k for k in mat.keys() if not k.startswith("__") and isinstance(mat[k], np.ndarray) and mat[k].size > 5000]
            if not de_keys:
                continue

            sig_raw = mat[de_keys[0]].ravel().astype(np.float32)
            rpm_keys = [k for k in mat.keys() if "RPM" in k]
            rpm = float(mat[rpm_keys[0]].ravel()[0]) if rpm_keys else 1750.0
            if rpm < 1000:
                rpm = 1750.0

            # CWRU is recorded at 12 kHz (drive end 12k)
            # Resample from 12000 to 16000 Hz
            new_len = int(len(sig_raw) * 16000 / 12000)
            sig_resampled = resample(sig_raw, new_len).astype(np.float32)

            # Slice into windows of length 16,000 with 50% overlap
            step = 8000
            for start in range(0, len(sig_resampled) - N_SAMPLES + 1, step):
                window = sig_resampled[start : start + N_SAMPLES]
                # Normalize window
                w_std = np.std(window)
                if w_std > 1e-6:
                    window = (window - np.mean(window)) / w_std

                feats = physics_features(window, FS, rpm, "6205")
                records["signals"].append(window.astype(np.float16))
                records["feats"].append(feats)
                records["cls"].append(CLASSES.index(fault_cls))
                records["deg"].append(float(deg))
                records["rul"].append(float(min(rul, RUL_CAP_H)))
                records["rpm"].append(float(rpm))
                records["bearing"].append("6205")

        except Exception as e:
            print(f"Error processing {fname}: {e}")

    print(f"Extracted {len(records['cls'])} samples from CWRU")
    return records


def extract_xjtu_samples(max_samples_per_bearing=30):
    """Extract sample windows from XJTU-SY run-to-failure dataset."""
    records = {k: [] for k in ["signals", "feats", "cls", "deg", "rul", "rpm", "bearing"]}
    if not XJTU_DIR.exists():
        print("XJTU-SY directory not found, skipping...")
        return records

    # Look for subfolders like 35Hz12kN/Bearing1_1, etc.
    bearing_folders = [p for p in XJTU_DIR.rglob("Bearing*") if p.is_dir()]
    print(f"Found {len(bearing_folders)} XJTU-SY bearing run-to-failure runs...")

    for b_folder in bearing_folders:
        csv_files = sorted(list(b_folder.glob("*.csv")), key=lambda p: int(p.stem) if p.stem.isdigit() else 0)
        if not csv_files:
            continue

        total_files = len(csv_files)
        # Operating condition RPM: 35Hz = 2100, 37.5Hz = 2250, 40Hz = 2400
        parent_name = b_folder.parent.name
        rpm = 2400.0 if "40Hz" in parent_name else (2250.0 if "37.5Hz" in parent_name else 2100.0)

        # Sample across the lifetime
        indices = np.linspace(0, total_files - 1, min(max_samples_per_bearing, total_files), dtype=int)
        for idx in indices:
            csv_path = csv_files[idx]
            lifetime_ratio = (idx + 1) / total_files
            try:
                df = pd.read_csv(csv_path)
                col = "Horizontal_vibration_signals" if "Horizontal_vibration_signals" in df.columns else df.columns[0]
                sig_raw = df[col].to_numpy().astype(np.float32)

                # XJTU-SY is sampled at 25.6 kHz. Resample to 16 kHz
                new_len = int(len(sig_raw) * 16000 / 25600)
                sig_resampled = resample(sig_raw, new_len).astype(np.float32)

                if len(sig_resampled) < N_SAMPLES:
                    continue
                window = sig_resampled[:N_SAMPLES]
                w_std = np.std(window)
                if w_std > 1e-6:
                    window = (window - np.mean(window)) / w_std

                # Outer race fault typically occurs at end of XJTU-SY tests
                if lifetime_ratio < 0.6:
                    fault_cls = "normal"
                    deg = 0.05 * (lifetime_ratio / 0.6)
                else:
                    fault_cls = "outer_race"
                    deg = 0.05 + 0.95 * ((lifetime_ratio - 0.6) / 0.4) ** 2

                rul = max(1.0, 350.0 * (1.0 - lifetime_ratio))
                feats = physics_features(window, FS, rpm, "6205")

                records["signals"].append(window.astype(np.float16))
                records["feats"].append(feats)
                records["cls"].append(CLASSES.index(fault_cls))
                records["deg"].append(float(deg))
                records["rul"].append(float(min(rul, RUL_CAP_H)))
                records["rpm"].append(float(rpm))
                records["bearing"].append("6205")

            except Exception as e:
                pass

    print(f"Extracted {len(records['cls'])} samples from XJTU-SY")
    return records


def build_hybrid_dataset(out_dir="data_hybrid", sim_units=80, seed=42):
    """Combine CWRU, XJTU-SY and simulated physics into train and val splits."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    # 1. Real CWRU
    cwru = extract_cwru_samples()
    # 2. Real XJTU-SY
    xjtu = extract_xjtu_samples()

    # Combine real data
    all_real = {k: cwru[k] + xjtu[k] for k in cwru}
    print(f"Total real lab samples: {len(all_real['cls'])}")

    # 3. Simulate baseline data
    print(f"Generating {sim_units} simulated baseline units...")
    sim_data = simulate.generate_units(sim_units, snapshots=20, seed=seed, bearings=("6205",), desc="sim")

    # Stack real data
    real_arrays = {
        "signals": np.stack(all_real["signals"]) if all_real["signals"] else np.empty((0, N_SAMPLES), np.float16),
        "feats": np.stack(all_real["feats"]) if all_real["feats"] else np.empty((0, 17), np.float32),
        "cls": np.array(all_real["cls"], np.int64),
        "deg": np.array(all_real["deg"], np.float32),
        "rul": np.array(all_real["rul"], np.float32),
        "rpm": np.array(all_real["rpm"], np.float32),
        "bearing": np.array(all_real["bearing"]),
    }

    # Merge real + sim
    n_real = len(real_arrays["cls"])
    n_sim = len(sim_data["cls"])
    print(f"Merging {n_real} real lab samples + {n_sim} physics simulation samples = {n_real + n_sim} total samples")

    merged = {
        "signals": np.concatenate([real_arrays["signals"], sim_data["signals"]]),
        "feats": np.concatenate([real_arrays["feats"], sim_data["feats"]]),
        "cls": np.concatenate([real_arrays["cls"], sim_data["cls"]]),
        "deg": np.concatenate([real_arrays["deg"], sim_data["deg"]]),
        "rul": np.concatenate([real_arrays["rul"], sim_data["rul"]]),
        "rpm": np.concatenate([real_arrays["rpm"], sim_data["rpm"]]),
        "bearing": np.concatenate([real_arrays["bearing"], sim_data["bearing"]]),
    }

    # Stratified shuffle split: 80% train, 20% val
    indices = np.arange(len(merged["cls"]))
    rng.shuffle(indices)

    split_idx = int(0.82 * len(indices))
    train_idx = indices[:split_idx]
    val_idx = indices[split_idx:]

    train_data = {k: merged[k][train_idx] for k in merged}
    val_data = {k: merged[k][val_idx] for k in merged}

    np.savez(out_path / "train.npz", **train_data)
    np.savez(out_path / "val.npz", **val_data)

    meta = {
        "train": {
            "samples": int(len(train_data["cls"])),
            "class_counts": {c: int((train_data["cls"] == i).sum()) for i, c in enumerate(CLASSES)},
        },
        "val": {
            "samples": int(len(val_data["cls"])),
            "class_counts": {c: int((val_data["cls"] == i).sum()) for i, c in enumerate(CLASSES)},
        },
    }
    (out_path / "meta.json").write_text(json.dumps(meta, indent=2))
    print("Hybrid dataset built successfully:")
    print(json.dumps(meta, indent=2))
    return meta

if __name__ == "__main__":
    build_hybrid_dataset()
