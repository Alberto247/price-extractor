import React, { useState } from "react";
import Form from "./components/Form";
import Results from "./components/Results";
import { DataItem, extractData,  } from "./api";

const App: React.FC = () => {
  const [data, setData] = useState<DataItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchData = async (url: string) => {
    setLoading(true);
    setError(null);
    setData(null);
    const response = await extractData(url);
  
    if (response.success) {
      setError(null);
      setData(response.data || []);
    } else {
      setError(response.error || "An unknown error occurred.");
      setData(null);
    }
    setLoading(false);
  };


  return (
    <div style={{ maxWidth: "480px", margin: "0 auto", padding: "1rem", fontFamily: "Arial" }}>
      <h1 style={{ textAlign: "center" }}>Price extractor</h1>
      <Form onSubmit={fetchData} />
      {loading ? (
        <div style={{ textAlign: "center", marginTop: "2rem" }}>
          <div className="spinner"></div>
        </div>
      ) : error ? (
        <div style={{ color: "red", marginTop: "1rem" }}>{error}</div>
      ) : (
        data && <Results items={data} />
      )}
    </div>
  );
};

export default App;
