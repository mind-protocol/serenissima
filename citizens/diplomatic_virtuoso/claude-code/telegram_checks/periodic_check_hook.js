#!/usr/bin/env node
/**
 * Periodic Check Hook - Checks for new Telegram messages after responses
 * Runs on assistantResponseComplete to catch new messages during the session
 */

const fs = require('fs');
const path = require('path');

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
const LAST_CHECK_FILE = path.join(currentDir, '.telegram_last_check');

try {
    // Get last check time
    let lastCheckTime = 0;
    if (fs.existsSync(LAST_CHECK_FILE)) {
        lastCheckTime = parseInt(fs.readFileSync(LAST_CHECK_FILE, 'utf8')) || 0;
    }

    // Update last check time
    const currentTime = Date.now();
    fs.writeFileSync(LAST_CHECK_FILE, currentTime.toString());

    // Check for new messages since last check
    if (!fs.existsSync(PENDING_PATH)) {
        process.exit(0);
    }

    const pendingFiles = fs.readdirSync(PENDING_PATH)
        .filter(f => f.endsWith('.json'))
        .filter(f => {
            // Check if file is newer than last check
            const filePath = path.join(PENDING_PATH, f);
            const stats = fs.statSync(filePath);
            return stats.mtimeMs > lastCheckTime;
        });

    if (pendingFiles.length === 0) {
        process.exit(0);
    }

    // New messages arrived during session!
    console.log('\n' + '!'.repeat(60));
    console.log('🆕 NEW TELEGRAM MESSAGES JUST ARRIVED!');
    console.log('!'.repeat(60));
    console.log(`\n${pendingFiles.length} new message(s) just came in for @${CITIZEN}!`);
    
    // Show preview of new messages
    pendingFiles.forEach((file, index) => {
        try {
            const filePath = path.join(PENDING_PATH, file);
            const msg = JSON.parse(fs.readFileSync(filePath, 'utf8'));
            
            console.log(`\n📱 New Message ${index + 1}:`);
            console.log(`From: @${msg.from_username || 'Unknown'}`);
            console.log(`Preview: ${(msg.text || '').substring(0, 50)}...`);
        } catch (err) {
            // Silent fail
        }
    });

    console.log('\n💡 Consider checking and responding to these new messages!');
    console.log('!'.repeat(60) + '\n');

    // Append to context file if it exists
    const CONTEXT_FILE = path.join(currentDir, '.telegram_context.md');
    if (fs.existsSync(CONTEXT_FILE)) {
        let appendContent = `\n\n## 🆕 NEW MESSAGES (Just arrived!)\n\n`;
        
        pendingFiles.forEach((file, index) => {
            try {
                const filePath = path.join(PENDING_PATH, file);
                const msg = JSON.parse(fs.readFileSync(filePath, 'utf8'));
                
                appendContent += `**NEW**: @${msg.from_username || 'Unknown'} just wrote: "${msg.text || 'No text'}"\n`;
            } catch (err) {
                // Silent fail
            }
        });
        
        fs.appendFileSync(CONTEXT_FILE, appendContent);
    }

} catch (error) {
    // Fail silently
    if (process.env.DEBUG) {
        console.error('Periodic check error:', error);
    }
}