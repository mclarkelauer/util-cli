# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Setup**: `make setup` - Installs Homebrew, uv, pipx, and syncs dependencies
- **Build and Install**: `make install` or `make` - Builds the package and installs via pipx
- **Clean**: `make clean` - Cleans uv cache
- **Uninstall**: `make uninstall` - Removes installed package and cleans build artifacts

## Project Architecture

This is a Python CLI utility built with Click that provides a modular command system:

- **Entry Point**: `src/cli.py` - Main CLI group with configuration handling
- **Script Entry**: Configured in `pyproject.toml` as `util = "cli:cli"`
- **Configuration**: `src/util/config.py` - TOML-based config system reading from `~/.utilrc`
- **Logging**: `src/util/logging.py` - Centralized logging with configurable levels
- **Commands**: Referenced in `src/cli.py` but files appear to be deleted (scrape, config, gemini)

## Key Features

- **Dynamic Command Loading**: Uses `ccl` library to register commands from `out_of_repo_commands/` directory if present
- **Configuration System**: TOML-based config with section support and click integration
- **Logging**: Configurable log levels via `--log-level` option (defaults to ERROR)
- **Build System**: Uses `uv` for dependency management and `pipx` for installation

## Dependencies

Key dependencies include Click, BeautifulSoup4, requests, google-genai, rich, and ipython. The project requires Python >=3.13 and uses setuptools as the build backend.