
# ESG Project Optimizer - Local Setup

## Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- Git

## Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
cd src/api
python server.py
```
The backend will be available at http://localhost:5000

### 3. Start the Frontend (in a new terminal)
```bash
npm install
npm run dev
```
The frontend will be available at http://localhost:5173

## Features
- 100,000 synthetic ESG projects
- Natural language query parsing (rule-based, no heavy ML models)
- Project filtering and optimization
- Real-time results with impact metrics

## API Endpoints
- GET /api/health - Health check
- POST /api/optimize - Main optimization endpoint
- GET /api/dataset/stats - Dataset statistics
- POST /api/search - Search projects

## Example Queries
- "Find low-risk renewable energy projects in Africa under $10M"
- "Solar projects with ROI above 15% and high impact"
- "Water management projects creating 100+ jobs"
