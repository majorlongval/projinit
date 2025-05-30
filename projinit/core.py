"""
core.py – all the heavy lifting for projinit
    • folder scaffold          (src/, README, .gitignore, requirements.txt)
    • local virtual-env        (.venv)
    • git repo + first commit
    • optional --github push   (per-project token in .projinit.env or $GITHUB_TOKEN)

Requires: requests, python-dotenv
    pip install requests python-dotenv
"""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import textwrap
import venv
from typing import List

import requests
from dotenv import dotenv_values

# ----------------------------------------------------------------------------- #
# Constants                                                                     #
# ----------------------------------------------------------------------------- #

README_TEXT = "# {name}\n\nProject initialized by `projinit`."

GITIGNORE = textwrap.dedent(
    """
    __pycache__/
    .venv/
    *.pyc
    .DS_Store
    """
).strip()


# ----------------------------------------------------------------------------- #
# Helper functions                                                              #
# ----------------------------------------------------------------------------- #


def _sh(cmd: List[str], cwd: pathlib.Path) -> None:
    """Run *cmd* in *cwd*; raise RuntimeError on non-zero exit."""
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"$ {' '.join(cmd)}\n{result.stderr.strip() or 'command failed'}"
        )


# ---------- per-project token helpers ---------------------------------------- #


def _project_token(project_root: pathlib.Path) -> str | None:
    """Return token from .projinit.env or '' if file missing/empty."""
    return dotenv_values(project_root / ".projinit.env").get("GITHUB_TOKEN", "")


def _save_project_token(project_root: pathlib.Path, token: str | None) -> None:
    """Persist token to .projinit.env and ensure it’s git-ignored."""
    (project_root / ".projinit.env").write_text(f"GITHUB_TOKEN={token}\n")

    gi = project_root / ".gitignore"
    lines: list[str] = gi.read_text().splitlines() if gi.exists() else []
    if ".projinit.env" not in lines:
        lines.append(".projinit.env")
        gi.write_text("\n".join(lines) + "\n")


# ---------- GitHub API ------------------------------------------------------- #


def _create_github_repo(repo_name: str, token: str | None = None) -> str:
    """
    Create repo under authenticated user; return ssh_url.
    *token* optional – falls back to $GITHUB_TOKEN.
    """
    token = token or os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "GitHub token not provided.\n"
            "Save one in .projinit.env, set $GITHUB_TOKEN, or pass --github without a token to be prompted."
        )

    r = requests.post(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
        json={"name": repo_name, "private": False},
        timeout=10,
    )
    if r.status_code >= 300:
        raise RuntimeError(f"GitHub API error {r.status_code}: {r.text.strip()}")
    return r.json()["ssh_url"]  # e.g. git@github.com:user/repo.git


# ----------------------------------------------------------------------------- #
# Public API                                                                    #
# ----------------------------------------------------------------------------- #


def create_project(path: pathlib.Path, github: bool = False) -> None:
    """
    Make a fully-initialised project directory.

    Parameters
    ----------
    path   : pathlib.Path  target directory (must not already exist)
    github : bool          if True, also create & push remote repo
    """
    # folder layout -----------------------------------------------------
    path.mkdir(parents=False, exist_ok=False)
    (path / "src").mkdir()
    (path / "README.md").write_text(README_TEXT.format(name=path.name))
    (path / ".gitignore").write_text(GITIGNORE + "\n")
    (path / "requirements.txt").touch()

    # local virtual env -------------------------------------------------
    venv.create(path / ".venv", with_pip=True)

    # git repository ------------------------------------------------------
    if shutil.which("git") is None:
        raise RuntimeError("`git` executable not found in PATH")

    # GitHub remote + push (optional) ------------------------------------
    token: str | None = None
    if github:
        # token preference: .projinit.env  >  $GITHUB_TOKEN  >  prompt user
        token = _project_token(path) or os.getenv("GITHUB_TOKEN", "")
        if not token:
            import typer  # lazy import to avoid hard dependency in library mode

            token = typer.prompt(
                "GitHub personal-access token **for this project** "
                "(saved to .projinit.env, never committed)"
            )
            _save_project_token(path, token)

    _sh(["git", "init", "-b", "main"], cwd=path)
    _sh(["git", "add", "."], cwd=path)
    _sh(["git", "commit", "-m", "Initial commit"], cwd=path)

    if github:
        ssh_url = _create_github_repo(path.name, token)
        _sh(["git", "remote", "add", "origin", ssh_url], cwd=path)
        _sh(["git", "push", "-u", "origin", "master"], cwd=path)
