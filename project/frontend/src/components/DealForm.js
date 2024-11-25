import React, { useState, useEffect, useCallback } from "react";
import { evaluateDeal, getIndustryMultiples } from "../api";

const DealForm = () => {
  const [deal, setDeal] = useState({
    company_name: "",
    industry: "",
    ask: "",
    valuation_cap: "",
    security_type: "",
    discount_rate: "",
    interest: "",
    yearly_revenue: "",
    monthly_burn: "",
    current_cash: "",
    previous_raise: "",
  });

  const [industries, setIndustries] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchIndustries = async () => {
      try {
        const data = await getIndustryMultiples();

        console.log("Industry multiples response:", data); // Debugging

        const industryMultiples = data.industry_multiples || {};

        const industryList = Object.keys(industryMultiples).map((key) => ({
          label: key,
        }));

        setIndustries(industryList);
      } catch (err) {
        console.error("Failed to fetch industries:", err);
        setError("Failed to load industry multiples. Please try again later.");
      }
    };

    fetchIndustries();
  }, []);

  const handleChange = useCallback((e) => {
    const { name, value } = e.target;
    setDeal((prev) => ({ ...prev, [name]: value }));
  }, []);

  const handleSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      setError(null);
      setLoading(true);

      try {
        // Parse yearly revenue as an array of numbers
        const yearlyRevenueArray = deal.yearly_revenue
          .split(",")
          .map((val) => val.trim())
          .map(Number);

        if (yearlyRevenueArray.some(isNaN)) {
          throw new Error("Yearly revenue must be comma-separated numbers.");
        }

        // Prepare the payload
        const payload = {
          ...deal,
          ask: parseFloat(deal.ask) || 0,
          valuation_cap: parseFloat(deal.valuation_cap) || 0,
          discount_rate: parseFloat(deal.discount_rate) || 0,
          interest: parseFloat(deal.interest) || 0,
          monthly_burn: parseFloat(deal.monthly_burn) || 0,
          current_cash: parseFloat(deal.current_cash) || 0,
          previous_raise: parseFloat(deal.previous_raise) || 0,
          yearly_revenue: yearlyRevenueArray,
        };

        console.log("Payload being sent:", payload); // Debugging

        const response = await evaluateDeal(payload);

        console.log("API response:", response); // Debugging
        setResult(response);
      } catch (err) {
        const errorMessage =
          err.message || "Failed to evaluate the deal. Please check your inputs.";
        setError(errorMessage);
        console.error("Error during evaluation:", err);
      } finally {
        setLoading(false);
      }
    },
    [deal]
  );

  return (
    <div>
      <h2>Enter Deal Details</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(deal).map((field, index) => {
          if (field === "months_of_cash") return null; // Exclude months_of_cash

          if (field === "industry") {
            return (
              <div key={field}>
                <label>Industry:</label>
                <select
                  name="industry"
                  value={deal.industry}
                  onChange={handleChange}
                  required
                >
                  <option value="" disabled>
                    Select an industry
                  </option>
                  {industries.map(({ label }) => (
                    <option key={label} value={label}>
                      {label}
                    </option>
                  ))}
                </select>
              </div>
            );
          }

          if (field === "security_type") {
            const securityOptions = [
              "Convertible Note",
              "SAFE",
              "Preferred Equity",
              "Common Equity",
            ];

            return (
              <div key={field}>
                <label>Security Type:</label>
                <select
                  name="security_type"
                  value={deal.security_type}
                  onChange={handleChange}
                  required
                >
                  <option value="" disabled>
                    Select a security type
                  </option>
                  {securityOptions.map((option) => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>
            );
          }

          const isPercentage = field === "discount_rate" || field === "interest";
          const isNumberField = [
            "ask",
            "valuation_cap",
            "monthly_burn",
            "current_cash",
            "previous_raise",
          ].includes(field);

          return (
            <div key={field}>
              <label style={{ textTransform: "capitalize" }}>
                {field.replace(/_/g, " ")}:
              </label>
              <input
                type={isPercentage || isNumberField ? "number" : "text"}
                name={field}
                value={deal[field]}
                onChange={handleChange}
                placeholder={
                  field === "yearly_revenue"
                    ? "Comma-separated values (e.g., 5000, 10000)"
                    : ""
                }
                required={
                  field !== "previous_raise" // Optional field
                }
                min={isPercentage ? 0 : undefined}
                max={isPercentage ? 100 : undefined}
                step={isPercentage ? 0.01 : undefined}
                autoFocus={index === 0}
              />
            </div>
          );
        })}
        <button type="submit" disabled={loading}>
          {loading ? "Evaluating..." : "Evaluate Deal"}
        </button>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div>
          <h3>Results</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default DealForm;
