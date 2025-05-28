import pathlib
import typer
from projinit.core import create_project

app = typer.Typer(
    help="projinit – create a new project repository quickly",
    invoke_without_command=True,  # allows root alias
    no_args_is_help=True,
)


# --- root alias ----------------------------------------------------
@app.callback()
def main(
    ctx: typer.Context,
    name: str = typer.Argument(None, help="Project name"),
    github: bool = typer.Option(False, "--github", help="Push to GitHub"),
):
    """If NAME is supplied directly, behave like `projinit new NAME`."""
    if name is not None:
        create_project(pathlib.Path.cwd() / name, github)
        raise typer.Exit()


# --- explicit sub‑command -----------------------------------------
@app.command()
def new(
    name: str,
    github: bool = typer.Option(False, "--github", help="Push to GitHub"),
):
    """Create a new project folder NAME (optionally push to GitHub)."""
    create_project(pathlib.Path.cwd() / name, github)
