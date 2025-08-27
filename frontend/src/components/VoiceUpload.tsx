import React, { useState } from "react";
import { Button } from "@mui/material";
import api from "../api/api";

interface Props {
  patientId: string;
  onUploadSuccess: () => void;
}

const VoiceUpload: React.FC<Props> = ({ patientId, onUploadSuccess }) => {
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post(`/patients/${patientId}/voice-samples`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      onUploadSuccess();
    } catch (err) {
      console.error("Upload failed", err);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept=".wav,.mp3,.flac"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <Button variant="contained" color="primary" onClick={handleUpload}>
        Upload Voice Sample
      </Button>
    </div>
  );
};

export default VoiceUpload;
