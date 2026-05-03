import React, { useState, useEffect } from "react";
import { api } from "../api";
import { Spinner, Alert } from "../components/common";

export default function DeliveryPage({ token }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const load = async () => {
    setLoading(true);
    try {
      const data = await api("/api/orders", {}, token);
      if (Array.isArray(data)) setOrders(data);
      else setOrders(data.results || []);
    } catch { setError("Failed to load assigned orders."); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const markDelivered = async (id) => {
    try {
      await api(`/api/orders/${id}`, { method: "PATCH", body: JSON.stringify({ status: 1 }) }, token);
      setSuccess("Order marked as delivered!"); load();
    } catch { setError("Update failed."); }
  };

  return (
    <div>
      <div className="section-header"><div><h2>Assigned Deliveries</h2><p>Your active deliveries</p></div></div>
      <Alert msg={error} />
      <Alert type="success" msg={success} />
      {loading ? <Spinner /> : orders.length === 0 ? (
        <div className="empty-state"><div className="empty-icon">🛵</div><p>No deliveries assigned.</p></div>
      ) : orders.map((o) => (
        <div className="delivery-card" key={o.id}>
          <div className="order-header">
            <span className="order-id">Order #{o.id}</span>
            <span className={`status-badge status-${o.status}`}>{o.status === 1 ? "Delivered" : "Pending"}</span>
            <span className="order-meta">${parseFloat(o.total).toFixed(2)}</span>
          </div>
          {o.status === 0 && (
            <button className="btn btn-primary btn-sm" style={{ marginTop: ".75rem" }} onClick={() => markDelivered(o.id)}>
              ✓ Mark Delivered
            </button>
          )}
        </div>
      ))}
    </div>
  );
}
