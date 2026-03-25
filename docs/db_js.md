# `node-service/src/db.js` - Understanding the Database Connection

This file is responsible for **bootstrapping and connecting** to SQLite. By exporting the database connection from this centrally managed file, we ensure the rest of the application uses one single, shared SQLite instance rather than continuously opening and closing files.

## Key Technologies Used:
1. **`better-sqlite3`**: The fastest SQLite3 wrapper for Node.js. Unlike traditional database clients that use asynchronous callbacks or Promises (like `await db.query()`), `better-sqlite3` is fully **synchronous**. Since SQLite essentially acts as a local file, synchronous operations are often faster than the Node.js event-loop overhead.
2. **`fs` and `path`** (from Node.js core): Used to dynamically build the absolute paths to where our database file actually lives on the hard drive, and check if directories exist.

## Code Walkthrough:

- **Path Resolving**: We generate `dbPath` to point roughly to our `../../../db/` directory so that Python and Node both correctly share the exact same `database.sqlite` file without paths colliding.
- **`fs.mkdirSync(..., { recursive: true })`**: Assures that the folder structure actually exists. If Node tries to make an SQLite file in a folder that doesn't exist, it crashes.
- **`journal_mode = WAL`**: (Write-Ahead Logging). This is a crucial SQLite optimization. By turning WAL on, multiple processes (like our Node app AND our Python app) can read the database concurrently without getting "Database is locked" errors.
- **`db.exec(schema)`**: Reads the plain SQL strings from `schema.sql` and instantly attempts to declare the tables. The SQL itself checks `IF NOT EXISTS` so it's perfectly safe to run on every startup.
- **`module.exports = db`**: Finalizes the file by exporting the configured database engine for `routes.js` to import and utilize.
