import subprocess
from pathlib import Path


class GitError(Exception):
    """Raised when a git subprocess exits with a non-zero return code."""


def _run(args: list[str], cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise GitError(f"Git command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout


def git_pull(repo_path: Path | str) -> str:
    """Run ``git pull`` in *repo_path* and return stdout.

    Raises:
        GitError: If the command exits with a non-zero return code.
    """
    return _run(["git", "pull"], Path(repo_path))


def git_push(repo_path: Path | str, message: str = "update schedule") -> str:
    """Stage all changes, commit with *message*, and push to ``origin main``.

    Equivalent to::

        git add .
        git commit -m <message>
        git push origin main

    Raises:
        GitError: If any of the three git commands fails.
    """
    path = Path(repo_path)
    _run(["git", "add", "."], path)
    _run(["git", "commit", "-m", message], path)
    return _run(["git", "push", "origin", "main"], path)


def git_status(repo_path: Path | str) -> str:
    """Run ``git status`` in *repo_path* and return stdout.

    Raises:
        GitError: If the command exits with a non-zero return code.
    """
    return _run(["git", "status"], Path(repo_path))
