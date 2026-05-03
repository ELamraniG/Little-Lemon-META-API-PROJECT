import React, { useState, useEffect } from "react";
import { api } from "../api";
import { Spinner, Alert } from "../components/common";

export default function AdminPage({ token }) {
  const [managers, setManagers] = useState([]);
  const [crew, setCrew] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [mInput, setMInput] = useState("");
  const [cInput, setCInput] = useState("");

  const load = async () => {
    setLoading(true);
    try {
      const [m, c] = await Promise.all([
        api("/api/groups/manager/users", {}, token),
        api("/api/groups/delivery-crew/users", {}, token),
      ]);
      setManagers(Array.isArray(m) ? m : []);
      setCrew(Array.isArray(c) ? c : []);
    } catch (err) { setError(err?.data?.message || "Failed to load groups."); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const addUser = async (group, userId, clearFn) => {
    setError(""); setSuccess("");
    try {
      const path = group === "manager" ? "/api/groups/manager/users" : "/api/groups/delivery-crew/users";
      await api(path, { method: "POST", body: JSON.stringify({ userId: parseInt(userId) }) }, token);
      setSuccess("User added."); clearFn(""); load();
    } catch (err) { setError(err?.data?.message || "Failed to add user."); }
  };

  const removeUser = async (group, userId) => {
    setError(""); setSuccess("");
    try {
      const path = group === "manager"
        ? `/api/groups/manager/users/${userId}`
        : `/api/groups/delivery-crew/users/${userId}`;
      await api(path, { method: "DELETE" }, token);
      setSuccess("User removed."); load();
    } catch (err) { setError(err?.data?.message || "Failed to remove user."); }
  };

  const GroupPanel = ({ title, users, groupKey, input, setInput }) => (
    <div className="admin-panel">
      <h3>{title}</h3>
      <div style={{ display: "flex", gap: ".5rem", marginBottom: "1rem" }}>
        <input
          className="field input"
          style={{ flex: 1, padding: ".55rem .9rem", border: "1.5px solid var(--border)", borderRadius: 10, fontSize: ".9rem", outline: "none" }}
          type="number" placeholder="User ID" value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="btn btn-lemon btn-sm" onClick={() => addUser(groupKey, input, setInput)} disabled={!input}>Add</button>
      </div>
      {users.length === 0 ? <p style={{ color: "var(--muted)", fontSize: ".9rem" }}>No users in this group.</p> : users.map((u) => (
        <div className="user-row" key={u.id}>
          <div>
            <div className="uname">{u.username}</div>
            <div className="uid">ID: {u.id}</div>
          </div>
          <button className="btn btn-danger btn-sm" onClick={() => removeUser(groupKey, u.id)}>Remove</button>
        </div>
      ))}
    </div>
  );

  return (
    <div>
      <div className="section-header"><div><h2>User Management</h2><p>Manage roles and groups</p></div></div>
      <Alert msg={error} />
      <Alert type="success" msg={success} />
      {loading ? <Spinner /> : (
        <div className="admin-grid">
          <GroupPanel title="Managers" users={managers} groupKey="manager" input={mInput} setInput={setMInput} />
          <GroupPanel title="Delivery Crew" users={crew} groupKey="delivery" input={cInput} setInput={setCInput} />
        </div>
      )}
    </div>
  );
}
