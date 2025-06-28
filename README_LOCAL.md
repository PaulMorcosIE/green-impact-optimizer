
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
✅ Enhanced LLM handler initialized (comprehensive rule-based parsing)
✅ Enhanced rule-based parsing ready (no model loading required)
✅ ESG Pipeline ready!
🌐 Starting Flask API server...
📊 Dataset loaded with 500,000 ESG projects
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
- 500,000 synthetic ESG projects with comprehensive project types
- Enhanced natural language query parsing with hierarchical project matching
- Credit rating integration for financial assessment
- Project filtering and optimization with 82 detailed metrics
- Real-time results with comprehensive impact metrics

## API Endpoints
- GET /api/health - Health check
- POST /api/optimize - Main optimization endpoint
- GET /api/dataset/stats - Dataset statistics
- POST /api/search - Search projects

## Enhanced Query Examples
- "Find low-risk renewable energy projects in Africa under $10M"
- "Solar photovoltaic projects with ROI above 15% and high impact"
- "Wind offshore projects creating 100+ jobs with investment grade rating"
- "Water treatment facilities with moderate risk and AAA credit rating"
- "Electric vehicle infrastructure projects in North America"
- "Green hydrogen projects with innovation scores above 80"

## Performance Notes
- Dataset generation: ~30-45 seconds on first run (500K projects)
- Query processing: ~3-8 seconds depending on complexity
- Memory usage: ~800MB-1.2GB for full dataset
