# Network Security Project: Phishing Detection System 🛡️

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-green)
![MLOps](https://img.shields.io/badge/MLOps-Pipeline-orange)
![AWS](https://img.shields.io/badge/AWS-Cloud-yellow)

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
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
├── data_schema/               # Data validation schemas
├── final_model/               # Saved model artifacts
├── Network_Data/              # Raw dataset directory
├── prediction_output/         # Directory for prediction results
├── templates/                 # HTML templates for the web interface
└── networksecurity/          # Core package
    ├── components/            # Pipeline components
    │   ├── data_ingestion.py  # Data loading from MongoDB
    │   ├── data_validation.py # Schema validation
    │   ├── data_transformation.py # Feature engineering
    │   └── model_trainer.py   # Model training and evaluation
    ├── cloud/                 # Cloud integration (AWS S3)
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

### Running the Training Pipeline

To train the model with the complete pipeline:

```python
python main.py
```

This will execute:
- Data ingestion from MongoDB
- Data validation against schema
- Data transformation and preprocessing
- Model training and evaluation
- Model saving

### Making Predictions

To run the FastAPI application for predictions:

```python
uvicorn app:app --reload
```

Visit `http://localhost:8000/docs` to access the Swagger UI for API documentation.

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

The application provides the following endpoints:

- `GET /`: Redirects to API documentation
- `GET /train`: Triggers the training pipeline
- `POST /predict`: Accepts CSV files for batch prediction

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