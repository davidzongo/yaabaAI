#!/bin/bash
# Emergency clean deployment script

echo "🚨 EMERGENCY STREAMLIT DEPLOYMENT CLEANUP"
echo "==========================================="

# Remove corrupted files
echo "🗑️ Removing corrupted files..."
rm -f requirements.txt 2>/dev/null || del requirements.txt 2>NUL

# Create ultra-minimal requirements.txt
echo "📝 Creating clean requirements.txt..."
echo "streamlit" > requirements.txt

# Verify file contents
echo "✅ Verifying requirements.txt contents:"
cat requirements.txt 2>/dev/null || type requirements.txt 2>NUL

echo ""
echo "🚀 Ready to deploy with:"
echo "   - app.py (working Streamlit app)"  
echo "   - requirements.txt (only 'streamlit')"
echo ""
echo "Deploy commands:"
echo "   git add ."
echo "   git commit -m 'Emergency clean deployment'"
echo "   git push"
echo ""
echo "This WILL work! 🎉"