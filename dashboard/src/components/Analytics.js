import React from 'react';
import { Typography, Paper, Box } from '@mui/material';

export default function Analytics() {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Analytics
      </Typography>
      <Box>
        <Typography>
          This section will show analytics, charts, and performance metrics for your models and assets.
        </Typography>
      </Box>
    </Paper>
  );
} 