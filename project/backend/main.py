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

    def calculate_metrics(self):
        growth_rates = [
            (self.yearly_revenue[i] - self.yearly_revenue[i - 1]) / self.yearly_revenue[i - 1] * 100
            for i in range(1, len(self.yearly_revenue))
        ]
        implied_multiples = [
            self.valuation_cap / revenue if revenue != 0 else None
            for revenue in self.yearly_revenue
        ]
        return {
            "growth_rates": growth_rates,
            "implied_multiples": implied_multiples,
        }


# API Routes
@app.post("/evaluate-deal")
def evaluate_deal(data: DealData):
    deal = Deal(**data.dict())
    metrics = deal.calculate_metrics()
    return {"company_name": deal.company_name, "metrics": metrics}


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