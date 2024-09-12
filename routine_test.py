import subprocess
import sys
import pytest

def test_user_profile_runs():
    """
    This test runs `user_profile.py` as a subprocess and checks for errors.
    """
    try:
        result = subprocess.run([sys.executable, 'user_profile.py'], check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"`user_profile.py` failed with error: {e}")
