from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from typing import List, Optional
from dataclasses import dataclass, field
from io import StringIO
import csv
from fastapi.middleware.cors import CORSMiddleware

from constants import DEFAULT_CONFIG, INDUSTRY_MULTIPLES

# Initialize FastAPI app
app = FastAPI(strict_slashes=False)

# Define Pydantic models for input validation
class DealData(BaseModel):
    company_name: str
    industry: str
    ask: float
    valuation_cap: float
    security_type: str
    discount_rate: float
    interest: float
    yearly_revenue: List[float]
    monthly_burn: Optional[float] = 0.0
    current_cash: Optional[float] = 0.0
    months_of_cash: Optional[float] = 0.0
    previous_raise: Optional[float] = 0.0


class Config(BaseModel):
    modeled_discount_rate: float = 0.20
    modeled_interest_rate: float = 0.06
    modeled_revenue_growth_aggressive: float = 5.00
    modeled_revenue_growth_standard: float = 0.50
    modeled_revenue_growth_low: float = 0.10
    modeled_valuation_threshold: float = 0.25
    modeled_cash_months: float = 12.00


# Define the Deal dataclass
@dataclass
class Deal:
    company_name: str = ""
    industry: str = ""
    ask: float = 0.0
    valuation_cap: float = 0.0
    security_type: str = ""
    discount_rate: float = 0.0
    interest: float = 0.0
    yearly_revenue: List[float] = field(default_factory=list)
    monthly_burn: float = 0.0
    current_cash: float = 0.0
    previous_raise: float = 0.0
    months_of_cash: float = 0.0
    config: dict = field(default_factory=lambda: DEFAULT_CONFIG)

    # Calculated metrics
    growth_rates: List[float] = field(default_factory=list)
    growth_rate_assessment: List[str] = field(default_factory=list)
    implied_multiple: float = None
    assessment_discount_rate: str = ""
    assessment_deal_interest: str = ""
    valuation_assessment: str = ""
    runway_assessment: str = ""

    def calculate_revenue_growth_rates(self):
        self.growth_rates = [
            (self.yearly_revenue[i] - self.yearly_revenue[i - 1]) / self.yearly_revenue[i - 1] * 100
            for i in range(1, len(self.yearly_revenue))
        ]

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
        industry_multiple = INDUSTRY_MULTIPLES.get(self.industry, 3.0)  # Default to 3.0 if industry not found
        if self.implied_multiple is None:
            self.valuation_assessment = "Incomplete"
        elif self.implied_multiple > industry_multiple:
            self.valuation_assessment = "High Valuation"
        elif self.implied_multiple >= (1 - self.config["modeled_valuation_threshold"]) * industry_multiple:
            self.valuation_assessment = "Fair Valuation"
        else:
            self.valuation_assessment = "Favorable Valuation"

        # Runway Assessment
        if self.monthly_burn == 0:
            self.runway_assessment = "Unknown"
        else:
            self.months_of_cash = self.current_cash / self.monthly_burn
            if self.months_of_cash > self.config["modeled_cash_months"]:
                self.runway_assessment = "Adequate"
            else:
                self.runway_assessment = "Inadequate"

        return {
            "growth_rates": self.growth_rates,
            "implied_multiples": self.implied_multiple,
            "discount_rate_assessment": self.assessment_discount_rate,
            "interest_rate_assessment": self.assessment_deal_interest,
            "valuation_assessment": self.valuation_assessment,
            "runway_assessment": self.runway_assessment,
        }

# API Routes
@app.post("/evaluate-deal")
def evaluate_deal(data: DealData):
    deal = Deal(**data.dict())
    metrics = deal.calculate_metrics()
    return metrics


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    csv_file = StringIO(contents.decode("utf-8"))
    reader = csv.DictReader(csv_file)

    results = []
    for row in reader:
        row["yearly_revenue"] = list(map(float, row["yearly_revenue"].split(",")))
        deal = Deal(**row)
        metrics = deal.calculate_metrics()
        results.append({"company_name": row["company_name"], "metrics": metrics})

    return {"results": results}


@app.put("/update-config")
def update_config(config: Config):
    global DEFAULT_CONFIG
    DEFAULT_CONFIG.update(config.dict())
    return {"message": "Configuration updated successfully", "config": DEFAULT_CONFIG}


@app.put("/update-industry-multiples")
def update_industry_multiples(multiples: dict):
    global INDUSTRY_MULTIPLES
    INDUSTRY_MULTIPLES.update(multiples)
    return {"message": "Industry multiples updated successfully", "industry_multiples": INDUSTRY_MULTIPLES}


@app.get("/get-industry-multiples")
def get_industry_multiples():
    return {"industry_multiples": INDUSTRY_MULTIPLES}


@app.get("/get-config")
def get_config():
    return {"config": DEFAULT_CONFIG}


# Middleware for CORS handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)