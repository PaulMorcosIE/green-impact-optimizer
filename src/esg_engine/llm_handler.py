
"""
Lightweight LLM Handler for ESG Optimization Engine
Focuses only on parsing user input with rule-based approach
"""

import json
import re
from typing import Dict, Any, Optional

class LLMHandler:
    """Lightweight handler for parsing user input using rule-based NLP"""
    
    def __init__(self):
        """Initialize with rule-based parsing only"""
        print("✅ Lightweight LLM handler initialized (rule-based parsing)")
    
    def load_llm_pipeline(self) -> None:
        """No model loading needed for rule-based approach"""
        print("✅ Rule-based parsing ready (no model loading required)")
    
    def parse_user_input(self, user_text: str) -> Dict[str, Any]:
        """
        Parse natural language input into structured filters using rule-based approach
        
        Args:
            user_text: Natural language query from user
            
        Returns:
            Dictionary of filters to apply to the dataset
        """
        filters = {}
        user_lower = user_text.lower()
        
        # Enhanced rule-based parsing for comprehensive dataset
        
        # Extract budget constraints
        budget_patterns = [
            r'under \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'below \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'less than \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'maximum \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'budget of \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)'
        ]
        
        for pattern in budget_patterns:
            budget_match = re.search(pattern, user_lower)
            if budget_match:
                amount = float(budget_match.group(1))
                unit = budget_match.group(2).lower() if budget_match.group(2) else ''
                multiplier = {'k': 1000, 'm': 1000000, 'b': 1000000000}.get(unit, 1)
                filters['Total_Investment_USD'] = f"<={amount * multiplier}"
                break
        
        # Extract ROI constraints
        roi_patterns = [
            r'roi above ([0-9]+(?:\.[0-9]+)?)%?',
            r'roi over ([0-9]+(?:\.[0-9]+)?)%?',
            r'roi greater than ([0-9]+(?:\.[0-9]+)?)%?',
            r'return above ([0-9]+(?:\.[0-9]+)?)%?',
            r'returns? of ([0-9]+(?:\.[0-9]+)?)%?'
        ]
        
        for pattern in roi_patterns:
            roi_match = re.search(pattern, user_lower)
            if roi_match:
                roi_value = float(roi_match.group(1))
                filters['Expected_ROI_Percent'] = f">={roi_value}"
                break
        
        # Extract jobs constraints
        jobs_patterns = [
            r'more than ([0-9]+) jobs',
            r'over ([0-9]+) jobs',
            r'([0-9]+)\+ jobs',
            r'create ([0-9]+) jobs',
            r'creating ([0-9]+) jobs'
        ]
        
        for pattern in jobs_patterns:
            jobs_match = re.search(pattern, user_lower)
            if jobs_match:
                jobs_value = int(jobs_match.group(1))
                filters['Jobs_Created_Total'] = f">={jobs_value}"
                break
        
        # Extract risk preferences
        risk_mappings = {
            'low risk': 'Low',
            'low-risk': 'Low',
            'minimal risk': 'Low',
            'safe': 'Low',
            'medium risk': 'Medium',
            'moderate risk': 'Medium',
            'high risk': 'High'
        }
        
        for risk_phrase, risk_level in risk_mappings.items():
            if risk_phrase in user_lower:
                filters['Financial_Risk_Level'] = risk_level
                break
        
        # Extract regions
        region_mappings = {
            'africa': 'Africa',
            'asia': 'Asia', 
            'europe': 'Europe',
            'north america': 'North America',
            'south america': 'South America',
            'oceania': 'Oceania'
        }
        
        for region_key, region_value in region_mappings.items():
            if region_key in user_lower:
                filters['Region'] = region_value
                break
        
        # Extract countries
        country_mappings = {
            'kenya': 'Kenya',
            'india': 'India',
            'germany': 'Germany',
            'usa': 'USA',
            'united states': 'USA',
            'brazil': 'Brazil',
            'nigeria': 'Nigeria',
            'china': 'China',
            'canada': 'Canada',
            'australia': 'Australia',
            'south africa': 'South Africa'
        }
        
        for country_key, country_value in country_mappings.items():
            if country_key in user_lower:
                filters['Country'] = country_value
                break
        
        # Extract project types
        project_type_mappings = {
            'renewable energy': 'Renewable Energy',
            'solar': 'Renewable Energy',
            'wind': 'Renewable Energy',
            'clean energy': 'Renewable Energy',
            'clean transportation': 'Clean Transportation',
            'transport': 'Clean Transportation',
            'water': 'Water Management',
            'water management': 'Water Management',
            'social housing': 'Social Housing',
            'housing': 'Social Housing',
            'healthcare': 'Healthcare Infrastructure',
            'health': 'Healthcare Infrastructure',
            'education': 'Education Technology',
            'tech': 'Education Technology'
        }
        
        for ptype_key, ptype_value in project_type_mappings.items():
            if ptype_key in user_lower:
                filters['Project_Type'] = ptype_value
                break
        
        # Extract sectors
        sector_mappings = {
            'energy': 'Energy',
            'healthcare': 'Healthcare',
            'health': 'Healthcare',
            'education': 'Education',
            'finance': 'Finance',
            'financial': 'Finance',
            'water': 'Water',
            'transportation': 'Transportation',
            'transport': 'Transportation',
            'agriculture': 'Agriculture',
            'farming': 'Agriculture',
            'technology': 'Technology',
            'tech': 'Technology'
        }
        
        for sector_key, sector_value in sector_mappings.items():
            if sector_key in user_lower:
                filters['Sector'] = sector_value
                break
        
        # Extract SDG alignment
        sdg_patterns = [
            r'sdg ([0-9]+)',
            r'sustainable development goal ([0-9]+)',
            r'goal ([0-9]+)'
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
            'finished': 'Completed',
            'operational': 'Operational',
            'running': 'Operational',
            'in development': 'In Development',
            'developing': 'In Development',
            'proposed': 'Proposed',
            'planned': 'Proposed'
        }
        
        for status_key, status_value in status_mappings.items():
            if status_key in user_lower:
                filters['Status'] = status_value
                break
        
        # Extract impact requirements
        if any(phrase in user_lower for phrase in ['high impact', 'maximum impact', 'strong impact']):
            filters['Impact_Potential_Score'] = '>=8'
        elif any(phrase in user_lower for phrase in ['medium impact', 'moderate impact']):
            filters['Impact_Potential_Score'] = '>=6'
        elif any(phrase in user_lower for phrase in ['low impact', 'minimal impact']):
            filters['Impact_Potential_Score'] = '>=4'
        
        # Extract innovation requirements
        if any(phrase in user_lower for phrase in ['innovative', 'innovation', 'cutting edge', 'advanced']):
            filters['Innovation_Score'] = '>=70'
        
        # Extract scalability requirements
        if any(phrase in user_lower for phrase in ['scalable', 'scale up', 'expandable']):
            filters['Scalability_Score'] = '>=70'
        
        print(f"🔍 Parsed {len(filters)} filters from user input: {filters}")
        return filters
    
    def explain_selection(self, df_selected, filters: Dict[str, Any]) -> str:
        """
        Generate simple explanation of project selection using real data
        
        Args:
            df_selected: DataFrame of selected projects
            filters: Applied filters dictionary
            
        Returns:
            Simple explanation string with real statistics
        """
        if df_selected.empty:
            return "No projects were selected based on the given criteria."
        
        num_projects = len(df_selected)
        total_investment = df_selected['Total_Investment_USD'].sum()
        avg_esg_score = df_selected['Overall_ESG_Score'].mean()
        
        explanation = f"Selected {num_projects} projects with total investment of ${total_investment:,.0f}. "
        explanation += f"Average ESG score: {avg_esg_score:.1f}. "
        
        # Add key impact metrics
        total_co2_reduction = df_selected['CO2_Reduction_Tonnes_Annual'].sum()
        total_jobs = df_selected['Jobs_Created_Total'].sum()
        avg_roi = df_selected['Expected_ROI_Percent'].mean()
        
        explanation += f"Expected impact: {total_co2_reduction:,.0f} tonnes CO2 reduction annually, "
        explanation += f"{total_jobs:,.0f} jobs created, {avg_roi:.1f}% average ROI."
        
        return explanation
