# Cookiecutter Data Science SaWiDay

_A logical, reasonably standardized but flexible project structure for doing and sharing data science work within the SaWiDay organisation._

[![PyPI - Version](https://img.shields.io/pypi/v/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

**Cookiecutter Data Science (CCDS)** is a tool for setting up a data science project template that incorporates best practices. To learn more about CCDS's philosophy, visit the [project homepage](https://cookiecutter-data-science.drivendata.org/).

This project has been cloned and addapted to fit the usecases within the SaWiDay organisation, taylored for Data Science projects.  

## Installation

Cookiecutter Data Science v2 requires Python 3.9+. Since this is a cross-project utility application, we recommend installing it as follows. Installation command options:

```bash
# Initialize a github repository to ensure pre-commit hooks are automatically linked during set up
git clone https://github.com/Ochku/cookiecutter.git
git init

# Witin your IDE set up an environment for the cookiecutter dependancies to host
conda create --name cookiecutter -y
conda activate cookiecutter
conda install -c conda-forge cookiecutter 
pip install cookiecutter-data-science conda-lock
```

## Starting a new project

To start a new project, run:

```bash
cookiecutter https://github.com/Ochku/cookiecutter_ds_template
```

### The resulting directory structure

The directory structure of your new project will look something like this (depending on the settings that you choose):

```
{{ cookiecutter.repo_name }}/           <- Name of the project
├── {{ cookiecutter.module_name }}/     <- Main package of functions used
│   ├── __init__.py                     <- Package initialization
│   ├── config.py                       <- Configuration using Pydantic and environment variables
│   ├── db_utils.py                     <- Utilities to load data from SQL database
│   ├── src.py                          <- Source file holding the main code base
│
├── data/                               <- Data directory
│   ├── raw/                            <- Raw, immutable data
│   └── processed/                      <- Cleaned, processed data
│
├── notebooks/                          <- Jupyter notebooks
│
├── output/                             <- Output files and models
│
├── scripts/                            <- Utility scripts
│   └── generate_lock.py                <- Script to generate conda-lock files
│   └── sync_dependencies.py            <- Sync dependencies between environment.yml and pyproject.toml
│
├── docs/                               <- A default mkdocs project; see www.mkdocs.org for details
│
├── .env.example                       <- Example environment variables
├── .pre-commit-config.yaml            <- Pre-commit hooks configuration
├── dependencies.yml                   <- Central dependencies definition
├── environment.yml                    <- Conda environment specification
├── pyproject.toml                     <- Python project configuration and tool settings
└── conda-lock.yml                     <- Lock file for reproducible environments
```

## Dependencies and Environment Setup
### Dependencies

Dependencies are managed in three files:
1. `dependencies.yml`: Central definition of all dependencies
2. `environment.yml`: Conda environment specification
3. `conda-lock.yml`: Generated lock file for reproducible environments

### Set up the environment after directory creation

To create the Conda environment for this project using a lock file:

```bash
conda env create --name env_name --file conda-win-64.lock.yml
```

### Updating Dependencies

If you need to add or update dependencies:

1. Export the current environment to `environment.yml`:
   ```bash
   conda env export > environment.yml
   ```
2. Remove the existing lock file using one of the following commands:
   ```bash
   rm conda-lock.yml
   del conda-lock.yml 
   ```
3. Generate a new lock file for Windows (win-64):
   ```bash
   conda-lock lock --file environment.yml --platform win-64
   ```
4. (Optional) Remove the previous environment:
   ```bash
   conda env remove --name env_name
   ```
5. Create or update the environment from the lock file:
   ```bash
   conda-lock install --name env_name conda-lock.yml
   ```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and adjust the values:
```bash
cp .env.example .env
```

Available settings:
- `DATA_DIR`: Directory for data files (default: "data")
- `OUTPUT_DIR`: Directory for outputs (default: "output")
- `API_KEY`: API key for external services
- `DATABASE_URL`: Database connection string
- `DATABASE_USER`: Username string for database connection
- `DB_PASSWORD`: Password string for database connection
- `DB_NAME`: Database name string for database connection

## Project Documentation with MkDocs
This project uses MkDocs to manage and publish documentation. The content is written in Markdown and organized using a clear folder structure, making the documentation maintainable, readable, and scalable.

### Documentation Structure
All MkDocs files are located in the docs/ directory and follow this layout standard:

```
docs/
│
├── index.md                        <- Landing page of the documentation
│
├── guides/                         <- Tutorials and how-to guides
│   └── getting-started.md         <- Getting started with the project
│
├── references/                     <- Technical reference documents
│   └── api.md                      <- API reference and specifications
│
└── decision_log.md                <- Log of key project decisions
```

This stucture serves as a start so feel free to add and changes to accomdate to your project.

### YAML Configuration (mkdocs.yml)
The navigation structure is defined in the mkdocs.yml configuration file:

```yaml
nav:
  - Home: index.md
  - Guides:
      - Getting Started: guides/getting-started.md
  - References:
      - API Reference: references/api.md
  - Decision log: decision_log.md
```

### Serve Documentation Locally
To preview the documentation locally:

```bash
pip install mkdocs-material
mkdocs serve
```
Then open: http://localhost:8000

