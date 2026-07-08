"""
Unit tests for ASTRAXIS-AI core module (config, hasher, logger).
"""
import pytest
from astraxis.core.config import AstraxisSettings
from astraxis.core.hasher import ArtifactHasher
from astraxis.core.logger import get_logger

def test_config_defaults():
    settings = AstraxisSettings()
    assert settings.engine_name == "ASTRAXIS-AI v1.0"
    assert settings.max_attack_depth == 5
    assert settings.sandbox_timeout_seconds == 30

def test_hasher_sha256():
    hasher = ArtifactHasher()
    res = hasher.hash_string("ASTRAXIS-AI")
    assert len(res) == 64
    assert res == hasher.hash_string("ASTRAXIS-AI")

def test_hasher_dict():
    hasher = ArtifactHasher()
    d1 = {"a": 1, "b": 2}
    d2 = {"b": 2, "a": 1}
    assert hasher.hash_dict(d1) == hasher.hash_dict(d2)

def test_logger():
    logger = get_logger("test")
    assert logger is not None
