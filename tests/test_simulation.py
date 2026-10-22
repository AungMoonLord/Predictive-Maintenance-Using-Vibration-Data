import numpy as np
import pytest

from mech_config import CLASSES, FAULT_TYPES, FS, N_SAMPLES
from simulate import degradation, resonance_kernel, simulate_signal


def test_resonance_kernel():
    k = resonance_kernel(FS, fn=3000, zeta=0.05, length_s=0.01)
    assert len(k) == int(0.01 * FS)
    assert np.all(np.isfinite(k))


def test_degradation_monotonic_trend():
    d0 = degradation(0.0, 3.0, 1.0, 0.0)
    d1 = degradation(1.0, 3.0, 1.0, 0.0)
    assert d0 >= 0.0
    assert d1 <= 1.0
    assert d1 > d0


@pytest.mark.parametrize("fault", CLASSES)
def test_simulate_signal_all_faults(fault):
    rng = np.random.default_rng(123)
    sig = simulate_signal(fault, severity=0.5, rpm=1800.0, rng=rng)
    assert sig.shape == (N_SAMPLES,)
    assert sig.dtype == np.float32
    assert np.all(np.isfinite(sig))
    assert np.std(sig) > 0.01  # non-silent signal
