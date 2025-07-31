#!/bin/bash
# Test avec UN seul angel

echo "🎭 Test Story Angel Direct"
echo "========================="
echo ""
echo "Lancement dans un nouveau terminal Windows..."
echo ""

# Create simple launch script
cat > /tmp/launch_story_angel.sh << 'EOF'
#!/bin/bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/story-angel
export HOME=/home/lester/.claude_account2
echo "📖 Story Angel starting..."
echo "Current directory: $(pwd)"
echo "CLAUDE.md exists: $([ -f CLAUDE.md ] && echo YES || echo NO)"
echo "awakening.txt exists: $([ -f awakening.txt ] && echo YES || echo NO)"
echo ""
echo "Launching Claude..."
claude
EOF

chmod +x /tmp/launch_story_angel.sh

# Open in Windows Terminal
cmd.exe /c start wt.exe -w 0 new-tab wsl.exe bash /tmp/launch_story_angel.sh

echo "✅ Story Angel lancé dans un nouveau terminal!"
echo ""
echo "Dans ce terminal:"
echo "1. Claude va démarrer"
echo "2. Il va lire CLAUDE.md automatiquement"
echo "3. Tapez un message pour le réveiller"
echo ""
echo "Exemple de message:"
echo "  'Venice awakens. What stories do you see?'"