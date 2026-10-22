"""Loader, scanner, and preprocessor for real lab datasets: CWRU and XJTU-SY.
Supports recursive discovery (rglob), numerical sequence sorting,
sampling rate harmonization (resample_poly), and metadata extraction.
"""
import io
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import scipy.io as sio
from scipy.signal import resample_poly

from bearing_physics import get_bearing, physics_features, time_features
from mech_config import FS, N_SAMPLES

# Base directory for datasets
DEFAULT_LAB_DIR = Path(__file__).resolve().parents[1] / "real_dataset_from_lab"

# CWRU Fault Label Mapping
CWRU_FAULT_MAP = {
    "Normal": ("normal", 0.02),
    "B007": ("ball", 0.35),
    "B014": ("ball", 0.60),
    "B021": ("ball", 0.85),
    "IR007": ("inner_race", 0.35),
    "IR014": ("inner_race", 0.60),
    "IR021": ("inner_race", 0.85),
    "OR007": ("outer_race", 0.35),
    "OR014": ("outer_race", 0.60),
    "OR021": ("outer_race", 0.85),
}

# XJTU-SY Operating Condition Parsing
XJTU_CONDITION_RPM = {
    "35Hz12kN": (2100.0, 12.0),
    "37.5Hz11kN": (2250.0, 11.0),
    "40Hz10kN": (2400.0, 10.0),
}


# ==============================================================================
# 1. CWRU Dataset Discovery & Loading
# ==============================================================================
def discover_cwru_files(base_dir: Optional[Path] = None) -> List[Path]:
    """Find all CWRU .mat files recursively using rglob."""
    root = Path(base_dir or (DEFAULT_LAB_DIR / "CWRU"))
    if not root.exists():
        return []
    return sorted(list(root.rglob("*.mat")), key=lambda p: p.name.lower())


def load_cwru_mat(file_path_or_bytes: Union[str, Path, bytes]) -> Tuple[np.ndarray, float, str, float]:
    """Load a CWRU .mat file.
    Returns:
        signal (resampled to 16 kHz), rpm, fault_class, ground_truth_severity
    """
    if isinstance(file_path_or_bytes, (str, Path)):
        p = Path(file_path_or_bytes)
        fname = p.stem
        mat = sio.loadmat(str(p))
    else:
        fname = getattr(file_path_or_bytes, "name", "unknown")
        mat = sio.loadmat(io.BytesIO(file_path_or_bytes))

    # Identify drive-end acceleration signal
    de_keys = [k for k in mat.keys() if "DE_time" in k]
    if not de_keys:
        de_keys = [k for k in mat.keys() if not k.startswith("__")
                   and isinstance(mat[k], np.ndarray) and mat[k].ndim <= 2 and mat[k].size > 5000]
    if not de_keys:
        raise ValueError(f"No vibration time-series found in CWRU file: {fname}")

    sig_raw = mat[de_keys[0]].ravel().astype(np.float32)

    # Detect RPM
    rpm_keys = [k for k in mat.keys() if "RPM" in k or "rpm" in k]
    rpm = 1750.0
    if rpm_keys:
        try:
            val = float(mat[rpm_keys[0]].ravel()[0])
            if 600 <= val <= 4000:
                rpm = val
        except Exception:
            pass

    # Detect fault class from filename
    fault = "normal"
    sev = 0.02
    for prefix, (f_cls, f_sev) in CWRU_FAULT_MAP.items():
        if fname.startswith(prefix) or prefix in fname:
            fault = f_cls
            sev = f_sev
            break

    # Determine native sampling rate (CWRU drive end is typically 12 kHz)
    # Resample 12 kHz -> 16 kHz using exact polyphase filter (ratio 4/3)
    sig_16k = resample_poly(sig_raw, 4, 3).astype(np.float32)
    return sig_16k, rpm, fault, sev


