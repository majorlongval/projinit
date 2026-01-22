import pathlib
import textwrap
from sparkstart.templates.javascript import GITIGNORE_JAVASCRIPT

def scaffold_javascript(path: pathlib.Path) -> None:
    """Create JavaScript project structure with Hello World."""
    (path / "index.js").write_text('console.log("Hello, world!");\n')
    (path / ".gitignore").write_text(GITIGNORE_JAVASCRIPT + "\n")
    
    # Create package.json
    package_json = textwrap.dedent(f'''
        {{
          "name": "{path.name}",
          "version": "0.1.0",
          "description": "",
          "main": "index.js",
          "scripts": {{
            "start": "node index.js"
          }}
        }}
    ''').strip()
    (path / "package.json").write_text(package_json + "\n")
