# App.js

**What it is for:** Application entry point, global state holder, and simple client-side router.
**Technologies used:** React (`useState`, `useEffect`, `useCallback`).
**Why:** To bootstrap the entire application, hold the active user token, determine the user's role (Customer, Manager, or Crew), and render the correct page component dynamically.
**How:** Checks `localStorage` for preexisting tokens. Uses simple state (`page`) instead of a heavyweight router library like React Router for navigation. Maintains a dynamic navigation bar based on the calculated access level (`role`).
