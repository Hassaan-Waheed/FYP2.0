import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, Box } from '@mui/material';
import NavigationTabs from './components/NavigationTabs';
import DashboardOverview from './components/DashboardOverview';
import DataIngestionForm from './components/DataIngestionForm';
import ModelPredictions from './components/ModelPredictions';
import Analytics from './components/Analytics';
import Settings from './components/Settings';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
  },
});

function App() {
  const [tab, setTab] = useState(0);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <NavigationTabs value={tab} onChange={(_, v) => setTab(v)} />
          {tab === 0 && <DashboardOverview />}
          {tab === 1 && <DataIngestionForm />}
          {tab === 2 && <ModelPredictions />}
          {tab === 3 && <Analytics />}
          {tab === 4 && <Settings />}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 