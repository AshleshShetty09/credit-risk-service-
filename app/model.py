from pydantic import BaseModel, Field

class CreditApplication(BaseModel):
    checking_status: str
    duration: int
    credit_history: str
    purpose: str
    credit_amount: int
    savings_status: str
    employment: str
    installment_rate: int
    personal_status_sex: str
    other_parties: str
    residence_since: int
    property_magnitude: str
    age: int
    other_payment_plans: str
    housing: str
    existing_credits: int
    job: str
    num_dependents: int
    own_telephone: str
    foreign_worker: str

class PredictionResponse(BaseModel):
    risk_probability: float = Field(..., description="Probability of bad credit risk")
    risk_label: str