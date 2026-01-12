#!/bin/bash

# Script to reset Cursor's localhost permissions

echo "🔧 Resetting Cursor Localhost Permissions..."
echo ""

# Method 1: Clear workspace storage
echo "1. Clearing workspace storage..."
rm -rf ~/Library/Application\ Support/Cursor/User/workspaceStorage/* 2>/dev/null
echo "   ✅ Workspace storage cleared"

# Method 2: Try to find and clear security settings
echo ""
echo "2. Looking for security/permission files..."
SECURITY_FILES=$(find ~/Library/Application\ Support/Cursor -name "*security*" -o -name "*permission*" 2>/dev/null | head -5)

if [ ! -z "$SECURITY_FILES" ]; then
    echo "   Found security files:"
    echo "$SECURITY_FILES"
    echo ""
    read -p "   Delete these files? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "$SECURITY_FILES" | xargs rm -f 2>/dev/null
        echo "   ✅ Security files deleted"
    fi
else
    echo "   ℹ️  No security files found"
fi

# Method 3: Clear defaults (macOS)
echo ""
echo "3. Clearing macOS defaults..."
defaults delete com.todesktop.230313mzl4w4u92 2>/dev/null
echo "   ✅ Defaults cleared"

echo ""
echo "✅ Done! Now:"
echo "   1. Close Cursor completely (Cmd+Q)"
echo "   2. Reopen Cursor"
echo "   3. Try Simple Browser again"
echo "   4. When pop-up appears, click 'Allow'"
echo ""
