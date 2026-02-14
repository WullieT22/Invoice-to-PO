import React, { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export default function InvoiceUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError(null);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const formData = new FormData();
      formData.append('file', file);

      const uploadRes = await axios.post(`${API_BASE}/invoices/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      // Now match the invoice
      const matchRes = await axios.post(
        `${API_BASE}/invoices/match/${uploadRes.data.invoice_id}`
      );

      setResult({
        upload: uploadRes.data,
        match: matchRes.data
      });
      setFile(null);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-3xl font-bold mb-6">Upload Invoice</h2>
      
      <form onSubmit={handleUpload} className="bg-white p-8 rounded shadow-lg">
        <div className="mb-6">
          <label className="block text-lg font-semibold mb-3">
            Select Invoice File (PDF, TXT, CSV)
          </label>
          <input
            type="file"
            onChange={handleFileChange}
            accept=".pdf,.txt,.csv"
            disabled={loading}
            className="block w-full border border-gray-300 rounded p-3"
          />
        </div>

        <button
          type="submit"
          disabled={loading || !file}
          className={`w-full py-3 rounded font-semibold text-white ${
            loading || !file
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-blue-500 hover:bg-blue-600'
          }`}
        >
          {loading ? 'Processing...' : 'Upload and Match'}
        </button>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="mt-6 space-y-4">
          <div className="p-4 bg-blue-100 border border-blue-400 rounded">
            <h3 className="font-bold text-lg mb-2">Upload Successful</h3>
            <p><strong>Invoice #:</strong> {result.upload.invoice_number}</p>
            <p><strong>Vendor:</strong> {result.upload.vendor_name}</p>
            <p><strong>Amount:</strong> ${result.upload.amount?.toFixed(2)}</p>
            <p><strong>Type:</strong> {result.upload.type}</p>
          </div>

          <div className={`p-4 border rounded ${
            result.match.match_found 
              ? 'bg-green-100 border-green-400' 
              : 'bg-yellow-100 border-yellow-400'
          }`}>
            <h3 className="font-bold text-lg mb-2">Match Result</h3>
            {result.match.match_found ? (
              <>
                <p><strong>Matched PO:</strong> {result.match.po_number}</p>
                <p><strong>Confidence:</strong> {(result.match.match_score * 100).toFixed(1)}%</p>
                <p><strong>Requires Approval:</strong> {result.match.requires_approval ? 'Yes' : 'No'}</p>
                <p className="mt-2"><strong>Reasoning:</strong> {result.match.reasoning}</p>
              </>
            ) : (
              <p>{result.match.message}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
