# projinit 🚀
**Start your new project in seconds, not minutes.**

You have an idea? `projinit` handles the boring setup so you can start coding immediately.

### What it does
1. 📂 Creates your project folder and structure.
2. 🐍 Sets up a Python virtual environment (for Python projects).
3. 🎯 Generates working "Hello World" starter code.
4. ☁️ **Automatically creates a GitHub repository** and pushes your code.

### Supported Languages
- **Python** (default) — pyproject.toml, src/, .venv
- **Rust** — Cargo.toml, src/main.rs
- **JavaScript** — package.json, index.js

---

### 1. Prerequisites (Do you have these?)
*   **Python** (3.8+) → [Download here](https://www.python.org/downloads/)
*   **Git** → [Download here](https://git-scm.com/downloads)

### 2. Install
Open your terminal and run:
```bash
pip install projinit
```

### 3. Create your Project

**Python (default):**
```bash
projinit new my-awesome-game
```

**Rust:**
```bash
projinit new my-rust-app --lang rust
```

**JavaScript:**
```bash
projinit new my-web-app --lang javascript
```

**With GitHub:**
```bash
projinit new my-awesome-game --github
```

**What happens next?**
1.  `projinit` creates your project with working starter code.
2.  If using `--github`, it will ask for a **GitHub Token**.
3.  It will **automatically open your browser** to the right GitHub page.
4.  Just scroll down, click **"Generate token"**, and paste it into the terminal.
5.  Done! Your project is live on GitHub and ready to code.