# ==============================================================================
# 2. XJTU-SY Dataset Discovery & Loading (Numerical Sequence Sorting)
# ==============================================================================
def discover_xjtu_conditions(base_dir: Optional[Path] = None) -> Dict[str, Dict[str, List[Path]]]:
    """Discover XJTU-SY conditions, bearings, and files sorted numerically.
    Structure: {condition_name: {bearing_name: [1.csv, 2.csv, ... 1515.csv]}}
    """
    root = Path(base_dir or (DEFAULT_LAB_DIR / "XJTU-SY" / "XJTU-SY_Bearing_Datasets"))
    if not root.exists():
        # Fallback check
        alt = Path(base_dir or DEFAULT_LAB_DIR)
        matches = list(alt.rglob("XJTU-SY_Bearing_Datasets"))
        if matches:
            root = matches[0]
        else:
            return {}

    tree = {}
    for cond_dir in sorted(root.iterdir()):
        if not cond_dir.is_dir():
            continue
        c_name = cond_dir.name
        tree[c_name] = {}
        for b_dir in sorted(cond_dir.iterdir()):
            if not b_dir.is_dir() or not b_dir.name.startswith("Bearing"):
                continue
            # CRITICAL REQUIREMENT: Numerical sorting by file number (1.csv -> 1515.csv)
            # Never use alphabetic string sorting!
            csv_files = [p for p in b_dir.glob("*.csv") if p.is_file()]
            csv_files_sorted = sorted(
                csv_files,
                key=lambda p: int(p.stem) if p.stem.isdigit() else 999999
            )
            tree[c_name][b_dir.name] = csv_files_sorted
    return tree


def parse_xjtu_rpm_load(path_or_str: Union[str, Path]) -> Tuple[float, float]:
    """Extract operating speed (RPM) and radial load (kN) from XJTU-SY path."""
    s = str(path_or_str)
    for cond_key, (rpm_val, load_val) in XJTU_CONDITION_RPM.items():
        if cond_key in s:
            return rpm_val, load_val
    if "40Hz" in s:
        return 2400.0, 10.0
    if "37.5Hz" in s:
        return 2250.0, 11.0
    if "35Hz" in s:
        return 2100.0, 12.0
    return 2100.0, 12.0


def load_xjtu_csv(file_path_or_bytes: Union[str, Path, bytes],
                  channel: str = "Horizontal") -> Tuple[np.ndarray, float, float, float]:
    """Load an XJTU-SY .csv file.
    Returns:
        signal (resampled to 16 kHz), rpm, ground_truth_deg_pct, ground_truth_rul_h
    """
    if isinstance(file_path_or_bytes, (str, Path)):
        p = Path(file_path_or_bytes)
        df = pd.read_csv(p)
        fname = p.name
        fpath_str = str(p)
        stem = p.stem
        # Derive total files in same folder if available
        parent = p.parent
        if parent.exists():
            all_csvs = list(parent.glob("*.csv"))
            total_files = max(1, len(all_csvs))
        else:
            total_files = 100
        cur_idx = int(stem) if stem.isdigit() else 1
    else:
        df = pd.read_csv(io.BytesIO(file_path_or_bytes))
        fname = getattr(file_path_or_bytes, "name", "1.csv")
        fpath_str = fname
        cur_idx = 1
        total_files = 100

    # Channel selection (Horizontal vibration is Drive End equivalent)
    target_col = None
    for c in df.columns:
        if channel.lower() in c.lower():
            target_col = c
            break
    if target_col is None:
        target_col = df.columns[0]

    sig_raw = df[target_col].to_numpy().astype(np.float32)

    # Native sampling rate is 25.6 kHz. Resample to 16 kHz (ratio 5/8)
    sig_16k = resample_poly(sig_raw, 5, 8).astype(np.float32)

    rpm, _ = parse_xjtu_rpm_load(fpath_str)

    # Ground-truth Degradation Index and RUL
    # Lifetime progression: ratio i / N
    progress = min(1.0, max(0.0, cur_idx / total_files))
    # Quadratic wear curve matches progressive fatigue wear:
    deg_pct = round(float((progress ** 1.8) * 100.0), 2)
    # Remaining Useful Life: 1 minute per test interval -> converted to hours
    remaining_minutes = max(0, total_files - cur_idx)
    rul_hours = round(remaining_minutes / 60.0, 2)

    return sig_16k, rpm, deg_pct, rul_hours


# ==============================================================================
# 3. Signal Standardization Windowing
# ==============================================================================
def prepare_signal_window(sig: np.ndarray, target_len: int = N_SAMPLES) -> np.ndarray:
    """Normalize and format signal array to exactly target_len (16,000 samples)."""
    sig = np.asarray(sig, dtype=np.float32).ravel()
    if len(sig) >= target_len:
        x = sig[:target_len]
    else:
        x = np.pad(sig, (0, target_len - len(sig)), mode="wrap")

    std_val = float(np.std(x))
    if std_val > 1e-7:
        x = (x - float(np.mean(x))) / std_val
    return x.astype(np.float32)
