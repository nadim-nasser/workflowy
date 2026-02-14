const express = require('express');
const Database = require('better-sqlite3');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Initialize database
const db = new Database(path.join(__dirname, 'weight.db'));
db.pragma('journal_mode = WAL');

db.exec(`
  CREATE TABLE IF NOT EXISTS weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT UNIQUE NOT NULL,
    weight REAL NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
  );
  CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
  );
`);

// GET all weight entries (sorted by date)
app.get('/api/weights', (req, res) => {
  const rows = db.prepare('SELECT * FROM weights ORDER BY date ASC').all();
  res.json(rows);
});

// POST a new weight entry (upsert by date)
app.post('/api/weights', (req, res) => {
  const { date, weight } = req.body;
  if (!date || weight == null) {
    return res.status(400).json({ error: 'date and weight are required' });
  }
  const parsed = parseFloat(weight);
  if (isNaN(parsed) || parsed <= 0 || parsed > 1000) {
    return res.status(400).json({ error: 'weight must be a number between 0 and 1000' });
  }
  const stmt = db.prepare(`
    INSERT INTO weights (date, weight) VALUES (?, ?)
    ON CONFLICT(date) DO UPDATE SET weight = excluded.weight
  `);
  stmt.run(date, parsed);
  res.json({ success: true, date, weight: parsed });
});

// DELETE a weight entry
app.delete('/api/weights/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  if (isNaN(id)) {
    return res.status(400).json({ error: 'invalid id' });
  }
  db.prepare('DELETE FROM weights WHERE id = ?').run(id);
  res.json({ success: true });
});

// GET goal
app.get('/api/goal', (req, res) => {
  const row = db.prepare("SELECT value FROM settings WHERE key = 'goal_weight'").get();
  res.json({ goal: row ? parseFloat(row.value) : null });
});

// PUT goal
app.put('/api/goal', (req, res) => {
  const { goal } = req.body;
  if (goal == null) {
    db.prepare("DELETE FROM settings WHERE key = 'goal_weight'").run();
    return res.json({ goal: null });
  }
  const parsed = parseFloat(goal);
  if (isNaN(parsed) || parsed <= 0) {
    return res.status(400).json({ error: 'goal must be a positive number' });
  }
  db.prepare(`
    INSERT INTO settings (key, value) VALUES ('goal_weight', ?)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value
  `).run(String(parsed));
  res.json({ goal: parsed });
});

app.listen(PORT, () => {
  console.log(`Weight tracker running at http://localhost:${PORT}`);
});
