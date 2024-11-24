const fs = require('fs');
const path = require('path');
const http = require('http');
const cors = require('cors');

const PORT = 3000;


function getCurrentDateTime() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
}


function writeLogFile(message) {
    const dateTime = getCurrentDateTime();
    const logDir = path.join(__dirname, 'logs', `${dateTime.replace(/[^\d]/g, '').slice(0, 10)}`);
    const logFile = path.join(logDir, `${dateTime.replace(/[^\d]/g, '').slice(0, 12)}.txt`);


    fs.mkdirSync(logDir, { recursive: true });


    fs.appendFileSync(logFile, `${dateTime} | ${message}\n`, 'utf8');
}


const server = http.createServer((req, res) => {
    if (req.method === 'OPTIONS') {
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        res.writeHead(200);
        res.end();
        return;
    }
    if (req.method === 'POST' && req.url === '/save-log') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });

        req.on('end', () => {
            const logEntry = JSON.parse(body);
            const message = logEntry.message;
            writeLogFile(message);
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ status: 'Log entry saved' }));
        });
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
    }
});


server.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
