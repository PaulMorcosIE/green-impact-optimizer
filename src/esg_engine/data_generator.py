
"""
Synthetic ESG Dataset Generator
Creates 100,000 synthetic ESG projects with 81 detailed columns
"""

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta

def generate_synthetic_esg_data(n_rows: int = 100000) -> pd.DataFrame:
    """
    Generate synthetic ESG dataset with 100,000 projects and 81 columns
    
    Args:
        n_rows: Number of projects to generate (default: 100,000)
        
    Returns:
        DataFrame with comprehensive ESG project data
    """
    faker = Faker()
    
    # Static lists for categorical data
    project_types = ["Renewable Energy", "Clean Transportation", "Social Housing", "Water Management", 
                    "Waste Management", "Healthcare Infrastructure", "Education Technology", "Agriculture Technology"]
    sectors = ["Energy", "Healthcare", "Education", "Finance", "Water", "Transportation", "Agriculture", "Technology"]
    regions = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]
    countries = ["Kenya", "India", "Germany", "USA", "Brazil", "Nigeria", "China", "Canada", "Australia", "South Africa"]
    statuses = ["Proposed", "In Development", "Operational", "Completed"]
    risk_levels = ["Low", "Medium", "High"]
    sdgs = [f"SDG {i}" for i in range(1, 18)]
    monitoring_frequencies = ["Monthly", "Quarterly", "Annually"]
    certifications = ["ISO 14001", "LEED", "B-Corp", "FSC", "ENERGY STAR", "None"]
    reporting_standards = ["GRI", "SASB", "TCFD", "CDP", "None"]

    def generate_date_range():
        start_date = faker.date_between(start_date='-5y', end_date='today')
        end_date = start_date + timedelta(days=random.randint(180, 1460))
        duration_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        return start_date, end_date, duration_months

    print(f"Generating {n_rows:,} synthetic ESG projects...")
    
    data = []
    for i in range(n_rows):
        if i % 10000 == 0:
            print(f"Generated {i:,} projects...")
            
        start_date, end_date, duration_months = generate_date_range()
        total_investment = np.random.uniform(1e6, 50e6)
        grant_funding = total_investment * np.random.uniform(0.1, 0.4)
        private_funding = total_investment * np.random.uniform(0.3, 0.6)
        public_funding = max(0, total_investment - grant_funding - private_funding)

        row = {
            "Project_ID": f"P{i:05}",
            "Project_Name": f"{faker.company()} {random.choice(['Solar Farm', 'Wind Project', 'Water System', 'Education Center', 'Healthcare Facility'])}",
            "Project_Type": random.choice(project_types),
            "Sector": random.choice(sectors),
            "Region": random.choice(regions),
            "Country": random.choice(countries),
            "Status": random.choice(statuses),
            "Start_Date": start_date,
            "End_Date": end_date,
            "Duration_Months": duration_months,
            "Total_Investment_USD": round(total_investment, 2),
            "Grant_Funding_USD": round(grant_funding, 2),
            "Private_Funding_USD": round(private_funding, 2),
            "Public_Funding_USD": round(public_funding, 2),
            "Expected_ROI_Percent": round(np.random.uniform(3, 15), 2),
            "Payback_Period_Years": round(np.random.uniform(2, 10), 1),
            "Cost_Per_Beneficiary_USD": round(np.random.uniform(10, 1000), 2),
            "Revenue_Generated_USD": round(np.random.uniform(0, 100e6), 2),
            "Cost_Savings_USD": round(np.random.uniform(0, 50e6), 2),
            "Market_Value_Created_USD": round(np.random.uniform(0, 200e6), 2),
            "Maintenance_Cost_Annual_USD": round(np.random.uniform(50000, 2e6), 2),
            "CO2_Reduction_Tonnes_Annual": round(np.random.uniform(100, 10000), 2),
            "Energy_Savings_MWh_Annual": round(np.random.uniform(50, 5000), 2),
            "Water_Savings_m3_Annual": round(np.random.uniform(1000, 100000), 2),
            "Waste_Reduction_Tonnes_Annual": round(np.random.uniform(10, 1000), 2),
            "Renewable_Energy_Capacity_MW": round(np.random.uniform(1, 500), 2),
            "Carbon_Intensity_Reduction_Percent": round(np.random.uniform(1, 80), 2),
            "Environmental_Score": round(np.random.uniform(0, 100), 2),
            "Environmental_Risk_Level": random.choice(risk_levels),
            "Biodiversity_Impact_Score": round(np.random.uniform(0, 100), 2),
            "Jobs_Created_Total": np.random.randint(10, 5000),
            "Jobs_Created_Women": np.random.randint(5, 2500),
            "Jobs_Created_Youth": np.random.randint(5, 2500),
            "Beneficiaries_Direct": np.random.randint(100, 100000),
            "Beneficiaries_Indirect": np.random.randint(500, 500000),
            "Community_Investment_USD": round(np.random.uniform(1e5, 10e6), 2),
            "Training_Hours_Provided": np.random.randint(100, 10000),
            "Gender_Equality_Score": round(np.random.uniform(0, 100), 2),
            "Social_Score": round(np.random.uniform(0, 100), 2),
            "Health_Impact_Score": round(np.random.uniform(0, 100), 2),
            "Education_Impact_Score": round(np.random.uniform(0, 100), 2),
            "Digital_Inclusion_Score": round(np.random.uniform(0, 100), 2),
            "Social_Risk_Level": random.choice(risk_levels),
            "Board_Diversity_Score": round(np.random.uniform(0, 100), 2),
            "Transparency_Score": round(np.random.uniform(0, 100), 2),
            "Stakeholder_Engagement_Score": round(np.random.uniform(0, 100), 2),
            "Ethics_Compliance_Score": round(np.random.uniform(0, 100), 2),
            "Data_Privacy_Score": round(np.random.uniform(0, 100), 2),
            "Governance_Score": round(np.random.uniform(0, 100), 2),
            "Governance_Risk_Level": random.choice(risk_levels),
            "Financial_Risk_Level": random.choice(risk_levels),
            "Certifications": random.choice(certifications),
            "Reporting_Standards_Followed": random.choice(reporting_standards),
            "Regulatory_Compliance_Score": round(np.random.uniform(0, 100), 2),
            "Primary_SDG": random.choice(sdgs),
            "Secondary_SDGs": ", ".join(random.sample(sdgs, k=random.randint(1, 3))),
            "Overall_ESG_Score": round(np.random.uniform(0, 100), 2),
            "Impact_Potential_Score": round(np.random.uniform(1, 10), 2),
            "Scalability_Score": round(np.random.uniform(0, 100), 2),
            "Innovation_Score": round(np.random.uniform(0, 100), 2),
            "Implementation_Progress_Percent": round(np.random.uniform(0, 100), 2),
            "Budget_Utilization_Percent": round(np.random.uniform(0, 100), 2),
            "Timeline_Adherence_Score": round(np.random.uniform(0, 100), 2),
            "Stakeholder_Satisfaction_Score": round(np.random.uniform(0, 100), 2),
            "Monitoring_Frequency": random.choice(monitoring_frequencies),
            "Third_Party_Verification": random.choice(["Yes", "No"]),
            "Public_Reporting": random.choice(["Yes", "No"]),
            "Data_Quality_Score": round(np.random.uniform(0, 100), 2),
            "Project_Complexity_Score": round(np.random.uniform(0, 100), 2),
            "Technology_Maturity_Level": round(np.random.uniform(0, 100), 2),
            "Local_Partnership_Score": round(np.random.uniform(0, 100), 2),
            "Replication_Potential_Score": round(np.random.uniform(0, 100), 2),
            "Long_Term_Viability_Score": round(np.random.uniform(0, 100), 2),
            "Climate_Resilience_Score": round(np.random.uniform(0, 100), 2),
            "Supply_Chain_Sustainability_Score": round(np.random.uniform(0, 100), 2),
            "Circular_Economy_Score": round(np.random.uniform(0, 100), 2),
            "Digital_Integration_Score": round(np.random.uniform(0, 100), 2),
            "Accessibility_Score": round(np.random.uniform(0, 100), 2),
            "Cultural_Sensitivity_Score": round(np.random.uniform(0, 100), 2),
            "Knowledge_Transfer_Score": round(np.random.uniform(0, 100), 2),
            "Emergency_Response_Capability": round(np.random.uniform(0, 100), 2),
        }
        data.append(row)

    # Create DataFrame
    df_esg = pd.DataFrame(data)
    print(f"✅ Generated {len(df_esg):,} ESG projects with {len(df_esg.columns)} columns")
    
    return df_esg

def get_column_info(df: pd.DataFrame) -> dict:
    """
    Get detailed information about dataset columns for filtering and scoring
    
    Args:
        df: ESG DataFrame
        
    Returns:
        Dictionary with column information
    """
    column_info = {
        'categorical_columns': [],
        'numerical_columns': [],
        'date_columns': [],
        'boolean_columns': [],
        'total_columns': len(df.columns)
    }
    
    for col in df.columns:
        dtype = str(df[col].dtype)
        if dtype in ['object', 'category']:
            # Check if it's actually boolean stored as string
            unique_vals = df[col].unique()
            if set(unique_vals).issubset({'Yes', 'No', 'True', 'False'}):
                column_info['boolean_columns'].append(col)
            else:
                column_info['categorical_columns'].append(col)
        elif 'datetime' in dtype:
            column_info['date_columns'].append(col)
        else:
            column_info['numerical_columns'].append(col)
    
    return column_info
