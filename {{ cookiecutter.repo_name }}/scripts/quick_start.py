#!/usr/bin/env python3
"""Quick start script to set up the entire project environment."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def check_conda_available():
    """Check if conda is available."""
    try:
        subprocess.run(["conda", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def create_conda_environment(env_name):
    """Create conda environment from lock file."""
    lock_file = Path("conda-win-64.lock.yml")
    
    if lock_file.exists():
        print(f"📦 Found lock file: {lock_file}")
        return run_command(f"conda env create --name {env_name} --file {lock_file}", 
                         f"Creating conda environment '{env_name}'")
    else:
        print("⚠️  No lock file found, creating environment from environment.yml")
        return run_command(f"conda env create --name {env_name} --file environment.yml", 
                         f"Creating conda environment '{env_name}'")


def activate_environment_instructions(env_name):
    """Print instructions for activating the environment."""
    print(f"\n🔧 Next steps to activate your environment:")
    print(f"   1. Activate the conda environment:")
    print(f"      conda activate {env_name}")
    print(f"   2. Install the package in development mode:")
    print(f"      pip install -e .")
    print(f"   3. Set up development tools:")
    print(f"      python scripts/dev_setup.py")
    print(f"   4. Run health check:")
    print(f"      python scripts/health_check.py")
    print(f"   5. Start coding!")


def main():
    """Main quick start function."""
    print("🚀 Welcome to {{ cookiecutter.project_name }}!")
    print("=" * 50)
    
    # Check if we're already in a conda environment
    current_env = os.environ.get('CONDA_DEFAULT_ENV')
    if current_env and current_env != 'base':
        print(f"📦 You're already in conda environment: {current_env}")
        print("💡 If you want to create a new environment, deactivate first with 'conda deactivate'")
        return 0
    
    # Check if conda is available
    if not check_conda_available():
        print("❌ Conda is not available. Please install Anaconda or Miniconda first.")
        print("   Download from: https://docs.conda.io/en/latest/miniconda.html")
        return 1
    
    # Get environment name from user
    default_env = "{{ cookiecutter.module_name }}_env"
    print(f"\n📝 Enter a name for your conda environment (or press Enter for '{default_env}'):")
    env_name = input().strip() or default_env
    
    print(f"\n🎯 Setting up environment: {env_name}")
    
    # Create conda environment
    if not create_conda_environment(env_name):
        print("❌ Failed to create conda environment")
        return 1
    
    # Print next steps
    activate_environment_instructions(env_name)
    
    print(f"\n🎉 Environment '{env_name}' created successfully!")
    print("💡 Remember to activate it before continuing with development setup.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

