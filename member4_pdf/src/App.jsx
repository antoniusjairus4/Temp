import React from 'react';
import { Header } from './components/Header';
import { MetricsOverview } from './components/MetricsOverview';
import { DashboardGrid } from './components/DashboardGrid';

function App() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <Header />
      <main className="p-6">
        <MetricsOverview />
        <DashboardGrid />
      </main>
    </div>
  );
}

export default App;