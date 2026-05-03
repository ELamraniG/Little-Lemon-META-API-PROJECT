# ManagerOrdersPage.js

**What it is for:** Overseeing and managing all customer orders (Manager view).
**Technologies used:** React, `api.js`.
**Why:** Managers need elevated access to see all global orders, assign delivery crew members, or mark orders as completed/deleted.
**How:** Similar to Customer OrdersPage, but fetches the manager's view of `/api/orders`. It includes a Modal form that allows updating the `status` or assigning a user ID as the `delivery_crew` via a `PATCH` request.
