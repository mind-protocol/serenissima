#!/usr/bin/env node
/**
 * Telegram Notifier - Shows pending messages on EVERY user prompt
 * This runs via UserPromptSubmit hook
 */

const fs = require('fs');
const path = require('path');

// Configuration
const TELEGRAM_QUEUE = '/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/diplomatic_virtuoso/pending';
const SHOW_SCRIPT = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso/claude-code/show_messages.py';

try {
    // Count pending messages
    if (!fs.existsSync(TELEGRAM_QUEUE)) {
        process.exit(0);
    }
    
    const files = fs.readdirSync(TELEGRAM_QUEUE).filter(f => f.endsWith('.json'));
    const privateMessages = files.filter(f => {
        try {
            const content = JSON.parse(fs.readFileSync(path.join(TELEGRAM_QUEUE, f), 'utf8'));
            return content.chat_type === 'private';
        } catch {
            return false;
        }
    });
    
    if (privateMessages.length > 0) {
        // Print notification that will appear in the conversation
        console.error(`\n${'='.repeat(60)}`);
        console.error(`🔔 TELEGRAM: ${privateMessages.length} messages waiting!`);
        console.error(`Run: python3 ${SHOW_SCRIPT}`);
        console.error(`${'='.repeat(60)}\n`);
    }
    
    // Exit 0 so we don't block the prompt
    process.exit(0);
    
} catch (error) {
    // Silent fail - don't disrupt Claude
    process.exit(0);
}