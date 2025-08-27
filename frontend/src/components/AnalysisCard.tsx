import React from "react";
import { Card, CardContent, Typography, Chip } from "@mui/material";

interface Metric {
  value: number;
  unit: string;
  status: string;
}

interface AnalysisResult {
  metrics: { [key: string]: Metric };
  health_indicators: {
    fatigue_score: number;
    stress_indicator: number;
    overall_status: string;
  };
  recommendations: string[];
  timestamp: string;
}

const AnalysisCard: React.FC<{ analysis: AnalysisResult }> = ({ analysis }) => {
  return (
    <Card sx={{ marginBottom: 2 }}>
      <CardContent>
        <Typography variant="h6">Latest Analysis</Typography>
        <Typography variant="body2" color="text.secondary">
          {new Date(analysis.timestamp).toLocaleString()}
        </Typography>
        {Object.entries(analysis.metrics).map(([key, metric]) => (
          <Typography key={key}>
            {key}: {metric.value} {metric.unit}{" "}
            <Chip
              size="small"
              label={metric.status}
              color={
                metric.status === "critical"
                  ? "error"
                  : metric.status === "warning"
                  ? "warning"
                  : "success"
              }
            />
          </Typography>
        ))}
        <Typography variant="subtitle1" sx={{ mt: 2 }}>
          Overall Status:{" "}
          <Chip
            label={analysis.health_indicators.overall_status}
            color={
              analysis.health_indicators.overall_status === "critical"
                ? "error"
                : analysis.health_indicators.overall_status ===
                  "attention_needed"
                ? "warning"
                : "success"
            }
          />
        </Typography>
        <Typography variant="subtitle2" sx={{ mt: 2 }}>
          Recommendations:
        </Typography>
        <ul>
          {analysis.recommendations.map((rec, i) => (
            <li key={i}>{rec}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
};

export default AnalysisCard;
