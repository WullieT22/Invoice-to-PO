import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import InvoiceUpload from './pages/InvoiceUpload';
import Dashboard from './pages/Dashboard';
import Navigation from './components/Navigation';

function App() {
  return (
    <Router>
      <div className="App">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<InvoiceUpload />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
