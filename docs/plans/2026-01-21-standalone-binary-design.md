# Design: Standalone Binary for sparkstart

**Date**: 2026-01-21  
**Status**: DRAFT  
**Author**: Antigravity

## Context
Potential users often face "setup fatigue" (dependency hell) before they even write their first line of code. `sparkstart` aims to solve this by scaffolding projects instantly. However, `sparkstart` itself currently requires Python and pip, which is a barrier.

## Goal
Create a "magic" single-file binary that a user can download and run to start a project without pre-installing Python or dependencies.

## Architecture

### 1. The Bundle (PyInstaller)
- **Core Technology**: `PyInstaller` will process the Python codebase (`sparkstart` package) and bundle it with a minimal Python interpreter.
- **Output**: A single executable file (approx. 15-20MB).
- **Behavior**: The binary behaves exactly like the `sparkstart` CLI.

### 2. The Dev Container "Hand-off"
The binary cannot contain Docker or VS Code. Instead, it acts as the "Architect" that checks for the "Construction Crew".

**Workflow:**
1.  User runs `./sparkstart new <project> --lang cpp`.
2.  Binary generates project files (including `.devcontainer`).
3.  **Bootstrap Check**:
    - Binary checks if `docker` is available in PATH.
    - **If missing**: Prints a helpful error/warning guiding the user to install Docker (or opens the download page).
    - **If present**: Continues.
4.  **Launch**:
    - Binary runs `code <project>` (if VS Code is found).
    - VS Code detects `.devcontainer` and takes over, building the environment.

### 3. Build Pipeline (MVP)
A new script `scripts/build_dist.py` will:
1.  Verify `pyinstaller` is present.
2.  Clean previous builds (`dist/`, `build/`).
3.  Run PyInstaller with:
    - `--onefile`
    - `--name sparkstart`
    - `--hidden-import` (if needed for dynamic imports)
4.  Output availability in `dist/sparkstart`.

## MVP Scope
- [x] Add `pyinstaller` to dev-dependencies.
- [x] Create build script.
- [x] Verify binary runs on the build machine (Linux).
- [ ] (Future) Cross-compilation for Windows/Mac.
- [ ] (Future) Automatic updates.

## Alternatives Considered
- **Rewrite in Rust**: Better performance and smaller binary, but high effort to rewrite logic. selected **PyInstaller** for speed of delivery (MVP).
