import React from 'react';
import { Typography, Paper, Box } from '@mui/material';

export default function DashboardOverview() {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>
      <Box>
        <Typography>
          Welcome! Here you will see a summary of market trends, recent predictions, and analytics.
        </Typography>
      </Box>
    </Paper>
  );
} 