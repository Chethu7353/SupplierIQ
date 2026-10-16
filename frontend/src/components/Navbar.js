import React from 'react';
import './Navbar.css';

function Navbar() {
  return (
    <nav className="navbar">

      {/* Logo */}
      <div className="navbar-logo">
        <span className="logo-icon">S</span>
        <span className="logo-text">SupplierIQ</span>
      </div>

      {/* Navigation Links */}
      <div className="navbar-links">
        <a href="/" className="nav-link active">Home</a>
        <a href="#features" className="nav-link">Features</a>
        <a href="#about" className="nav-link">About</a>
      </div>

      {/* Authentication Buttons */}
      <div className="navbar-actions">
        <a href="/login" className="login-btn">Login</a>
        <a href="/register" className="register-btn">Register</a>
      </div>

    </nav>
  );
}

export default Navbar;