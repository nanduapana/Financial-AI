@echo off
cd "C:\Users\nandk\Documents\Project Documentation\Financial-AI"

:: Initialize Git repository if not already initialized
git rev-parse --is-inside-work-tree 2>nul
if %errorlevel% neq 0 (
    git init
    git remote add origin https://github.com/your-username/your-repo-name.git
)

:: Add and commit changes
git add .
git commit -m "Updated data and preprocessing scripts"

:: Push changes to the remote repository
git push origin main  :: Change to master if your default branch is master

pause
