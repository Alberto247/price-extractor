import React, { useState } from "react";

interface FormProps {
  onSubmit: (url: string) => void;
}

const Form: React.FC<FormProps> = ({ onSubmit }) => {
  const [url, setUrl] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(url.trim());
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
      <input
        type="url"
        placeholder="Enter URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          padding: "0.75rem",
          fontSize: "1rem",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
        required
      />
      <button
        type="submit"
        style={{
          padding: "0.75rem",
          fontSize: "1rem",
          borderRadius: "8px",
          backgroundColor: "#007BFF",
          color: "white",
          border: "none",
        }}
      >
        Extract
      </button>
    </form>
  );
};

export default Form;
