import React, { useState } from "react";
import { Container, Card, Tabs, Tab, Form, Button, Alert, Spinner } from "react-bootstrap";
import { api } from "../api";

export default function AuthScreen({ onLogin }) {
  const [tab, setTab] = useState("login");
  const [form, setForm] = useState({ username: "", password: "", email: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    setError(""); setLoading(true);
    try {
      if (tab === "register") {
        await api("/auth/users/", {
          method: "POST",
          body: JSON.stringify({ username: form.username, password: form.password, email: form.email }),
        });
      }
      const { auth_token } = await api("/auth/token/login/", {
        method: "POST",
        body: JSON.stringify({ username: form.username, password: form.password }),
      });
      const me = await api("/auth/users/me/", {}, auth_token);
      onLogin(auth_token, me);
    } catch (err) {
      const msgs = Object.values(err?.data || {}).flat();
      setError(msgs.length ? msgs.join(" ") : "Something went wrong.");
    } finally { setLoading(false); }
  };

  return (
    <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: "100vh" }}>
      <Card style={{ width: "100%", maxWidth: "400px" }} className="p-4 shadow-sm">
        <div className="text-center mb-4">
          <div className="display-4 fw-bold text-primary mb-2">L</div>
          <h2>Little Lemon</h2>
          <p className="text-muted">Mediterranean restaurant experience</p>
        </div>

        {error && <Alert variant="danger">{error}</Alert>}

        <Tabs
          id="auth-tabs"
          activeKey={tab}
          onSelect={(k) => { setTab(k); setError(""); }}
          className="mb-4 d-flex"
          justify
        >
          <Tab eventKey="login" title="Sign In">
            <Form onSubmit={submit}>
              <Form.Group className="mb-3">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" value={form.username} onChange={set("username")} required />
              </Form.Group>
              <Form.Group className="mb-4">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" value={form.password} onChange={set("password")} required />
              </Form.Group>
              <Button variant="primary" type="submit" className="w-100" disabled={loading}>
                {loading ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" /> : "Sign In"}
              </Button>
            </Form>
          </Tab>
          <Tab eventKey="register" title="Register">
            <Form onSubmit={submit}>
              <Form.Group className="mb-3">
                <Form.Label>Username</Form.Label>
                <Form.Control type="text" value={form.username} onChange={set("username")} required />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" value={form.email} onChange={set("email")} required />
              </Form.Group>
              <Form.Group className="mb-4">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" value={form.password} onChange={set("password")} required />
              </Form.Group>
              <Button variant="primary" type="submit" className="w-100" disabled={loading}>
                {loading ? <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" /> : "Create Account"}
              </Button>
            </Form>
          </Tab>
        </Tabs>
      </Card>
    </Container>
  );
}
