# AdTrack Investor Presentation Website

## Overview
This repository contains the AdTrack Investor Presentation Website, a secure platform designed to showcase AdTrack's value proposition, technology, and investment opportunity to potential investors.

AdTrack is the industry's first LLM designed to track ROI, compare performance against local businesses, and optimize advertising budget for maximum returns.

## Key Features
- **Authentication System** with email verification and admin approval
- **Role-based Access Control** for different investor tiers
- **Content Tracking** to monitor which investors view what content
- **Marketing Assets Section** showcasing AdTrack's marketing materials
- **Admin Dashboard** for user management and analytics

## Technology Stack
- Flask framework with Python
- SQLite database (configurable for production databases)
- Bootstrap for responsive design
- Role-based permission system
- Email verification system

## Deployment
This application is configured for deployment on Heroku. Required files:
- `Procfile` - Specifies the command to run the application
- `runtime.txt` - Specifies the Python version
- `requirements.txt` - Lists all Python dependencies

## Getting Started
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run locally: `python src/main.py`
4. Access at http://localhost:5000

## Default Admin Account
- Email: admin@adtrack.online
- Password: adminpassword (change immediately after first login )

## Documentation
- Deployment Guide - Detailed instructions for deploying the website
- User Guide - Comprehensive information about using the website

## About AdTrack
AdTrack is a sophisticated marketing performance analytics platform delivering intelligent, AI-driven solutions for business optimization and ROI enhancement.

For more information, visit [adtrack.online](https://adtrack.online )
