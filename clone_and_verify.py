#!/usr/bin/env python3
"""
Git Clone and Verification Script for Ouroboros

This script clones the Ouroboros repository from GitHub to the target directory,
handles git configuration, and verifies the clone was successful.
Target directory: C:\Users\bam\Documents\bot
"""

import os
import subprocess
import pathlib
import sys
import json
from typing import Optional, Dict, Any

class GitCloneVerifier:
    def __init__(self, target_dir: str = r"C:\\Users\\bam\\Documents\\bot"):
        self.target_dir = pathlib.Path(target_dir)
        self.repo_url = "https://github.com/joi-lab/ouroboros.git"
        self.branch = "ouroboros"
        
    def print_header(self, title: str):
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        
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
            
    def check_directory(self) -> bool:
        """Check if target directory exists and has write permissions."""
        self.print_header("Checking Target Directory")
        
        try:
            if not self.target_dir.exists():
                self.target_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created directory: {self.target_dir}")
                
            # Test write permissions
            test_file = self.target_dir / "test_permission.txt"
            with open(test_file, "w") as f:
                f.write("test\n")
            test_file.unlink()
            
            print(f"Write permission OK: {self.target_dir}")
            return True
        except Exception as e:
            print(f"ERROR: Cannot write to directory: {e}")
            print(f"Please check permissions or choose a different directory.")
            return False
            
    def clone_repository(self) -> bool:
        """Clone the Ouroboros repository."""
        self.print_header("Cloning Ouroboros Repository")
        
        try:
            # Check if repository already exists
            if (self.target_dir / "ouroboros").exists():
                print("Repository already exists. Updating...")
                result = subprocess.run(["git", "pull", "origin", self.branch], 
                                      cwd=self.target_dir, 
                                      capture_output=True, text=True, check=True)
                print("Repository updated successfully.")
            else:
                result = subprocess.run(["git", "clone", "--branch", self.branch, 
                                        self.repo_url, "ouroboros"], 
                                      cwd=self.target_dir, 
                                      capture_output=True, text=True, check=True)
                print("Repository cloned successfully.")
                
            repo_path = self.target_dir / "ouroboros"
            print(f"Repository location: {repo_path}")
            
            # Verify clone
            if repo_path.exists():
                print("Verification: Repository directory exists")
                
                # Check for essential files
                essential_files = ["README.md", "BIBLE.md", "VERSION", "ouroboros/agent.py"]
                missing_files = []
                
                for file in essential_files:
                    file_path = repo_path / file
                    if file_path.exists():
                        print(f"  ✓ {file}")
                    else:
                        missing_files.append(file)
                        print(f"  ✗ {file} (missing)")
                
                if missing_files:
                    print(f"WARNING: {len(missing_files)} essential files missing")
                    return False
                
                print("Verification: All essential files present")
                return True
            else:
                print("ERROR: Repository directory not found after clone")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to clone repository: {e}")
            return False
            
    def verify_git_status(self) -> bool:
        """Verify git status and configuration."""
        self.print_header("Verifying Git Status")
        
        try:
            repo_path = self.target_dir / "ouroboros"
            
            # Check git status
            result = subprocess.run(["git", "status"], 
                                  cwd=repo_path, 
                                  capture_output=True, text=True, check=True)
            print(f"Git status:\n{result.stdout}")
            
            # Check current branch
            result = subprocess.run(["git", "branch", "--show-current"], 
                                  cwd=repo_path, 
                                  capture_output=True, text=True, check=True)
            current_branch = result.stdout.strip()
            print(f"Current branch: {current_branch}")
            
            if current_branch == self.branch:
                print("Branch verification: OK")
                return True
            else:
                print(f"WARNING: Expected branch '{self.branch}' but found '{current_branch}'")
                return False
                
        except Exception as e:
            print(f"ERROR: Failed to verify git status: {e}")
            return False
            
    def create_summary(self):
        """Create summary of the clone operation."""
        self.print_header("Clone Summary")
        
        repo_path = self.target_dir / "ouroboros"
        
        print("\nClone Summary:")
        print(f"  Target Directory: {self.target_dir}")
        print(f"  Repository URL: {self.repo_url}")
        print(f"  Branch: {self.branch}")
        print(f"  Repository Location: {repo_path}")
        print(f"  Repository Size: {sum(f.stat().st_size for f in repo_path.rglob('*') if f.is_file()) / (1024*1024):.2f} MB")
        
        # List important files
        print("\nImportant Files:")
        important_files = ["README.md", "BIBLE.md", "VERSION", "ouroboros/agent.py", "colab_launcher.py"]
        for file in important_files:
            file_path = repo_path / file
            if file_path.exists():
                print(f"  ✓ {file_path}")
            else:
                print(f"  ✗ {file_path} (missing)")
                
        print("\nNext Steps:")
        print("1. Review the configuration files")
        print("2. Set up API keys in configuration")
        print("3. Run the launcher script")
        print("4. Test basic functionality")
        
        print("\nClone completed successfully!")
        
    def run(self) -> bool:
        """Run the complete clone and verification process."""
        print("Ouroboros Git Clone and Verification Script")
        print("Version 1.0.0")
        
        # Check prerequisites
        if not self.check_git():
            return False
            
        if not self.check_directory():
            return False
            
        # Clone repository
        if not self.clone_repository():
            return False
            
        # Verify git status
        if not self.verify_git_status():
            return False
            
        # Create summary
        self.create_summary()
        
        return True

if __name__ == "__main__":
    # Create and run the verifier
    verifier = GitCloneVerifier()
    
    if verifier.run():
        print("\n✅ Clone and verification completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Clone and verification failed.")
        sys.exit(1)