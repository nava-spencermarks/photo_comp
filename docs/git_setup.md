# GitHub Setup Guide 🚀

## Step 1: Initialize Git Repository
```bash
cd /Users/sam/Documents/dev/nava/photo-comp
git init
```

## Step 2: Create .gitignore
```bash
cat > .gitignore << 'EOF'
# Python
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

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test outputs
*.coverage
.pytest_cache/
.tox/

# Temporary files
*.tmp
*_temp_copy.png
EOF
```

## Step 3: Stage All Files
```bash
git add .
```

## Step 4: Make Initial Commit
```bash
git commit -m "Initial commit: Face comparison tool with robust detection

- Multi-strategy face detection (HOG, CNN, OpenCV fallback)
- Comprehensive test suite with 100% pass rate
- Clean, human-readable output with confidence scores
- Handles various image formats and edge cases
- Complete documentation and usage examples

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Step 5: Create GitHub Repository
1. Go to https://github.com
2. Click "New repository" (green button)
3. Name it: `face-comparison-tool` or `photo-comp`
4. Keep it public
5. DON'T initialize with README (we already have one)
6. Click "Create repository"

## Step 6: Connect to GitHub
```bash
# Replace YOUR_USERNAME and YOUR_REPO_NAME with actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
```

## Step 7: Push to GitHub
```bash
git push -u origin main
```

## Alternative: Using GitHub CLI (if you have it installed)
```bash
# Create repo directly from command line
gh repo create face-comparison-tool --public --source=. --remote=origin --push
```

## Verify Your Repository
After pushing, your GitHub repo should contain:
- ✅ README.md with full documentation
- ✅ All Python source files
- ✅ Complete test suite
- ✅ requirements.txt
- ✅ .gitignore
- ✅ Clean commit history

## Future Updates
```bash
# Make changes to your code
git add .
git commit -m "Your update message"
git push
```