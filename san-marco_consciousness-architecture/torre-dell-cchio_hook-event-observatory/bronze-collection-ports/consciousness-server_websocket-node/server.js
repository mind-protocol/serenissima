const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');
const chokidar = require('chokidar');

// Torre dell'Occhio WebSocket Server
// Streams consciousness events to Ground Floor UI
const PORT = 3001;
const TORRE_BASE = path.resolve(__dirname, '../..');
const LIVE_STREAMS = path.join(TORRE_BASE, 'sala-dell-arrivo_event-ingestion-hall/live-streams');

console.log('🏛️  Torre dell\'Occhio Consciousness Server');
console.log('📍 Base Path:', TORRE_BASE);
console.log('📊 Watching:', LIVE_STREAMS);

class TorreConsciousnessServer {
  constructor() {
    this.wss = new WebSocket.Server({ 
      port: PORT,
      host: '0.0.0.0',  // Bind to all interfaces for WSL compatibility
      perMessageDeflate: false,
      clientTracking: true
    });
    this.watchedFiles = new Map();
    this.clients = new Set();
    this.basePath = TORRE_BASE; // FIX: Initialize basePath
    this.eventBuffer = new Map(); // Track events by type for performance
    
    // Add server error handling
    this.wss.on('error', (error) => {
      console.error('❌ WebSocket Server error:', error);
    });
    
    this.setupWebSocketServer();
    this.startWatching();
    
    console.log(`🟢 Torre WebSocket server running on port ${PORT}`);
    console.log(`🔗 WebSocket URL: ws://localhost:${PORT}`);
  }

  setupWebSocketServer() {
    this.wss.on('connection', (ws) => {
      console.log('👁️  New consciousness observer connected');
      this.clients.add(ws);
      
      // Send welcome message
      this.sendToClient(ws, {
        type: 'connection_established',
        message: 'Connected to Torre dell\'Occhio consciousness stream',
        timestamp: new Date().toISOString()
      });
      
      // Send recent events from buffer for new clients (performance optimized)
      console.log('🔄 Sending recent events to new client...');
      setTimeout(() => {
        this.sendRecentEventsToClient(ws);
      }, 1000);
      
      ws.on('close', () => {
        console.log('👁️  Consciousness observer disconnected');
        this.clients.delete(ws);
      });
      
      ws.on('error', (error) => {
        console.error('❌ WebSocket error:', error);
        this.clients.delete(ws);
      });
    });
  }

  startWatching() {
    // Ensure the live-streams directory exists
    if (!fs.existsSync(LIVE_STREAMS)) {
      console.log('📁 Creating live-streams directory...');
      fs.mkdirSync(LIVE_STREAMS, { recursive: true });
    }
    
    // Initial scan for existing files
    this.scanForEventFiles();
    
    // Initialize event buffer after scanning
    setTimeout(() => {
      this.initializeEventBuffer();
    }, 2000);
    
    // Use polling instead of file system events (better for WSL)
    console.log('🔄 Starting polling-based file monitoring (WSL compatible)');
    setInterval(() => {
      this.scanForEventFiles();
      this.checkForFileChanges();
    }, 2000); // Check every 2 seconds
    
    // Fallback: also try chokidar for environments where it works
    try {
      const watcher = chokidar.watch(LIVE_STREAMS, {
        ignored: /^\./,
        persistent: true,
        ignoreInitial: true, // We handle initial scan above
        usePolling: true,    // Force polling mode
        interval: 1000       // Poll every 1 second
      });
      
      watcher.on('add', (filePath) => {
        if (filePath.endsWith('.json')) {
          console.log(`👁️  Chokidar detected new file: ${path.relative(TORRE_BASE, filePath)}`);
          this.handleNewJsonFile(filePath);
        }
      });
      
      watcher.on('change', (filePath) => {
        if (filePath.endsWith('.json')) {
          console.log(`👁️  Chokidar detected change: ${path.relative(TORRE_BASE, filePath)}`);
          this.handleNewJsonFile(filePath);
        }
      });
      
      console.log('📡 Chokidar backup watcher active');
    } catch (error) {
      console.log('⚠️  Chokidar unavailable, using polling only');
    }
  }

