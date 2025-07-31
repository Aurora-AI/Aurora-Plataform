import os


def test_dummy_auth():
    fake_secret = "supersecretkey123"  # pragma: allowlist secret
    assert isinstance(fake_secret, str)
