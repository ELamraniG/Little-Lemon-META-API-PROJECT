import React, { useState, useEffect, useCallback } from "react";
import { api } from "../api";
import { Spinner, Alert, Modal, QtyCtrl } from "../components/common";

export default function MenuPage({ token, role, cart, onAddToCart }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [sort, setSort] = useState("");
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [showAdd, setShowAdd] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [form, setForm] = useState({ title: "", price: "", inventory: "" });
  const [formErr, setFormErr] = useState("");
  const [saving, setSaving] = useState(false);

  const isManager = role === "Manager";
  const PER_PAGE = 5;

  const load = useCallback(async () => {
    setLoading(true); setError("");
    try {
      let url = `/api/menu-items?page=${page}&perpage=${PER_PAGE}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;
      if (sort) url += `&ordering=${sort}`;
      const data = await api(url, {}, token);
      if (Array.isArray(data)) { setItems(data); setTotal(data.length); }
      else { setItems(data.results || []); setTotal(data.count || 0); }
    } catch { setError("Failed to load menu."); }
    finally { setLoading(false); }
  }, [token, search, sort, page]);

  useEffect(() => { load(); }, [load]);

  const openAdd = () => { setForm({ title: "", price: "", inventory: "" }); setFormErr(""); setShowAdd(true); };
  const openEdit = (item) => { setForm({ title: item.title, price: item.price, inventory: item.inventory }); setEditItem(item); setFormErr(""); };

  const saveItem = async () => {
    setSaving(true); setFormErr("");
    try {
      if (editItem) {
        await api(`/api/menu-items/${editItem.id}`, {
          method: "PUT",
          body: JSON.stringify({ title: form.title, price: parseFloat(form.price), inventory: parseInt(form.inventory) }),
        }, token);
        setSuccess("Item updated."); setEditItem(null);
      } else {
        await api("/api/menu-items", {
          method: "POST",
          body: JSON.stringify({ title: form.title, price: parseFloat(form.price), inventory: parseInt(form.inventory) }),
        }, token);
        setSuccess("Item added."); setShowAdd(false);
      }
      load();
    } catch (err) {
      const msgs = Object.values(err?.data || {}).flat();
      setFormErr(msgs.length ? msgs.join(" ") : "Save failed.");
    } finally { setSaving(false); }
  };

  const deleteItem = async (id) => {
    if (!window.confirm("Delete this item?")) return;
    try {
      await api(`/api/menu-items/${id}`, { method: "DELETE" }, token);
      setSuccess("Item deleted."); load();
    } catch { setError("Delete failed."); }
  };

  const addToCart = (item) => {
    onAddToCart(item);
    setSuccess(`"${item.title}" added to cart!`);
    setTimeout(() => setSuccess(""), 2500);
  };

  const pages = Math.max(1, Math.ceil(total / PER_PAGE));

  const formModal = (isEdit) => (
    <Modal
      title={isEdit ? "Edit Menu Item" : "Add Menu Item"}
      onClose={() => isEdit ? setEditItem(null) : setShowAdd(false)}
      footer={<>
        <button className="btn btn-outline" onClick={() => isEdit ? setEditItem(null) : setShowAdd(false)}>Cancel</button>
        <button className="btn btn-primary" onClick={saveItem} disabled={saving}>{saving ? "Saving…" : "Save"}</button>
      </>}
    >
      <Alert msg={formErr} />
      {["title", "price", "inventory"].map((k) => (
        <div className="field" key={k}>
          <label>{k.charAt(0).toUpperCase() + k.slice(1)}</label>
          <input
            type={k === "title" ? "text" : "number"}
            step={k === "price" ? "0.01" : "1"}
            value={form[k]}
            onChange={(e) => setForm((f) => ({ ...f, [k]: e.target.value }))}
          />
        </div>
      ))}
    </Modal>
  );

  return (
    <div>
      <div className="section-header">
        <div>
          <h2>Menu</h2>
          <p>Explore our Mediterranean selection</p>
        </div>
        {isManager && <button className="btn btn-lemon" onClick={openAdd}>+ Add Item</button>}
      </div>
      <Alert type="success" msg={success} />
      <Alert msg={error} />
      <div className="menu-controls">
        <input placeholder="Search dishes…" value={search} onChange={(e) => { setSearch(e.target.value); setPage(1); }} />
        {["price", "-price", "title"].map((s) => (
          <button key={s} className={`sort-btn ${sort === s ? "active" : ""}`} onClick={() => setSort(sort === s ? "" : s)}>
            {s === "price" ? "Price ↑" : s === "-price" ? "Price ↓" : "A–Z"}
          </button>
        ))}
      </div>
      {loading ? <Spinner /> : (
        <>
          {items.length === 0 ? (
            <div className="empty-state"><div className="empty-icon">🍋</div><p>No items found.</p></div>
          ) : (
            <div className="menu-grid">
              {items.map((item) => (
                <div className="menu-card" key={item.id}>
                  <h3>{item.title}</h3>
                  <div className="price">${parseFloat(item.price).toFixed(2)}</div>
                  <div className="inv">Stock: {item.inventory}</div>
                  <div className="card-actions">
                    {role === "Customer" && (
                      <button className="btn btn-lemon btn-sm" onClick={() => addToCart(item)}>+ Cart</button>
                    )}
                    {isManager && (
                      <>
                        <button className="btn btn-outline btn-sm" onClick={() => openEdit(item)}>Edit</button>
                        <button className="btn btn-danger btn-sm" onClick={() => deleteItem(item.id)}>Delete</button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
          {pages > 1 && (
            <div className="pagination">
              <button onClick={() => setPage((p) => p - 1)} disabled={page === 1}>← Prev</button>
              <span className="page-info">Page {page} of {pages}</span>
              <button onClick={() => setPage((p) => p + 1)} disabled={page >= pages}>Next →</button>
            </div>
          )}
        </>
      )}
      {showAdd && formModal(false)}
      {editItem && formModal(true)}
    </div>
  );
}