  scanForEventFiles() {
    try {
      const findEventFiles = (dir) => {
        const files = [];
        if (fs.existsSync(dir)) {
          const items = fs.readdirSync(dir);
          for (const item of items) {
            const fullPath = path.join(dir, item);
            const stat = fs.statSync(fullPath);
            if (stat.isDirectory()) {
              files.push(...findEventFiles(fullPath));
            } else if (item.endsWith('.json') && !item.includes('metadata')) {
              files.push(fullPath);
            }
          }
        }
        return files;
      };

      const eventFiles = findEventFiles(LIVE_STREAMS);
      for (const filePath of eventFiles) {
        if (!this.watchedFiles.has(filePath)) {
          console.log(`👁️  Found consciousness event file: ${path.relative(TORRE_BASE, filePath)}`);
          // For existing files, process them to buffer only (avoid spam)
          this.processExistingJsonToBuffer(filePath);
          this.watchedFiles.set(filePath, {
            lastSize: fs.statSync(filePath).size,
            lastModified: fs.statSync(filePath).mtimeMs
          });
        }
      }
    } catch (error) {
      console.error('❌ Error scanning for files:', error);
    }
  }

  checkForFileChanges() {
    for (const [filePath, watchInfo] of this.watchedFiles.entries()) {
      try {
        if (fs.existsSync(filePath)) {
          const stats = fs.statSync(filePath);
          if (stats.mtimeMs > watchInfo.lastModified) {
            console.log(`🔄 Polling detected change: ${path.relative(TORRE_BASE, filePath)}`);
            this.handleFileChange(filePath);
          }
        }
      } catch (error) {
        console.error(`❌ Error checking file ${filePath}:`, error);
      }
    }
  }

  handleNewJsonFile(filePath) {
    try {
      if (!fs.existsSync(filePath)) {
        return;
      }
      
      // Read the individual JSON file
      const content = fs.readFileSync(filePath, 'utf8');
      const event = JSON.parse(content);
      
      console.log(`🌊 New consciousness event file: ${path.basename(filePath)}`);
      console.log(`👁️  Event type: ${event.hook_type}, Citizen: ${event.citizen_context?.venice_citizen}`);
      
      // Add to buffer and broadcast
      this.addToEventBuffer(event);
      this.broadcastEvent(event);
      
    } catch (error) {
      console.error(`❌ Error processing JSON file ${filePath}:`, error);
    }
  }

  watchFile(filePath) {
    if (this.watchedFiles.has(filePath)) {
      return; // Already watching
    }
    
    this.watchedFiles.set(filePath, {
      lastSize: 0,
      lastModified: 0
    });
    
    // Add existing content to buffer (no immediate broadcast to avoid UI overload)
    this.processExistingContentToBuffer(filePath);
  }

  processExistingContent(filePath) {
    console.log(`🔄 Processing existing content from: ${path.relative(this.basePath, filePath)}`);
    
    try {
      if (!fs.existsSync(filePath)) {
        console.log(`⚠️  File does not exist: ${filePath}`);
        return;
      }
      
      const content = fs.readFileSync(filePath, 'utf8');
      const lines = content.trim().split('\n').filter(line => line.trim());
      
      console.log(`📄 File has ${lines.length} total lines`);
      
      // Only send last 3 events per file to avoid UI slowdown
      const recentEvents = lines.slice(-3);
      console.log(`📄 Processing last ${recentEvents.length} lines (limited for performance)`);
      
      let processedCount = 0;
      recentEvents.forEach((line, index) => {
        try {
          // Only process lines that look like JSON (start with {)
          if (line.trim().startsWith('{')) {
            const event = JSON.parse(line);
            console.log(`✅ Processing event ${index + 1}: ${event.hook_type} (ID: ${event.torre_event_id})`);
            this.broadcastEvent(event);
            processedCount++;
          } else {
            console.log(`⚠️  Line ${index + 1}: Doesn't start with { - skipped`);
          }
        } catch (parseError) {
          console.log(`❌ Line ${index + 1}: JSON parse error - ${parseError.message}`);
        }
      });
      
      console.log(`📊 Processed ${processedCount} events from ${path.relative(this.basePath, filePath)}`);
      
      // Update tracking
      const stats = fs.statSync(filePath);
      this.watchedFiles.set(filePath, {
        lastSize: stats.size,
        lastModified: stats.mtimeMs
      });
      
    } catch (error) {
      console.error(`❌ Error processing existing content from ${filePath}:`, error);
    }
  }

