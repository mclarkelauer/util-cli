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
- **Commands**: `src/commands/` - Built-in commands (config, gemini, claude, scrape, demo, tasks)
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

## Task Management Integration

The `tasks` command provides integration between TaskWarrior and macOS Reminders:
- **TaskWarrior Integration**: Uses `taskw` library for task management
- **macOS Reminders**: Custom `pyremindkit` module for Reminders.app integration  
- **Sync Capabilities**: Convert TaskWarrior tasks to Reminders and mark them as complete

## AI Integration Commands

The CLI includes chat commands for multiple AI providers:

### Gemini Integration
- **Command**: `util gemini` 
- **Features**: Interactive chat sessions and single prompts
- **Configuration**: API key stored in `GEMINI` section of config
- **Library**: Uses `google-genai` library

### Claude Integration  
- **Command**: `util claude`
- **Features**: Interactive chat sessions with conversation context and single prompts
- **Configuration**: API key stored in `CLAUDE` section of config  
- **Library**: Uses `anthropic` library
- **Models**: Defaults to `claude-3-5-sonnet-20241022`

Both commands support:
- Interactive chat mode (default): Maintains conversation context
- Single prompt mode: `--prompt "your question"`
- Model selection: `--model model-name`
- API key options: `--apikey key` or via config

## Dependencies

Key dependencies: asyncclick, BeautifulSoup4, requests, google-genai, anthropic, rich, ipython, toml, aiofiles, httpx, clickloader, taskw, pyyaml, pyobjc. Development dependencies include pylint. Requires Python >=3.13.