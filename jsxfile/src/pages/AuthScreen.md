# AuthScreen.js

**What it is for:** User Authentication (Login and Registration).
**Technologies used:** React (`useState`), `api.js` helper.
**Why:** So users can log in and retrieve their JWT/token to interact with authenticated routes.
**How:** Maintains `tab` state to switch between Login and Register. On submit, it posts credentials to Djoser auth endpoints (`/auth/users/` and `/auth/token/login/`), then fetches the user profile using `/auth/users/me/`, and passes the token up via the `onLogin` callback.
