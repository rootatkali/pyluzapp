import subprocess
from pathlib import Path


class GitError(Exception):
    pass


def _run(args: list[str], cwd: Path) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise GitError(f"Git command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout


def git_pull(repo_path: Path | str) -> str:
    return _run(["git", "pull"], Path(repo_path))


def git_push(repo_path: Path | str, message: str = "update schedule") -> str:
    path = Path(repo_path)
    _run(["git", "add", "."], path)
    _run(["git", "commit", "-m", message], path)
    return _run(["git", "push", "origin", "main"], path)


def git_status(repo_path: Path | str) -> str:
    return _run(["git", "status"], Path(repo_path))
