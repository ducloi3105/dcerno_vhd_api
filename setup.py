#!/usr/bin/env python3
"""
Setup script for Dcerno VHD API development environment
"""

import os
import json
import yaml
from pathlib import Path


def create_env_yaml():
    """Create env.yaml template file"""
    env_config = {
        'ENVIRONMENT': 'development',
        'DEBUG': True,
        'SECRET_KEY': 'your-secret-key-change-this-in-production',
        'VERSION': 'v1',
        'MONGO_URI': 'mongodb://localhost:27017',
        'MONGO_DB_NAME': 'camera_tracking',
        'REDIS': {
            'password': '813417',
            'host': 'localhost',
            'port': 6379
        },
        'DCERNO_CONFIG': {
            'host': '192.168.0.20',
            'port': 5011
        },
        'VHD_CONFIG': {
            'ips': [
                'http://192.168.0.88'
            ]
        },
        'DECERNO_VHD_MAPPING_PATH': str(Path.home() / 'Documents' / 'decerno_vhd_camera_config.json'),
        'DECERNO_VHD_SETTING_PATH': str(Path.home() / 'Documents' / 'decerno_vhd_settings.json'),
        'SENTRY_DNS': ''
    }
    
    env_file = 'env.yaml'
    if not os.path.exists(env_file):
        with open(env_file, 'w') as f:
            yaml.dump(env_config, f, default_flow_style=False, indent=2)
        print(f"✓ Created {env_file}")
    else:
        print(f"- {env_file} already exists, skipping...")


def create_config_files():
    """Create configuration files for microphone-camera mapping"""
    documents_path = Path.home() / 'Documents'
    documents_path.mkdir(exist_ok=True)
    
    # Mapping config template
    mapping_config = {
        "example_micro_123": {
            "camera_ip": "192.168.0.88",
            "number": "1",
            "micro_id": "example_micro_123"
        },
        "example_micro_456": {
            "camera_ip": "192.168.0.89",
            "number": "2", 
            "micro_id": "example_micro_456"
        }
    }
    
    mapping_file = documents_path / 'decerno_vhd_camera_config.json'
    if not mapping_file.exists():
        with open(mapping_file, 'w') as f:
            json.dump(mapping_config, f, indent=2)
        print(f"✓ Created {mapping_file}")
    else:
        print(f"- {mapping_file} already exists, skipping...")
    
    # Tracking settings template
    tracking_settings = {
        "192.168.0.88": True,
        "192.168.0.89": False
    }
    
    settings_file = documents_path / 'decerno_vhd_settings.json'
    if not settings_file.exists():
        with open(settings_file, 'w') as f:
            json.dump(tracking_settings, f, indent=2)
        print(f"✓ Created {settings_file}")
    else:
        print(f"- {settings_file} already exists, skipping...")


def create_gitignore():
    """Create/update .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment
env.yaml
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Config files with sensitive data
**/config/production.yaml
**/config/staging.yaml

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Dependency directories
node_modules/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# next.js build output
.next

# Nuxt.js build output
.nuxt

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out

# Temporary folders
tmp/
temp/

# Database
*.db
*.sqlite

# Redis dump
dump.rdb
"""
    
    gitignore_file = '.gitignore'
    if not os.path.exists(gitignore_file):
        with open(gitignore_file, 'w') as f:
            f.write(gitignore_content)
        print(f"✓ Created {gitignore_file}")
    else:
        print(f"- {gitignore_file} already exists, skipping...")


def check_requirements():
    """Check if required tools are installed"""
    print("\n🔍 Checking requirements...")
    
    # Check Python version
    import sys
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is required")
        return False
    else:
        print(f"✓ Python {sys.version}")
    
    # Check Poetry
    import subprocess
    try:
        result = subprocess.run(['poetry', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {result.stdout.strip()}")
        else:
            print("❌ Poetry not found. Install from https://python-poetry.org/docs/#installation")
            return False
    except FileNotFoundError:
        print("❌ Poetry not found. Install from https://python-poetry.org/docs/#installation")
        return False
    
    # Check Docker (optional)
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {result.stdout.strip()}")
        else:
            print("⚠️  Docker not found (optional for development)")
    except FileNotFoundError:
        print("⚠️  Docker not found (optional for development)")
    
    return True


def install_dependencies():
    """Install Python dependencies using Poetry"""
    print("\n📦 Installing dependencies...")
    import subprocess
    
    try:
        result = subprocess.run(['poetry', 'install'], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Setting up Dcerno VHD API development environment...")
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup failed. Please install required tools and try again.")
        return
    
    # Create configuration files
    print("\n📄 Creating configuration files...")
    create_env_yaml()
    create_config_files()
    create_gitignore()
    
    # Install dependencies
    if not install_dependencies():
        return
    
    print("\n✅ Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Review and update env.yaml with your specific configuration")
    print("2. Update the mapping and settings JSON files in ~/Documents/")
    print("3. Start development:")
    print("   - API server: poetry run uvicorn src.api:app --host=0.0.0.0 --port=5000 --reload")
    print("   - Background tracking: poetry run python schedule_tracking.py")
    print("   - Or use Docker: docker-compose up -d")
    print("\n📚 See README.md and DEVELOPMENT.md for detailed documentation")


if __name__ == '__main__':
    main() 