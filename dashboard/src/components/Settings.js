import React from 'react';
import { Typography, Paper, Box } from '@mui/material';

export default function Settings() {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Settings
      </Typography>
      <Box>
        <Typography>
          Configure your preferences, API keys, and other settings here.
        </Typography>
      </Box>
    </Paper>
  );
} 