#!/usr/bin/env python3
"""
Windows Setup Script for Ouroboros

This script automates the installation and configuration of Ouroboros on Windows.
It handles:
- Repository cloning
- Python environment setup
- Dependencies installation
- Configuration file creation
- First-run verification
"""

import sys
import os
import subprocess
import pathlib
import json
import shutil
import time
from typing import Optional, Dict, Any

class WindowsSetup:
    def __init__(self, install_dir: str = r"C:\Users\bam\Documents\bot"):
        self.install_dir = pathlib.Path(install_dir)
        self.repo_url = "https://github.com/joi-lab/ouroboros.git"
        self.venv_dir = self.install_dir / "venv"
        self.config_file = self.install_dir / "config.json"
        self.requirements_file = self.install_dir / "requirements.txt"
        
    def print_header(self, title: str):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        
    def check_python(self) -> bool:
        """Check if Python is available and get version info."""
        self.print_header("Checking Python Installation")
        
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"Python found: {result.stdout.strip()}")
            print(f"Python executable: {sys.executable}")
            return True
        except Exception as e:
            print(f"ERROR: Python not found or not accessible: {e}")
            return False
            
    def check_uv(self) -> bool:
        """Check if uv is available for Python version management."""
        self.print_header("Checking uv Installation")
        
        try:
            result = subprocess.run(["uv", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"uv found: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"WARNING: uv not found. Using system Python.")
            print(f"You can install uv from: https://github.com/astral-sh/uv")
            return False
            
    def check_git(self) -> bool:
        """Check if Git is available."""
        self.print_header("Checking Git Installation")
        
        try:
            result = subprocess.run(["git", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"Git found: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"ERROR: Git not found or not accessible: {e}")
            print("Please install Git from: https://git-scm.com/download/win")
            return False
            
    def check_permissions(self) -> bool:
        """Check write permissions to installation directory."""
        self.print_header("Checking Directory Permissions")
        
        try:
            if not self.install_dir.exists():
                self.install_dir.mkdir(parents=True, exist_ok=True)
                
            test_file = self.install_dir / "test_permission.txt"
            with open(test_file, "w") as f:
                f.write("test\n")
            test_file.unlink()
            
            print(f"Write permission OK: {self.install_dir}")
            return True
        except Exception as e:
            print(f"ERROR: Cannot write to directory: {e}")
            print(f"Please check permissions or choose a different directory.")
            return False
            
    def clone_repository(self) -> bool:
        """Clone the Ouroboros repository."""
        self.print_header("Cloning Ouroboros Repository")
        
        try:
            if (self.install_dir / "ouroboros").exists():
                print("Repository already exists. Updating...")
                result = subprocess.run(["git", "pull", "origin", "ouroboros"], 
                                      cwd=self.install_dir, 
                                      capture_output=True, text=True, check=True)
                print("Repository updated successfully.")
            else:
                result = subprocess.run(["git", "clone", "--branch", "ouroboros", 
                                        self.repo_url, "ouroboros"], 
                                      cwd=self.install_dir, 
                                      capture_output=True, text=True, check=True)
                print("Repository cloned successfully.")
                
            print(f"Repository location: {self.install_dir / 'ouroboros'}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to clone repository: {e}")
            return False
            
    def setup_virtual_environment(self) -> bool:
        """Set up Python virtual environment."""
        self.print_header("Setting Up Virtual Environment")
        
        try:
            if self.venv_dir.exists():
                print("Virtual environment already exists. Skipping...")
                return True
                
            if self.check_uv():
                print("Creating virtual environment with uv...")
                result = subprocess.run(["uv", "venv", "--python", "3.11", str(self.venv_dir)], 
                                      cwd=self.install_dir, 
                                      capture_output=True, text=True, check=True)
            else:
                print("Creating virtual environment with venv module...")
                result = subprocess.run([sys.executable, "-m", "venv", str(self.venv_dir)], 
                                      cwd=self.install_dir, 
                                      capture_output=True, text=True, check=True)
                
            print(f"Virtual environment created: {self.venv_dir}")
            
            # Verify activation
            activate_script = self.venv_dir / "Scripts" / "activate"
            if activate_script.exists():
                print("Virtual environment activation script found.")
                return True
            else:
                print("WARNING: Virtual environment activation script not found.")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to create virtual environment: {e}")
            return False
            
    def install_dependencies(self) -> bool:
        """Install Python dependencies."""
        self.print_header("Installing Python Dependencies")
        
        try:
            # Copy requirements.txt from repository
            repo_requirements = self.install_dir / "ouroboros" / "requirements.txt"
            if repo_requirements.exists():
                shutil.copy(repo_requirements, self.install_dir)
                print(f"Copied requirements.txt: {self.requirements_file}")
            else:
                print("WARNING: requirements.txt not found in repository.")
                
            # Install dependencies
            pip_executable = self.venv_dir / "Scripts" / "pip.exe"
            if not pip_executable.exists():
                print("WARNING: pip not found in virtual environment.")
                return False
                
            # Install from requirements.txt if available
            if self.requirements_file.exists():
                print(f"Installing dependencies from {self.requirements_file}...")
                result = subprocess.run([str(pip_executable), "install", "-r", str(self.requirements_file)], 
                                      cwd=self.install_dir, 
                                      capture_output=True, text=True, check=True)
            else:
                print("Installing core dependencies directly...")
                result = subprocess.run([str(pip_executable), "install", 
                                        "openai>=1.0.0", "requests", "playwright", "playwright-stealth"], 
                                      cwd=self.install_dir, 
                                      capture_output=True, text=True, check=True)
                
            print("Dependencies installed successfully.")
            return True
        except Exception as e:
            print(f"ERROR: Failed to install dependencies: {e}")
            return False
            
    def setup_configuration(self) -> bool:
        """Create configuration file with API keys."""
        self.print_header("Setting Up Configuration")
        
        try:
            config = {
                "openrouter_api_key": "YOUR_OPENROUTER_API_KEY_HERE",
                "google_drive_credentials": "YOUR_GOOGLE_DRIVE_CREDENTIALS_JSON_HERE",
                "telegram_bot_token": "YOUR_TELEGRAM_BOT_TOKEN_HERE",
                "telegram_owner_id": 6266662418,
                "budget_total_usd": 10.0,
                "install_dir": str(self.install_dir),
                "python_executable": str(self.venv_dir / "Scripts" / "python.exe") if self.venv_dir.exists() else sys.executable,
                "version": "6.2.0"
            }
            
            with open(self.config_file, "w") as f:
                json.dump(config, f, indent=2)
                
            print(f"Configuration file created: {self.config_file}")
            print("\nIMPORTANT: Edit this file to add your API keys:")
            print(f"  {self.config_file}")
            print("\nRequired keys:")
            print("  - OpenRouter API key (for LLM access)")
            print("  - Google Drive credentials (for memory storage)")
            print("  - Telegram bot token (for communication)")
            
            return True
        except Exception as e:
            print(f"ERROR: Failed to create configuration file: {e}")
            return False
            
    def verify_installation(self) -> bool:
        """Verify the installation works correctly."""
        self.print_header("Verifying Installation")
        
        try:
            print("Testing Python execution...")
            python_executable = self.venv_dir / "Scripts" / "python.exe" if self.venv_dir.exists() else sys.executable
            result = subprocess.run([str(python_executable), "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"Python OK: {result.stdout.strip()}")
            
            print("Testing pip...")
            pip_executable = self.venv_dir / "Scripts" / "pip.exe" if self.venv_dir.exists() else python_executable
            result = subprocess.run([str(pip_executable), "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"pip OK: {result.stdout.strip()}")
            
            print("Testing git...")
            result = subprocess.run(["git", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"git OK: {result.stdout.strip()}")
            
            if (self.install_dir / "ouroboros").exists():
                print("Repository OK: Found ouroboros directory")
            
            if self.config_file.exists():
                print(f"Configuration OK: {self.config_file}")
                
            print("\nInstallation verification completed successfully!")
            return True
        except Exception as e:
            print(f"ERROR: Installation verification failed: {e}")
            return False
            
    def create_startup_script(self) -> bool:
        """Create a startup script for easy launching."""
        self.print_header("Creating Startup Script")
        
        try:
            startup_script = self.install_dir / "start_ouroboros.bat"
            
            with open(startup_script, "w") as f:
                f.write(f"@echo off\n")
                f.write(f"echo Starting Ouroboros...\n")
                f.write(f"cd {self.install_dir / 'ouroboros'}\n")
                
                if self.venv_dir.exists():
                    f.write(f"{self.venv_dir / 'Scripts' / 'activate.bat'} && python ouroboros/agent.py\n")
                else:
                    f.write(f"python ouroboros/agent.py\n")
                    
                f.write(f"pause\n")
                
            print(f"Startup script created: {startup_script}")
            print("You can now start Ouroboros by double-clicking this file.")
            return True
        except Exception as e:
            print(f"ERROR: Failed to create startup script: {e}")
            return False
            
    def create_uninstall_script(self) -> bool:
        """Create an uninstall script."""
        self.print_header("Creating Uninstall Script")
        
        try:
            uninstall_script = self.install_dir / "uninstall_ouroboros.bat"
            
            with open(uninstall_script, "w") as f:
                f.write(f"@echo off\n")
                f.write(f"echo Uninstalling Ouroboros...\n")
                f.write(f"echo This will delete the entire installation directory:\n")
                f.write(f"echo {self.install_dir}\n")
                f.write(f"echo.\n")
                f.write(f"choice /M \"Are you sure you want to continue?\"\n")
                f.write(f"if errorlevel 2 goto :eof\n")
                f.write(f"echo.\n")
                f.write(f"echo Deleting installation directory...\n")
                f.write(f"rmdir /s /q {self.install_dir}\n")
                f.write(f"echo Ouroboros has been uninstalled.\n")
                f.write(f"pause\n")
                
            print(f"Uninstall script created: {uninstall_script}")
            return True
        except Exception as e:
            print(f"ERROR: Failed to create uninstall script: {e}")
            return False
            
    def print_summary(self):
        """Print installation summary."""
        self.print_header("Installation Complete!")
        
        print("\nInstallation Summary:")
        print(f"  Installation Directory: {self.install_dir}")
        print(f"  Repository: {self.install_dir / 'ouroboros'}")
        print(f"  Configuration: {self.config_file}")
        print(f"  Virtual Environment: {self.venv_dir if self.venv_dir.exists() else 'Not created'}")
        print(f"  Startup Script: {self.install_dir / 'start_ouroboros.bat'}")
        print(f"  Uninstall Script: {self.install_dir / 'uninstall_ouroboros.bat'}")
        
        print("\n\nNext Steps:")
        print("1. Edit the configuration file to add your API keys:")
        print(f"   {self.config_file}")
        print("   - OpenRouter API key (for LLM access)")
        print("   - Google Drive credentials (for memory storage)")
        print("   - Telegram bot token (for communication)")
        print("2. Start Ouroboros by double-clicking:")
        print(f"   {self.install_dir / 'start_ouroboros.bat'}")
        print("3. Or run manually:")
        print(f"   cd {self.install_dir / 'ouroboros'}")
        print(f"   python ouroboros/agent.py")
        
        print("\nAPI Keys Required:")
        print("  - OpenRouter API key: https://openrouter.ai/")
        print("  - Google Drive API: https://console.cloud.google.com/")
        print("  - Telegram Bot Token: https://t.me/botfather")
        
        print("\nFor more information, visit:")
        print("  https://joi-lab.github.io/ouroboros/")
        
        print("\nThank you for installing Ouroboros!")
        
    def run(self) -> bool:
        """Run the complete installation process."""
        print("Ouroboros Windows Setup Script")
        print("==============================")
        
        # Check prerequisites
        if not self.check_python():
            return False
            
        if not self.check_git():
            return False
            
        if not self.check_permissions():
            return False
            
        # Run installation steps
        success = True
        
        if not self.clone_repository():
            success = False
            
        if not self.setup_virtual_environment():
            success = False
            
        if not self.install_dependencies():
            success = False
            
        if not self.setup_configuration():
            success = False
            
        if not self.verify_installation():
            success = False
            
        if not self.create_startup_script():
            success = False
            
        if not self.create_uninstall_script():
            success = False
            
        # Print summary
        self.print_summary()
        
        return success


def main():
    """Main entry point."""
    # Get installation directory from command line or use default
    install_dir = r"C:\Users\bam\Documents\bot"
    
    if len(sys.argv) > 1:
        install_dir = sys.argv[1]
        
    setup = WindowsSetup(install_dir)
    
    try:
        if setup.run():
            print(f"\n\nSetup completed successfully!")
            return 0
        else:
            print(f"\n\nSetup completed with errors.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n\nUnexpected error during setup: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())