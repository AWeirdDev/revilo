"""Windows - Powershell utilities."""

import subprocess
from typing import Mapping


def check_powershell() -> bool:
    """Checks if Powershell (short name 'ps') is available.

    Returns:
        bool: True if it's available, False otherwise.
    """
    try:
        subprocess.check_output(["powershell", "-Command", "Write-Host Yo!"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


class PowershellError(Exception):
    """Raised when a command fails to execute."""


def run_powershell(command: str, vars: Mapping[str, str] = {}) -> str:
    """Runs a Powershell command.

    Args:
        command (str): The Powershell command to run.

    Returns:
        str: The Powershell output.
    """
    assert check_powershell(), "Powershell is not available."

    command = pstemplate(command, vars)

    try:
        out = subprocess.check_output(["powershell", "-Command", command])
        try:
            return out.decode("ansi")
        except UnicodeDecodeError:
            return out.decode("utf-8")

    except subprocess.CalledProcessError as e:
        raise PowershellError("\n" + e.output.decode("ansi")) from e


def pstemplate(command: str, vars: Mapping[str, str]) -> str:
    for key, value in vars.items():
        command = command.replace("{%s}" % key, value)
    return command


def psstr(__str: str, /, *, noendl: bool = False) -> str:
    """Returns a Powershell string.

    Args:
        __str (str): The string.
        noendl (bool): No endl replacement?
    """
    k = f'"{__str}"'

    if not noendl:
        k = k.replace("\n", psendl())

    return k


def psbool(__bool: bool) -> str:
    """Returns a Powershell boolean.

    Args:
        __bool (bool): The boolean.
    """
    return "true" if __bool else "false"


def psendl():
    """Returns a Powershell ENDL."""
    return "`n"
