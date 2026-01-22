import pathlib
import textwrap
import shutil
import typer
from sparkstart.templates.cpp import GITIGNORE_CPP, README_CPP, BUILD_SH
from sparkstart.templates.devcontainer import DEVCONTAINER_JSON

def scaffold_cpp(path: pathlib.Path) -> None:
    """Create C++ project structure with CMake + Conan and Hello World."""
    # Check for C++ compiler
    if shutil.which("g++") is None:
        raise RuntimeError(
            "g++ not found. Install a C++ compiler:\n"
            "  Ubuntu/Debian:  sudo apt install g++\n"
            "  Fedora:         sudo dnf install gcc-c++\n"
            "  Arch:           sudo pacman -S gcc\n"
            "  macOS:          xcode-select --install"
        )
    
    # Check for CMake (Required for our project structure)
    if shutil.which("cmake") is None:
        raise RuntimeError(
            "cmake not found. Install CMake to build the project:\n"
            "  Ubuntu/Debian:  sudo apt install cmake\n"
            "  Fedora:         sudo dnf install cmake\n"
            "  Mac:            brew install cmake"
        )

    # Check for Conan (Optional / Warning)
    if shutil.which("conan") is None:
        typer.secho(
            "WARNING: 'conan' not found. You will need it later to manage dependencies.\n"
            "  Install: pip install conan",
            fg=typer.colors.YELLOW
        )
    (path / "src").mkdir()
    (path / "build").mkdir()  # Convention: out-of-source builds
    
    # Hello World main.cpp
    main_cpp = textwrap.dedent('''
        #include <iostream>
        
        int main() {
            std::cout << "Hello, world!" << std::endl;
            return 0;
        }
    ''').strip()
    (path / "src" / "main.cpp").write_text(main_cpp + "\n")
    
    (path / ".gitignore").write_text(GITIGNORE_CPP + "\n")
    
    # CMakeLists.txt with comments explaining each section
    cmake_content = textwrap.dedent(f'''
        # ==============================================================================
        # CMakeLists.txt — The "build recipe" for your C++ project
        # ==============================================================================
        # CMake reads this file and generates platform-specific build files
        # (Makefiles on Linux/Mac, Visual Studio projects on Windows, etc.)
        #
        # To build this project:
        #   1. cd build
        #   2. cmake ..          # Generate build files from this recipe
        #   3. cmake --build .   # Actually compile the code
        # ==============================================================================
        
        cmake_minimum_required(VERSION 3.15)
        
        # Project name and version — CMake uses this to name outputs
        project({path.name} VERSION 0.1.0 LANGUAGES CXX)
        
        # Use C++17 standard (modern C++ features)
        set(CMAKE_CXX_STANDARD 17)
        set(CMAKE_CXX_STANDARD_REQUIRED ON)
        
        # ------------------------------------------------------------------------------
        # CONAN INTEGRATION (optional — uncomment when you add dependencies)
        # ------------------------------------------------------------------------------
        # After running `conan install . --output-folder=build --build=missing`
        # this line tells CMake where Conan put the dependency info:
        #
        # include(${{CMAKE_BINARY_DIR}}/conan_toolchain.cmake)
        # ------------------------------------------------------------------------------
        
        # Create an executable named after your project
        # This tells CMake: "compile src/main.cpp into an executable"
        add_executable(${{PROJECT_NAME}} src/main.cpp)
        
        # ------------------------------------------------------------------------------
        # ADDING MORE SOURCE FILES
        # ------------------------------------------------------------------------------
        # As your project grows, list all .cpp files:
        #
        # add_executable(${{PROJECT_NAME}}
        #     src/main.cpp
        #     src/utils.cpp
        #     src/game.cpp
        # )
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # ADDING SUBDIRECTORIES (Tutorial)
        # ------------------------------------------------------------------------------
        # To organize code into folders (e.g. src/engine/), create a CMakeLists.txt inside
        # that folder and use:
        #
        # add_subdirectory(src/engine)
        # ------------------------------------------------------------------------------
        
        # ------------------------------------------------------------------------------
        # LINKING CONAN DEPENDENCIES (uncomment when you add libraries)
        # ------------------------------------------------------------------------------
        # find_package(fmt REQUIRED)
        # target_link_libraries(${{PROJECT_NAME}} fmt::fmt)
        # ------------------------------------------------------------------------------

        # ------------------------------------------------------------------------------
        # TESTING
        # ------------------------------------------------------------------------------
        enable_testing()
        add_subdirectory(tests)
    ''').strip()
    (path / "CMakeLists.txt").write_text(cmake_content + "\n")
    
    # conanfile.txt — simple dependency list format
    conan_content = textwrap.dedent('''
        # ==============================================================================
        # conanfile.txt — Your C++ dependency list
        # ==============================================================================
        # Conan is a package manager for C++ (like pip for Python or npm for JS).
        # This file lists what libraries you want and how to integrate them.
        #
        # To install dependencies:
        #   conan install . --output-folder=build --build=missing
        #
        # This downloads libraries and generates files that CMake can use.
        # ==============================================================================
        
        [requires]
        # Add dependencies here, one per line. Examples:
        # fmt/10.2.1          # Modern formatting library
        # spdlog/1.13.0       # Fast logging library  
        # nlohmann_json/3.11.3  # JSON parsing
        gtest/1.14.0

        [generators]
        # CMakeToolchain — generates conan_toolchain.cmake for CMake integration
        # CMakeDeps — generates find_package() config for each dependency
        CMakeToolchain
        CMakeDeps
        
        [layout]
        cmake_layout
    ''').strip()
    (path / "conanfile.txt").write_text(conan_content + "\n")

    # Tests directory
    (path / "tests").mkdir()
    
    tests_cmake = textwrap.dedent(f'''
        find_package(GTest REQUIRED)

        add_executable(unit_tests test_main.cpp)
        
        target_link_libraries(unit_tests GTest::gtest_main)
        
        include(GoogleTest)
        gtest_discover_tests(unit_tests)
    ''').strip()
    (path / "tests" / "CMakeLists.txt").write_text(tests_cmake + "\n")
    
    test_main_cpp = textwrap.dedent('''
        #include <gtest/gtest.h>

        TEST(HelloTest, BasicAssertions) {
            EXPECT_STRNE("hello", "world");
            EXPECT_EQ(7 * 6, 42);
        }
    ''').strip()
    (path / "tests" / "test_main.cpp").write_text(test_main_cpp + "\n")

    # Build script
    build_sh = path / "build.sh"
    build_sh.write_text(BUILD_SH.format(name=path.name) + "\n")
    # Make executable (chmod +x)
    build_sh.chmod(build_sh.stat().st_mode | 0o111)

