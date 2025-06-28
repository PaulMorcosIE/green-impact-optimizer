
# ESG Project Optimizer - Local Setup

## Prerequisites
- Python 3.8-3.11 (avoid Python 3.12+ due to compatibility issues)
- Node.js 18 or higher
- Git

## Quick Start

### 1. Check Python Version
```bash
python --version
# or
python3 --version
```
**Important**: If you have Python 3.12+, you may encounter compatibility issues. Consider using Python 3.11 or earlier.

### 2. Install Python Dependencies

#### Option A: Standard Installation
```bash
pip install -r requirements.txt
```

#### Option B: If you get "distutils" or build errors
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install packages individually (more reliable)
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install pandas==2.1.4
pip install numpy==1.26.2
pip install scikit-learn==1.3.2
pip install scipy==1.11.4
pip install faker==20.1.0
```

#### Option C: Alternative simplified installation
```bash
# Install only essential packages for basic functionality
pip install flask flask-cors pandas numpy faker
```

### 3. Start the Backend Server
```bash
cd src/api
python server.py
```
The backend will be available at http://localhost:5000

You should see output like:
```
🚀 Initializing ESG Pipeline...
✅ Lightweight LLM handler initialized (rule-based parsing)
✅ Rule-based parsing ready (no model loading required)
✅ ESG Pipeline ready!
🌐 Starting Flask API server...
📊 Dataset loaded with 100,000 ESG projects
```

### 4. Start the Frontend (in a new terminal)
```bash
npm install
npm run dev
```
The frontend will be available at http://localhost:5173

## Troubleshooting

### Python Version Issues
- **Problem**: `ModuleNotFoundError: No module named 'distutils'`
- **Solution**: Use Python 3.11 or earlier, or try installing `setuptools` first:
  ```bash
  pip install setuptools
  ```

### Package Installation Issues
- **Problem**: Build errors with numpy/pandas
- **Solution**: Install pre-compiled wheels:
  ```bash
  pip install --only-binary=all numpy pandas scikit-learn
  ```

### Virtual Environment Issues
- **Problem**: Packages not found after installation
- **Solution**: Make sure virtual environment is activated:
  ```bash
  # Windows
  venv\Scripts\activate
  
  # Mac/Linux  
  source venv/bin/activate
  ```

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

## Performance Notes
- Dataset generation: ~10-15 seconds on first run
- Query processing: ~2-5 seconds
- Memory usage: ~200-300MB for dataset
