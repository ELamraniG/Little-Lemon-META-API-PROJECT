# CartPage.js

**What it is for:** Managing and displaying the user's cart, and triggering the checkout/order placement.
**Technologies used:** React, `api.js`.
**Why:** To let users verify what they are about to order and calculate their total costs.
**How:** On mount, it synchronizes any local-only cart items to the server using `POST /api/cart/menu-items`. It fetches the complete server-side cart. Users can clear the cart or click "Place Order," which hits `POST /api/orders` to checkout.
