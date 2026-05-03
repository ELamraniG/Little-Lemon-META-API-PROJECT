# DeliveryPage.js

**What it is for:** Dashboard for delivery crew members.
**Technologies used:** React, `api.js`.
**Why:** Delivery personnel only need to see the orders specifically assigned to them so they can fulfill deliveries.
**How:** Hits `GET /api/orders`. Because backend filters based on role, it returns only orders assigned to this crew member. They can click "Mark Delivered" which sends a `PATCH` to update the status to 1.
