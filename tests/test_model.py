import numpy as np
import pytest
import torch
from transformers import AutoConfig

from dataset import rul_to_target, target_to_rul
from mech_config import DEFAULT_BACKBONE, RUL_CAP_H
from mtl_model import MechAgentMTL, multitask_loss


def test_rul_conversion():
    # RUL cap
    assert np.isclose(rul_to_target(0.0), 0.0)
    assert np.isclose(rul_to_target(RUL_CAP_H), 1.0)
    assert np.isclose(target_to_rul(0.0), 0.0)
    assert np.isclose(target_to_rul(1.0), RUL_CAP_H)

    # Invertible
    vals = np.array([5.0, 50.0, 200.0, 800.0])
    recon = target_to_rul(rul_to_target(vals))
    assert np.allclose(vals, recon, rtol=1e-5)


def test_mtl_model_forward():
    # Using tiny config to test without heavy weights
    bcfg = AutoConfig.from_pretrained(DEFAULT_BACKBONE)
    bcfg.num_hidden_layers = 1
    model = MechAgentMTL(n_phys=17, n_classes=5, backbone_config=bcfg)
    model.eval()

    B, T = 2, 16000
    x = torch.randn(B, T)
    phys = torch.randn(B, 17)
    out = model(x, phys)

    assert "logits" in out
    assert "deg" in out
    assert "rul_mu" in out
    assert "rul_logvar" in out

    assert out["logits"].shape == (B, 5)
    assert out["deg"].shape == (B,)
    assert out["rul_mu"].shape == (B,)
    assert out["rul_logvar"].shape == (B,)

    assert torch.all((out["deg"] >= 0) & (out["deg"] <= 1))
    assert torch.all((out["rul_mu"] >= 0) & (out["rul_mu"] <= 1))


def test_multitask_loss():
    B = 4
    out = {
        "logits": torch.randn(B, 5),
        "deg": torch.rand(B),
        "rul_mu": torch.rand(B),
        "rul_logvar": torch.zeros(B),
    }
    batch = {
        "cls": torch.tensor([0, 1, 2, 3]),
        "deg": torch.rand(B),
        "rul": torch.rand(B),
    }
    task_log_vars = torch.nn.Parameter(torch.zeros(2))
    total_loss, parts = multitask_loss(out, batch, task_log_vars)

    assert total_loss > 0
    assert "cls" in parts
    assert "deg" in parts
    assert "rul" in parts
