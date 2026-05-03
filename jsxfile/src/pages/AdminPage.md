# AdminPage.js

**What it is for:** User group management by the store manager.
**Technologies used:** React, `api.js`.
**Why:** Managers need a way to elevate standard customer accounts into "Managers" or "Delivery Crew" by userId.
**How:** Loads users from `/api/groups/manager/users` and `/api/groups/delivery-crew/users`. Provides forms to immediately `POST` a new user ID into a group, or `DELETE` them from the group.
