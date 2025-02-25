const express = require('express');
const app = express();
const statusMonitor = require('express-status-monitor')();
app.use(statusMonitor);
app.get('/status', statusMonitor.pageRoute)
const port = 3000;
// Serve static files from the "public" directory
app.use(express.static('public'));
app.listen(port, () => {
  console.log(`Static server running at http://localhost:${port}`);
});
