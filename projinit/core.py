import pathlib
import venv
import textwrap
import subprocess
import shutil

README_TEXT = "# {name}\
Project initialized by `projinit`."

GITIGNORE = textwrap.dedent("""\
__pycache__/
.venv/
*.pyc
""").rstrip()


def _sh(cmd: list[str], cwd: pathlib.Path):
    """Run shell command in *cwd*, raise on non‑zero exit."""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "command failed")


def create_project(path: pathlib.Path, github: bool = False):
    """Scaffold folder, venv, and initial git commit."""
    path.mkdir(parents=False, exist_ok=False)
    (path / "src").mkdir()
    (path / "README.md").write_text(README_TEXT.format(name=path.name))
    (path / ".gitignore").write_text(GITIGNORE + "")

    (path / "requirements.txt").touch()

    venv.create(path / ".venv", with_pip=True)

    if shutil.which("git") is None:
        raise RuntimeError("git executable not found")

    _sh(["git", "init", "-b", "master"], cwd=path)
    _sh(["git", "add", "."], cwd=path)
    _sh(["git", "commit", "-m", "Initial commit"], cwd=path)

    if github:
        raise NotImplementedError("--github not implemented yet")
