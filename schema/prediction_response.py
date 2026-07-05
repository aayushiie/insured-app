# to fix datatype of model's response
from pydantic import BaseModel, Field
from typing import Dict

class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description='The predicted medical insurance category')
    confidence: float = Field(..., description="Model's confidence score for the predicted class {range: 0 to 1}")
    class_probabilities: Dict = Field(..., description="Probability distribution across all possible classes")