@echo off
cd "C:\Users\nandk\Documents\Project Documentation\Financial-AI"

git rev-parse --is-inside-work-tree 2>nul
if %errorlevel% neq 0 (
    git init
    git remote add origin https://github.com/your-username/your-repo-name.git
)

git add .
git commit -m "Updated data and preprocessing scripts"

git push origin main  :: Change to master if your default branch is master

pause
