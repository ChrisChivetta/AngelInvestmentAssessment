# Default configuration
default_config = {
    "modeled_discount_rate": 0.20,  # 20%
    "modeled_interest_rate": 0.06,  # 6%
    "modeled_revenue_growth_aggressive": 5.00,  # 500%
    "modeled_revenue_growth_standard": 0.50,  # 50%
    "modeled_revenue_growth_low": 0.10,  # 10%
    "modeled_valuation_threshold": 0.25,  # 25%
    "modeled_cash_months": 12.00
}

# Industry Multiples
industry_multiples = {
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
    "Other": None,
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
}

class Deal:
    def __init__(self, config=None):
        # Original inputs
        self.company_name = ""
        self.industry = ""
        self.ask = 0.0
        self.valuation_cap = 0.0
        self.security_type = ""
        self.discount_rate = 0.0
        self.interest = 0.0
        self.yearly_revenue = []
        self.monthly_burn = 0.0
        self.current_cash = 0.0
        self.previous_raise = 0.0
        self.months_of_cash = 0.0
        
        # Use provided config or default
        self.config = config if config is not None else default_config

        # Calculated metrics
        self.growth_rates = []
        self.growth_rate_assessment = []
        self.implied_multiple = None
        self.assessment_discount_rate = ""
        self.assessment_deal_interest = ""
        self.valuation_assessment = ""
        self.runway_assessment = ""

    def calculate_revenue_growth_rates(self):
        self.growth_rates = []
        for i in range(1, len(self.yearly_revenue)):
            growth_rate = (self.yearly_revenue[i] - self.yearly_revenue[i - 1]) / self.yearly_revenue[i - 1] * 100
            self.growth_rates.append(growth_rate)

    def assess_growth_rate(self):
        self.growth_rate_assessment = []
        for growth_rate in self.growth_rates:
            if growth_rate >= self.config["modeled_revenue_growth_aggressive"] * 100:
                self.growth_rate_assessment.append("Aggressive")
            elif growth_rate >= self.config["modeled_revenue_growth_standard"] * 100:
                self.growth_rate_assessment.append("Standard")
            else:
                self.growth_rate_assessment.append("Low")

    def calculate_metrics(self):
        self.calculate_revenue_growth_rates()
        self.assess_growth_rate()

        # Implied Multiple
        self.implied_multiple = self.valuation_cap / self.yearly_revenue[0] if self.yearly_revenue[0] != 0 else None

        # Discount Rate Assessment
        if self.security_type in ["Convertible Note", "SAFE"]:
            if self.discount_rate == 0:
                self.assessment_discount_rate = "Zero Discount"
            elif self.discount_rate < self.config["modeled_discount_rate"]:
                self.assessment_discount_rate = "Lower Discount"
            elif self.discount_rate == self.config["modeled_discount_rate"]:
                self.assessment_discount_rate = "Standard Discount"
            else:
                self.assessment_discount_rate = "Higher Discount"
        else:
            self.assessment_discount_rate = "Does not apply"

        # Interest Rate Assessment
        if self.security_type == "Convertible Note":
            if self.interest == 0:
                self.assessment_deal_interest = "Zero Interest"
            elif self.interest < self.config["modeled_interest_rate"]:
                self.assessment_deal_interest = "Lower Interest"
            elif self.interest == self.config["modeled_interest_rate"]:
                self.assessment_deal_interest = "Standard Interest"
            else:
                self.assessment_deal_interest = "Higher Interest"
        else:
            self.assessment_deal_interest = "Does not apply"

        # Valuation Assessment
        industry_multiple = industry_multiples.get(self.industry, 3.0)  # Default to 3.0 if industry not found
        if self.implied_multiple is None:
            self.valuation_assessment = "Incomplete"
        elif self.implied_multiple > industry_multiple:
            self.valuation_assessment = "High Valuation"
        elif self.implied_multiple >= (1 - self.config["modeled_valuation_threshold"]) * industry_multiple:
            self.valuation_assessment = "Fair Valuation"
        else:
            self.valuation_assessment = "Favorable Valuation"

        # Runway Assessment
        if self.months_of_cash is None or self.months_of_cash == 0:
            self.runway_assessment = "Unknown"
        elif self.months_of_cash > self.config["modeled_cash_months"]:
            self.runway_assessment = "Adequate"
        else:
            self.runway_assessment = "Inadequate"

    def print_metrics(self):
        print(f"\nMetrics for {self.company_name}:")
        print(f"Industry: {self.industry}")
        print(f"Security Type: {self.security_type}")
        print("Growth Rates and Assessments:")
        for i, (rate, assessment) in enumerate(zip(self.growth_rates, self.growth_rate_assessment), start=1):
            print(f"  Year {i} to {i+1}: {rate:.2f}% - {assessment}")
        print(f"Implied Multiple: {self.implied_multiple:.2f}" if self.implied_multiple is not None else "Implied Multiple: N/A")
        print(f"Months of Cash: {self.months_of_cash:.2f}" if self.months_of_cash is not None else "Months of Cash: N/A")
        print(f"Discount Rate Assessment: {self.assessment_discount_rate}")
        print(f"Interest Rate Assessment: {self.assessment_deal_interest}")
        print(f"Valuation Assessment: {self.valuation_assessment}")
        print(f"Runway Assessment: {self.runway_assessment}")

def evaluate_deal(data, config=None):
    deal = Deal(config)
    for key, value in data.items():
        setattr(deal, key, value)
    deal.calculate_metrics()
    deal.print_metrics()



# Run the test cases with default configuration
for case in test_cases:
    evaluate_deal(case)

# Example of running with a custom configuration
custom_config = {
    "modeled_discount_rate": 0.25,  # 25%
    "modeled_interest_rate": 0.08,  # 8%
    "modeled_revenue_growth_aggressive": 4.00,  # 400%
    "modeled_revenue_growth_standard": 0.75,  # 75%
    "modeled_revenue_growth_low": 0.15,  # 15%
    "modeled_valuation_threshold": 0.30,  # 30%
    "modeled_cash_months": 18.00
}

print("\nRunning with custom configuration:")
for case in test_cases:
    evaluate_deal(case, custom_config)
