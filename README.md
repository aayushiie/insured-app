# insured-app

A small FastAPI service that predicts a medical insurance category based on user details like age, BMI, smoker status, region, etc. Comes with a Streamlit frontend for a quick UI. Live demo: https://insured.streamlit.app/

## Tech stack

- **Backend:** FastAPI + Pydantic (schema validation)
- **Model:** scikit-learn model loaded and served via `model/predict.py`
- **Frontend:** Streamlit
- **Data handling:** pandas, numpy
- **Server:** Uvicorn
- **Containerization:** Docker

## API routes

- `GET /` — health-check style welcome message
- `GET /health` — returns API status, model version, and whether the model is loaded
- `POST /predict` — takes user input (age group, sex, bmi, smoker, region, etc.) and returns the predicted insurance category

## Running locally

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Running with Docker

Build the image:

```bash
docker build -t insured-app .
```

Run the container:

```bash
docker run -d -p 8000:8000 --name insured-app insured-app
```

The API will be available at `http://204.236.253.180:8000`.

Useful commands:

```bash
docker ps                     # check running containers
docker logs insured-app       # view logs
docker stop insured-app       # stop the container
docker rm insured-app         # remove the container
```

## Deployment (AWS EC2)

The Dockerized app is deployed on an AWS EC2 instance:

1. SSH into the EC2 instance.
2. Install Docker (if not already installed):
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   ```
3. Pull/copy the repo onto the instance and build the image:
   ```bash
   docker build -t insured-app .
   ```
4. Run the container, mapping port 8000 (make sure the EC2 security group allows inbound traffic on this port):
   ```bash
   docker run -d -p 8000:8000 --name insured-app insured-app
   ```
5. Access the API at `http://<ec2-public-ip>:8000`.

Now, the container runs the same way it does locally, just on the EC2 host.