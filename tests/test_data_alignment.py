"""Unit tests for Phase 2: Data Alignment and Resampling.
Verifies numerical sorting of nested XJTU-SY files, polyphase resampling ratios,
and standard window preparation for both CWRU and XJTU-SY datasets.
"""
from pathlib import Path
import numpy as np
import pytest
from scipy.signal import resample_poly

from real_dataset import (
    discover_cwru_files,
    discover_xjtu_conditions,
    load_cwru_mat,
    load_xjtu_csv,
    prepare_signal_window,
)


def test_xjtu_numerical_sorting():
    """Verify that integer stem sorting key=lambda p: int(p.stem) preserves chronological order."""
    test_stems = ["1", "10", "100", "1000", "2", "20", "200", "15", "1515"]
    fake_paths = [Path(f"C:/fake/{s}.csv") for s in test_stems]
    
    # Standard string sort (alphabetical error: 10 comes before 2)
    bad_sorted = sorted(fake_paths)
    assert bad_sorted[1].stem == "10"
    assert bad_sorted[6].stem == "2"
    
    # Engineering numerical sort
    good_sorted = sorted(fake_paths, key=lambda p: int(p.stem) if p.stem.isdigit() else 999999)
    assert [p.stem for p in good_sorted] == ["1", "2", "10", "15", "20", "100", "200", "1000", "1515"]


def test_cwru_resampling_polyphase():
    """Verify polyphase resampling from 12 kHz to 16 kHz (up=4, down=3)."""
    fs_in = 12000
    fs_out = 16000
    duration_s = 0.5
    n_in = int(fs_in * duration_s)
    
    # 50 Hz test sine wave
    t = np.arange(n_in) / fs_in
    sig_12k = np.sin(2 * np.pi * 50 * t).astype(np.float32)
    
    # Resample
    sig_16k = resample_poly(sig_12k, 4, 3)
    expected_len = int(n_in * 4 / 3)
    
    assert abs(len(sig_16k) - expected_len) <= 1
    # Verify amplitude preservation (sin amplitude ~ 1.0)
    assert 0.95 <= np.max(sig_16k) <= 1.05


def test_xjtu_resampling_polyphase():
    """Verify polyphase resampling from 25.6 kHz to 16 kHz (up=5, down=8)."""
    fs_in = 25600
    fs_out = 16000
    duration_s = 0.5
    n_in = int(fs_in * duration_s)
    
    # 100 Hz test sine wave
    t = np.arange(n_in) / fs_in
    sig_25k = np.sin(2 * np.pi * 100 * t).astype(np.float32)
    
    # Resample
    sig_16k = resample_poly(sig_25k, 5, 8)
    expected_len = int(n_in * 5 / 8)
    
    assert abs(len(sig_16k) - expected_len) <= 1
    assert 0.95 <= np.max(sig_16k) <= 1.05


def test_prepare_signal_window():
    """Verify prepare_signal_window returns exactly target_length array with normalization."""
    raw = np.random.normal(2.0, 0.5, 30000).astype(np.float32)
    win = prepare_signal_window(raw, target_len=16000)
    
    assert len(win) == 16000
    assert win.dtype == np.float32
    # Mean should be centered near 0
    assert abs(np.mean(win)) < 0.1
