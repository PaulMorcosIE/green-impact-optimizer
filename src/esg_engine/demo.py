
"""
Demo script showing how to use the ESG Optimization Engine
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pipeline import ESGOptimizationPipeline

def generate_synthetic_esg_data(n_projects: int = 10000) -> pd.DataFrame:
    """
    Generate synthetic ESG dataset with 81 columns for demonstration
    
    Args:
        n_projects: Number of projects to generate
        
    Returns:
        DataFrame with synthetic ESG project data
    """
    np.random.seed(42)
    random.seed(42)
    
    # Define options for categorical columns
    project_types = ['Solar Farm', 'Wind Farm', 'Hydroelectric', 'Energy Efficiency', 'Waste Management', 
                    'Water Treatment', 'Education Initiative', 'Healthcare Program', 'Affordable Housing']
    sectors = ['Energy', 'Water', 'Waste Management', 'Education', 'Healthcare', 'Housing', 'Agriculture']
    regions = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
    countries = ['Kenya', 'India', 'Germany', 'USA', 'Brazil', 'Australia', 'Ghana', 'Vietnam', 
                'France', 'Canada', 'Chile', 'New Zealand']
    statuses = ['Active', 'Completed', 'Planning', 'On Hold']
    risk_levels = ['Low', 'Medium', 'High']
    
    data = []
    
    for i in range(n_projects):
        # Generate project basics
        project_type = random.choice(project_types)
        sector = random.choice(sectors)
        region = random.choice(regions)
        country = random.choice(countries)
        
        # Generate dates
        start_date = datetime.now() - timedelta(days=random.randint(0, 1095))  # Within 3 years
        duration_months = random.randint(6, 60)
        end_date = start_date + timedelta(days=duration_months * 30)
        
        # Generate financial data
        total_investment = random.uniform(100000, 50000000)
        grant_funding = total_investment * random.uniform(0.1, 0.6)
        private_funding = total_investment * random.uniform(0.2, 0.7)
        public_funding = total_investment - grant_funding - private_funding
        public_funding = max(0, public_funding)
        
        # Generate impact metrics based on project type and size
        investment_factor = total_investment / 1000000  # Scale factor
        
        if 'Solar' in project_type or 'Wind' in project_type:
            co2_reduction = random.uniform(100, 5000) * investment_factor
            energy_savings = random.uniform(500, 10000) * investment_factor
            renewable_capacity = random.uniform(1, 100) * investment_factor
        else:
            co2_reduction = random.uniform(10, 1000) * investment_factor
            energy_savings = random.uniform(50, 2000) * investment_factor
            renewable_capacity = 0
        
        # Generate scores (0-100)
        base_score = random.uniform(60, 95)
        environmental_score = base_score + random.uniform(-10, 10)
        social_score = base_score + random.uniform(-10, 10)
        governance_score = base_score + random.uniform(-10, 10)
        overall_esg_score = (environmental_score + social_score + governance_score) / 3
        
        project = {
            'Project_ID': f'ESG_{i+1:05d}',
            'Project_Name': f'{project_type} - {country} {i+1}',
            'Project_Type': project_type,
            'Sector': sector,
            'Region': region,
            'Country': country,
            'Status': random.choice(statuses),
            'Start_Date': start_date.strftime('%Y-%m-%d'),
            'End_Date': end_date.strftime('%Y-%m-%d'),
            'Duration_Months': duration_months,
            
            # Financial metrics
            'Total_Investment_USD': round(total_investment, 2),
            'Grant_Funding_USD': round(grant_funding, 2),
            'Private_Funding_USD': round(private_funding, 2),
            'Public_Funding_USD': round(public_funding, 2),
            'Expected_ROI_Percent': round(random.uniform(3, 25), 2),
            'Payback_Period_Years': round(random.uniform(2, 15), 1),
            'Cost_Per_Beneficiary_USD': round(random.uniform(50, 2000), 2),
            'Revenue_Generated_USD': round(total_investment * random.uniform(0.1, 0.8), 2),
            'Cost_Savings_USD': round(total_investment * random.uniform(0.05, 0.3), 2),
            'Market_Value_Created_USD': round(total_investment * random.uniform(1.1, 3.0), 2),
            'Maintenance_Cost_Annual_USD': round(total_investment * random.uniform(0.02, 0.08), 2),
            
            # Environmental metrics
            'CO2_Reduction_Tonnes_Annual': round(co2_reduction, 2),
            'Energy_Savings_MWh_Annual': round(energy_savings, 2),
            'Water_Savings_m3_Annual': round(random.uniform(1000, 100000) * investment_factor, 2),
            'Waste_Reduction_Tonnes_Annual': round(random.uniform(10, 1000) * investment_factor, 2),
            'Renewable_Energy_Capacity_MW': round(renewable_capacity, 2),
            'Carbon_Intensity_Reduction_Percent': round(random.uniform(10, 80), 2),
            'Environmental_Score': round(max(0, min(100, environmental_score)), 2),
            'Environmental_Risk_Level': random.choice(risk_levels),
            'Biodiversity_Impact_Score': round(random.uniform(40, 90), 2),
            
            # Social metrics
            'Jobs_Created_Total': int(random.uniform(10, 500) * investment_factor),
            'Jobs_Created_Women': int(random.uniform(5, 250) * investment_factor),
            'Jobs_Created_Youth': int(random.uniform(3, 150) * investment_factor),
            'Beneficiaries_Direct': int(random.uniform(100, 10000) * investment_factor),
            'Beneficiaries_Indirect': int(random.uniform(500, 50000) * investment_factor),
            'Community_Investment_USD': round(total_investment * random.uniform(0.02, 0.15), 2),
            'Training_Hours_Provided': int(random.uniform(100, 5000)),
            'Gender_Equality_Score': round(random.uniform(50, 95), 2),
            'Social_Score': round(max(0, min(100, social_score)), 2),
            'Health_Impact_Score': round(random.uniform(40, 90), 2),
            'Education_Impact_Score': round(random.uniform(30, 85), 2),
            'Digital_Inclusion_Score': round(random.uniform(25, 80), 2),
            'Social_Risk_Level': random.choice(risk_levels),
            
            # Governance metrics
            'Board_Diversity_Score': round(random.uniform(40, 90), 2),
            'Transparency_Score': round(random.uniform(50, 95), 2),
            'Stakeholder_Engagement_Score': round(random.uniform(45, 90), 2),
            'Ethics_Compliance_Score': round(random.uniform(60, 98), 2),
            'Data_Privacy_Score': round(random.uniform(55, 95), 2),
            'Governance_Score': round(max(0, min(100, governance_score)), 2),
            'Governance_Risk_Level': random.choice(risk_levels),
            'Financial_Risk_Level': random.choice(risk_levels),
            
            # Additional metrics
            'Certifications': random.choice(['ISO 14001', 'B Corp', 'LEED', 'Fair Trade', 'None']),
            'Reporting_Standards_Followed': random.choice(['GRI', 'SASB', 'TCFD', 'UNGC', 'Multiple']),
            'Regulatory_Compliance_Score': round(random.uniform(70, 98), 2),
            'Primary_SDG': f'SDG {random.randint(1, 17)}',
            'Secondary_SDGs': f'SDG {random.randint(1, 17)}, SDG {random.randint(1, 17)}',
            'Overall_ESG_Score': round(max(0, min(100, overall_esg_score)), 2),
            'Impact_Potential_Score': round(random.uniform(50, 95), 2),
            'Scalability_Score': round(random.uniform(40, 90), 2),
            'Innovation_Score': round(random.uniform(30, 85), 2),
            'Implementation_Progress_Percent': round(random.uniform(20, 100), 2),
            'Budget_Utilization_Percent': round(random.uniform(60, 98), 2),
            'Timeline_Adherence_Score': round(random.uniform(70, 95), 2),
            'Stakeholder_Satisfaction_Score': round(random.uniform(65, 90), 2),
            'Monitoring_Frequency': random.choice(['Monthly', 'Quarterly', 'Semi-Annual', 'Annual']),
            'Third_Party_Verification': random.choice([True, False]),
            'Public_Reporting': random.choice([True, False]),
            'Data_Quality_Score': round(random.uniform(60, 95), 2),
            'Project_Complexity_Score': round(random.uniform(30, 80), 2),
            'Technology_Maturity_Level': random.choice(['Emerging', 'Developing', 'Mature']),
            'Local_Partnership_Score': round(random.uniform(40, 90), 2),
            'Replication_Potential_Score': round(random.uniform(35, 85), 2),
            'Long_Term_Viability_Score': round(random.uniform(50, 90), 2),
            'Climate_Resilience_Score': round(random.uniform(45, 85), 2),
            'Supply_Chain_Sustainability_Score': round(random.uniform(40, 80), 2),
            'Circular_Economy_Score': round(random.uniform(25, 75), 2),
            'Digital_Integration_Score': round(random.uniform(30, 80), 2),
            'Accessibility_Score': round(random.uniform(50, 90), 2),
            'Cultural_Sensitivity_Score': round(random.uniform(55, 90), 2),
            'Knowledge_Transfer_Score': round(random.uniform(40, 85), 2),
            'Emergency_Response_Capability': round(random.uniform(30, 80), 2)
        }
        
        data.append(project)
    
    return pd.DataFrame(data)

def main():
    """Main demo function"""
    print("ESG Optimization Engine Demo")
    print("=" * 50)
    
    # Generate synthetic data
    print("Generating synthetic ESG dataset...")
    df_esg = generate_synthetic_esg_data(1000)  # Smaller dataset for demo
    print(f"Generated {len(df_esg)} projects with {len(df_esg.columns)} columns")
    
    # Initialize pipeline
    print("\nInitializing ESG optimization pipeline...")
    pipeline = ESGOptimizationPipeline(df_esg)
    
    # Demo queries
    demo_queries = [
        "Find low-risk renewable energy projects in Africa under $10M with high impact",
        "Select educational projects in Asia with good governance scores under $5M budget",
        "Find water management projects with high CO2 reduction potential under $15M"
    ]
    
    budgets = [10000000, 5000000, 15000000]
    
    for i, (query, budget) in enumerate(zip(demo_queries, budgets)):
        print(f"\n{'='*60}")
        print(f"DEMO QUERY {i+1}")
        print(f"{'='*60}")
        
        # Run pipeline
        results = pipeline.run_pipeline(query, budget=budget)
        
        if results['success']:
            print(f"✅ Successfully processed query: {query}")
            print(f"📊 Selected {results['selected_count']} projects")
            print(f"💰 Total investment: ${results['project_summary']['total_investment']:,.0f}")
            print(f"🌍 Average ESG score: {results['project_summary']['average_esg_score']:.1f}")
            print(f"📝 Explanation: {results['explanation']}")
        else:
            print(f"❌ Query failed: {results.get('error', 'Unknown error')}")
    
    print(f"\n{'='*60}")
    print("Demo completed!")

if __name__ == "__main__":
    main()
