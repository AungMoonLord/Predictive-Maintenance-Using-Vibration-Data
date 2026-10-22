"""Seed real XJTU-SY Run-to-Failure degradation trajectory into vibration_telemetry."""
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from db import get_db
from real_dataset import discover_xjtu_conditions, load_xjtu_csv

BKK = timezone(timedelta(hours=7))


def seed_real_xjtu_history(machine_id="PUMP-01", condition="40Hz10kN", bearing="Bearing3_4", num_snapshots=25):
    db = get_db()
    tree = discover_xjtu_conditions()
    if condition not in tree or bearing not in tree[condition]:
        print(f"Dataset {condition}/{bearing} not found, generating simulated baseline...")
        return

    files = tree[condition][bearing]
    total_files = len(files)
    print(f"Seeding from XJTU-SY: {condition}/{bearing} ({total_files} files)")

    # Sample snapshots evenly
    indices = np.linspace(0, total_files - 1, num_snapshots, dtype=int)
    now = datetime.now(BKK)

    for step_idx, i in enumerate(indices):
        f = files[i]
        sig, rpm, deg_pct, rul_h = load_xjtu_csv(f)
        
        # Calculate signal statistics
        rms = float(np.sqrt(np.mean(sig ** 2)))
        kurt = float(np.mean((sig - np.mean(sig)) ** 4) / ((np.std(sig) + 1e-7) ** 4))
        
        # Determine fault label based on wear
        if deg_pct < 20.0:
            fault = "normal"
            conf = 0.95
            urgency = "NORMAL"
        elif deg_pct < 50.0:
            fault = "outer_race"
            conf = 0.82
            urgency = "PLAN_MAINTENANCE"
        elif deg_pct < 80.0:
            fault = "outer_race"
            conf = 0.91
            urgency = "URGENT"
        else:
            fault = "outer_race"
            conf = 0.98
            urgency = "EMERGENCY" if kurt > 4.5 else "CRITICAL"

        # Timestamp spacing (e.g. 1 hour per snapshot leading up to now)
        ts = (now - timedelta(hours=int(num_snapshots - step_idx))).isoformat()
        
        rul_p50 = float(rul_h)
        rul_p05 = round(max(1.0, rul_p50 * 0.4), 1)
        rul_p95 = round(rul_p50 * 1.6, 1)

        db.log_telemetry(
            machine_id=machine_id,
            rpm=float(rpm),
            rms=round(rms, 4),
            kurtosis=round(kurt, 2),
            predicted_fault=fault,
            confidence=conf,
            degradation_pct=deg_pct,
            rul_p05=rul_p05,
            rul_p50=rul_p50,
            rul_p95=rul_p95,
            urgency=urgency,
            timestamp=ts
        )

    print(f"Successfully seeded {len(indices)} telemetry records for {machine_id}")


if __name__ == "__main__":
    seed_real_xjtu_history("PUMP-01")
    seed_real_xjtu_history("TEST-RIG-01")
