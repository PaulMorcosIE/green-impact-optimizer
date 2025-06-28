
# 🌍 ESG Optimization Web App

A comprehensive end-to-end system for selecting optimal ESG (Environmental, Social, Governance) investment projects using advanced machine learning, natural language processing, and linear optimization. The system processes a synthetic dataset of **100,000 ESG projects** with over **80 sustainability metrics** to provide intelligent project recommendations.

## 🚀 Features

- **Natural Language Processing**: Parse user queries like "Find low-risk renewable energy projects in Africa under $10M with high impact"
- **Advanced Filtering**: Support for 80+ ESG metrics with dynamic filtering capabilities
- **Intelligent Scoring**: Weighted composite scoring based on ESG performance, ROI, impact potential, and risk factors
- **Linear Optimization**: Uses scipy.optimize to select optimal project portfolios under budget constraints
- **AI Explanations**: Generates human-readable explanations for project selections
- **Interactive UI**: Modern React-based interface with real-time results and visualizations
- **Comprehensive Dataset**: 100,000 synthetic ESG projects with realistic impact metrics

---

## 🧪 How to Run This Project - Complete Step-by-Step Guide

### Prerequisites (What You Need Installed)

Before you can run this project, you need to have these programs installed on your computer:

#### 1. Install Node.js and npm
- **Windows/Mac**: Go to [nodejs.org](https://nodejs.org/) and download the LTS version
- **Linux**: Run `sudo apt update && sudo apt install nodejs npm`
- **Verify installation**: Open terminal/command prompt and type:
  ```bash
  node --version
  npm --version
  ```
  You should see version numbers like `v18.17.0` and `9.6.7`

#### 2. Install Python (3.8 or higher)
- **Windows**: Download from [python.org](https://python.org/downloads/) - **IMPORTANT**: Check "Add Python to PATH" during installation
- **Mac**: Install via Homebrew: `brew install python3` or download from python.org
- **Linux**: Run `sudo apt update && sudo apt install python3 python3-pip python3-venv`
- **Verify installation**: Open terminal/command prompt and type:
  ```bash
  python --version
  # or try python3 --version if the above doesn't work
  pip --version
  # or try pip3 --version if the above doesn't work
  ```

#### 3. Install Git (Optional but Recommended)
- Download from [git-scm.com](https://git-scm.com/downloads)
- Follow the installation wizard with default settings

### Step 1: Download the Project

Choose one of these methods:

#### Method A: Using Git (Recommended)
```bash
# Open terminal/command prompt and run:
git clone <your-repo-url>
cd esg-optimization-app
```

#### Method B: Download ZIP
1. Click the green "Code" button on GitHub
2. Click "Download ZIP"
3. Extract the ZIP file to a folder
4. Open terminal/command prompt and navigate to that folder:
   ```bash
   cd path/to/esg-optimization-app
   ```

### Step 2: Set Up the Frontend (React App)

1. **Open Terminal/Command Prompt** in the project folder
2. **Install Dependencies**:
   ```bash
   npm install
   ```
   This will take 2-5 minutes and download all required packages.

3. **Start the Frontend Development Server**:
   ```bash
   npm run dev
   ```
   You should see output like:
   ```
   Local:   http://localhost:5173/
   Network: http://192.168.1.100:5173/
   ```

4. **Keep this terminal window open** - the frontend server needs to keep running

### Step 3: Set Up the Backend (Python API)

1. **Open a NEW terminal/command prompt window** (keep the first one running)
2. **Navigate to the API folder**:
   ```bash
   cd src/api
   ```

3. **Create a Python Virtual Environment** (this keeps packages isolated):
   ```bash
   # On Windows:
   python -m venv venv
   
   # On Mac/Linux:
   python3 -m venv venv
   ```

4. **Activate the Virtual Environment**:
   ```bash
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```
   You should see `(venv)` appear at the beginning of your terminal prompt.

5. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This will take 5-10 minutes as it downloads machine learning libraries.

6. **Start the Python API Server**:
   ```bash
   python server.py
   ```
   You should see output like:
   ```
   🚀 Initializing ESG Pipeline...
   ✅ ESG Pipeline ready!
   🌐 Starting Flask API server...
   📊 Dataset loaded with 100,000 ESG projects
   🔗 API endpoints available:
      - GET  /api/health
      - POST /api/optimize
      - GET  /api/dataset/stats
      - POST /api/search
   * Running on http://0.0.0.0:5000
   ```

7. **Keep this terminal window open** - the backend server needs to keep running

### Step 4: Access the Application

1. **Open your web browser** (Chrome, Firefox, Safari, Edge)
2. **Go to**: `http://localhost:5173`
3. You should see the ESG Optimization Dashboard!

### Step 5: Test the Application

1. **Enter a query** like: "Find renewable energy projects in Africa under $5M with high impact"
2. **Set a budget** (default is $10,000,000)
3. **Click "Find Optimal Projects"**
4. **Wait 10-30 seconds** for the AI to process your request
5. **View results** in the different tabs (Summary, Projects, Filters, Explanation)

### Troubleshooting Common Issues

#### Problem: "npm command not found"
- **Solution**: Node.js wasn't installed correctly. Reinstall Node.js and make sure to restart your terminal.

#### Problem: "python command not found" 
- **Solution**: Try `python3` instead of `python`. On Windows, make sure Python was added to PATH during installation.

#### Problem: "pip install fails with permission errors"
- **Solution**: Make sure you activated the virtual environment (`venv\Scripts\activate` on Windows or `source venv/bin/activate` on Mac/Linux)

#### Problem: Frontend shows "Connection Error"
- **Solution**: Make sure the Python API server is running on port 5000. Check that you see the "✅ ESG Pipeline ready!" message.

#### Problem: "Port 5173 already in use"
- **Solution**: Kill other processes using that port or use a different port:
  ```bash
  npm run dev -- --port 3000
  ```

#### Problem: Python packages fail to install
- **Solution**: Update pip first:
  ```bash
  pip install --upgrade pip
  ```
  Then try installing requirements again.

### Stopping the Application

1. **Stop the Frontend**: Press `Ctrl+C` in the terminal running `npm run dev`
2. **Stop the Backend**: Press `Ctrl+C` in the terminal running `python server.py`
3. **Deactivate Python Environment**: Type `deactivate` in the Python terminal

### Development Workflow

When developing:
1. **Keep both servers running** during development
2. **Frontend changes** are automatically reflected in the browser
3. **Backend changes** require restarting the Python server (Ctrl+C then `python server.py` again)
4. **Always activate the virtual environment** before working with Python:
   ```bash
   cd src/api
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate
   python server.py
   ```

### Available Scripts

```bash
# Frontend (run from project root)
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint

# Backend (run from src/api with venv activated)
python server.py     # Start API server
```

---

## 📂 Project Structure

```
esg-optimization-app/
├── src/
│   ├── esg_engine/                    # Core ESG optimization backend
│   │   ├── __init__.py               # Package initialization
│   │   ├── data_generator.py         # Synthetic ESG dataset generation (100K projects)
│   │   ├── pipeline.py               # Main orchestration pipeline
│   │   ├── llm_handler.py            # LLM integration for NLP parsing & explanations
│   │   ├── project_filter.py         # Dynamic filtering logic for 80+ columns
│   │   ├── project_scorer.py         # Weighted ESG scoring algorithms
│   │   ├── optimizer.py              # Linear optimization using scipy
│   │   └── demo.py                   # Demonstration script with sample queries
│   ├── api/                          # Flask API server
│   │   ├── server.py                 # Main API endpoints
│   │   └── requirements.txt          # Python dependencies
│   ├── components/
│   │   ├── esg/                      # ESG-specific UI components
│   │   │   ├── FilterPanel.tsx       # Dynamic filter interface
│   │   │   ├── WeightingPanel.tsx    # Scoring weight configuration
│   │   │   ├── ProjectResults.tsx    # Project results display
│   │   │   └── OptimizationSummary.tsx # Portfolio summary metrics
│   │   └── ui/                       # Reusable UI components (shadcn/ui)
│   ├── pages/
│   │   ├── ESGDashboard.tsx          # Main dashboard interface
│   │   ├── Index.tsx                 # Landing page
│   │   └── NotFound.tsx              # 404 error page
│   ├── hooks/                        # Custom React hooks
│   ├── lib/                          # Utility functions
│   └── main.tsx                      # React application entry point
├── package.json                      # Node.js dependencies and scripts
└── README.md                         # This file
```

---

## 🧠 Function-by-Function Breakdown

### Core Backend Functions

#### `ESGOptimizationPipeline`
- **Main Class**: Orchestrates the complete ESG optimization workflow
- **Methods**:
  - `run_pipeline(user_text, budget, weights_dict)` — End-to-end pipeline execution
  - `get_dataset_statistics()` — Returns comprehensive dataset statistics
  - `search_projects_by_text(search_text)` — Text-based project search

#### Data Generation
- `generate_synthetic_esg_data(n_rows=100000)` — Creates comprehensive synthetic ESG dataset with 81 columns
- `get_column_info(df)` — Analyzes dataset structure and column types

#### Natural Language Processing
- `parse_user_input(user_text)` — Converts natural language queries into structured filters
- `explain_selection(df_selected, filters)` — Generates human-readable explanations using real data

#### Filtering & Scoring
- `apply_filters(df, filters)` — Applies structured filters with support for operators (>=, <=, ==)
- `score_projects(df, weights)` — Calculates weighted composite scores using normalized metrics
- `rank_projects(df, score_column)` — Ranks projects by composite score

#### Optimization
- `optimize_projects(df, budget, method)` — Uses linear programming to select optimal project portfolios
- `optimize_with_constraints(df, budget, additional_constraints)` — Advanced optimization with custom constraints

### Frontend Components

#### Dashboard Components
- `ESGDashboard` — Main interface with query input, budget configuration, and results display
- `ProjectResults` — Displays selected projects with detailed metrics and visualizations
- `FilterPanel` — Dynamic filter interface for manual project filtering
- `WeightingPanel` — Allows customization of scoring weights
- `OptimizationSummary` — Shows portfolio-level metrics and impact summary

---

## 🤖 Models Used

### Language Models
- **Primary Model**: `microsoft/DialoGPT-small` (HuggingFace)
  - **Purpose**: Natural language parsing and explanation generation
  - **Usage**: Loaded via HuggingFace `pipeline` function with text generation capabilities
  - **Fallback**: Rule-based parsing for robust operation

### Model Loading
```python
from transformers import pipeline

# Load LLM for text generation
llm = pipeline(
    "text-generation",
    model="microsoft/DialoGPT-small",
    device=0 if torch.cuda.is_available() else -1,
    max_length=512,
    temperature=0.3
)
```

### Optimization Algorithms
- **Linear Programming**: `scipy.optimize.linprog` for portfolio optimization
- **Normalization**: `sklearn.preprocessing.MinMaxScaler` for feature scaling
- **Scoring**: Custom weighted composite scoring algorithm

---

## 🔁 Pipeline Overview

The complete ESG optimization pipeline follows these steps:

### 1. **Natural Language Processing**
- User enters query: *"Find low-risk renewable energy projects in Africa under $10M with high impact"*
- LLM parses constraints into structured filters:
  ```json
  {
    "Total_Investment_USD": "<=10000000",
    "Region": "Africa",
    "Project_Type": "Renewable Energy",
    "Financial_Risk_Level": "Low",
    "Impact_Potential_Score": ">=8"
  }
  ```

### 2. **Dataset Filtering**
- Apply parsed filters to 100,000-project dataset
- Support for numeric operators (>=, <=, ==) and categorical matching
- Dynamic column validation and error handling

### 3. **Project Scoring**
- Calculate weighted composite scores using normalized metrics:
  - ESG Score (20%)
  - Impact Potential (15%)
  - CO2 Reduction (12%)
  - Job Creation (10%)
  - Expected ROI (8%)
  - And 6 additional weighted factors

### 4. **Portfolio Optimization**
- Use `scipy.optimize.linprog` for linear programming
- Maximize composite score subject to budget constraints
- Fallback to greedy selection for robustness

### 5. **Results & Explanation**
- Generate comprehensive portfolio summary with real metrics
- AI-powered explanation: *"Selected 12 projects totaling $9.2M investment, creating 2,847 jobs and reducing 15,200 tonnes CO2 annually. Portfolio focuses on renewable energy in Africa with average ESG score of 78.3."*

---

## 📊 Dataset Overview

### Synthetic ESG Dataset Specifications
- **Size**: 100,000 projects
- **Columns**: 81 comprehensive ESG metrics
- **Data Sources**: Faker.js for realistic synthetic data generation

### Key Metrics Categories

#### 📈 **Financial Metrics**
- Total Investment, ROI, Payback Period, Revenue Generated
- Grant/Private/Public funding breakdown
- Cost per beneficiary, Maintenance costs

#### 🌍 **Environmental Impact**
- CO2 Reduction (tonnes/year), Energy Savings (MWh)
- Renewable Energy Capacity (MW), Water Savings (m³)
- Environmental Score, Biodiversity Impact

#### 👥 **Social Impact**
- Jobs Created (Total, Women, Youth)
- Direct/Indirect Beneficiaries
- Gender Equality, Health Impact, Education Impact

#### 🏛️ **Governance Metrics**
- Board Diversity, Transparency Score
- Ethics Compliance, Stakeholder Engagement
- Regulatory Compliance, Data Privacy

#### 🎯 **Performance Indicators**
- Overall ESG Score, Impact Potential Score
- Innovation Score, Scalability Score
- Implementation Progress, Timeline Adherence

---

## 🔧 Configuration

### Default Scoring Weights
```python
default_weights = {
    'Overall_ESG_Score': 0.20,
    'Impact_Potential_Score': 0.15,
    'CO2_Reduction_Tonnes_Annual': 0.12,
    'Jobs_Created_Total': 0.10,
    'Expected_ROI_Percent': 0.08,
    'Beneficiaries_Direct': 0.08,
    'Innovation_Score': 0.06,
    'Scalability_Score': 0.06,
    'Long_Term_Viability_Score': 0.05,
    'Social_Score': 0.05,
    'Governance_Score': 0.05
}
```

### Customization Options
- **Scoring Weights**: Modify weights in `WeightingPanel` component
- **Filter Criteria**: Add custom filters in `FilterPanel`
- **Budget Constraints**: Configure in main dashboard
- **Risk Preferences**: Select risk tolerance levels

---

## 🚀 Deployment

### Production Build
```bash
npm run build
```

### Deployment Options
- **Vercel**: Connect your GitHub repository for automatic deployments
- **Netlify**: Drag and drop the `dist` folder after building
- **GitHub Pages**: Use GitHub Actions for automated deployment

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙋‍♀️ Support

For questions or support, please open an issue in the GitHub repository or contact the development team.

---

## 🔮 Future Enhancements

- **Real-time Data Integration**: Connect to live ESG data sources
- **Advanced ML Models**: Implement transformer-based models for better NLP
- **API Integration**: RESTful API for external system integration
- **Mobile App**: React Native version for mobile access
- **Advanced Visualizations**: Interactive charts and geographic mapping
- **User Authentication**: Multi-user support with saved preferences
- **Export Capabilities**: PDF reports and CSV data export

---

Built with ❤️ using React, TypeScript, and cutting-edge AI technologies.
