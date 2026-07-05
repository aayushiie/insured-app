from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal

class UserInput(BaseModel):
    age: int = Field(..., gt=0, lt=120)
    gender: Literal['male', 'female'] = Field(...)
    weight: float = Field(..., gt=0)
    height: float = Field(..., gt=0)
    smokes: Literal['yes', 'no'] = Field(...)
    region: Literal['northeast', 'northwest', 'southeast', 'southwest'] = Field(...)
    charges: float = Field(..., gt=0)
    monthly_premium_est: float = Field(..., gt=0)
    charges_per_child: float = Field(..., gt=0)
    bmi_age_interaction: float = Field(..., gt=0)
    risk_score: float = Field(..., gt=0, lt=9)
    is_high_risk: bool = Field(...)
    num_children: int = Field(...)

    @field_validator('region')
    @classmethod
    def normalize_region(cls, v:str)-> str:
        v = v.strip().lower()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def age_group(self)-> str:
        if self.age in range(18, 26):
            return "Young Adult (18-25)"
        elif self.age in range(26, 36):
            return "Adult (26-35)"
        elif self.age in range(36, 46):
            return "Middle-Aged (36-45)"
        elif self.age in range(46, 56):
            return "Senior-Middle (46-55)"
        elif self.age > 56:
            return "Senior (56+)"
        
    @computed_field
    @property
    def sex(self)-> bool:
        if self.gender == 'female':
            return 1
        else:
            return 0
        
    @computed_field
    @property
    def smoker(self)-> bool:
        if self.smokes == 'no':
            return 0
        else:
            return 1