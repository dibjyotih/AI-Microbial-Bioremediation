# AI-Driven Microbial Bioremediation Model for Plastic Waste Treatment in Urban Water Bodies

## Project Overview
This project develops an AI-driven model to identify plastic types in urban water bodies using spectral data and recommend microbes for bioremediation. It processes spectral datasets (single-sample or multi-sample) to classify plastics as PET, PE, or PP, recommends optimal microbes for degradation, and estimates degradation progress over 30 days. The app features a Flask backend for AI processing and a React frontend for user interaction.

## Key Features
- **Plastic Identification**: Classifies plastics (PET, PE, PP) from spectral data using a pre-trained TensorFlow model with heuristic adjustments.
- **Microbial Recommendation**: Suggests microbes (e.g., *Aspergillus flavus* for PET) based on environmental conditions (pH 7.2, temperature 32°C).
- **Degradation Monitoring**: Estimates degradation progress (e.g., 24.0% for PET in 30 days).
- **Flexible Input**: Supports datasets with varying numbers of spectral bands (e.g., band1 to bandN).
- **User-Friendly Interface**: React frontend with clear instructions for uploading datasets.

## Requirements
### For Developers/Students Studying the Project
- Basic understanding of Python (Flask, TensorFlow, pandas).
- Familiarity with JavaScript/TypeScript and React.
- Knowledge of Git for version control.
- Interest in environmental science, AI, and bioremediation.

### Software Requirements
- Python 3.8+: For the backend.
- Node.js 16+ and npm: For the frontend.
- Git: For cloning the repository.
- Text Editor: VS Code recommended.
- Operating System: Windows, macOS, or Linux.

## Setup and Installation
Follow these steps to run the project on your local machine.

### Step 1: Clone the Repository
```bash
git clone https://github.com/dibjyotih/AI-Microbial-Bioremediation.git
cd AI-Microbial-Bioremediation
```
### Step 2: Set Up the Backend
```bash
cd api
```
### Step 3 Install Python Dependencies
```bash
pip install -r requirements.txt
```
### Step 4 Run the Flask Backend
```bash
python app.py
```
### Step 5: Set Up the Frontend
#### Install Node.js Dependencies:
```bash
npm install
```
### Step 6: Run the React Frontend
```bash
npm run dev
```
## Future Improvements
- Train the TensorFlow model on real spectral data for better accuracy.
- Allow users to input custom environmental conditions (pH, temperature).
- Add support for more plastic types and microbes.
- Improve frontend UI/UX with better visualizations.

## 🛠 Built With

### Backend
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?logo=flask)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0%2B-orange?logo=tensorflow)
![Pandas](https://img.shields.io/badge/Pandas-1.0%2B-blue?logo=pandas&logoColor=white)

### Frontend  
![React](https://img.shields.io/badge/React-18%2B-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-4.0%2B-blue?logo=typescript)
![Node.js](https://img.shields.io/badge/Node.js-16%2B-green?logo=node.js)

### Tools
![Git](https://img.shields.io/badge/Git-2.0%2B-orange?logo=git)
![VS Code](https://img.shields.io/badge/VS_Code-1.0%2B-blue?logo=visual-studio-code)
## Contributors
- Dibjyoti Hota ([GitHub: dibjyotih](https://github.com/dibjyotih))
- Harsh Pandey ([GitHub: rn-harsh04](https://github.com/rn-harsh04))

