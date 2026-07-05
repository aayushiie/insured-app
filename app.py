from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import MODEL_VERSION, model, predict_output
from schema.prediction_response import PredictionResponse

app = FastAPI()

# human readable
@app.get('/')
def home():
    return {'message': 'Medical Insurance Category Prediction API'}

# machine readable 
@app.get('/health')
def health_check():                
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict', response_model=PredictionResponse)
def predict_insurance(data: UserInput):
    user_input = {
        'age_group': data.age_group,
        'sex': data.sex,
        'bmi': data.bmi,
        'children': data.num_children,
        'smoker': data.smoker,
        'is_high_risk': data.is_high_risk,
        'risk_score': data.risk_score,
        'region': data.region,
        'charges': data.charges,
        'monthly_premium_est': data.monthly_premium_est,
        'charges_per_child': data.charges_per_child,
        'bmi_age_interaction': data.bmi_age_interaction
    }

    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))