#!/bin/bash
# =============================================================================
# GitHub Repo Creator — Turn existing local project into a new GitHub repo
# Works on macOS (requires gh CLI and git)
# =============================================================================

set -e  # Exit on any error

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI ('gh') is not installed."
    echo "   Install it with: brew install gh"
    echo "   Then authenticate with: gh auth login"
    exit 1
fi

# Check if we're inside a git repo already
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "⚠️  This folder is already a git repository."
    read -p "Do you want to continue anyway and create/add a remote? (y/N): " force
    [[ "$force" =~ ^[Yy]$ ]] || exit 0
else
    echo "✅ Initializing git repository..."
    git init > /dev/null
fi

# Get current directory name as default repo name
current_dir="$(basename "$(pwd)")"

# Ask for repo name
read -p "Enter repository name [$current_dir]: " repo_name
repo_name="${repo_name:-$current_dir}"

# Ask for description (optional)
read -p "Enter repository description (optional): " description

# Ask for visibility
echo "Visibility:"
echo "  1) Private (default)"
echo "  2) Public"
read -p "Choose [1-2]: " visibility_choice
case $visibility_choice in
    2) visibility="public" ;;
    *) visibility="private" ;;
esac

echo "🚀 Creating GitHub repository '$repo_name' ($visibility)..."
if [ -n "$description" ]; then
    gh repo create "$repo_name" --description "$description" --$visibility --source=. --remote=origin -y
else
    gh repo create "$repo_name" --$visibility --source=. --remote=origin -y
fi

# Add all files and make initial commit if no commits exist yet
if ! git rev-parse --quiet HEAD >/dev/null 2>&1; then
    echo "📝 Adding files and making initial commit..."
    git add .
    git commit -m "Initial commit" > /dev/null
fi

echo "⬆️  Pushing to GitHub..."
git push -u origin main || git push -u origin master  # handles both cases

echo "🎉 Done! Your project is now on GitHub:"
echo "   https://github.com/$(gh api user --jq '.login')/$repo_name"
open "https://github.com/$(gh repo view --json url -q .url)"  # opens in default browser
