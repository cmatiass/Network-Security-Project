# MLOps: Network Security Project: Phishing Detection System 🛡️

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-green)
![MLOps](https://img.shields.io/badge/MLOps-Pipeline-orange)
![AWS](https://img.shields.io/badge/AWS-Cloud-yellow)

## 🚀 Live Demo

Try out the live demo of the project: [Network Security Project Demo](https://network-security-project.onrender.com) 
(Please note that the application may take a few minutes to start up on first access)

![Network Security Demo](https://raw.githubusercontent.com/cmatiass/Network-Security-Project/main/static/img/demo-screenshot.png)


## 📋 Table of Contents
- [Live Demo](#-live-demo)
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Frontend Interface](#frontend-interface)
- [MLOps Pipeline](#mlops-pipeline)
- [API Endpoints](#api-endpoints)
- [Deployment on AWS](#deployment-on-aws)
- [CI/CD Pipeline](#cicd-pipeline)
- [Results and Examples](#results-and-examples)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Project Overview

This Network Security Project is designed to detect phishing websites using machine learning techniques. The primary goal is to create a robust MLOps (Machine Learning Operations) solution with a clear and modular structure that can:

1. Ingest data from MongoDB
2. Validate data against a predefined schema
3. Transform and preprocess the data
4. Train machine learning models
5. Deploy the best model via a FastAPI application
6. Make batch predictions on new data
7. Provide an easy-to-use interface for predictions

The project follows industry best practices for MLOps, ensuring reproducibility, scalability, and maintainability.

## 📁 Project Structure

The project follows a modular architecture with separate components for each step in the ML lifecycle:

```
Network-Security-Project/
├── app.py                     # FastAPI application
├── Dockerfile                 # Docker configuration for containerization
├── main.py                    # Main pipeline execution script
├── push_data.py               # Script to push data to MongoDB
├── requirements.txt           # Project dependencies
├── setup.py                   # Package setup configuration
├── training_status.json       # Training process status tracking
├── test_mongodb.py            # MongoDB connection test script
├── Artifacts/                 # Saved data artifacts by timestamp
│   └── 05_18_2025_21_05_00/  # Example artifact directory
│       ├── data_ingestion/    # Data fetching artifacts
│       ├── data_transformation/ # Preprocessing artifacts
│       ├── data_validation/   # Validation reports
│       └── model_trainer/     # Model artifacts
├── daily_logs/                # Daily operation logs
├── logs/                      # Detailed timestamped log files
├── data_schema/               # Data validation schemas
│   └── schema.yaml            # Schema definition file
├── final_model/               # Production-ready model
│   ├── model.pkl              # Trained model
│   └── preprocessor.pkl       # Data preprocessor
├── Network_Data/              # Raw dataset directory
│   └── phisingData.csv        # Phishing website dataset
├── prediction_output/         # Directory for prediction results
│   └── output.csv             # Example prediction output
├── valid_data/                # Validated data for testing
│   └── test.csv               # Test dataset
├── templates/                 # HTML templates for the web interface
│   ├── index.html             # Landing page
│   ├── prediction.html        # Prediction interface
│   ├── train_model.html       # Model training interface
│   ├── training_complete.html # Training success page
│   └── table.html             # Results display page
├── static/                    # Static assets for the frontend
│   ├── css/                   # CSS stylesheets
│   ├── js/                    # JavaScript files
│   └── img/                   # Images and icons
└── networksecurity/           # Core package
    ├── __init__.py            # Package initialization
    ├── components/            # Pipeline components
    │   ├── __init__.py        # Component initialization
    │   ├── data_ingestion.py  # Data loading from MongoDB
    │   ├── data_validation.py # Schema validation
    │   ├── data_transformation.py # Feature engineering
    │   └── model_trainer.py   # Model training and evaluation
    ├── cloud/                 # Cloud integration (AWS S3)
    │   ├── __init__.py        # Cloud module initialization
    │   └── s3_syncer.py       # AWS S3 synchronization
    ├── constant/              # Project constants and configurations
    ├── entity/                # Data classes and entities
    ├── exception/             # Custom exception handling
    ├── logging/               # Logging configuration
    ├── pipeline/              # ML pipelines
    └── utils/                 # Utility functions
```

## ✨ Features

- 🔄 End-to-end MLOps pipeline
- 📊 Data validation with schema enforcement
- 🧠 Machine learning model training with hyperparameter tuning
- 🚀 FastAPI-based REST API for real-time predictions
- 🎨 Modern, responsive web interface with cybersecurity aesthetics
- 📱 User-friendly UI for model training and predictions
- 📦 Containerization with Docker
- ☁️ AWS deployment ready
- 🔁 CI/CD with GitHub Actions for automated testing and deployment
- 📈 Experiment tracking with MLflow
- 🔒 Security-focused for phishing detection

## 🛠️ Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/cmatiass/Network-Security-Project.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   # Create a .env file with:
   MONGODB_URL_KEY=your_mongodb_connection_string
   ```

4. Install the package in development mode:
   ```
   pip install -e .
   ```

## 🚀 Usage

### Running the Application

1. After installation, start the FastAPI application:
   ```
   python app.py
   ```

2. The application will start on `http://localhost:8000`

3. Open your web browser and navigate to this address

4. You'll see the main dashboard with options to:
   - Learn about the project
   - Train a new model
   - Make predictions on network data

### Training a Model

1. Navigate to the "Train Model" page
2. Click the "Start Training" button
3. The system will display real-time progress of the training pipeline
4. Once complete, you'll see performance metrics and can proceed to making predictions

### Making Predictions

1. Navigate to the "Make Prediction" page
2. Upload your network data in CSV format, or use the provided sample data
3. Click "Analyze Network Data"
4. View the detailed results showing:
   - Classification results (safe or malicious)
   - Confidence scores
   - Feature importance
   - Summary statistics

### Sample Data

The project includes a `test.csv` file in the `valid_data` directory that can be used to test the prediction functionality. This sample data contains various network security features like:

- IP address characteristics
- URL properties
- Domain registration information
- SSL certificate status
- HTTP/HTTPS token information

## 🔄 MLOps Pipeline

The project implements a comprehensive MLOps pipeline:

### 1. Data Ingestion 📥
- Connects to MongoDB to fetch phishing data
- Splits data into training and testing sets
- Stores the split data as artifacts

### 2. Data Validation ✅
- Validates the dataset against a predefined schema (schema.yaml)
- Checks for missing values, data types, and column names
- Generates validation reports

### 3. Data Transformation 🔄
- Preprocesses the data with appropriate scaling and encoding
- Handles categorical features
- Creates preprocessor pipeline artifacts

### 4. Model Training 🧪
- Trains multiple classification algorithms
- Performs hyperparameter tuning
- Evaluates models using appropriate metrics
- Selects the best performing model

### 5. Model Deployment 🚀
- Packages the model with a FastAPI application
- Exposes REST API endpoints for predictions
- Containerizes the application with Docker

## 🌐 API Endpoints

The application provides several API endpoints for both frontend functionality and direct programmatic access:

### Frontend Pages
- `GET /`: Main landing page with project overview
- `GET /train-model`: Model training interface
- `GET /prediction`: Prediction interface for data uploads
- `GET /training-complete`: Training completion confirmation page

### API Functionality
- `POST /train-status`: Initiates model training process
- `POST /finalize-training`: Finalizes and persists the trained model
- `GET /check-model`: Checks if a trained model exists and its status
- `POST /predict`: Makes predictions on uploaded data
- `GET /predict-sample`: Makes predictions using the sample test dataset

### Example API Usage:

**Check if model exists:**
```python
import requests
response = requests.get("http://localhost:8000/check-model")
print(response.json())
# {"trained": true, "status": "completed"}
```

**Upload data for prediction:**
```python
import requests
files = {"file": open("network_data.csv", "rb")}
response = requests.post("http://localhost:8000/predict", files=files)
# Returns HTML with prediction results
```

**Use sample data for prediction:**
```python
import requests
response = requests.get("http://localhost:8000/predict-sample")
# Returns HTML with prediction results using test.csv
```

## ☁️ Deployment on AWS

The project is designed to be deployed on AWS following these steps:

1. **Build Docker Image**:
   ```
   docker build -t network-security-project .
   ```

2. **Push to Amazon ECR**:
   ```
   aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com
   docker tag network-security-project:latest <account-id>.dkr.ecr.<region>.amazonaws.com/network-security-project:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/network-security-project:latest
   ```

3. **Deploy on ECS/Fargate**:
   - Create an ECS cluster
   - Define a task definition using the ECR image
   - Create a service with desired configurations
   - Set up Application Load Balancer for exposing the API

4. **Model Storage**:
   - Models are stored in S3 using the S3 syncer utility
   - This allows for version control of models


## 🔁 CI/CD Pipeline

This project implements Continuous Integration and Continuous Deployment using GitHub Actions:

1. **Automated Testing**:
   - Every push and pull request to the main branch triggers automated tests
   - Unit tests validate individual components
   - Integration tests verify the entire pipeline functionality

2. **Continuous Deployment**:
   - Successful builds on the main branch automatically deploy to AWS
   - The workflow builds the Docker image, pushes it to ECR, and updates the ECS service
   - Environment variables are securely stored as GitHub Secrets


The CI/CD pipeline ensures that the application is always in a deployable state, reducing manual errors and speeding up the development process.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created with ❤️ for secure networks