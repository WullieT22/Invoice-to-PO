import React from 'react';
import { Link } from 'react-router-dom';

export default function Navigation() {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <div className="text-2xl font-bold">
          Invoice to PO Matching
        </div>
        <ul className="flex space-x-6">
          <li><Link to="/" className="hover:text-blue-200">Dashboard</Link></li>
          <li><Link to="/upload" className="hover:text-blue-200">Upload Invoice</Link></li>
        </ul>
      </div>
    </nav>
  );
}
