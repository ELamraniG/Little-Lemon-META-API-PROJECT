# MenuPage.js

**What it is for:** Displaying the restaurant's menu items and providing management controls for Managers.
**Technologies used:** React (`useState`, `useEffect`, `useCallback`), `api.js` helper.
**Why:** Serves as the primary landing dashboard where customers browse or add items to their cart, and where managers can perform CRUD operations on the menu.
**How:** Hits the `/api/menu-items` endpoint. Uses pagination, sorting, and searching query parameters. Shows Add/Edit/Delete buttons only if the `role` prop is 'Manager'.
