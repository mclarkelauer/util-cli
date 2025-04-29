all: install

install:
	@uv build 
	@pipx install dist/util-*.whl

setup:
	@/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	@brew install uv
	@brew install pipx
	@uv sync

clean:
	@uv clean

uninstall: clean
	@pipx uninstall util
