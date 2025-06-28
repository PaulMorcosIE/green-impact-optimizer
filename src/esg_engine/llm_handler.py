
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
            print(f"✅ LLM pipeline loaded successfully")
        except Exception as e:
            print(f"⚠️ Error loading LLM: {e}")
            # Fallback to a simple text generation approach
            self.llm = None
    
    def parse_user_input(self, user_text: str) -> Dict[str, Any]:
        """
        Parse natural language input into structured filters for the comprehensive ESG dataset
        
        Args:
            user_text: Natural language query from user
            
        Returns:
            Dictionary of filters to apply to the dataset
        """
        filters = {}
        user_lower = user_text.lower()
        
        # Enhanced column mappings for the comprehensive dataset
        column_mappings = {
            'budget': 'Total_Investment_USD',
            'investment': 'Total_Investment_USD',
            'cost': 'Total_Investment_USD',
            'funding': 'Total_Investment_USD',
            'region': 'Region',
            'country': 'Country',
            'sector': 'Sector',
            'type': 'Project_Type',
            'status': 'Status',
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
            'renewable': 'Renewable_Energy_Capacity_MW',
            'innovation': 'Innovation_Score',
            'impact': 'Impact_Potential_Score',
            'scalability': 'Scalability_Score'
        }
        
        # Extract numerical constraints with enhanced patterns
        # Budget constraints
        budget_patterns = [
            r'under \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'below \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'less than \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'maximum \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)'
        ]
        
        for pattern in budget_patterns:
            budget_match = re.search(pattern, user_lower)
            if budget_match:
                amount = float(budget_match.group(1))
                unit = budget_match.group(2).lower() if budget_match.group(2) else ''
                multiplier = {'k': 1000, 'm': 1000000, 'b': 1000000000}.get(unit, 1)
                filters['Total_Investment_USD'] = f"<={amount * multiplier}"
                break
        
        # ROI constraints
        roi_patterns = [
            r'roi above ([0-9]+(?:\.[0-9]+)?)%?',
            r'roi over ([0-9]+(?:\.[0-9]+)?)%?',
            r'roi greater than ([0-9]+(?:\.[0-9]+)?)%?',
            r'return above ([0-9]+(?:\.[0-9]+)?)%?'
        ]
        
        for pattern in roi_patterns:
            roi_match = re.search(pattern, user_lower)
            if roi_match:
                roi_value = float(roi_match.group(1))
                filters['Expected_ROI_Percent'] = f">={roi_value}"
                break
        
        # Jobs created constraints
        jobs_patterns = [
            r'more than ([0-9]+) jobs',
            r'over ([0-9]+) jobs',
            r'([0-9]+)\+ jobs',
            r'created ([0-9]+) jobs'
        ]
        
        for pattern in jobs_patterns:
            jobs_match = re.search(pattern, user_lower)
            if jobs_match:
                jobs_value = int(jobs_match.group(1))
                filters['Jobs_Created_Total'] = f">={jobs_value}"
                break
        
        # Extract risk level preferences
        risk_preferences = {
            'low risk': 'Low',
            'low-risk': 'Low',
            'medium risk': 'Medium',
            'high risk': 'High',
            'minimal risk': 'Low',
            'safe': 'Low'
        }
        
        for risk_phrase, risk_level in risk_preferences.items():
            if risk_phrase in user_lower:
                filters['Financial_Risk_Level'] = risk_level
                break
        
        # Extract regions and countries
        regions = ['africa', 'asia', 'europe', 'north america', 'south america', 'oceania']
        countries = ['kenya', 'india', 'germany', 'usa', 'brazil', 'nigeria', 'china', 'canada', 'australia', 'south africa']
        
        for region in regions:
            if region in user_lower:
                filters['Region'] = region.title()
                break
        
        for country in countries:
            if country in user_lower:
                if country == 'usa':
                    filters['Country'] = 'USA'
                else:
                    filters['Country'] = country.title()
                break
        
        # Extract project types and sectors
        project_type_mappings = {
            'renewable energy': 'Renewable Energy',
            'solar': 'Renewable Energy',
            'wind': 'Renewable Energy',
            'clean transportation': 'Clean Transportation',
            'water': 'Water Management',
            'water management': 'Water Management',
            'social housing': 'Social Housing',
            'healthcare': 'Healthcare Infrastructure',
            'education': 'Education Technology'
        }
        
        for ptype_key, ptype_value in project_type_mappings.items():
            if ptype_key in user_lower:
                filters['Project_Type'] = ptype_value
                break
        
        # Extract sectors
        sector_mappings = {
            'energy': 'Energy',
            'healthcare': 'Healthcare', 
            'education': 'Education',
            'finance': 'Finance',
            'water': 'Water',
            'transportation': 'Transportation',
            'agriculture': 'Agriculture',
            'technology': 'Technology'
        }
        
        for sector_key, sector_value in sector_mappings.items():
            if sector_key in user_lower:
                filters['Sector'] = sector_value
                break
        
        # Extract SDG alignment
        sdg_patterns = [
            r'sdg ([0-9]+)',
            r'sustainable development goal ([0-9]+)',
            r'aligned with sdg ([0-9]+)'
        ]
        
        for pattern in sdg_patterns:
            sdg_match = re.search(pattern, user_lower)
            if sdg_match:
                sdg_number = int(sdg_match.group(1))
                if 1 <= sdg_number <= 17:
                    filters['Primary_SDG'] = f"SDG {sdg_number}"
                break
        
        # Extract status preferences
        status_mappings = {
            'completed': 'Completed',
            'operational': 'Operational',
            'in development': 'In Development',
            'proposed': 'Proposed'
        }
        
        for status_key, status_value in status_mappings.items():
            if status_key in user_lower:
                filters['Status'] = status_value
                break
        
        # Extract impact requirements
        if 'high impact' in user_lower:
            filters['Impact_Potential_Score'] = '>=8'
        elif 'medium impact' in user_lower:
            filters['Impact_Potential_Score'] = '>=6'
        elif 'low impact' in user_lower:
            filters['Impact_Potential_Score'] = '>=4'
        
        # Extract innovation requirements
        if 'innovative' in user_lower or 'innovation' in user_lower:
            filters['Innovation_Score'] = '>=70'
        
        # Extract scalability requirements
        if 'scalable' in user_lower:
            filters['Scalability_Score'] = '>=70'
        
        print(f"🔍 Parsed {len(filters)} filters from user input: {filters}")
        return filters
    
    def explain_selection(self, df_selected, filters: Dict[str, Any]) -> str:
        """
        Generate human-readable explanation of project selection using real data
        
        Args:
            df_selected: DataFrame of selected projects
            filters: Applied filters dictionary
            
        Returns:
            Human-readable explanation string with real statistics
        """
        if df_selected.empty:
            return "No projects were selected based on the given criteria."
        
        num_projects = len(df_selected)
        total_investment = df_selected['Total_Investment_USD'].sum()
        avg_esg_score = df_selected['Overall_ESG_Score'].mean()
        
        # Generate explanation with real data
        explanation = f"Selected {num_projects} projects with a total investment of ${total_investment:,.0f}. "
        explanation += f"The average ESG score of selected projects is {avg_esg_score:.1f}. "
        
        # Add filter-specific explanations
        if 'Region' in filters:
            explanation += f"All projects are located in {filters['Region']}. "
        
        if 'Country' in filters:
            explanation += f"Projects are specifically in {filters['Country']}. "
        
        if 'Sector' in filters:
            explanation += f"Projects focus on the {filters['Sector']} sector. "
        
        if 'Financial_Risk_Level' in filters:
            explanation += f"Risk level is constrained to {filters['Financial_Risk_Level']}. "
        
        if 'Primary_SDG' in filters:
            explanation += f"Projects are aligned with {filters['Primary_SDG']}. "
        
        # Add real impact summary from selected projects
        total_co2_reduction = df_selected['CO2_Reduction_Tonnes_Annual'].sum()
        total_jobs = df_selected['Jobs_Created_Total'].sum()
        total_beneficiaries = df_selected['Beneficiaries_Direct'].sum()
        avg_roi = df_selected['Expected_ROI_Percent'].mean()
        
        explanation += f"Combined impact includes {total_co2_reduction:,.0f} tonnes of CO2 reduction annually, "
        explanation += f"{total_jobs:,.0f} jobs created, and {total_beneficiaries:,.0f} direct beneficiaries. "
        explanation += f"Expected average ROI is {avg_roi:.1f}%."
        
        # Add sector and region diversity
        sectors = df_selected['Sector'].nunique()
        regions = df_selected['Region'].nunique()
        if sectors > 1:
            explanation += f" The portfolio spans {sectors} different sectors."
        if regions > 1:
            explanation += f" Projects are distributed across {regions} regions."
        
        return explanation
