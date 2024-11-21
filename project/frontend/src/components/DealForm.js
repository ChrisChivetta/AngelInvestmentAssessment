import React, { useState } from "react";
import { evaluateDeal } from "../api";

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
    months_of_cash: "",
    previous_raise: "",
  });

  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDeal((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      const payload = {
        ...deal,
        yearly_revenue: deal.yearly_revenue.split(",").map(Number),
      };

      const response = await evaluateDeal(payload);
      setResult(response.data);
    } catch (err) {
      setError("Failed to evaluate the deal. Please check your inputs.");
      console.error(err);
    }
  };

  return (
    <div>
      <h2>Enter Deal Details</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(deal).map((field) => (
          <div key={field}>
            <label style={{ textTransform: "capitalize" }}>{field.replace(/_/g, " ")}:</label>
            <input
              type={field === "yearly_revenue" ? "text" : "number"}
              name={field}
              value={deal[field]}
              onChange={handleChange}
              placeholder={
                field === "yearly_revenue"
                  ? "Comma-separated values (e.g., 5000, 10000)"
                  : ""
              }
              required={field !== "previous_raise" && field !== "months_of_cash"}
            />
          </div>
        ))}
        <button type="submit">Evaluate Deal</button>
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
