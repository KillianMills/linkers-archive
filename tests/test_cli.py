import subprocess
import sys


def test_cli_version():
    # run the CLI with --version and capture output
    result = subprocess.run(
        [sys.executable, "-m", "linkers_archive.cli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "0.0.1"
