import subprocess
import sys


def test_echo():
    res = subprocess.run(
        [sys.executable, "-m", "linkers_archive.cli", "echo", "hello"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert res.stdout.strip() == "hello"
