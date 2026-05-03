import React, { useState, useEffect, useCallback } from "react";
import { api } from "../api";
import { Spinner, Alert, Modal } from "../components/common";

export default function ManagerOrdersPage({ token }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [editOrder, setEditOrder] = useState(null);
  const [editForm, setEditForm] = useState({ status: 0, delivery_crew: "" });
  const [saving, setSaving] = useState(false);
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

  const openEdit = (o) => {
    setEditOrder(o);
    setEditForm({ status: o.status, delivery_crew: o.delivery_crew || "" });
  };

  const saveOrder = async () => {
    setSaving(true);
    try {
      const body = { status: parseInt(editForm.status) };
      if (editForm.delivery_crew) body.delivery_crew = parseInt(editForm.delivery_crew);
      await api(`/api/orders/${editOrder.id}`, { method: "PATCH", body: JSON.stringify(body) }, token);
      setSuccess("Order updated."); setEditOrder(null); load();
    } catch (err) {
      setError(err?.data?.message || "Update failed.");
    } finally { setSaving(false); }
  };

  const deleteOrder = async (id) => {
    if (!window.confirm("Delete this order?")) return;
    try {
      await api(`/api/orders/${id}`, { method: "DELETE" }, token);
      setSuccess("Order deleted."); load();
    } catch { setError("Delete failed."); }
  };

  const pages = Math.max(1, Math.ceil(total / PER_PAGE));

  return (
    <div>
      <div className="section-header"><div><h2>All Orders</h2><p>Manage customer orders</p></div></div>
      <Alert msg={error} />
      <Alert type="success" msg={success} />
      {loading ? <Spinner /> : orders.length === 0 ? (
        <div className="empty-state"><div className="empty-icon">📦</div><p>No orders found.</p></div>
      ) : (
        <>
          {orders.map((o) => (
            <div className="order-card" key={o.id}>
              <div className="order-header">
                <span className="order-id">Order #{o.id}</span>
                <span className={`status-badge status-${o.status}`}>{o.status === 1 ? "Delivered" : "Pending"}</span>
                <span className="order-meta">Customer #{o.user}</span>
                {o.delivery_crew && <span className="order-meta">Crew #{o.delivery_crew}</span>}
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
              <div style={{ display: "flex", gap: ".5rem", marginTop: ".75rem" }}>
                <button className="btn btn-outline btn-sm" onClick={() => openEdit(o)}>Manage</button>
                <button className="btn btn-danger btn-sm" onClick={() => deleteOrder(o.id)}>Delete</button>
              </div>
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
      {editOrder && (
        <Modal title={`Manage Order #${editOrder.id}`} onClose={() => setEditOrder(null)}
          footer={<>
            <button className="btn btn-outline" onClick={() => setEditOrder(null)}>Cancel</button>
            <button className="btn btn-primary" onClick={saveOrder} disabled={saving}>{saving ? "Saving…" : "Update"}</button>
          </>}
        >
          <div className="field">
            <label>Status</label>
            <select value={editForm.status} onChange={(e) => setEditForm((f) => ({ ...f, status: e.target.value }))}>
              <option value={0}>Pending</option>
              <option value={1}>Delivered</option>
            </select>
          </div>
          <div className="field">
            <label>Delivery Crew User ID</label>
            <input type="number" value={editForm.delivery_crew}
              onChange={(e) => setEditForm((f) => ({ ...f, delivery_crew: e.target.value }))}
              placeholder="Enter user ID" />
          </div>
        </Modal>
      )}
    </div>
  );
}
