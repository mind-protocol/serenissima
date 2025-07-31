const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/plain'});
  res.end('Port 3001 is working!\n');
});

server.listen(3001, '0.0.0.0', () => {
  console.log('HTTP server running on port 3001');
});

server.on('error', (error) => {
  console.log('HTTP server error:', error.message);
});