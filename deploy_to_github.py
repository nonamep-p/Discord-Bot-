
import subprocess
import os
import sys

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {command}")
            return True
        else:
            print(f"❌ {command}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def deploy_to_github():
    """Deploy code to GitHub repository"""
    print("🚀 Starting deployment to GitHub...")
    
    # Check if git is installed
    if not run_command("git --version"):
        print("❌ Git is not installed!")
        return False
    
    # Initialize git if not already done
    if not os.path.exists('.git'):
        run_command("git init")
    
    # Set up remote repository
    remote_url = "https://github.com/nonamep-p/Discord-Bot-.git"
    
    # Remove existing remote if it exists
    run_command("git remote remove origin")
    
    # Add the remote repository
    if not run_command(f"git remote add origin {remote_url}"):
        print("❌ Failed to add remote repository!")
        return False
    
    # Add all files
    if not run_command("git add ."):
        print("❌ Failed to add files!")
        return False
    
    # Commit changes
    commit_message = "Complete bot implementation with economy, games, and all README features"
    if not run_command(f'git commit -m "{commit_message}"'):
        print("❌ Failed to commit changes!")
        return False
    
    # Set the main branch
    run_command("git branch -M main")
    
    # Push to GitHub
    if not run_command("git push -u origin main --force"):
        print("❌ Failed to push to GitHub!")
        print("You may need to authenticate with GitHub.")
        print("Try running: git push -u origin main --force")
        return False
    
    print("✅ Successfully deployed to GitHub!")
    print(f"🔗 Repository: {remote_url}")
    return True

if __name__ == "__main__":
    deploy_to_github()
