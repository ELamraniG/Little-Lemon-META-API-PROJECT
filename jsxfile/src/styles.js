import { useEffect } from "react";

export const STYLE = `
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --lemon: #F4CE14;
  --green: #495E57;
  --dark:  #1A1A1A;
  --mid:   #333;
  --muted: #666;
  --light: #F9F5EC;
  --card:  #FFFDF5;
  --border:#E8E0CC;
  --red:   #C0392B;
  --radius: 12px;
  --shadow: 0 4px 24px rgba(0,0,0,.10);
}

body { font-family: 'DM Sans', sans-serif; background: var(--light); color: var(--dark); }

h1,h2,h3,h4 { font-family: 'Playfair Display', serif; }

.app { min-height: 100vh; display: flex; flex-direction: column; }

nav {
  background: var(--green);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 2rem; height: 64px;
  position: sticky; top: 0; z-index: 100;
  box-shadow: 0 2px 12px rgba(0,0,0,.25);
}
nav .brand { display: flex; align-items: center; gap: .6rem; cursor: pointer; }
nav .brand .logo-circle {
  width: 36px; height: 36px; border-radius: 50%;
  background: var(--lemon); display: flex; align-items: center; justify-content: center;
  font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.1rem; color: var(--green);
}
nav .brand span { color: var(--lemon); font-family: 'Playfair Display', serif; font-size: 1.25rem; font-weight: 700; }
nav .nav-links { display: flex; gap: .5rem; align-items: center; }
nav .nav-links button {
  background: none; border: none; color: rgba(255,255,255,.85);
  font-family: 'DM Sans', sans-serif; font-size: .9rem; padding: .5rem .9rem;
  border-radius: 8px; cursor: pointer; transition: background .15s, color .15s;
}
nav .nav-links button:hover { background: rgba(255,255,255,.12); color: #fff; }
nav .nav-links button.active { background: var(--lemon); color: var(--green); font-weight: 500; }
nav .nav-links .badge {
  display: inline-flex; align-items: center; justify-content: center;
  background: var(--lemon); color: var(--green); font-size: .7rem; font-weight: 700;
  width: 18px; height: 18px; border-radius: 50%; margin-left: .25rem;
}
nav .user-pill {
  display: flex; align-items: center; gap: .5rem;
  background: rgba(255,255,255,.12); padding: .3rem .8rem;
  border-radius: 20px; color: #fff; font-size: .85rem;
}
nav .user-pill .role-tag {
  background: var(--lemon); color: var(--green); font-size: .68rem;
  font-weight: 700; padding: .1rem .4rem; border-radius: 4px; text-transform: uppercase;
}
nav .logout-btn {
  background: none; border: 1px solid rgba(255,255,255,.3); color: rgba(255,255,255,.8);
  font-size: .8rem; padding: .3rem .7rem; border-radius: 8px; cursor: pointer;
  transition: all .15s;
}
nav .logout-btn:hover { background: rgba(255,255,255,.15); color: #fff; }

.auth-wrap {
  flex: 1; display: flex; align-items: center; justify-content: center;
  background: radial-gradient(ellipse at 60% 40%, #e8f0ec 0%, var(--light) 70%);
  padding: 2rem;
}
.auth-card {
  background: var(--card); border-radius: 20px; padding: 2.5rem;
  width: 100%; max-width: 400px; box-shadow: var(--shadow);
  border: 1px solid var(--border);
}
.auth-card .logo-big {
  width: 56px; height: 56px; border-radius: 50%; background: var(--green);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.6rem; color: var(--lemon);
  margin: 0 auto 1rem;
}
.auth-card h2 { text-align: center; font-size: 1.6rem; margin-bottom: .25rem; }
.auth-card p { text-align: center; color: var(--muted); font-size: .9rem; margin-bottom: 1.5rem; }
.auth-tabs { display: flex; background: var(--light); border-radius: 10px; padding: 3px; margin-bottom: 1.5rem; }
.auth-tabs button {
  flex: 1; padding: .5rem; border: none; background: none;
  border-radius: 8px; cursor: pointer; font-family: 'DM Sans', sans-serif;
  font-size: .9rem; color: var(--muted); transition: all .15s;
}
.auth-tabs button.active { background: var(--card); color: var(--dark); font-weight: 500; box-shadow: 0 2px 8px rgba(0,0,0,.08); }

.field { margin-bottom: 1rem; }
.field label { display: block; font-size: .8rem; font-weight: 500; color: var(--muted); margin-bottom: .35rem; text-transform: uppercase; letter-spacing: .05em; }
.field input, .field select, .field textarea {
  width: 100%; padding: .65rem .9rem;
  border: 1.5px solid var(--border); border-radius: 10px;
  font-family: 'DM Sans', sans-serif; font-size: .95rem; color: var(--dark);
  background: #fff; transition: border-color .15s;
  outline: none;
}
.field input:focus, .field select:focus, .field textarea:focus { border-color: var(--green); }

.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: .4rem;
  padding: .65rem 1.4rem; border-radius: 10px; border: none; cursor: pointer;
  font-family: 'DM Sans', sans-serif; font-size: .9rem; font-weight: 500;
  transition: all .15s; text-decoration: none;
}
.btn-primary { background: var(--green); color: #fff; }
.btn-primary:hover { background: #3d4f49; }
.btn-lemon { background: var(--lemon); color: var(--green); }
.btn-lemon:hover { background: #e6c010; }
.btn-outline { background: none; border: 1.5px solid var(--border); color: var(--dark); }
.btn-outline:hover { border-color: var(--green); color: var(--green); }
.btn-danger { background: none; border: 1.5px solid var(--red); color: var(--red); }
.btn-danger:hover { background: var(--red); color: #fff; }
.btn-sm { padding: .4rem .9rem; font-size: .82rem; border-radius: 8px; }
.btn:disabled { opacity: .5; cursor: not-allowed; }
.btn-full { width: 100%; }

.alert { padding: .75rem 1rem; border-radius: 10px; font-size: .9rem; margin-bottom: 1rem; }
.alert-error { background: #fdecea; color: var(--red); border: 1px solid #f5c6c2; }
.alert-success { background: #eaf5ea; color: #2e7d32; border: 1px solid #c8e6c9; }
.alert-info { background: #e8f0ec; color: var(--green); border: 1px solid #c5d8d2; }

main { flex: 1; max-width: 1100px; margin: 0 auto; width: 100%; padding: 2rem 1.5rem; }

.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; flex-wrap: wrap; gap: .75rem; }
.section-header h2 { font-size: 1.75rem; color: var(--dark); }
.section-header p { color: var(--muted); font-size: .9rem; margin-top: .15rem; }

.menu-controls { display: flex; gap: .75rem; flex-wrap: wrap; align-items: center; margin-bottom: 1.5rem; }
.menu-controls input { flex: 1; min-width: 180px; padding: .55rem .9rem; border: 1.5px solid var(--border); border-radius: 10px; font-family: 'DM Sans', sans-serif; font-size: .9rem; outline: none; background: #fff; }
.menu-controls input:focus { border-color: var(--green); }
.sort-btn { padding: .5rem .9rem; border: 1.5px solid var(--border); background: #fff; border-radius: 10px; cursor: pointer; font-size: .85rem; color: var(--muted); transition: all .15s; }
.sort-btn:hover, .sort-btn.active { border-color: var(--green); color: var(--green); }

.menu-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1.25rem; }
.menu-card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1.25rem; transition: box-shadow .2s, transform .2s;
}
.menu-card:hover { box-shadow: var(--shadow); transform: translateY(-2px); }
.menu-card h3 { font-size: 1.05rem; margin-bottom: .35rem; }
.menu-card .price { font-size: 1.2rem; font-weight: 700; color: var(--green); }
.menu-card .inv { font-size: .8rem; color: var(--muted); margin-top: .15rem; }
.menu-card .card-actions { display: flex; gap: .5rem; margin-top: 1rem; flex-wrap: wrap; }

.modal-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,.45);
  display: flex; align-items: center; justify-content: center; z-index: 200;
  padding: 1rem;
}
.modal {
  background: var(--card); border-radius: 18px; padding: 2rem;
  width: 100%; max-width: 440px; box-shadow: 0 8px 40px rgba(0,0,0,.2);
  max-height: 90vh; overflow-y: auto;
}
.modal h3 { font-size: 1.3rem; margin-bottom: 1.25rem; }
.modal-footer { display: flex; gap: .75rem; margin-top: 1.25rem; justify-content: flex-end; }

.cart-wrap { display: grid; grid-template-columns: 1fr 280px; gap: 1.5rem; align-items: start; }
@media (max-width: 700px) { .cart-wrap { grid-template-columns: 1fr; } }
.cart-item { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem 1.25rem; display: flex; align-items: center; gap: 1rem; margin-bottom: .75rem; }
.cart-item .ci-title { font-weight: 500; flex: 1; }
.cart-item .ci-price { font-size: .95rem; color: var(--green); font-weight: 600; white-space: nowrap; }
.cart-summary { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; position: sticky; top: 80px; }
.cart-summary h3 { font-size: 1.1rem; margin-bottom: 1rem; }
.summary-row { display: flex; justify-content: space-between; font-size: .9rem; margin-bottom: .5rem; }
.summary-row.total { font-weight: 700; font-size: 1.05rem; border-top: 1px solid var(--border); padding-top: .75rem; margin-top: .25rem; }
.empty-state { text-align: center; padding: 3rem 2rem; color: var(--muted); }
.empty-state .empty-icon { font-size: 3rem; margin-bottom: .75rem; }

.order-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem; margin-bottom: 1rem; }
.order-header { display: flex; align-items: center; gap: .75rem; margin-bottom: .75rem; flex-wrap: wrap; }
.order-id { font-weight: 700; font-size: 1rem; }
.status-badge { display: inline-block; padding: .2rem .65rem; border-radius: 20px; font-size: .78rem; font-weight: 600; }
.status-0 { background: #fff3cd; color: #856404; }
.status-1 { background: #d1e7dd; color: #0a5c36; }
.order-meta { font-size: .85rem; color: var(--muted); }
.order-items-list { margin-top: .75rem; padding-top: .75rem; border-top: 1px solid var(--border); }
.order-item-row { display: flex; justify-content: space-between; font-size: .88rem; padding: .25rem 0; }
.order-total { font-weight: 700; margin-top: .5rem; display: flex; justify-content: space-between; }

.admin-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }
@media (max-width: 700px) { .admin-grid { grid-template-columns: 1fr; } }
.admin-panel { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.5rem; }
.admin-panel h3 { font-size: 1.1rem; margin-bottom: 1rem; }
.user-row { display: flex; align-items: center; gap: .75rem; padding: .6rem 0; border-bottom: 1px solid var(--border); }
.user-row:last-child { border-bottom: none; }
.user-row .uname { flex: 1; font-size: .9rem; font-weight: 500; }
.user-row .uid { font-size: .78rem; color: var(--muted); }

.spinner-wrap { display: flex; align-items: center; justify-content: center; padding: 3rem; }
.spinner {
  width: 36px; height: 36px; border: 3px solid var(--border);
  border-top-color: var(--green); border-radius: 50%;
  animation: spin .7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.delivery-card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem; margin-bottom: 1rem; }

.qty-ctrl { display: flex; align-items: center; gap: .5rem; }
.qty-ctrl button { width: 28px; height: 28px; border: 1.5px solid var(--border); background: #fff; border-radius: 6px; cursor: pointer; font-size: 1rem; display: flex; align-items: center; justify-content: center; transition: all .15s; }
.qty-ctrl button:hover { border-color: var(--green); color: var(--green); }
.qty-ctrl span { width: 24px; text-align: center; font-weight: 600; }

.pagination { display: flex; gap: .5rem; align-items: center; margin-top: 1.25rem; justify-content: center; }
.pagination button { padding: .4rem .8rem; border: 1.5px solid var(--border); background: #fff; border-radius: 8px; cursor: pointer; font-size: .85rem; transition: all .15s; }
.pagination button:hover:not(:disabled) { border-color: var(--green); color: var(--green); }
.pagination button:disabled { opacity: .4; cursor: not-allowed; }
.pagination .page-info { font-size: .85rem; color: var(--muted); }
`;

export const StyleTag = () => {
  useEffect(() => {
    const el = document.createElement("style");
    el.textContent = STYLE;
    document.head.appendChild(el);
    return () => document.head.removeChild(el);
  }, []);
  return null;
};
