import shutil
from pathlib import Path
import subprocess
import sys
import yaml
import tomlkit

def create_dependencies_yml():
    """Create the dependencies.yml file with all required packages."""
    deps = {
        "dependencies": {
            "python": "{{ cookiecutter.python_version_number }}",
            "packages": {
                "numpy": ">=1.24.0",
                "pandas": ">=2.0.0",
                "scikit-learn": ">=1.3.0",
                "matplotlib": ">=3.7.0",
                "seaborn": ">=0.12.0",
                "jupyter": ">=1.0.0"
            }
        },
        "dev_dependencies": {
            "ruff": ">=0.4.0",
            "black": ">=24.0.0",
            "mypy": ">=1.9.0",
            "bandit": ">=1.7.7",
            "nbstripout": ">=0.6.1",
            {% if cookiecutter.pre_commit_hook == "yes" %}
            "pre-commit": ">=3.5.0",
            {% endif %}
            "pytest": ">=8.0.0"
        },
        "pip_only": {
            "pydantic": ">=2.0.0",
            "pydantic-settings": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    }

    with open("dependencies.yml", "w") as f:
        yaml.dump(deps, f, sort_keys=False, default_flow_style=False)

def generate_lock_files():
    """Generate conda-lock file."""
    try:
        # Generate single lock file for current platform
        subprocess.run([
            "conda-lock",
            "lock",
            "--file", "environment.yml",
        ], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to generate lock files: {e}")
        print("You can generate them later with: conda-lock lock --file environment.yml")

def resolve_python_version_specifier(python_version):
    version_parts = python_version.split(".")
    if len(version_parts) == 2:
        major, minor = version_parts
        patch = "0"
        operator = "~="
    elif len(version_parts) == 3:
        major, minor, patch = version_parts
        operator = "=="
    else:
        raise ValueError(f"Invalid Python version: {python_version}")

    return f"{operator}{major}.{minor}.{patch}"

def write_python_version(python_version, pyproject_path="pyproject.toml"):
    try:
        with open(pyproject_path, "r") as f:
            doc = tomlkit.parse(f.read())

        doc["project"]["requires-python"] = resolve_python_version_specifier(python_version)

        with open(pyproject_path, "w") as f:
            f.write(tomlkit.dumps(doc))
    except Exception as e:
        print(f"Warning: Could not update pyproject.toml: {e}")

# Create dependencies.yml
create_dependencies_yml()

# Update pyproject.toml with correct Python version
py_version = "{{ cookiecutter.python_version_number }}"
write_python_version(py_version, Path("pyproject.toml"))

# Generate lock files
generate_lock_files()

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
try:
    pyproject_text = Path("pyproject.toml").read_text()
    Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))
except Exception as e:
    print(f"Warning: Could not clean up pyproject.toml: {e}")

# Handle scaffolding based on user choices
module_dir = Path("{{ cookiecutter.module_name }}")

# Remove scaffold files if not requested
{% if cookiecutter.scaffolding_basic == "no" %}
basic_files = ["config.py", "src.py"]
for file_name in basic_files:
    file_path = module_dir / file_name
    if file_path.exists():
        file_path.unlink()
{% endif %}

{% if cookiecutter.scaffolding_database == "no" %}
db_files = ["db_utils.py"]
for file_name in db_files:
    file_path = module_dir / file_name
    if file_path.exists():
        file_path.unlink()
{% endif %}

{% if cookiecutter.scaffolding_visualisations == "no" %}
viz_files = ["visualizations.py"]
for file_name in viz_files:
    file_path = module_dir / file_name
    if file_path.exists():
        file_path.unlink()
{% endif %}

{% if cookiecutter.scaffolding_data_cleaning == "no" %}
cleaning_files = ["data_cleaning.py"]
for file_name in cleaning_files:
    file_path = module_dir / file_name
    if file_path.exists():
        file_path.unlink()
{% endif %}

# Remove notebooks if not requested
{% if cookiecutter.include_notebooks == "no" %}
notebooks_dir = Path("notebooks")
if notebooks_dir.exists():
    shutil.rmtree(notebooks_dir)
{% endif %}

{% if cookiecutter.pre_commit_hook == "yes" %}
# Initialize pre-commit hooks
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "pre-commit"], check=True)
    subprocess.run(["pre-commit", "install"], check=True)
except subprocess.CalledProcessError:
    print("Warning: Failed to initialize pre-commit hooks. Please run 'pre-commit install' manually after setting up your environment.")
{% endif %}

# Remove optional files when features are disabled
{% if cookiecutter.pre_commit_hook != "yes" %}
pre_commit_config = Path(".pre-commit-config.yaml")
if pre_commit_config.exists():
    pre_commit_config.unlink()
{% endif %}

# Create .env.example file
env_example_content = f"""# Project paths
DATA_DIR={{ cookiecutter.project_slug }}/data
RAW_DIR={{ cookiecutter.project_slug }}/data/raw
PROCESSED_DIR={{ cookiecutter.project_slug }}/data/processed
OUTPUT_DIR={{ cookiecutter.project_slug }}/output

# API configurations
API_KEY=your_api_key_here

# Database configurations
DB_URL=db_url
DB_USER=db_user
DB_PASSWORD=db_password
DB_NAME=db_name
"""

with open(".env.example", "w") as f:
    f.write(env_example_content)

print("Project generated successfully!")
print("Next steps:")
print("1. cd {{ cookiecutter.project_slug }}")
print("2. conda env create -f environment.yml")
print("3. conda activate {{ cookiecutter.project_slug }}")
print("4. pip install -e .")
{% if cookiecutter.pre_commit_hook == "yes" %}
print("5. pre-commit install")
{% endif %}
