"""Loader and preprocessor for real lab datasets: CWRU and XJTU-SY."""
import os
from pathlib import Path
import numpy as np
import pandas as pd
import scipy.io as sio

from mech_config import FS, N_SAMPLES
from bearing_physics import physics_features, get_bearing, time_features

CWRU_FAULT_MAP = {
    "Normal": ("normal", 0.05),
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

def load_cwru_mat(file_path_or_bytes):
    """Load a CWRU .mat file and return (signal, rpm, detected_fault, fault_size)."""
    if isinstance(file_path_or_bytes, (str, Path)):
        mat = sio.loadmat(file_path_or_bytes)
    else:
        import io
        mat = sio.loadmat(io.BytesIO(file_path_or_bytes))
    
    de_keys = [k for k in mat.keys() if "DE_time" in k]
    if not de_keys:
        de_keys = [k for k in mat.keys() if not k.startswith("__") and isinstance(mat[k], np.ndarray) and mat[k].ndim <= 2 and mat[k].size > 5000]
    if not de_keys:
        raise ValueError("No vibration time-series found in .mat file")
    
    sig = mat[de_keys[0]].ravel().astype(np.float32)
    
    rpm_keys = [k for k in mat.keys() if "RPM" in k]
    rpm = float(mat[rpm_keys[0]].ravel()[0]) if rpm_keys else 1750.0
    
    # Inferred fault from filename
    fname = Path(getattr(file_path_or_bytes, "name", str(file_path_or_bytes))).stem
    fault = "normal"
    sev = 0.05
    for prefix, (f_cls, f_sev) in CWRU_FAULT_MAP.items():
        if fname.startswith(prefix) or prefix in fname:
            fault = f_cls
            sev = f_sev
            break
            
    return sig, rpm, fault, sev


def load_xjtu_csv(file_path_or_bytes, channel="Horizontal"):
    """Load an XJTU-SY .csv file and return (signal, rpm)."""
    if isinstance(file_path_or_bytes, (str, Path)):
        df = pd.read_csv(file_path_or_bytes)
    else:
        import io
        df = pd.read_csv(io.BytesIO(file_path_or_bytes))
        
    cols = df.columns
    target_col = None
    for c in cols:
        if channel.lower() in c.lower():
            target_col = c
            break
    if target_col is None:
        target_col = cols[0]
        
    sig = df[target_col].to_numpy().astype(np.float32)
    # Default XJTU-SY operating speeds: 35Hz = 2100 RPM, 37.5Hz = 2250 RPM, 40Hz = 2400 RPM
    rpm = 2100.0
    fname = str(file_path_or_bytes)
    if "40Hz" in fname:
        rpm = 2400.0
    elif "37.5Hz" in fname:
        rpm = 2250.0
        
    return sig, rpm


def prepare_signal_window(sig, target_len=N_SAMPLES, fs_in=None, fs_out=FS):
    """Normalize or resample signal to target_len (16,000 samples)."""
    if fs_in and fs_in != fs_out:
        from scipy.signal import resample
        new_len = int(len(sig) * fs_out / fs_in)
        sig = resample(sig, new_len).astype(np.float32)
        
    if len(sig) >= target_len:
        # Take center or start window
        x = sig[:target_len]
    else:
        # Pad with wrapping
        x = np.pad(sig, (0, target_len - len(sig)), mode="wrap")
        
    # Standardize
    x = (x - np.mean(x)) / (np.std(x) + 1e-7)
    return x.astype(np.float32)
