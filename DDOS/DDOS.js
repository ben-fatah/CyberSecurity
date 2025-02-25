const { spawn } = require('child_process');
const zombie = 100;
for (let i = 0; i < zombie; i++) {
spawn('node', ['DOS.js']);
}