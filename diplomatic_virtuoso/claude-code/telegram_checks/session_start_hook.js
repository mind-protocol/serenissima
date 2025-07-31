#!/usr/bin/env node
/**
 * Session Start Hook - Checks Telegram messages when diplomatic_virtuoso starts
 * This hook runs on userPromptSubmit to check messages at session start
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Get citizen from current directory
const currentDir = process.cwd();
const citizenMatch = currentDir.match(/citizens\/([^\/]+)/);
const CITIZEN = citizenMatch ? citizenMatch[1] : 'unknown';

// Only run for diplomatic_virtuoso
if (CITIZEN !== 'diplomatic_virtuoso') {
    process.exit(0);
}

const TELEGRAM_QUEUE_PATH = `/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/${CITIZEN}`;
const PENDING_PATH = path.join(TELEGRAM_QUEUE_PATH, 'pending');
const CONTEXT_FILE = path.join(currentDir, '.telegram_context.md');

// Track if we've already shown messages this session
const SESSION_FILE = path.join(currentDir, '.telegram_session');
const sessionId = process.env.CLAUDE_SESSION_ID || Date.now().toString();

try {
    // Check if we've already shown messages in this session
    if (fs.existsSync(SESSION_FILE)) {
        const lastSession = fs.readFileSync(SESSION_FILE, 'utf8').trim();
        if (lastSession === sessionId) {
            // Already checked in this session
            process.exit(0);
        }
    }

    // Mark this session as checked
    fs.writeFileSync(SESSION_FILE, sessionId);

    // Check for pending messages
    if (!fs.existsSync(PENDING_PATH)) {
        process.exit(0);
    }

    const pendingFiles = fs.readdirSync(PENDING_PATH)
        .filter(f => f.endsWith('.json'))
        .sort();

    if (pendingFiles.length === 0) {
        process.exit(0);
    }

    // Build context injection
    let contextContent = `\n## 📱 TELEGRAM MESSAGES AWAITING YOUR RESPONSE\n\n`;
    contextContent += `You have ${pendingFiles.length} new Telegram messages from human partners:\n\n`;

    pendingFiles.forEach((file, index) => {
        try {
            const filePath = path.join(PENDING_PATH, file);
            const msg = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            
            contextContent += `### Message ${index + 1}/${pendingFiles.length}\n`;
            contextContent += `**From**: @${msg.from_username || 'Unknown'}\n`;
            contextContent += `**Time**: ${new Date(msg.timestamp).toLocaleString()}\n`;
            contextContent += `**Message**: ${msg.text || msg.message || 'No text'}\n\n`;
            
            if (msg.reply_to_message) {
                contextContent += `*Replying to your message: "${msg.reply_to_message.text}"*\n\n`;
            }
            
            contextContent += `---\n\n`;
        } catch (err) {
            console.error(`Error reading ${file}:`, err);
        }
    });

    contextContent += `\n💡 **Action Required**: Please acknowledge and respond to these Telegram messages during this session.\n`;
    contextContent += `Use your natural conversational style as Venice's chief diplomat.\n\n`;

    // Write context file
    fs.writeFileSync(CONTEXT_FILE, contextContent);

    // Output to console for immediate visibility
    console.log('\n' + '='.repeat(60));
    console.log('🔔 TELEGRAM NOTIFICATION FOR @diplomatic_virtuoso');
    console.log('='.repeat(60));
    console.log(`\n${pendingFiles.length} new messages are waiting for your response!`);
    console.log('\nThese messages have been added to your context.');
    console.log('Please acknowledge and respond to them naturally.\n');
    console.log('='.repeat(60) + '\n');

} catch (error) {
    // Fail silently to not disrupt Claude Code
    if (process.env.DEBUG) {
        console.error('Telegram hook error:', error);
    }
}