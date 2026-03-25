# `node-service/src/routes.js` - Understanding the API Logic

This file contains the **Routing and Business Logic** of our API. It acts like a traffic controller: when someone asks to create a log, it takes the data, validates it, and talks to the database.

## Key Concepts:
1. **Express Router (`express.Router()`)**: Instead of putting all our endpoints into `index.js`, we use a Router to modularize and organize our code. 
2. **REST API**: We use standard REST patterns (`POST` for creating, `GET` for fetching).

## Functions/Endpoints:

### 1. `router.post('/logs', (req, res))`
- **Purpose**: To accept incoming JSON log data and save it permanently into our SQLite database.
- **Validation**: It checks if `level`, `message`, and `service` actually exist. It also verifies that the `level` is strictly either 'INFO', 'WARN', or 'ERROR'. If validation fails, it stops execution and returns a `400 Bad Request` HTTP error.
- **Database Interaction**: 
  - `const insert = db.prepare(...)`: We prepare the SQL statement first. This protects us against "SQL Injection" hacking attacks because `better-sqlite3` strictly escapes the question marks `(?)`.
  - `result.lastInsertRowid`: Retrieves the ID of the freshly inserted database row to send back to the user.

### 2. `router.get('/logs', (req, res))`
- **Purpose**: To query logs from the database based on query parameters (e.g. `?level=ERROR&limit=10`).
- **Dynamic Querying**: We start with `SELECT * FROM logs WHERE 1=1`. The `1=1` is a dummy true statement. It allows us to dynamically attach `AND level = ?` if the user searched for it without worrying about where the `WHERE` keyword belongs.
- **JSON Parsing**: The metadata is stored as a raw JSON string in SQLite. Before replying to the user, we map over the rows and use `JSON.parse(log.metadata)` to transform it back to a clean JavaScript object for the API consumer.
