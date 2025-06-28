
"""
LLM Handler for ESG Optimization Engine
Handles loading and interfacing with instruction-following LLMs
"""

import json
import re
from typing import Dict, Any, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class LLMHandler:
    """Handles LLM operations for parsing user input and generating explanations"""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium"):
        """
        Initialize LLM handler with specified model
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self.llm = None
        self.tokenizer = None
        
    def load_llm_pipeline(self) -> None:
        """Load the LLM pipeline for text generation"""
        try:
            # Use a lightweight model that works well for instruction following
            self.llm = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",  # Fallback to smaller model
                tokenizer="microsoft/DialoGPT-small",
                device=0 if torch.cuda.is_available() else -1,
                max_length=512,
                do_sample=True,
                temperature=0.3
            )
            print(f"LLM pipeline loaded successfully")
        except Exception as e:
            print(f"Error loading LLM: {e}")
            # Fallback to a simple text generation approach
            self.llm = None
    
    def parse_user_input(self, user_text: str) -> Dict[str, Any]:
        """
        Parse natural language input into structured filters
        
        Args:
            user_text: Natural language query from user
            
        Returns:
            Dictionary of filters to apply to the dataset
        """
        filters = {}
        
        # Define mapping of common terms to column names
        column_mappings = {
            'budget': 'Total_Investment_USD',
            'investment': 'Total_Investment_USD',
            'cost': 'Total_Investment_USD',
            'funding': 'Total_Investment_USD',
            'region': 'Region',
            'country': 'Country',
            'sector': 'Sector',
            'type': 'Project_Type',
            'risk': 'Financial_Risk_Level',
            'esg score': 'Overall_ESG_Score',
            'environmental': 'Environmental_Score',
            'social': 'Social_Score',
            'governance': 'Governance_Score',
            'co2': 'CO2_Reduction_Tonnes_Annual',
            'carbon': 'CO2_Reduction_Tonnes_Annual',
            'energy': 'Energy_Savings_MWh_Annual',
            'jobs': 'Jobs_Created_Total',
            'beneficiaries': 'Beneficiaries_Direct',
            'roi': 'Expected_ROI_Percent',
            'payback': 'Payback_Period_Years',
            'renewable': 'Renewable_Energy_Capacity_MW'
        }
        
        # Extract numerical constraints
        budget_match = re.search(r'under \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)', user_text.lower())
        if budget_match:
            amount = float(budget_match.group(1))
            unit = budget_match.group(2).lower()
            multiplier = {'k': 1000, 'm': 1000000, 'b': 1000000000}.get(unit, 1)
            filters['Total_Investment_USD'] = f"<={amount * multiplier}"
        
        # Extract risk level
        if 'low risk' in user_text.lower() or 'low-risk' in user_text.lower():
            filters['Financial_Risk_Level'] = 'Low'
        elif 'medium risk' in user_text.lower():
            filters['Financial_Risk_Level'] = 'Medium'
        elif 'high risk' in user_text.lower():
            filters['Financial_Risk_Level'] = 'High'
        
        # Extract regions/countries
        regions = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
        for region in regions:
            if region.lower() in user_text.lower():
                filters['Region'] = region
                break
        
        # Extract project types
        project_types = ['renewable energy', 'solar', 'wind', 'water', 'waste', 'education', 'healthcare']
        for ptype in project_types:
            if ptype.lower() in user_text.lower():
                if 'renewable' in ptype or 'solar' in ptype or 'wind' in ptype:
                    filters['Sector'] = 'Energy'
                elif 'water' in ptype:
                    filters['Sector'] = 'Water'
                elif 'waste' in ptype:
                    filters['Sector'] = 'Waste Management'
                elif 'education' in ptype:
                    filters['Sector'] = 'Education'
                elif 'healthcare' in ptype:
                    filters['Sector'] = 'Healthcare'
                break
        
        # Extract impact requirements
        if 'high impact' in user_text.lower():
            filters['Impact_Potential_Score'] = '>=80'
        elif 'medium impact' in user_text.lower():
            filters['Impact_Potential_Score'] = '>=60'
        
        return filters
    
    def explain_selection(self, df_selected, filters: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of project selection
        
        Args:
            df_selected: DataFrame of selected projects
            filters: Applied filters dictionary
            
        Returns:
            Human-readable explanation string
        """
        if df_selected.empty:
            return "No projects were selected based on the given criteria."
        
        num_projects = len(df_selected)
        total_investment = df_selected['Total_Investment_USD'].sum()
        avg_esg_score = df_selected['Overall_ESG_Score'].mean()
        
        # Generate basic explanation
        explanation = f"Selected {num_projects} projects with a total investment of ${total_investment:,.0f}. "
        explanation += f"The average ESG score of selected projects is {avg_esg_score:.1f}. "
        
        # Add filter-specific explanations
        if 'Region' in filters:
            explanation += f"All projects are located in {filters['Region']}. "
        
        if 'Sector' in filters:
            explanation += f"Projects focus on the {filters['Sector']} sector. "
        
        if 'Financial_Risk_Level' in filters:
            explanation += f"Risk level is constrained to {filters['Financial_Risk_Level']}. "
        
        # Add impact summary
        total_co2_reduction = df_selected['CO2_Reduction_Tonnes_Annual'].sum()
        total_jobs = df_selected['Jobs_Created_Total'].sum()
        total_beneficiaries = df_selected['Beneficiaries_Direct'].sum()
        
        explanation += f"Combined impact includes {total_co2_reduction:,.0f} tonnes of CO2 reduction annually, "
        explanation += f"{total_jobs:,.0f} jobs created, and {total_beneficiaries:,.0f} direct beneficiaries."
        
        return explanation
