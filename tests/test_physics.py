import numpy as np
import pytest

from bearing_physics import (
    BEARINGS,
    PHYS_FEATURE_NAMES,
    BearingGeometry,
    _peak_ratio,
    envelope_spectrum,
    get_bearing,
    physics_check,
    physics_features,
    time_features,
)
from mech_config import FS, N_SAMPLES


def test_bearing_geometry():
    b = get_bearing("6205")
    assert isinstance(b, BearingGeometry)
    assert b.n_balls == 9
    orders = b.fault_orders()
    assert "inner_race" in orders
    assert "outer_race" in orders
    assert "ball" in orders
    assert "cage" in orders
    # BPFI > BPFO for fixed outer ring
    assert orders["inner_race"] > orders["outer_race"]
    assert 5.0 < orders["inner_race"] < 6.0
    assert 3.0 < orders["outer_race"] < 4.0


def test_time_features():
    t = np.linspace(0, 1, FS)
    x = np.sin(2 * np.pi * 50 * t)
    tf = time_features(x)
    assert "rms" in tf
    assert "peak" in tf
    assert "crest" in tf
    assert "kurtosis" in tf
    assert "skewness" in tf
    assert abs(tf["rms"] - 1 / np.sqrt(2)) < 0.05
    assert np.isfinite(tf["kurtosis"])


def test_envelope_spectrum():
    t = np.linspace(0, 1, FS)
    # Carrier 2500 Hz modulated by 100 Hz
    x = (1 + np.sin(2 * np.pi * 100 * t)) * np.sin(2 * np.pi * 2500 * t)
    freqs, spec = envelope_spectrum(x, FS)
    assert len(freqs) == len(spec)
    assert len(freqs) > 0
    assert np.all(spec >= 0)


def test_peak_ratio_safeguard():
    freqs = np.linspace(0, 8000, 4000)
    spec = np.ones_like(freqs)
    # Uniform noise -> ratio ~ 1.0
    r = _peak_ratio(freqs, spec, 100.0)
    assert 0.8 < r < 1.2
    # Extreme edge cases
    assert _peak_ratio(freqs, spec, 0.0) == 1.0
    assert _peak_ratio(freqs, spec, 99999.0) == 1.0


def test_physics_features():
    rng = np.random.default_rng(42)
    x = rng.normal(0, 1, N_SAMPLES).astype(np.float32)
    feats = physics_features(x, FS, rpm=1800.0, bearing="6205")
    assert len(feats) == len(PHYS_FEATURE_NAMES)
    assert len(feats) == 17
    assert np.all(np.isfinite(feats))


def test_physics_check():
    rng = np.random.default_rng(42)
    x = rng.normal(0, 1, N_SAMPLES).astype(np.float32)
    chk = physics_check(x, FS, rpm=1800.0, bearing="6205")
    assert "physics_fault" in chk
    assert "threshold" in chk
    assert "scores" in chk
    assert "envelope_order_spectrum" in chk
