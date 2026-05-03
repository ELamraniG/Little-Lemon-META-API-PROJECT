# api.js

**What it is for:** Centralized API wrapper for making HTTP requests to the backend server.
**Technologies used:** JavaScript, Fetch API.
**Why:** To avoid repeating headers, base URLs, token injection, and JSON parsing logic across all components.
**How:** Exports a `BASE_URL` and an `api` async function. It intercepts the request, appends the Authorization header if a token is provided, parses JSON responses, and throws an object on non-2xx statuses so that callers can catch and display errors consistently.
