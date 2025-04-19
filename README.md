## Setting up a new CLI

Note - this project uses UV to manage the project dependencies and venv. UV will keep the the pyproject file up to date

In the project.scripts section of the pyproject.toml file, replace [INSERT_CLI_NAME] with the name of the executable you are creating and remove comments for the following two lines

> [project.scripts]
> [INSERT_CLI_NAME_HERE] = "cli:cli"
