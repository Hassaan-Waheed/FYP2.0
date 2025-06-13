import React from 'react';
import { Typography, Paper, Box } from '@mui/material';

export default function ModelPredictions() {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Model Predictions
      </Typography>
      <Box>
        <Typography>
          This section will display the latest predictions from each model, including scores and timestamps.
        </Typography>
      </Box>
    </Paper>
  );
} 