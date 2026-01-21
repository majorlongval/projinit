# projinit Worklog

## 2026-01-21: Multi-Language Support Planning

**Goal:** Add support for Python, Rust, and JavaScript project scaffolding.

**Current state assessed:**
- CLI works with `projinit new <name>` and `projinit delete <name>`
- Python-only: creates pyproject.toml, src/, .venv, git init
- No existing tests

**Decision:** Start with multi-language basics (Option 2) before adding templates. Keep it simple — each language gets a working "Hello World" starter.

---

## 2026-01-21: Multi-Language Support Implementation

**Completed:**
1. Fixed broken `core.py` (recovered from git history, code had been truncated)
2. Added `--lang` option to CLI: `python` (default), `rust`, `javascript`
3. Each language now scaffolds with working Hello World:
   - Python: `src/main.py` with `print("Hello, world!")`
   - Rust: `src/main.rs` with `println!("Hello, world!")`
   - JavaScript: `index.js` with `console.log("Hello, world!")`
4. Updated README with new usage examples
5. Added `python-dotenv` to dependencies in pyproject.toml

**Verified:** Created test projects in all three languages, ran Hello World successfully.

---

## 2026-01-21: Published to PyPI as sparkstart

**Package name journey:** projinit → initforge → sparkstart (first two were taken)

**Published:** `pip install sparkstart` now works globally!

**Final package:** sparkstart v0.1.0
