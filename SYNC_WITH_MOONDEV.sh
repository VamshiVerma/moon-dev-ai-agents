#!/bin/bash

# 🌙 Moon Dev Repo Sync Script
# Pulls latest updates from Moon Dev's original repo into your fork

echo ""
echo "================================================================================"
echo "🌙 Syncing with Moon Dev's Original Repo"
echo "================================================================================"
echo ""

# Make sure we're in the right directory
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    exit 1
fi

# Show current status
echo "📊 Current status:"
git log --oneline -1
echo ""

# Fetch from upstream (Moon Dev's original repo)
echo "📡 Fetching latest from Moon Dev's repo..."
git fetch upstream

echo ""
echo "🔍 Checking for new commits..."
NEW_COMMITS=$(git log --oneline main..upstream/main)

if [ -z "$NEW_COMMITS" ]; then
    echo "✅ Already up to date! No new commits from Moon Dev."
    echo ""
    echo "Your repo: $(git log --oneline -1)"
    echo "Moon Dev:  $(git log upstream/main --oneline -1)"
    echo ""
    echo "================================================================================"
    exit 0
fi

echo ""
echo "🆕 New commits available from Moon Dev:"
echo "$NEW_COMMITS"
echo ""

# Show what changed
echo "📋 Files that will change:"
git diff --stat main upstream/main
echo ""

# Ask for confirmation
read -p "🤔 Merge these updates? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Sync cancelled"
    exit 0
fi

# Merge upstream changes
echo ""
echo "🔄 Merging Moon Dev's updates..."
git merge upstream/main -m "Merge upstream updates from Moon Dev

Synced with: https://github.com/moondevonyt/moon-dev-ai-agents
$(git log --oneline main..upstream/main | wc -l) new commits merged

Co-authored-by: factory-droid[bot] <138933559+factory-droid[bot]@users.noreply.github.com>"

if [ $? -eq 0 ]; then
    echo "✅ Merge successful!"
    echo ""
    
    # Ask about pushing
    read -p "🚀 Push to your GitHub fork? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git push origin main
        echo "✅ Pushed to your fork!"
    else
        echo "⏸️  Not pushed - run 'git push origin main' when ready"
    fi
else
    echo "❌ Merge conflicts detected!"
    echo ""
    echo "📝 To resolve:"
    echo "   1. Fix conflicts in the listed files"
    echo "   2. git add <resolved-files>"
    echo "   3. git commit"
    echo "   4. git push origin main"
    exit 1
fi

echo ""
echo "================================================================================"
echo "✅ Sync complete!"
echo "================================================================================"
echo ""
