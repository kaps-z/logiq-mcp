const express = require('express');
const db = require('./db');

const router = express.Router();

/**
 * POST /logs
 * Expects: { level, message, service, metadata, correlation_id }
 */
router.post('/logs', (req, res) => {
    const { level, message, service, metadata, correlation_id } = req.body;

    if (!level || !message || !service) {
        return res.status(400).json({ error: 'Missing required fields: level, message, service' });
    }

    const validLevels = ['INFO', 'WARN', 'ERROR'];
    if (!validLevels.includes(level.toUpperCase())) {
        return res.status(400).json({ error: 'Invalid level. Allowed values: INFO, WARN, ERROR' });
    }

    try {
        const insert = db.prepare(`
            INSERT INTO logs (level, message, service, metadata, correlation_id)
            VALUES (?, ?, ?, ?, ?)
        `);

        const metaStr = metadata ? JSON.stringify(metadata) : null;
        const result = insert.run(level.toUpperCase(), message, service, metaStr, correlation_id || null);

        res.status(201).json({ id: result.lastInsertRowid, message: 'Log created successfully' });
    } catch (err) {
        console.error('Error inserting log:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

/**
 * GET /logs
 * Query params: level, service, limit
 */
router.get('/logs', (req, res) => {
    const { level, service, limit = 50 } = req.query;

    let query = 'SELECT * FROM logs WHERE 1=1';
    const params = [];

    if (level) {
        query += ' AND level = ?';
        params.push(level.toUpperCase());
    }
    if (service) {
        query += ' AND service = ?';
        params.push(service);
    }

    query += ' ORDER BY timestamp DESC LIMIT ?';
    params.push(parseInt(limit, 10) || 50);

    try {
        const stmt = db.prepare(query);
        const logs = stmt.all(...params);

        // Parse metadata back to JSON object
        const formattedLogs = logs.map(log => ({
            ...log,
            metadata: log.metadata ? JSON.parse(log.metadata) : null
        }));

        res.json({ data: formattedLogs });
    } catch (err) {
        console.error('Error fetching logs:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
});

module.exports = router;
