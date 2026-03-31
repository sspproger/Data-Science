#!/usr/bin/env python3

import subprocess
import sys
import os
import zipfile

def check_env():
    if not os.environ.get('VIRTUAL_ENV'):
        raise Exception("Activate virtual environment first!")
    return os.environ['VIRTUAL_ENV']

def install_packages():
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', '../../datasets/requirements.txt'], check=True)

def save_packages():
    result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True)
    packages = [p for p in result.stdout.strip().split('\n') if p and '==' in p]
    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(packages))
    return packages

def create_archive(env_path):
    env_name = os.path.basename(env_path)
    with zipfile.ZipFile(f'{env_name}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(env_path):
            dirs[:] = [d for d in dirs if d not in ['__pycache__']]
            for file in files:
                if not file.endswith('.pyc'):
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, os.path.dirname(env_path))
                    zipf.write(file_path, arcname)
    return f'{env_name}.zip'

def main():
    try:
        env_path = check_env()
        print(f"Env: {os.path.basename(env_path)}")
        
        install_packages()
        
        packages = save_packages()
        for pkg in sorted(packages):
            print(pkg)
        
        archive = create_archive(env_path)
        print(f"Archive created: {archive}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
