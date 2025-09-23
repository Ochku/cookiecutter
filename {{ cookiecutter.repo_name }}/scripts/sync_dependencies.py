#!/usr/bin/env python3
"""Sync dependencies between environment.yml and pyproject.toml."""


import yaml


def read_dependencies():
    """Read dependencies from dependencies.yml."""
    with open("dependencies.yml") as f:
        return yaml.safe_load(f)


def write_environment_yml(deps):
    """Generate environment.yml from dependencies."""
    env_content = {
        "name": "kvk_database",
        "channels": ["conda-forge", "defaults"],
        "dependencies": [f"python={deps['dependencies']['python']}"],
    }

    # Add conda-available packages
    for pkg, version in deps["dependencies"]["packages"].items():
        env_content["dependencies"].append(f"{pkg}{version}")

    # Add pip-installable packages in a pip section
    pip_packages = []
    # Add dev dependencies
    for pkg, version in deps["dev_dependencies"].items():
        pip_packages.append(f"{pkg}{version}")
    # Add pip-only packages
    for pkg, version in deps["pip_only"].items():
        pip_packages.append(f"{pkg}{version}")

    if pip_packages:
        env_content["dependencies"].append({"pip": pip_packages})

    with open("environment.yml", "w") as f:
        yaml.dump(env_content, f, sort_keys=False, default_flow_style=False)


def update_pyproject_toml(deps):
    """Update dependencies in pyproject.toml."""
    with open("pyproject.toml") as f:
        content = f.read()

    # Create dependencies section
    deps_section = "\n[project.dependencies]\n"
    for pkg, version in deps["dependencies"]["packages"].items():
        deps_section += f'{pkg} = "{version}"\n'
    for pkg, version in deps["pip_only"].items():
        deps_section += f'{pkg} = "{version}"\n'

    # Create optional dependencies section for dev tools
    deps_section += "\n[project.optional-dependencies]\n"
    deps_section += "dev = [\n"
    for pkg, version in deps["dev_dependencies"].items():
        deps_section += f'    "{pkg}{version}",\n'
    deps_section += "]\n"

    # Find the insertion point after [project] section
    project_end = content.find("[tool.")
    if project_end == -1:
        project_end = len(content)

    # Insert dependencies sections
    new_content = content[:project_end] + deps_section + content[project_end:]

    with open("pyproject.toml", "w") as f:
        f.write(new_content)


def main():
    """Main function to sync dependencies."""
    deps = read_dependencies()
    write_environment_yml(deps)
    update_pyproject_toml(deps)
    print("Dependencies synced successfully!")


if __name__ == "__main__":
    main()
