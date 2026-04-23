#!/usr/bin/env python
"""
Quick start script to set up the project locally.
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n{'='*50}")
    print(f"  {description}")
    print(f"{'='*50}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    # Create virtual environment
    run_command('python -m venv venv', 'Creating virtual environment')
    
    # Activate and install dependencies
    if sys.platform == 'win32':
        activate = 'venv\\Scripts\\activate.bat'
    else:
        activate = 'source venv/bin/activate'
    
    run_command(f'{activate} && pip install --upgrade pip', 'Upgrading pip')
    run_command(f'{activate} && pip install -r requirements.txt', 'Installing dependencies')
    
    # Copy environment file
    if not os.path.exists('.env'):
        run_command('copy .env.example .env', 'Creating .env file')
        print("\n⚠️  IMPORTANT: Please edit .env and add your OpenAI API key!")
    
    # Run migrations
    run_command(f'{activate} && python manage.py migrate', 'Running migrations')
    
    # Create superuser prompt
    print("\n" + "="*50)
    print("  Create Django Superuser")
    print("="*50)
    print("You will now create a superuser account for Django admin.")
    if sys.platform == 'win32':
        os.system('venv\\Scripts\\activate.bat && python manage.py createsuperuser')
    else:
        os.system('source venv/bin/activate && python manage.py createsuperuser')
    
    print("\n✅ Setup complete!")
    print("\nTo start the development server, run:")
    if sys.platform == 'win32':
        print("  venv\\Scripts\\activate.bat")
    else:
        print("  source venv/bin/activate")
    print("  python manage.py runserver")
