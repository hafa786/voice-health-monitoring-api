import React, { useEffect, useState } from "react";
import { Container, Typography } from "@mui/material";
import api from "./api/api";
import VoiceUpload from "./components/VoiceUpload";
import AnalysisCard from "./components/AnalysisCard";
import TrendChart from "./components/TrendChart";

const PATIENT_ID = "P001";

function App() {
  const [analysis, setAnalysis] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      const latest = await api.get(`/patients/${PATIENT_ID}/analysis`);
      setAnalysis(latest.data);

      const hist = await api.get(`/patients/${PATIENT_ID}/history`);
      setHistory(hist.data);
    } catch (err) {
      console.error("Failed to fetch data", err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        AddedHealth - Patient Voice Health Dashboard
      </Typography>
      <VoiceUpload patientId={PATIENT_ID} onUploadSuccess={fetchData} />
      {analysis && <AnalysisCard analysis={analysis} />}
      {history.length > 0 && <TrendChart history={history} />}
    </Container>
  );
}

export default App;
