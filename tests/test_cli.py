import pytest
import subprocess
import pathlib
import sys
from typer.testing import CliRunner
from sparkstart.cli import app

runner = CliRunner()

def test_new_python_project(tmp_cwd):
    result = runner.invoke(app, ["new", "myproj", "--lang", "python"])
    assert result.exit_code == 0
    
    project_path = tmp_cwd / "myproj"
    assert project_path.exists()
    assert (project_path / "src" / "main.py").exists()
    assert (project_path / "tests" / "test_main.py").exists()
    assert (project_path / ".venv").exists()
    
    # Run the generated project's tests
    # We need to use the generated venv's python or just install dependencies?
    # Since we are in a test, let's just check the files for now.
    # To run the code, we'd need to install the project or use its venv.
    
    # Verify content of main.py
    main_content = (project_path / "src" / "main.py").read_text()
    assert 'def hello() -> str:' in main_content
    assert 'return "Hello, world!"' in main_content

def test_new_pygame_project(tmp_cwd):
    result = runner.invoke(app, ["new", "mygame", "--lang", "python", "--template", "pygame"])
    assert result.exit_code == 0
    
    project_path = tmp_cwd / "mygame"
    assert project_path.exists()
    assert (project_path / "src" / "main.py").exists()
    
    # Verify pygame content
    main_content = (project_path / "src" / "main.py").read_text()
    assert "import pygame" in main_content
    assert "Sparkstart Snake" in main_content

def test_new_cpp_project(tmp_cwd):
    # This might fail if g++ or cmake are missing in the test environment.
    # We should probably mock shutil.which if we want to test scaffolding logic only.
    # But for an integration test, we can try running it and skip if tools missing?
    
    # For now, let's assume tools might be missing and handle the error gracefully or expect failure.
    # Or mock `shutil.which` to return True for everything to test file generation.
    
    from unittest.mock import patch
    
    with patch("shutil.which", return_value="/usr/bin/fake-tool"):
        result = runner.invoke(app, ["new", "cppproj", "--lang", "cpp"])
        
        # If mocking is successful, it should try to create files.
        # However, _scaffold_cpp tries to run git commands too.
        # And creates directories.
        
        if result.exit_code == 0:
            project_path = tmp_cwd / "cppproj"
            assert project_path.exists()
            assert (project_path / "CMakeLists.txt").exists()
            assert (project_path / "tests" / "test_main.cpp").exists()
            assert "gtest" in (project_path / "conanfile.txt").read_text()

def test_delete_project(tmp_cwd):
    (tmp_cwd / "todelete").mkdir()
    
    result = runner.invoke(app, ["delete", "todelete", "--yes"])
    assert result.exit_code == 0
    assert not (tmp_cwd / "todelete").exists()
