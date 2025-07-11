#!/bin/bash

echo "🚀 Railway Deployment Setup Script"
echo "=================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial Railway deployment setup"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if all required files exist
echo "🔍 Checking required files..."

required_files=("requirements.txt" "Procfile" "runtime.txt" "railway.json" "bot.py" "config.py")

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

echo ""
echo "🎯 Next Steps:"
echo "1. Create a GitHub repository"
echo "2. Push your code: git remote add origin YOUR_GITHUB_REPO_URL"
echo "3. Push: git push -u origin main"
echo "4. Go to Railway.app and connect your GitHub repo"
echo "5. Add your environment variables in Railway dashboard"
echo ""
echo "📖 See RAILWAY_DEPLOYMENT_GUIDE.md for detailed instructions"
