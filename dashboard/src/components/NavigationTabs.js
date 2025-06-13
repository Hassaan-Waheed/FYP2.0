import React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

export default function NavigationTabs({ value, onChange }) {
  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
      <Tabs value={value} onChange={onChange} aria-label="navigation tabs">
        <Tab label="Dashboard" />
        <Tab label="Data Ingestion" />
        <Tab label="Model Predictions" />
        <Tab label="Analytics" />
        <Tab label="Settings" />
      </Tabs>
    </Box>
  );
} 