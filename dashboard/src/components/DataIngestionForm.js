import React, { useState } from 'react';
import { Paper, Typography, Box, TextField, Button, Alert } from '@mui/material';
import axios from 'axios';

export default function DataIngestionForm() {
  const [form, setForm] = useState({
    asset_id: '',
    timestamp: '',
    open: '',
    high: '',
    low: '',
    close: '',
    volume: ''
  });
  const [status, setStatus] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus(null);
    try {
      const payload = { ...form, open: parseFloat(form.open), high: parseFloat(form.high), low: parseFloat(form.low), close: parseFloat(form.close), volume: parseFloat(form.volume) };
      await axios.post('http://localhost:8000/api/v1/ohlcv', payload);
      setStatus('success');
      setForm({ asset_id: '', timestamp: '', open: '', high: '', low: '', close: '', volume: '' });
    } catch (err) {
      console.error(err);
      setStatus('error');
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Ingest OHLCV Data</Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField label="Asset ID" name="asset_id" value={form.asset_id} onChange={handleChange} required />
        <TextField label="Timestamp" name="timestamp" value={form.timestamp} onChange={handleChange} required placeholder="YYYY-MM-DDTHH:MM:SS" />
        <TextField label="Open" name="open" value={form.open} onChange={handleChange} required type="number" />
        <TextField label="High" name="high" value={form.high} onChange={handleChange} required type="number" />
        <TextField label="Low" name="low" value={form.low} onChange={handleChange} required type="number" />
        <TextField label="Close" name="close" value={form.close} onChange={handleChange} required type="number" />
        <TextField label="Volume" name="volume" value={form.volume} onChange={handleChange} required type="number" />
        <Button type="submit" variant="contained">Submit</Button>
        {status === 'success' && <Alert severity="success">Data inserted!</Alert>}
        {status === 'error' && <Alert severity="error">Error inserting data.</Alert>}
      </Box>
    </Paper>
  );
} 