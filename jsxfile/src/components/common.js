import React from 'react';

export const Spinner = () => (
  <div className="spinner-wrap"><div className="spinner" /></div>
);

export const Alert = ({ type = "error", msg }) =>
  msg ? <div className={`alert alert-${type}`}>{msg}</div> : null;

export const Modal = ({ title, onClose, children, footer }) => (
  <div className="modal-backdrop" onClick={(e) => e.target === e.currentTarget && onClose()}>
    <div className="modal">
      <h3>{title}</h3>
      {children}
      {footer && <div className="modal-footer">{footer}</div>}
    </div>
  </div>
);

export const QtyCtrl = ({ qty, onDec, onInc }) => (
  <div className="qty-ctrl">
    <button onClick={onDec}>−</button>
    <span>{qty}</span>
    <button onClick={onInc}>+</button>
  </div>
);
