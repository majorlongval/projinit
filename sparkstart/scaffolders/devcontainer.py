import pathlib
from sparkstart.templates.devcontainer import DEVCONTAINER_JSON, DEVCONTAINER_PYTHON

def scaffold_devcontainer(path: pathlib.Path, lang: str) -> None:
    """Create .devcontainer configuration."""
    (path / ".devcontainer").mkdir()
    
    if lang == "cpp":
        content = DEVCONTAINER_JSON
    elif lang == "python":
        content = DEVCONTAINER_PYTHON
    else:
        # Fallback or Todo
        return

    (path / ".devcontainer" / "devcontainer.json").write_text(content + "\n")
