# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- **Setup**: `make setup` - Installs Homebrew, uv, pipx, and syncs dependencies
- **Build and Install**: `make install` or `make` - Builds the package and installs via pipx
- **Clean**: `make clean` - Cleans uv cache
- **Uninstall**: `make uninstall` - Removes installed package and cleans build artifacts
- **Lint**: `pylint src/` - Run pylint on source code (requires dev dependencies)

## Project Architecture

This is a Python CLI utility built with asyncclick that provides a modular command system:

- **Entry Point**: `src/cli.py` - Main CLI group with async configuration handling
- **Script Entry**: Configured in `pyproject.toml` as `util = "cli:cli"`
- **Configuration**: `src/util/config.py` - TOML-based config system reading from `~/.utilrc` with async support
- **Logging**: `src/util/logging.py` - Centralized logging with configurable levels
- **Commands**: `src/commands/` - Built-in commands (config, gemini, scrape, demo)
- **External Commands**: `out_of_repo_commands/` - External command directory (ccl integration disabled due to asyncclick compatibility)

## Key Features

- **Async Click Integration**: Uses `asyncclick` for async command handling
- **Modular Command System**: Commands auto-registered from `src/commands/` with graceful import handling
- **Configuration Management**: TOML-based config with section support, async loading, and Gemini API key management
- **Rich Output**: Uses Rich library for enhanced console output in commands
- **Build System**: Uses `uv` for dependency management and `pipx` for installation
- **Dynamic Command Loading**: External commands via `out_of_repo_commands/` (currently disabled pending ccl/asyncclick compatibility fix)

## Configuration System

- Configuration file: `~/.utilrc` (TOML format)
- Default section: `GLOBAL`
- Supports per-command sections
- Async configuration loading and saving
- Built-in Gemini API key management methods

## Command Development

When adding new commands:
1. Create command file in `src/commands/`
2. Use `asyncclick` decorators and async functions
3. Import and register in `src/cli.py` with try/except for graceful handling
4. Commands can access config via context: `ctx.obj` (Config instance)

## Dependencies

Key dependencies: asyncclick, BeautifulSoup4, requests, google-genai, rich, ipython, toml, aiofiles, httpx, clickloader. Development dependencies include pylint. Requires Python >=3.13.