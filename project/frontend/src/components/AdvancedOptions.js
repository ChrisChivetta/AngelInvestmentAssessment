import React, { useState } from 'react';
import axios from 'axios';

const AdvancedOptions = () => {
    const [config, setConfig] = useState({
        modeled_discount_rate: 0.20,
        modeled_interest_rate: 0.06,
        modeled_revenue_growth_aggressive: 5.00,
        modeled_revenue_growth_standard: 0.50,
        modeled_revenue_growth_low: 0.10,
        modeled_valuation_threshold: 0.25,
        modeled_cash_months: 12.00
    });

    const [industryMultiples, setIndustryMultiples] = useState({
        "Biotechnology": 4.51,
        "Health Sustainability and Wellness": 2.555,
        "Foodtech": 2.765,
        "Medical Devices and Equipment": 3.38,
        "Energy": 3.51,
        "Software": 3.13,
        "Robotics": 2.78,
        "Education": 3.19,
        "Sports": 2.215,
        "Manufacturing": 2.43,
        "Clothing and Apparel": 1.805,
        "Apps": 2.855,
        "Artificial Intelligence": 3.38,
        "Climate Tech": 2.15,
        "Security": 4.02,
        "Restaurant Tech": 2.47,
        "Sustainability": 3.775,
        "Clean Technology": 2.62,
        "Ecommerce": 2.685,
        "Fintech": 3.365,
        "Healthcare Services": 2.495,
        "Business Services": 5.99,
        "Consumer Products": 2.335,
        "Beauty": 2.22,
        "Other": null,
        "Consumer Services": 2.925,
        "Marketing / Advertising": 2.225,
        "Music and Audio": 1.775,
        "Wearables and Quantified Self": 3.635,
        "Internet / Web Services": 2.465,
        "HRtech": 4.61,
        "Construction": 4.86,
        "Food and Beverage": 2.5,
        "Mobility Tech": 2.46,
        "Esports": 1.92,
        "Commerce and Shopping": 2.185,
        "Digital Health": 2.76,
        "Ridesharing": 2.485,
        "Life Sciences": 3.975,
        "Privacy and Security": 4.47
    });

    const handleConfigChange = (e) => {
        const { name, value } = e.target;
        setConfig(prevConfig => ({
            ...prevConfig,
            [name]: parseFloat(value)
        }));
    };

    const handleIndustryMultiplesChange = (e) => {
        const { name, value } = e.target;
        setIndustryMultiples(prevMultiples => ({
            ...prevMultiples,
            [name]: parseFloat(value)
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.put('/update-config', config);
            await axios.put('/update-industry-multiples', industryMultiples);
            alert('Configuration and industry multiples updated successfully');
        } catch (error) {
            console.error('Error updating configuration and industry multiples:', error);
            alert('Failed to update configuration and industry multiples');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Advanced Options</h2>
            <div>
                <label>Modeled Discount Rate:</label>
                <input
                    type="number"
                    name="modeled_discount_rate"
                    value={config.modeled_discount_rate}
                    onChange={handleConfigChange}
                />
            </div>
            <div>
                <label>Modeled Interest Rate:</label>
                <input
                    type="number"
                    name="modeled_interest_rate"
                    value={config.modeled_interest_rate}
                    onChange={handleConfigChange}
                />
            </div>
            <div>
                <label>Modeled Revenue Growth Aggressive:</label>
                <input
                    type="number"
                    name="modeled_revenue_growth_aggressive"
                    value={config.modeled_revenue_growth_aggressive}
                    onChange={handleConfigChange}
                />
            </div>
            <div>
                <label>Modeled Revenue Growth Standard:</label>
                <input
                    type="number"
                    name="modeled_revenue_growth_standard"
                    value={config.modeled_revenue_growth_standard}
                    onChange={handleConfigChange}
                />
            </div>
            <div>
                <label>Modeled Revenue Growth Low:</label>
                <input
                    type="number"
                    name="modeled_revenue_growth_low"
                    value={config.modeled_revenue_growth_low}
                    onChange={handleConfigChange}
                />
            </div>
            <div>
                <label>Modeled Valuation Threshold:</label>
                <input
                    type="number"
                    name="modeled_valuation_threshold"
                    value={config.modeled_valuation_threshold}
                    onChange={handleConfigChange}
                />
            </div>
            <div>
                <label>Modeled Cash Months:</label>
                <input
                    type="number"
                    name="modeled_cash_months"
                    value={config.modeled_cash_months}
                    onChange={handleConfigChange}
                />
            </div>
            <h3>Industry Multiples</h3>
            {Object.keys(industryMultiples).map((industry) => (
                <div key={industry}>
                    <label>{industry}:</label>
                    <input
                        type="number"
                        name={industry}
                        value={industryMultiples[industry]}
                        onChange={handleIndustryMultiplesChange}
                    />
                </div>
            ))}
            <button type="submit">Update</button>
        </form>
    );
};

export default AdvancedOptions;