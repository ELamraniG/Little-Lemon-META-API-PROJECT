export const BASE_URL = "http://127.0.0.1:8000";

export const api = async (path, opts = {}, token = null) => {
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  if (token) headers["Authorization"] = `Token ${token}`;
  const res = await fetch(`${BASE_URL}${path}`, { ...opts, headers });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw { status: res.status, data };
  return data;
};
