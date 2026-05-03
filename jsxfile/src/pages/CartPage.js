import React, { useState, useEffect, useCallback } from "react";
import { api } from "../api";
import { Spinner, Alert, Modal, QtyCtrl } from "../components/common";

export default function CartPage({ token, localCart, onClearLocal, onSyncCart }) {
  const [serverCart, setServerCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [ordering, setOrdering] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const data = await api("/api/cart/menu-items", {}, token);
      setServerCart(Array.isArray(data) ? data : (data.results || []));
    } catch { setError("Failed to load cart from server."); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  useEffect(() => {
    const sync = async () => {
      for (const item of localCart) {
        try {
          await api("/api/cart/menu-items", {
            method: "POST",
            body: JSON.stringify({ menuitem_id: item.id, quantity: item.qty }),
          }, token);
        } catch { }
      }
      onClearLocal();
      load();
    };
    if (localCart.length > 0) sync();
  }, []);

  const clearCart = async () => {
    try {
      await api("/api/cart/menu-items", { method: "DELETE" }, token);
      setServerCart([]); setSuccess("Cart cleared.");
    } catch { setError("Clear failed."); }
  };

  const placeOrder = async () => {
    setOrdering(true); setError(""); setSuccess("");
    try {
      await api("/api/orders", { method: "POST" }, token);
      setServerCart([]);
      setSuccess("Order placed successfully! 🎉");
    } catch (err) {
      setError(err?.data?.message || "Could not place order.");
    } finally { setOrdering(false); }
  };

  const total = serverCart.reduce((s, i) => s + parseFloat(i.price || 0), 0);

  return (
    <div>
      <div className="section-header">
        <div><h2>Your Cart</h2><p>{serverCart.length} item(s)</p></div>
        {serverCart.length > 0 && (
          <button className="btn btn-outline btn-sm" onClick={clearCart}>Clear Cart</button>
        )}
      </div>
      <Alert msg={error} />
      <Alert type="success" msg={success} />
      {loading ? <Spinner /> : serverCart.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🛒</div>
          <p>Your cart is empty.</p>
          <p style={{ marginTop: ".5rem", fontSize: ".85rem" }}>Browse the menu and add some items!</p>
        </div>
      ) : (
        <div className="cart-wrap">
          <div>
            {serverCart.map((item, i) => (
              <div className="cart-item" key={i}>
                <div className="ci-title">{item.menuitem?.title || item.menuitem_title || "Item"}</div>
                <div style={{ fontSize: ".85rem", color: "var(--muted)" }}>×{item.quantity}</div>
                <div className="ci-price">${parseFloat(item.price).toFixed(2)}</div>
              </div>
            ))}
          </div>
          <div className="cart-summary">
            <h3>Order Summary</h3>
            {serverCart.map((item, i) => (
              <div className="summary-row" key={i}>
                <span>{item.menuitem?.title || item.menuitem_title || "Item"}</span>
                <span>${parseFloat(item.price).toFixed(2)}</span>
              </div>
            ))}
            <div className="summary-row total">
              <span>Total</span>
              <span>${total.toFixed(2)}</span>
            </div>
            <button className="btn btn-lemon btn-full" style={{ marginTop: "1rem" }} onClick={placeOrder} disabled={ordering}>
              {ordering ? "Placing Order…" : "Place Order"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
