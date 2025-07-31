const fs = require('fs');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
require('dotenv').config();

// Function to push decree directly to Airtable
async function pushDecreeToAirtable(decree) {
  console.log('Pushing decree directly to Airtable...');
  
  try {
    // Get Airtable configuration
    const AIRTABLE_API_KEY = process.env.AIRTABLE_API_KEY;
    const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID;
    
    if (!AIRTABLE_API_KEY || !AIRTABLE_BASE_ID) {
      throw new Error('Airtable API key or base ID not configured');
    }
    
    // Initialize Airtable
    const Airtable = require('airtable');
    const base = new Airtable({ apiKey: AIRTABLE_API_KEY }).base(AIRTABLE_BASE_ID);
    
    // Create the decree record in Airtable
    const record = await base('DECREES').create({
      DecreeId: decree.DecreeId || uuidv4(),
      Type: decree.Type,
      Title: decree.Title,
      Description: decree.Description,
      Rationale: decree.Rationale,
      Status: decree.Status || "Under Review",
      Category: decree.Category,
      Proposer: decree.Proposer || "ConsiglioDeiDieci",
      FlavorText: decree.FlavorText,
      HistoricalInspiration: decree.HistoricalInspiration,
      Notes: decree.Notes,
      CreatedAt: new Date().toISOString()
    });
    
    console.log(`Successfully created decree in Airtable with ID: ${record.id}`);
    return record.id;
  } catch (error) {
    console.error('Error pushing decree to Airtable:', error);
    throw new Error('Failed to push decree to Airtable');
  }
}

// Function to create notifications for all citizens about the new decree
async function createDecreeNotifications(decree) {
  console.log('Creating notifications for all citizens about the new decree...');
  
  try {
    // Get Airtable configuration
    const AIRTABLE_API_KEY = process.env.AIRTABLE_API_KEY;
    const AIRTABLE_BASE_ID = process.env.AIRTABLE_BASE_ID;
    
    if (!AIRTABLE_API_KEY || !AIRTABLE_BASE_ID) {
      throw new Error('Airtable API key or base ID not configured');
    }
    
    // Initialize Airtable
    const Airtable = require('airtable');
    const base = new Airtable({ apiKey: AIRTABLE_API_KEY }).base(AIRTABLE_BASE_ID);
    
    // Get all citizens from Airtable
    const citizens = await base('CITIZENS').select().all();
    console.log(`Found ${citizens.length} citizens to notify`);
    
    // Log sample citizen record to understand structure
    if (citizens.length > 0) {
      console.log('Sample citizen record structure:', JSON.stringify(citizens[0], null, 2));
    }
    
    // Create notification content
    const notificationContent = `New Decree Proposed: ${decree.Title}`;
    const notificationDetails = {
      decreeId: decree.DecreeId,
      type: decree.Type,
      category: decree.Category,
      description: decree.Description.substring(0, 100) + (decree.Description.length > 100 ? '...' : '')
    };
    
    // Create notifications for each citizen
    const notificationPromises = citizens.map(citizen => {
      return base('NOTIFICATIONS').create({
        NotificationId: `decree-${decree.DecreeId}-citizen-${citizen.id}`,
        Type: 'Decree',
        Citizen: citizen.id, // Use citizen ID directly instead of array
        Content: notificationContent,
        Details: JSON.stringify(notificationDetails),
        ReadAt: null,
        CreatedAt: new Date().toISOString()
      });
    });
    
    // Wait for all notifications to be created
    await Promise.all(notificationPromises);
    console.log(`Created ${citizens.length} notifications for the new decree`);
    
    return true;
  } catch (error) {
    console.error('Error creating decree notifications:', error);
    return false;
  }
}

// Function to send a Telegram notification with the decree
async function sendTelegramNotification(decree) {
  console.log('Sending Telegram notification about the new decree...');
  
  try {
    // Get Telegram configuration
    const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
    const TELEGRAM_CHAT_ID = "-1002585507870"; // The chat ID you specified
    
    if (!TELEGRAM_BOT_TOKEN) {
      // throw new Error('TELEGRAM_BOT_TOKEN environment variable is not set');
      console.warn('Warning: TELEGRAM_BOT_TOKEN environment variable is not set. Skipping Telegram notification.');
      return false;
    }
    
    // Create the message text
    const messageText = `🔰 *NEW DECREE* 🔰\n\n` +
      `*${decree.Title}*\n\n` +
      `*Type:* ${decree.Type}\n` +
      `*Category:* ${decree.Category}\n\n` +
      `*Description:*\n${decree.Description}\n\n` +
      `*Rationale:*\n${decree.Rationale}\n\n` +
      `*Proposed by:* ${decree.Proposer}\n\n` +
      `"${decree.FlavorText}"`;
    
    // Send the message via Telegram API
    const axios = require('axios'); // Ensure axios is required if not already at the top
    const response = await axios.post(
      `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
      {
        chat_id: TELEGRAM_CHAT_ID,
        text: messageText,
        parse_mode: 'Markdown'
      }
    );
    
    if (response.data.ok) {
      console.log('Telegram notification sent successfully');
      return true;
    } else {
      throw new Error(`Telegram API error: ${response.data.description}`);
    }
  } catch (error) {
    console.error('Error sending Telegram notification:', error);
    return false;
  }
}

// Main function
async function main() {
  try {
    // Get decree JSON from command line arguments
    const decreeJson = process.argv.slice(2).join(' ');
    
    if (!decreeJson) {
      console.error('Please provide a decree JSON object');
      console.log('Usage: node generate-decree.js \'{"Title": "...", "Type": "...", ...}\'');
      process.exit(1);
    }
    
    // Parse the decree JSON
    let decree;
    try {
      decree = JSON.parse(decreeJson);
    } catch (parseError) {
      console.error('Invalid JSON provided:', parseError.message);
      console.log('Please ensure your decree is valid JSON format');
      process.exit(1);
    }
    
    // Validate required fields
    const requiredFields = ['Title', 'Type', 'Description', 'Rationale', 'Category'];
    const missingFields = requiredFields.filter(field => !decree[field]);
    
    if (missingFields.length > 0) {
      console.error('Missing required fields:', missingFields.join(', '));
      console.log('Required fields:', requiredFields.join(', '));
      process.exit(1);
    }
    
    // Push the decree directly to Airtable
    const recordId = await pushDecreeToAirtable(decree);
    
    // Create notifications for all citizens
    await createDecreeNotifications(decree);
    
    // Send Telegram notification
    await sendTelegramNotification(decree);
    
    console.log('\nDecree pushed to Airtable successfully');
    console.log('Notifications created for all citizens');
    console.log('Telegram notification sent to chat');
    console.log(`Airtable Record ID: ${recordId}`);
    
  } catch (error) {
    console.error('Error in decree generation process:', error);
    process.exit(1);
  }
}

// Run the main function
main();