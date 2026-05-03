import React, { useState, useEffect, useCallback } from "react";
import { api } from "./api";
import { StyleTag } from "./styles";
import AuthScreen from "./pages/AuthScreen";
import MenuPage from "./pages/MenuPage";
import CartPage from "./pages/CartPage";
import OrdersPage from "./pages/OrdersPage";
import ManagerOrdersPage from "./pages/ManagerOrdersPage";
import DeliveryPage from "./pages/DeliveryPage";
import AdminPage from "./pages/AdminPage";

export default function App() {
  const [token, setToken] = useState(() => localStorage.getItem("ll_token") || "");
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem("ll_user") || "null"); } catch { return null; }
  });
  const [role, setRole] = useState("Customer");
  const [page, setPage] = useState("menu");
  const [localCart, setLocalCart] = useState([]); // pre-login cart
  const [cartCount, setCartCount] = useState(0);

  // Determine role from groups
  const resolveRole = useCallback(async (tok, u) => {
    // Try fetching group info
    try {
      await api("/api/groups/manager/users", {}, tok);
      setRole("Manager"); return "Manager";
    } catch { }
    try {
      const orders = await api("/api/orders", {}, tok);
      const arr = Array.isArray(orders) ? orders : (orders.results || []);
      // Delivery crew can only see their assigned orders — heuristic: if user.id matches delivery_crew
      const assigned = arr.find((o) => o.delivery_crew === u?.id);
      if (assigned) { setRole("Delivery crew"); return "Delivery crew"; }
    } catch { }
    setRole("Customer"); return "Customer";
  }, []);

  useEffect(() => {
    if (token && user) resolveRole(token, user);
  }, [token, user]);

  const handleLogin = (tok, u) => {
    localStorage.setItem("ll_token", tok);
    localStorage.setItem("ll_user", JSON.stringify(u));
    setToken(tok); setUser(u);
    setPage("menu");
  };

  const handleLogout = async () => {
    try { await api("/auth/token/logout/", { method: "POST" }, token); } catch { }
    localStorage.removeItem("ll_token"); localStorage.removeItem("ll_user");
    setToken(""); setUser(null); setRole("Customer"); setPage("menu"); setLocalCart([]);
  };

  const addToLocalCart = (item) => {
    setLocalCart((prev) => {
      const existing = prev.find((i) => i.id === item.id);
      if (existing) return prev.map((i) => i.id === item.id ? { ...i, qty: i.qty + 1 } : i);
      return [...prev, { ...item, qty: 1 }];
    });
    setCartCount((c) => c + 1);
  };

  const syncCartCount = async () => {
    if (!token) return;
    try {
      const data = await api("/api/cart/menu-items", {}, token);
      const arr = Array.isArray(data) ? data : (data.results || []);
      setCartCount(arr.length + localCart.length);
    } catch { }
  };

  useEffect(() => { if (token) syncCartCount(); }, [token, page]);

  if (!token) return (
    <>
      <StyleTag />
      <div className="app">
        <AuthScreen onLogin={handleLogin} />
      </div>
    </>
  );

  const nav = [
    { id: "menu", label: "Menu" },
    ...(role === "Customer" ? [{ id: "cart", label: "Cart", badge: cartCount > 0 ? cartCount : null }] : []),
    ...(role === "Customer" ? [{ id: "orders", label: "Orders" }] : []),
    ...(role === "Manager" ? [{ id: "mgr-orders", label: "Orders" }] : []),
    ...(role === "Manager" ? [{ id: "admin", label: "User Groups" }] : []),
    ...(role === "Delivery crew" ? [{ id: "delivery", label: "Deliveries" }] : []),
  ];

  return (
    <>
      <StyleTag />
      <div className="app">
        <nav>
          <div className="brand" onClick={() => setPage("menu")}>
            <div className="logo-circle">L</div>
            <span>Little Lemon</span>
          </div>
          <div className="nav-links">
            {nav.map((n) => (
              <button key={n.id} className={page === n.id ? "active" : ""} onClick={() => setPage(n.id)}>
                {n.label}
                {n.badge && <span className="badge">{n.badge}</span>}
              </button>
            ))}
          </div>
          <div style={{ display: "flex", gap: ".75rem", alignItems: "center" }}>
            <div className="user-pill">
              <span>{user?.username}</span>
              <span className="role-tag">{role === "Delivery crew" ? "Crew" : role}</span>
            </div>
            <button className="logout-btn" onClick={handleLogout}>Sign Out</button>
          </div>
        </nav>
        <main>
          {page === "menu" && <MenuPage token={token} role={role} cart={localCart} onAddToCart={addToLocalCart} />}
          {page === "cart" && <CartPage token={token} localCart={localCart} onClearLocal={() => { setLocalCart([]); setCartCount(0); }} onSyncCart={syncCartCount} />}
          {page === "orders" && <OrdersPage token={token} />}
          {page === "mgr-orders" && <ManagerOrdersPage token={token} />}
          {page === "admin" && <AdminPage token={token} />}
          {page === "delivery" && <DeliveryPage token={token} />}
        </main>
      </div>
    </>
  );
}
