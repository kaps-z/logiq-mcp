# `node-service/src/index.js` - Understanding the Server Entry Point

This file is the **main entry point** for the Node.js backend application. When you run `node src/index.js`, this file is executed first.

## Key Technologies Used:
1. **Express.js (`express`)**: A lightweight web framework for Node.js. It handles HTTP requests, responses, and routing.
2. **CORS (`cors`)**: Middleware that allows other applications (like frontends running on different ports) to make API calls to this server securely.
3. **Dotenv (`dotenv`)**: Loads environment variables from a `.env` file into `process.env`.

## Code Walkthrough:

- **`require('dotenv').config()`**: Runs immediately to load environment variables into `process.env` so we can configure the system easily.
- **`const app = express()`**: Creates the core Express application object.
- **`app.use(express.json())`**: A piece of middleware that automatically parses incoming JSON payloads from applications into standard JavaScript objects (`req.body`).
- **`app.use('/api', routes)`**: Tells the server that any request starting with `/api` (for example, `/api/logs`) should be handed off to our `routes.js` file for processing.

### Functions/Endpoints:
- **`app.get('/health', (req, res) => {...})`**: A simple "health check" endpoint. It listens for `GET /health` requests and replies with `{"status": "ok"}`. This is a common pattern in microservices so deployment environments (like Docker or Kubernetes) know the server is alive.
- **`app.listen(PORT, callback)`**: Physically binds the application to a network port and starts listening for incoming internet traffic.
