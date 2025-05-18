import sys
import os
import json
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.staticfiles import StaticFiles
from uvicorn import run as app_run
from fastapi.responses import Response, RedirectResponse, FileResponse, JSONResponse
from starlette.responses import HTMLResponse
import pandas as pd
import os.path

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.utils.ml_utils.model.estimator import NetworkModel

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create prediction_output directory if it doesn't exist
os.makedirs("prediction_output", exist_ok=True)

# Setup templates
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

# Create a status file for tracking model training
if not os.path.exists("training_status.json"):
    with open("training_status.json", "w") as f:
        json.dump({"status": "not_started"}, f)

@app.get("/", response_class=HTMLResponse, tags=["pages"])
async def index(request: Request):
    """Main landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train-model", response_class=HTMLResponse, tags=["pages"])
async def train_model_page(request: Request):
    """Model training page"""
    return templates.TemplateResponse("train_model.html", {"request": request})

@app.get("/prediction", response_class=HTMLResponse, tags=["pages"])
async def prediction_page(request: Request):
    """Prediction page"""
    return templates.TemplateResponse("prediction.html", {"request": request})

@app.get("/training-complete", response_class=HTMLResponse, tags=["pages"])
async def training_complete_page(request: Request):
    """Training complete page"""
    return templates.TemplateResponse("training_complete.html", {"request": request})

@app.post("/train-status", tags=["api"])
async def train_status():
    """API endpoint to start the training process without waiting for completion"""
    # Start training in background
    try:
        # Set status flag for training (could use a file or db in production)
        with open("training_status.json", "w") as f:
            json.dump({"status": "in_progress"}, f)
        
        # Return immediate response
        return JSONResponse({"status": "training_started"})
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/finalize-training", tags=["api"])
async def finalize_training():
    """API endpoint to finalize the training (asynchronously starts the actual training)"""
    try:
        # Update status flag to in_progress
        with open("training_status.json", "w") as f:
            json.dump({"status": "in_progress"}, f)
        
        # Start training in a separate thread to avoid blocking
        import threading
        
        def run_training():
            try:
                # Start actual training
                train_pipeline = TrainingPipeline()
                train_pipeline.run_pipeline()
                
                # Update status flag when complete
                with open("training_status.json", "w") as f:
                    json.dump({"status": "completed"}, f)
            except Exception as e:
                # Update status flag on error
                with open("training_status.json", "w") as f:
                    json.dump({"status": "failed", "error": str(e)}, f)
                logging.error(f"Training failed: {str(e)}")
        
        # Start the training thread
        training_thread = threading.Thread(target=run_training)
        training_thread.daemon = True
        training_thread.start()
        
        return JSONResponse({"status": "training_started"})
    except Exception as e:
        with open("training_status.json", "w") as f:
            json.dump({"status": "failed", "error": str(e)}, f)
        raise NetworkSecurityException(e, sys)

@app.get("/check-model", tags=["api"])
async def check_model():
    """API endpoint to check if the model is trained"""
    try:
        # Check if model files exist
        model_exists = os.path.exists("final_model/model.pkl")
        preprocessor_exists = os.path.exists("final_model/preprocessor.pkl")
        
        # Check if there's a status file
        status = {"status": "unknown"}
        if os.path.exists("training_status.json"):
            try:
                with open("training_status.json", "r") as f:
                    status = json.load(f)
            except json.JSONDecodeError:
                status = {"status": "error"}
        
        # Determine if model is trained based on both file existence and status
        is_trained = model_exists and preprocessor_exists and status.get("status") == "completed"
        
        # Get current status
        current_status = status.get("status", "unknown")
        
        return JSONResponse({
            "trained": is_trained, 
            "status": current_status,
            "files_exist": model_exists and preprocessor_exists
        })
    except Exception as e:
        logging.error(f"Error checking model: {str(e)}")
        return JSONResponse({"trained": False, "error": str(e)}, status_code=500)
    
    
@app.post("/predict", tags=["api"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    """API endpoint to make predictions on uploaded data"""
    try:
        # Check if model exists and is properly trained
        model_exists = os.path.exists("final_model/model.pkl") and os.path.exists("final_model/preprocessor.pkl")
        
        # Also check the training status file
        status = {"status": "unknown"}
        if os.path.exists("training_status.json"):
            try:
                with open("training_status.json", "r") as f:
                    status = json.load(f)
            except Exception:
                pass
        
        is_trained = model_exists and status.get("status") == "completed"
        
        if not is_trained:
            return JSONResponse(
                {"error": "Model not trained yet. Please train the model first."}, 
                status_code=400
            )
        
        # Log file details for debugging
        logging.info(f"Received file: {file.filename}, content_type: {file.content_type}")
        
        # Validar que el archivo tiene extensión .csv
        if not file.filename.endswith('.csv'):
            return JSONResponse(
                {"error": "Only CSV files are accepted. Please upload a file with .csv extension."},
                status_code=400
            )
            
        # Save the uploaded file temporarily to avoid memory issues with large files
        temp_file_path = "temp_upload.csv"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        try:
            # Load from the saved file with explicit parameters
            df = pd.read_csv(temp_file_path, delimiter=',', on_bad_lines='skip')
            
            # Verify if the dataframe has data
            if df.empty:
                return JSONResponse(
                    {"error": "The uploaded CSV file is empty. Please upload a file with valid data."},
                    status_code=400
                )
                
            # Check if the file contains the required columns
            # Puedes añadir una verificación específica de columnas aquí si es necesario
            
            # Make predictions
            preprocessor = load_object("final_model/preprocessor.pkl")
            final_model = load_object("final_model/model.pkl")
            network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
            
            y_pred = network_model.predict(df)
            df['predicted_column'] = y_pred
            
            # Save results
            os.makedirs('prediction_output', exist_ok=True)
            df.to_csv('prediction_output/output.csv')
              # Count the prediction results for the summary
            # 0 is Malicious Entry, 1 is Safe Entry
            malicious_count = (df['predicted_column'] == 0).sum()
            safe_count = (df['predicted_column'] == 1).sum()
            total_count = len(df)
            
            # Generate HTML table
            table_html = df.to_html(classes='table')
            
            # Return results template with counts
            return templates.TemplateResponse("table.html", {
                "request": request, 
                "table": table_html,
                "safe_count": safe_count,
                "malicious_count": malicious_count,
                "total_count": total_count
            })
            
        except pd.errors.EmptyDataError:
            return JSONResponse(
                {"error": "The uploaded CSV file is empty or improperly formatted. Please check the file content."},
                status_code=400
            )
        except pd.errors.ParserError:
            return JSONResponse(
                {"error": "Unable to parse the CSV file. Please ensure the file has the correct format with proper column headers and data."},
                status_code=400
            )
    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        # Return a more user-friendly error message instead of raising an exception
        return JSONResponse(
            {"error": f"Prediction failed: {str(e)}"},
            status_code=500
        )

@app.get("/predict-sample", tags=["api"])
async def predict_sample(request: Request):
    """API endpoint to make predictions on the sample test.csv file"""
    try:
        # Check if model exists and is properly trained
        model_exists = os.path.exists("final_model/model.pkl") and os.path.exists("final_model/preprocessor.pkl")
        
        # Also check the training status file
        status = {"status": "unknown"}
        if os.path.exists("training_status.json"):
            try:
                with open("training_status.json", "r") as f:
                    status = json.load(f)
            except Exception:
                pass
        
        is_trained = model_exists and status.get("status") == "completed"
        
        if not is_trained:
            return JSONResponse(
                {"error": "Model not trained yet. Please train the model first."}, 
                status_code=400
            )
        
        # Load the sample file
        sample_path = "valid_data/test.csv"
        if not os.path.exists(sample_path):
            return JSONResponse(
                {"error": "Sample data not found."}, 
                status_code=404
            )
        
        df = pd.read_csv(sample_path)
        
        # Make predictions
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        
        # Save results
        os.makedirs('prediction_output', exist_ok=True)
        df.to_csv('prediction_output/output.csv')
          # Count the prediction results for the summary
        # 0 is Malicious Entry, 1 is Safe Entry
        malicious_count = (df['predicted_column'] == 0).sum()
        safe_count = (df['predicted_column'] == 1).sum()
        total_count = len(df)
        
        # Generate HTML table
        table_html = df.to_html(classes='table')
        
        # Return results template with counts
        return templates.TemplateResponse("table.html", {
            "request": request, 
            "table": table_html,
            "safe_count": safe_count,
            "malicious_count": malicious_count,
            "total_count": total_count
        })
    except Exception as e:
        logging.error(f"Error in sample prediction: {str(e)}")
        # Return a more user-friendly error message instead of raising an exception
        return JSONResponse(
            {"error": f"Sample prediction failed: {str(e)}"},
            status_code=500
        )

    
if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8000)
