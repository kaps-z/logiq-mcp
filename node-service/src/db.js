const Database = require('better-sqlite3');
const fs = require('fs');
const path = require('path');

// Ensure correct paths based on project structure
const dbPath = process.env.DB_PATH || path.join(__dirname, '../../db/database.sqlite');
const schemaPath = path.join(__dirname, '../../db/schema.sql');

// Ensure db directory exists
const dbDir = path.dirname(dbPath);
if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
}

const db = new Database(dbPath, { verbose: console.log });
db.pragma('journal_mode = WAL');

// Initialize schema
if (fs.existsSync(schemaPath)) {
    const schema = fs.readFileSync(schemaPath, 'utf-8');
    db.exec(schema);
} else {
    console.error(`Schema file not found at ${schemaPath}`);
}

module.exports = db;
