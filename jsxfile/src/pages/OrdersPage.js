import React, { useState, useEffect, useCallback } from "react";
import { api } from "../api";
import { Spinner, Alert, Modal, QtyCtrl } from "../components/common";

export default function OrdersPage({ token }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const PER_PAGE = 5;

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api(`/api/orders?page=${page}&perpage=${PER_PAGE}`, {}, token);
      if (Array.isArray(data)) { setOrders(data); setTotal(data.length); }
      else { setOrders(data.results || []); setTotal(data.count || 0); }
    } catch { setError("Failed to load orders."); }
    finally { setLoading(false); }
  }, [token, page]);

  useEffect(() => { load(); }, [load]);

  const pages = Math.max(1, Math.ceil(total / PER_PAGE));

  return (
    <div>
      <div className="section-header">
        <div><h2>My Orders</h2><p>Track your order history</p></div>
      </div>
      <Alert msg={error} />
      {loading ? <Spinner /> : orders.length === 0 ? (
        <div className="empty-state"><div className="empty-icon">📋</div><p>No orders yet.</p></div>
      ) : (
        <>
          {orders.map((o) => (
            <div className="order-card" key={o.id}>
              <div className="order-header">
                <span className="order-id">Order #{o.id}</span>
                <span className={`status-badge status-${o.status}`}>{o.status === 1 ? "Delivered" : "Pending"}</span>
                <span className="order-meta">{o.date}</span>
                <span className="order-meta" style={{ marginLeft: "auto", fontWeight: 700 }}>${parseFloat(o.total).toFixed(2)}</span>
              </div>
              {o.order_items && (
                <div className="order-items-list">
                  {o.order_items.map((oi, i) => (
                    <div className="order-item-row" key={i}>
                      <span>{oi.menuitem_title || `Item #${oi.menuitem}`} ×{oi.quantity}</span>
                      <span>${parseFloat(oi.price).toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
          {pages > 1 && (
            <div className="pagination">
              <button onClick={() => setPage((p) => p - 1)} disabled={page === 1}>← Prev</button>
              <span className="page-info">Page {page} of {pages}</span>
              <button onClick={() => setPage((p) => p + 1)} disabled={page >= pages}>Next →</button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
