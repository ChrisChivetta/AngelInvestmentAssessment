import React, { useState, useEffect } from "react";
import { getConfig, getIndustryMultiples } from "../api";

const AdvancedOptions = () => {
  const [isVisible, setIsVisible] = useState(false); // Visibility toggle
  const [config, setConfig] = useState(null); // Store model configurations
  const [multiples, setMultiples] = useState(null); // Store industry multiples
  const [error, setError] = useState(null); // Error state

  // Fetch configurations and multiples on mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const fetchedConfig = await getConfig(); // Fetch the config data
        const fetchedMultiples = await getIndustryMultiples(); // Fetch the industry multiples data

        setConfig(fetchedConfig.config); // Update state with fetched config
        setMultiples(fetchedMultiples.industry_multiples); // Update state with fetched multiples
      } catch (err) {
        console.error("Failed to fetch data:", err);
        setError("Could not load advanced options.");
      }
    };

    fetchData(); // Fetch data when the component mounts
  }, []); // Empty dependency array ensures this runs only once after the component mounts

  // Toggle visibility of the advanced options section
  const toggleVisibility = () => setIsVisible((prev) => !prev);

  // Handle changes to model configuration fields
  const handleConfigChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({ ...prev, [name]: parseFloat(value) || 0 }));
  };

  // Handle changes to industry multiples fields
  const handleMultiplesChange = (e) => {
    const { name, value } = e.target;
    setMultiples((prev) => ({ ...prev, [name]: parseFloat(value) || 0 }));
  };

  return (
    <div>
      <button onClick={toggleVisibility}>
        {isVisible ? "Hide Advanced Options" : "Show Advanced Options"}
      </button>

      {isVisible && (
        <div>
          <h2>Advanced Options</h2>
          {error && <p style={{ color: "red" }}>{error}</p>}

          {/* Model Configuration Section */}
          <div>
            <h3>Model Configuration</h3>
            {config ? (
              Object.keys(config).map((field) => (
                <div key={field}>
                  <label>{field.replace(/_/g, " ")}:</label>
                  <input
                    type="number"
                    name={field}
                    value={config[field] || 0}
                    onChange={handleConfigChange}
                  />
                </div>
              ))
            ) : (
              <p>Loading model configuration...</p>
            )}
          </div>

          {/* Industry Multiples Section */}
          <div>
            <h3>Industry Multiples</h3>
            {multiples ? (
              Object.keys(multiples).map((field) => (
                <div key={field}>
                  <label>{field}:</label>
                  <input
                    type="number"
                    name={field}
                    value={multiples[field] || 0}
                    onChange={handleMultiplesChange}
                  />
                </div>
              ))
            ) : (
              <p>Loading industry multiples...</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedOptions;