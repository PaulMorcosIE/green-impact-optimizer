
"""
Synthetic ESG Dataset Generator
Creates 500,000 synthetic ESG projects with 82 detailed columns including credit ratings
"""

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta

def generate_synthetic_esg_data(n_rows: int = 500000) -> pd.DataFrame:
    """
    Generate synthetic ESG dataset with 500,000 projects and 82 columns
    
    Args:
        n_rows: Number of projects to generate (default: 500,000)
        
    Returns:
        DataFrame with comprehensive ESG project data
    """
    faker = Faker()
    
    # Comprehensive project types with subcategories
    project_types = [
        # Renewable Energy (expanded)
        "Solar Photovoltaic", "Solar Thermal", "Wind Onshore", "Wind Offshore", 
        "Hydroelectric", "Geothermal", "Biomass Energy", "Ocean Wave Energy",
        "Tidal Energy", "Green Hydrogen", "Energy Storage", "Smart Grid",
        
        # Clean Transportation (expanded)
        "Electric Vehicle Infrastructure", "Public Transit Systems", "Electric Buses",
        "Rail Electrification", "Cycling Infrastructure", "Walking Paths",
        "Electric Maritime", "Sustainable Aviation", "Cargo Optimization",
        
        # Water & Sanitation (expanded)
        "Water Treatment Plants", "Desalination Systems", "Rainwater Harvesting",
        "Wastewater Management", "Smart Water Networks", "Irrigation Systems",
        "Water Conservation", "Flood Management", "Groundwater Protection",
        
        # Waste Management (expanded)
        "Recycling Facilities", "Waste-to-Energy", "Composting Systems",
        "Plastic Recycling", "E-Waste Processing", "Circular Economy Hubs",
        "Zero Waste Programs", "Industrial Symbiosis",
        
        # Social Infrastructure (expanded)
        "Affordable Housing", "Social Housing", "Community Centers",
        "Healthcare Facilities", "Hospitals", "Clinics", "Telemedicine",
        "Medical Equipment", "Health Education Programs",
        
        # Education (expanded)
        "Schools", "Universities", "Vocational Training", "Digital Literacy",
        "STEM Education", "Adult Education", "Educational Technology",
        "Libraries", "Research Facilities",
        
        # Agriculture & Food (expanded)
        "Sustainable Farming", "Vertical Farming", "Precision Agriculture",
        "Organic Farming", "Aquaculture", "Food Processing", "Cold Storage",
        "Agricultural Technology", "Livestock Management",
        
        # Technology & Innovation
        "Fintech Solutions", "Digital Inclusion", "Blockchain for Good",
        "AI for Sustainability", "IoT Environmental Monitoring",
        "Clean Technology R&D", "Innovation Hubs"
    ]
    
    # Enhanced project name patterns
    company_prefixes = [
        "Green", "Eco", "Sustainable", "Clean", "Renewable", "Smart", "Future",
        "Global", "Advanced", "Innovative", "Premier", "Elite", "NextGen"
    ]
    
    company_suffixes = [
        "Solutions", "Technologies", "Systems", "Energy", "Partners", "Group",
        "Corporation", "Industries", "Ventures", "Holdings", "Enterprises"
    ]
    
    project_descriptors = [
        "Project", "Initiative", "Program", "Facility", "Center", "Hub",
        "Complex", "Development", "Infrastructure", "Network", "System"
    ]
    
    # Credit rating system
    credit_ratings = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-"]
    credit_rating_weights = [2, 3, 5, 7, 10, 12, 15, 18, 20, 15, 8, 6, 4, 3, 2, 1]  # Higher ratings more common for ESG projects
    
    sectors = ["Energy", "Healthcare", "Education", "Finance", "Water", "Transportation", "Agriculture", "Technology", "Manufacturing", "Construction"]
    regions = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]
    countries = ["Kenya", "India", "Germany", "USA", "Brazil", "Nigeria", "China", "Canada", "Australia", "South Africa", "Japan", "UK", "France", "Mexico", "Indonesia"]
    statuses = ["Proposed", "In Development", "Operational", "Completed"]
    risk_levels = ["Low", "Medium", "High"]
    sdgs = [f"SDG {i}" for i in range(1, 18)]
    monitoring_frequencies = ["Monthly", "Quarterly", "Annually"]
    certifications = ["ISO 14001", "LEED", "B-Corp", "FSC", "ENERGY STAR", "None"]
    reporting_standards = ["GRI", "SASB", "TCFD", "CDP", "None"]

    def generate_project_name(project_type):
        """Generate more realistic project names based on type"""
        if random.random() < 0.3:  # 30% use company + descriptor pattern
            company = f"{random.choice(company_prefixes)} {random.choice(company_suffixes)}"
            descriptor = random.choice(project_descriptors)
            return f"{company} {descriptor}"
        else:  # 70% use location + type pattern
            location = faker.city()
            if "Solar" in project_type:
                variants = ["Solar Farm", "Solar Park", "Photovoltaic Plant", "Solar Installation"]
                return f"{location} {random.choice(variants)}"
            elif "Wind" in project_type:
                variants = ["Wind Farm", "Wind Park", "Wind Energy Project", "Wind Installation"]
                return f"{location} {random.choice(variants)}"
            elif "Water" in project_type or "Waste" in project_type:
                return f"{location} {project_type} Facility"
            elif "Housing" in project_type or "Social" in project_type:
                return f"{location} {project_type} Development"
            elif "Healthcare" in project_type or "Hospital" in project_type or "Clinic" in project_type:
                return f"{location} {project_type}"
            elif "School" in project_type or "Education" in project_type:
                return f"{location} {project_type} Center"
            else:
                return f"{location} {project_type} {random.choice(project_descriptors)}"

    def generate_date_range():
        start_date = faker.date_between(start_date='-5y', end_date='today')
        end_date = start_date + timedelta(days=random.randint(180, 1460))
        duration_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        return start_date, end_date, duration_months

    print(f"Generating {n_rows:,} synthetic ESG projects...")
    
    data = []
    for i in range(n_rows):
        if i % 50000 == 0:
            print(f"Generated {i:,} projects...")
            
        project_type = random.choice(project_types)
        start_date, end_date, duration_months = generate_date_range()
        total_investment = np.random.uniform(1e6, 100e6)
        grant_funding = total_investment * np.random.uniform(0.1, 0.4)
        private_funding = total_investment * np.random.uniform(0.3, 0.6)
        public_funding = max(0, total_investment - grant_funding - private_funding)
        
        # Generate credit rating with higher ratings more likely for ESG projects
        credit_rating = np.random.choice(credit_ratings, p=[w/sum(credit_rating_weights) for w in credit_rating_weights])

        row = {
            "Project_ID": f"P{i:06}",
            "Project_Name": generate_project_name(project_type),
            "Project_Type": project_type,
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
            "Expected_ROI_Percent": round(np.random.uniform(3, 18), 2),
            "Credit_Rating": credit_rating,
            "Payback_Period_Years": round(np.random.uniform(2, 10), 1),
            "Cost_Per_Beneficiary_USD": round(np.random.uniform(10, 1000), 2),
            "Revenue_Generated_USD": round(np.random.uniform(0, 150e6), 2),
            "Cost_Savings_USD": round(np.random.uniform(0, 75e6), 2),
            "Market_Value_Created_USD": round(np.random.uniform(0, 300e6), 2),
            "Maintenance_Cost_Annual_USD": round(np.random.uniform(50000, 3e6), 2),
            "CO2_Reduction_Tonnes_Annual": round(np.random.uniform(100, 15000), 2),
            "Energy_Savings_MWh_Annual": round(np.random.uniform(50, 8000), 2),
            "Water_Savings_m3_Annual": round(np.random.uniform(1000, 150000), 2),
            "Waste_Reduction_Tonnes_Annual": round(np.random.uniform(10, 1500), 2),
            "Renewable_Energy_Capacity_MW": round(np.random.uniform(1, 1000), 2),
            "Carbon_Intensity_Reduction_Percent": round(np.random.uniform(1, 90), 2),
            "Environmental_Score": round(np.random.uniform(0, 100), 2),
            "Environmental_Risk_Level": random.choice(risk_levels),
            "Biodiversity_Impact_Score": round(np.random.uniform(0, 100), 2),
            "Jobs_Created_Total": np.random.randint(10, 8000),
            "Jobs_Created_Women": np.random.randint(5, 4000),
            "Jobs_Created_Youth": np.random.randint(5, 4000),
            "Beneficiaries_Direct": np.random.randint(100, 200000),
            "Beneficiaries_Indirect": np.random.randint(500, 1000000),
            "Community_Investment_USD": round(np.random.uniform(1e5, 15e6), 2),
            "Training_Hours_Provided": np.random.randint(100, 15000),
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
    Get comprehensive information about DataFrame columns
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with column type information
    """
    numerical_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    boolean_columns = df.select_dtypes(include=['bool']).columns.tolist()
    datetime_columns = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    return {
        'total_columns': len(df.columns),
        'numerical_columns': numerical_columns,
        'categorical_columns': categorical_columns,
        'boolean_columns': boolean_columns,
        'datetime_columns': datetime_columns,
        'all_columns': df.columns.tolist()
    }
