import React from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

interface HistoryItem {
  timestamp: string;
  metrics: {
    pitch: { value: number };
    speech_rate: { value: number };
    pause_duration: { value: number };
    voice_energy: { value: number };
  };
}

const TrendChart: React.FC<{ history: HistoryItem[] }> = ({ history }) => {
  const data = history.map((h) => ({
    timestamp: new Date(h.timestamp).toLocaleTimeString(),
    pitch: h.metrics.pitch.value,
    speech_rate: h.metrics.speech_rate.value,
    pause_duration: h.metrics.pause_duration.value,
    voice_energy: h.metrics.voice_energy.value,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="timestamp" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="pitch" stroke="#1976d2" />
        <Line type="monotone" dataKey="speech_rate" stroke="#9c27b0" />
        <Line type="monotone" dataKey="pause_duration" stroke="#f57c00" />
        <Line type="monotone" dataKey="voice_energy" stroke="#2e7d32" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TrendChart;
