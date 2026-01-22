import pathlib
import textwrap
from sparkstart.templates.rust import GITIGNORE_RUST

def scaffold_rust(path: pathlib.Path) -> None:
    """Create Rust project structure with Hello World."""
    (path / "src").mkdir()
    (path / "src" / "main.rs").write_text('fn main() {\n    println!("Hello, world!");\n}\n')
    (path / ".gitignore").write_text(GITIGNORE_RUST + "\n")
    
    # Create Cargo.toml
    cargo_toml = textwrap.dedent(f'''
        [package]
        name = "{path.name}"
        version = "0.1.0"
        edition = "2021"

        [dependencies]
    ''').strip()
    (path / "Cargo.toml").write_text(cargo_toml + "\n")
