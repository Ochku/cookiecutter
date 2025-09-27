# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── {{ cookiecutter.module_name }}/          # Source code
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── src.py              # Main processing script
│   {% if cookiecutter.scaffolding_database == "yes" %}
│   ├── db_utils.py         # Database utilities
│   {% endif %}
│   {% if cookiecutter.scaffolding_visualisations == "yes" %}
│   ├── visualizations.py   # Visualization utilities
│   {% endif %}
│   {% if cookiecutter.scaffolding_data_cleaning == "yes" %}
│   ├── data_cleaning.py    # Data cleaning utilities
│   {% endif %}
├── data/                   # Data directory
│   ├── raw/               # Raw data
│   ├── processed/         # Processed data
│   └── external/          # External data
├── notebooks/             # Jupyter notebooks
{% if cookiecutter.include_notebooks == "yes" %}
│   └── start_set_up.ipynb # Setup notebook
{% endif %}
├── output/                # Output files
├── environment.yml        # Conda environment
├── pyproject.toml         # Project configuration
{% if cookiecutter.pre_commit_hook == "yes" %}
├── .pre-commit-config.yaml # Pre-commit hooks
{% endif %}
└── README.md              # This file
```

## Setup

1. **Create conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate {{ cookiecutter.project_slug }}
   ```

2. **Install in development mode:**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

{% if cookiecutter.pre_commit_hook == "yes" %}
4. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```
{% endif %}

## Usage

### Basic Usage

```python
from {{ cookiecutter.module_name }}.config import settings
from {{ cookiecutter.module_name }}.src import main

# Use settings
print(f"Data directory: {settings.data_dir}")

# Run main processing
main()
```

{% if cookiecutter.scaffolding_database == "yes" %}
### Database Usage

```python
from {{ cookiecutter.module_name }}.db_utils import extract_query

# Query database
df = extract_query("SELECT * FROM my_table")
```
{% endif %}

{% if cookiecutter.scaffolding_visualisations == "yes" %}
### Visualization Usage

```python
from {{ cookiecutter.module_name }}.visualizations import create_plot, plot_correlation_matrix

# Create plots
fig = create_plot(data, "scatter", "My Plot", "x", "y")
corr_fig = plot_correlation_matrix(data)
```
{% endif %}

{% if cookiecutter.scaffolding_data_cleaning == "yes" %}
### Data Cleaning Usage

```python
from {{ cookiecutter.module_name }}.data_cleaning import clean_data_pipeline

# Clean data
cleaned_data = clean_data_pipeline(
    raw_data,
    text_columns=['name', 'description'],
    outlier_columns=['age', 'salary']
)
```
{% endif %}

## Development

### Running Tests
{% if cookiecutter.include_tests == "yes" %}
```bash
pytest
```
{% else %}
No tests configured. Add pytest to your dependencies to enable testing.
{% endif %}

### Code Quality
```bash
# Format code
black {{ cookiecutter.module_name }}

# Lint code
ruff check {{ cookiecutter.module_name }}

# Type checking
mypy {{ cookiecutter.module_name }}
```

## Configuration

The project uses Pydantic for configuration management. Key settings can be configured via environment variables:

- `DATA_DIR`: Data directory path
- `RAW_DIR`: Raw data directory path
- `PROCESSED_DIR`: Processed data directory path
- `OUTPUT_DIR`: Output directory path
- `API_KEY`: API key for external services
- `DATABASE_URL`: Database connection URL
- `DATABASE_USER`: Database username
- `DATABASE_PASSWORD`: Database password
- `DATABASE_NAME`: Database name
- `LOG_LEVEL`: Logging level (default: INFO)

## License

[Add your license here]
