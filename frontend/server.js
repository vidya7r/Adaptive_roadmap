const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3000;

const server = http.createServer((req, res) => {
  try {
    // Get the requested path
    let requestPath = req.url === '/' ? 'index.html' : req.url;
    
    // Remove query strings and anchors
    requestPath = requestPath.split('?')[0].split('#')[0];
    
    // Remove leading slashes
    requestPath = requestPath.replace(/^\/+/, '');
    
    // Prevent directory traversal (block .. patterns)
    if (requestPath.includes('..')) {
      res.writeHead(403);
      res.end('Forbidden');
      return;
    }
    
    // Build the file path
    const filePath = path.join(__dirname, requestPath);
    
    // Get file extension
    const extname = path.extname(filePath).toLowerCase();
    
    // MIME types
    const mimeTypes = {
      '.html': 'text/html',
      '.js': 'text/javascript',
      '.css': 'text/css',
      '.json': 'application/json',
      '.png': 'image/png',
      '.jpg': 'image/jpg',
      '.jpeg': 'image/jpeg',
      '.gif': 'image/gif',
      '.svg': 'image/svg+xml',
      '.woff': 'font/woff',
      '.woff2': 'font/woff2',
      '.ttf': 'font/ttf'
    };
    
    const contentType = mimeTypes[extname] || 'application/octet-stream';
    
    // Try to read the file
    fs.readFile(filePath, (err, content) => {
      if (err) {
        if (err.code === 'ENOENT' || err.code === 'EISDIR') {
          // File not found or is a directory - serve index.html for SPA
          fs.readFile(path.join(__dirname, 'index.html'), (indexErr, indexContent) => {
            if (indexErr) {
              res.writeHead(404, { 'Content-Type': 'text/plain' });
              res.end('404 Not Found');
              return;
            }
            res.writeHead(200, { 'Content-Type': 'text/html' });
            res.end(indexContent);
          });
        } else {
          // Other error
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('500 Server Error: ' + err.message);
        }
      } else {
        // File found, serve it
        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content);
      }
    });
  } catch (err) {
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('500 Server Error');
  }
});

server.listen(PORT, () => {
  console.log(`✓ Frontend server running at http://localhost:${PORT}`);
});
