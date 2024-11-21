import requests

# Define the API endpoint
url = "http://127.0.0.1:8000/evaluate-deal"

# Define the payload
payload = {
    "data": {
        "company_name": "Achieve Clinics",
        "industry": "Biotechnology",
        "ask": 500000,
        "valuation_cap": 5000000,
        "security_type": "Convertible Note",
        "discount_rate": 0.20,
        "interest": 0.06,
        "yearly_revenue": [18500, 775000, 6325000],
        "monthly_burn": 1000,
        "current_cash": 74672,
        "months_of_cash": 75,
        "previous_raise": 98668
    },
    "config": {
        "modeled_discount_rate": 0.20,
        "modeled_interest_rate": 0.06,
        "modeled_revenue_growth_aggressive": 5.00,
        "modeled_revenue_growth_standard": 0.50,
        "modeled_revenue_growth_low": 0.10,
        "modeled_valuation_threshold": 0.25,
        "modeled_cash_months": 12.00
    }
}

# Define headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print(f"Error {response.status_code}: {response.text}")
