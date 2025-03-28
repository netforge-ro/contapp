#\!/bin/bash

# This script will rewrite git history to remove references to "Claude" in commit messages

# Make sure you run this from the root of the repository
if [ \! -d ".git" ]; then
    echo "Error: This script must be run from the root of the git repository"
    exit 1
fi

# Create a filter-branch command that rewrites commit messages
git filter-branch --force --msg-filter  sed -e s/🤖 Generated with \[Claude Code\](https:\/\/claude.ai\/code)//g -e s/Generated with \[Claude Code\](https:\/\/claude.ai\/code)//g -e s/Co-Authored-By: Claude <noreply@anthropic.com>//g  -- HEAD~10..HEAD

echo "Git history has been rewritten to remove references to Claude"
echo "Note: You will need to force push to your remote repository with:"
echo "git push origin main --force"

