from fastapi import FastAPI, File, UploadFile, HTTPException
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.pipeline.prediction_pipeline import PredictionPipeline
from sensor.constant.application import APP_HOST, APP_PORT
import os, sys
import pandas as pd
import uvicorn
from starlette.responses import RedirectResponse
from fastapi.responses import Response

app = FastAPI()

@app.get("/", tags=["authentication"])
async def root():
    """
    Redirects the root URL to the API documentation (Swagger UI).
    """
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    """
    Endpoint to trigger the Training Pipeline.
    Includes a check to prevent multiple simultaneous runs.
    """
    try:
        train_pipeline = TrainPipeline()
        
        # Check if the pipeline is already active
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        # Start the training process in the background
        train_pipeline.run_pipeline()
        
        return Response("Training successful !!")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(SensorException(e, sys)))


@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    """
    Endpoint for future Prediction Pipeline integration.
    You will upload a CSV here and receive predictions.
    """
    try:
        # 1. Read the uploaded CSV into a pandas DataFrame
        df = pd.read_csv(file.file)
        
        # 2. Instantiate the Prediction Pipeline
        pred_pipeline = PredictionPipeline()
        
        # 3. Get predictions (The pipeline handles dropping the target column)
        prediction_df = pred_pipeline.predict(df)
        
        # 4. Convert the first few rows to JSON for the response
        # In a real app, you might return the full CSV as a download
        results = prediction_df.head(10).to_dict(orient="records")
        
        return {"predictions": results}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn
    # Make sure APP_HOST and APP_PORT are defined in your constants
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)