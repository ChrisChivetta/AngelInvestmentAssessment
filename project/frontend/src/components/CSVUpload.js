import React, { useState } from "react";
import axios from "axios";

const CSVUpload = () => {
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/upload-csv", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(response.data.results);
    } catch (err) {
      setError("Failed to process the CSV file.");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Upload CSV</h2>
      <input type="file" accept=".csv" onChange={handleFileUpload} />
      {error && <p style={{ color: "red" }}>{error}</p>}
      {results.length > 0 && (
        <div>
          <h3>Results</h3>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default CSVUpload;
