import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export default function Dashboard() {
  const [matches, setMatches] = useState([]);
  const [pos, setPos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [matchesRes, posRes] = await Promise.all([
        axios.get(`${API_BASE}/invoices/pending-matches`),
        axios.get(`${API_BASE}/purchase-orders`)
      ]);
      setMatches(matchesRes.data);
      setPos(posRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const approveMatch = async (matchId) => {
    try {
      await axios.post(`${API_BASE}/invoices/approve-match/${matchId}`);
      setMatches(matches.filter(m => m.match_id !== matchId));
    } catch (error) {
      console.error('Error approving match:', error);
    }
  };

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold mb-4">Pending Matches</h2>
        {matches.length === 0 ? (
          <p className="text-gray-500">No pending matches</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border p-2 text-left">Invoice #</th>
                  <th className="border p-2 text-left">PO #</th>
                  <th className="border p-2 text-left">Amount</th>
                  <th className="border p-2 text-left">Score</th>
                  <th className="border p-2 text-left">Reasoning</th>
                  <th className="border p-2">Action</th>
                </tr>
              </thead>
              <tbody>
                {matches.map((match) => (
                  <tr key={match.match_id} className="hover:bg-gray-100">
                    <td className="border p-2">{match.invoice_number}</td>
                    <td className="border p-2">{match.po_number}</td>
                    <td className="border p-2">${match.amount?.toFixed(2)}</td>
                    <td className="border p-2">{(match.score * 100).toFixed(1)}%</td>
                    <td className="border p-2 text-sm">{match.reasoning}</td>
                    <td className="border p-2 text-center">
                      <button
                        onClick={() => approveMatch(match.match_id)}
                        className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                      >
                        Approve
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div>
        <h2 className="text-3xl font-bold mb-4">Available Purchase Orders</h2>
        {pos.length === 0 ? (
          <p className="text-gray-500">No purchase orders available</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead className="bg-gray-200">
                <tr>
                  <th className="border p-2 text-left">PO #</th>
                  <th className="border p-2 text-left">Vendor</th>
                  <th className="border p-2 text-left">Description</th>
                  <th className="border p-2 text-right">Amount</th>
                  <th className="border p-2 text-right">Remaining</th>
                </tr>
              </thead>
              <tbody>
                {pos.map((order) => (
                  <tr key={order.po_id} className="hover:bg-gray-100">
                    <td className="border p-2">{order.po_number}</td>
                    <td className="border p-2">{order.vendor_name}</td>
                    <td className="border p-2 text-sm">{order.description}</td>
                    <td className="border p-2 text-right">${order.line_amount?.toFixed(2)}</td>
                    <td className="border p-2 text-right">${order.remaining_amount?.toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
