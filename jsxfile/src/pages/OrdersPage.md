# OrdersPage.js

**What it is for:** Displaying a customer's order history.
**Technologies used:** React, `api.js`.
**Why:** Customers need to be able to see the orders they have placed and track their statuses (pending vs delivered).
**How:** Hits `GET /api/orders` to fetch orders belonging only to the authenticated customer. It handles pagination and displays order items inside individual cards.
