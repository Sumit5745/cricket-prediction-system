# Cricket Prediction System

A FastAPI-based cricket prediction system with enhanced utilities for data validation, consistency, and performance optimization.

## Features

- Player performance prediction
- Match outcome prediction
- Fantasy team selection
- Data validation and consistency checks
- Performance optimization

## Project Structure

- `src/api`: API endpoints and routers
- `src/core`: Core prediction logic
- `src/ml`: Machine learning models and algorithms
- `src/utils`: Utility functions and helpers
- `data`: Cricket data (players, teams, matches)
- `models`: Trained ML models

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API server: `python run_api_server.py`

## API Endpoints

- `/api/v1/predict/player`: Predict player performance
- `/api/v1/predict/match`: Predict match outcome
- `/api/v1/fantasy/team`: Generate fantasy team
- `/api/v1/teams`: List available teams