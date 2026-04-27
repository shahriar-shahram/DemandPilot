# AWS Deployment Plan for DemandPilot

## Goal

Deploy DemandPilot as a client-facing retail demand forecasting dashboard on AWS.

## Recommended First Deployment

Use Docker with AWS App Runner or Elastic Beanstalk.

## Current Architecture

```text
User Browser
    ↓
Streamlit Dashboard
    ↓
Backend Inference Module
    ↓
best_demand_model.joblib
    ↓
Forecast Output