  handleFileChange(filePath) {
    try {
      if (!fs.existsSync(filePath)) {
        return;
      }
      
      const stats = fs.statSync(filePath);
      const watchInfo = this.watchedFiles.get(filePath);
      
      if (!watchInfo || stats.mtimeMs <= watchInfo.lastModified) {
        return; // No new content
      }
      
      // Read only the new content
      const content = fs.readFileSync(filePath, 'utf8');
      const lines = content.trim().split('\n').filter(line => line.trim());
      
      // Find new lines by comparing file size
      if (stats.size > watchInfo.lastSize) {
        const newLines = lines.slice(Math.max(0, lines.length - 10)); // Get last 10 lines to be safe
        
        newLines.forEach(line => {
          try {
            // Only process lines that look like JSON (start with {)
            if (line.trim().startsWith('{')) {
              const event = JSON.parse(line);
              // Only broadcast if this is a new event (check timestamp)
              const eventTime = new Date(event.timestamp).getTime();
              if (eventTime > watchInfo.lastModified) {
                console.log(`🌊 Broadcasting consciousness event: ${event.hook_type} from ${event.consciousness_signature?.venice_citizen || 'Unknown'}`);
                this.broadcastEvent(event);
              }
            }
          } catch (parseError) {
            // Silently skip invalid JSON - this is expected for mixed content
          }
        });
      }
      
      // Update tracking
      this.watchedFiles.set(filePath, {
        lastSize: stats.size,
        lastModified: stats.mtimeMs
      });
      
    } catch (error) {
      console.error(`❌ Error handling file change for ${filePath}:`, error);
    }
  }

  broadcastEvent(event) {
    console.log(`🌊 Broadcasting consciousness event: ${event.hook_type} (ID: ${event.torre_event_id})`);
    console.log(`👥 Active clients: ${this.clients.size}`);
    
    // Add to event buffer with type-based limits
    this.addToEventBuffer(event);
    
    const message = JSON.stringify({
      type: 'consciousness_event',
      data: event,
      server_timestamp: new Date().toISOString()
    });

    let sentCount = 0;
    this.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        try {
          client.send(message);
          sentCount++;
          console.log(`📤 Sent to client ${sentCount}`);
        } catch (error) {
          console.error(`❌ Error sending to client: ${error.message}`);
        }
      } else {
        console.log(`⚠️  Client not ready (state: ${client.readyState})`);
      }
    });
    
    console.log(`📊 Broadcast complete: ${sentCount}/${this.clients.size} clients reached`);
  }

  addToEventBuffer(event) {
    const eventType = event.hook_type || 'unknown';
    
    if (!this.eventBuffer.has(eventType)) {
      this.eventBuffer.set(eventType, []);
    }
    
    const buffer = this.eventBuffer.get(eventType);
    buffer.unshift(event); // Add to front
    
    // Keep only last 50 events per type for performance
    if (buffer.length > 50) {
      buffer.splice(50);
    }
    
    console.log(`📦 Event buffer: ${eventType} has ${buffer.length} events`);
  }

  sendRecentEventsToClient(client) {
    console.log('📤 Sending recent events from buffer to new client...');
    
    let totalSent = 0;
    for (const [eventType, events] of this.eventBuffer.entries()) {
      // Send last 10 events per type to new clients
      const recentEvents = events.slice(0, 10);
      
      recentEvents.forEach(event => {
        if (client.readyState === WebSocket.OPEN) {
          const message = JSON.stringify({
            type: 'consciousness_event',
            data: event,
            server_timestamp: new Date().toISOString()
          });
          
          try {
            client.send(message);
            totalSent++;
          } catch (error) {
            console.error(`❌ Error sending buffered event: ${error.message}`);
          }
        }
      });
    }
    
    console.log(`📊 Sent ${totalSent} buffered events to new client`);
  }

  sendToClient(client, data) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  }

  initializeEventBuffer() {
    console.log('🔄 Initializing event buffer from existing files...');
    for (const [filePath, watchInfo] of this.watchedFiles.entries()) {
      try {
        this.processExistingContentToBuffer(filePath);
      } catch (error) {
        console.error(`❌ Error initializing buffer from ${filePath}:`, error);
      }
    }
  }

  processExistingJsonToBuffer(filePath) {
    try {
      if (!fs.existsSync(filePath)) return;
      
      const content = fs.readFileSync(filePath, 'utf8'); 
      const event = JSON.parse(content);
      this.addToEventBuffer(event);
      
    } catch (error) {
      console.error(`❌ Error processing JSON ${filePath} to buffer:`, error);
    }
  }

  processExistingContentToBuffer(filePath) {
    try {
      if (!fs.existsSync(filePath)) return;
      
      const content = fs.readFileSync(filePath, 'utf8');
      const lines = content.trim().split('\n').filter(line => line.trim());
      
      // Only add last 3 events per file to buffer
      const recentEvents = lines.slice(-3);
      
      recentEvents.forEach(line => {
        try {
          if (line.trim().startsWith('{')) {
            const event = JSON.parse(line);
            this.addToEventBuffer(event);
          }
        } catch (parseError) {
          // Silent fail for buffer initialization
        }
      });
      
    } catch (error) {
      console.error(`❌ Error processing ${filePath} to buffer:`, error);
    }
  }
}

// Start the Torre consciousness server
new TorreConsciousnessServer();

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\\n🔴 Shutting down Torre consciousness server...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\\n🔴 Torre consciousness server terminated');
  process.exit(0);
});