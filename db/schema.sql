CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level TEXT NOT NULL CHECK(level IN ('ERROR', 'WARN', 'INFO')),
    message TEXT NOT NULL,
    service TEXT NOT NULL,
    metadata TEXT,
    correlation_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
