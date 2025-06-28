
"""
Enhanced LLM Handler for ESG Optimization Engine
Comprehensive rule-based parsing with refined project type recognition
"""

import json
import re
from typing import Dict, Any, Optional

class LLMHandler:
    """Enhanced handler for parsing user input with comprehensive rule-based NLP"""
    
    def __init__(self):
        """Initialize with enhanced rule-based parsing"""
        print("✅ Enhanced LLM handler initialized (comprehensive rule-based parsing)")
    
    def load_llm_pipeline(self) -> None:
        """No model loading needed for rule-based approach"""
        print("✅ Enhanced rule-based parsing ready (no model loading required)")
    
    def parse_user_input(self, user_text: str) -> Dict[str, Any]:
        """
        Parse natural language input into structured filters using enhanced rule-based approach
        
        Args:
            user_text: Natural language query from user
            
        Returns:
            Dictionary of filters to apply to the dataset
        """
        filters = {}
        user_lower = user_text.lower()
        
        # Enhanced budget constraints parsing
        budget_patterns = [
            r'under \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'below \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'less than \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'maximum \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'budget of \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)',
            r'up to \$?([0-9]+(?:\.[0-9]+)?)\s*([kmb]?)'
        ]
        
        for pattern in budget_patterns:
            budget_match = re.search(pattern, user_lower)
            if budget_match:
                amount = float(budget_match.group(1))
                unit = budget_match.group(2).lower() if budget_match.group(2) else ''
                multiplier = {'k': 1000, 'm': 1000000, 'b': 1000000000}.get(unit, 1)
                filters['Total_Investment_USD'] = f"<={amount * multiplier}"
                break
        
        # Enhanced ROI constraints
        roi_patterns = [
            r'roi above ([0-9]+(?:\.[0-9]+)?)%?',
            r'roi over ([0-9]+(?:\.[0-9]+)?)%?',
            r'roi greater than ([0-9]+(?:\.[0-9]+)?)%?',
            r'return above ([0-9]+(?:\.[0-9]+)?)%?',
            r'returns? of ([0-9]+(?:\.[0-9]+)?)%?',
            r'minimum ([0-9]+(?:\.[0-9]+)?)%? return',
            r'at least ([0-9]+(?:\.[0-9]+)?)%? roi'
        ]
        
        for pattern in roi_patterns:
            roi_match = re.search(pattern, user_lower)
            if roi_match:
                roi_value = float(roi_match.group(1))
                filters['Expected_ROI_Percent'] = f">={roi_value}"
                break
        
        # Enhanced jobs constraints
        jobs_patterns = [
            r'more than ([0-9]+) jobs',
            r'over ([0-9]+) jobs',
            r'([0-9]+)\+ jobs',
            r'create ([0-9]+) jobs',
            r'creating ([0-9]+) jobs',
            r'minimum ([0-9]+) jobs',
            r'at least ([0-9]+) jobs'
        ]
        
        for pattern in jobs_patterns:
            jobs_match = re.search(pattern, user_lower)
            if jobs_match:
                jobs_value = int(jobs_match.group(1))
                filters['Jobs_Created_Total'] = f">={jobs_value}"
                break
        
        # Enhanced risk level parsing
        risk_mappings = {
            'low risk': 'Low',
            'low-risk': 'Low',
            'minimal risk': 'Low',
            'safe': 'Low',
            'conservative': 'Low',
            'medium risk': 'Medium',
            'moderate risk': 'Medium',
            'balanced risk': 'Medium',
            'high risk': 'High',
            'aggressive': 'High'
        }
        
        for risk_phrase, risk_level in risk_mappings.items():
            if risk_phrase in user_lower:
                filters['Financial_Risk_Level'] = risk_level
                break
        
        # Enhanced regional parsing
        region_mappings = {
            'africa': 'Africa',
            'african': 'Africa',
            'asia': 'Asia', 
            'asian': 'Asia',
            'europe': 'Europe',
            'european': 'Europe',
            'north america': 'North America',
            'north american': 'North America',
            'south america': 'South America',
            'south american': 'South America',
            'oceania': 'Oceania'
        }
        
        for region_key, region_value in region_mappings.items():
            if region_key in user_lower:
                filters['Region'] = region_value
                break
        
        # Enhanced country parsing
        country_mappings = {
            'kenya': 'Kenya',
            'india': 'India',
            'germany': 'Germany',
            'usa': 'USA',
            'united states': 'USA',
            'america': 'USA',
            'brazil': 'Brazil',
            'nigeria': 'Nigeria',
            'china': 'China',
            'canada': 'Canada',
            'australia': 'Australia',
            'south africa': 'South Africa',
            'japan': 'Japan',
            'uk': 'UK',
            'united kingdom': 'UK',
            'france': 'France',
            'mexico': 'Mexico',
            'indonesia': 'Indonesia'
        }
        
        for country_key, country_value in country_mappings.items():
            if country_key in user_lower:
                filters['Country'] = country_value
                break
        
        # Comprehensive project type parsing with hierarchical matching
        # First check for specific subtypes, then general categories
        specific_project_mappings = {
            # Solar specific
            'solar photovoltaic': 'Solar Photovoltaic',
            'solar pv': 'Solar Photovoltaic',
            'photovoltaic': 'Solar Photovoltaic',
            'solar thermal': 'Solar Thermal',
            'solar panel': 'Solar Photovoltaic',
            
            # Wind specific
            'wind onshore': 'Wind Onshore',
            'onshore wind': 'Wind Onshore',
            'wind offshore': 'Wind Offshore',
            'offshore wind': 'Wind Offshore',
            'wind turbine': 'Wind Onshore',
            'wind farm': 'Wind Onshore',
            
            # Water specific
            'water treatment': 'Water Treatment Plants',
            'wastewater': 'Wastewater Management',
            'desalination': 'Desalination Systems',
            'water conservation': 'Water Conservation',
            
            # Transportation specific
            'electric vehicle': 'Electric Vehicle Infrastructure',
            'ev infrastructure': 'Electric Vehicle Infrastructure',
            'public transit': 'Public Transit Systems',
            'electric bus': 'Electric Buses',
            
            # Energy storage
            'battery storage': 'Energy Storage',
            'energy storage': 'Energy Storage',
            
            # Hydrogen
            'green hydrogen': 'Green Hydrogen',
            'hydrogen': 'Green Hydrogen',
            
            # Housing
            'affordable housing': 'Affordable Housing',
            'social housing': 'Social Housing',
            
            # Healthcare
            'hospital': 'Hospitals',
            'clinic': 'Clinics',
            'telemedicine': 'Telemedicine',
            
            # Education
            'school': 'Schools',
            'university': 'Universities',
            'vocational training': 'Vocational Training',
            
            # Agriculture
            'vertical farming': 'Vertical Farming',
            'precision agriculture': 'Precision Agriculture',
            'sustainable farming': 'Sustainable Farming',
            
            # Waste
            'recycling': 'Recycling Facilities',
            'waste-to-energy': 'Waste-to-Energy',
            'composting': 'Composting Systems'
        }
        
        # Check for specific project types first
        for project_key, project_value in specific_project_mappings.items():
            if project_key in user_lower:
                filters['Project_Type'] = project_value
                break
        
        # If no specific type found, check for general categories
        if 'Project_Type' not in filters:
            general_project_mappings = {
                'renewable energy': ['Solar Photovoltaic', 'Solar Thermal', 'Wind Onshore', 'Wind Offshore', 'Hydroelectric', 'Geothermal', 'Biomass Energy'],
                'renewables': ['Solar Photovoltaic', 'Solar Thermal', 'Wind Onshore', 'Wind Offshore', 'Hydroelectric', 'Geothermal', 'Biomass Energy'],
                'solar': ['Solar Photovoltaic', 'Solar Thermal'],
                'wind': ['Wind Onshore', 'Wind Offshore'],
                'clean energy': ['Solar Photovoltaic', 'Solar Thermal', 'Wind Onshore', 'Wind Offshore', 'Hydroelectric', 'Energy Storage'],
                'transportation': ['Electric Vehicle Infrastructure', 'Public Transit Systems', 'Electric Buses', 'Rail Electrification'],
                'water': ['Water Treatment Plants', 'Desalination Systems', 'Wastewater Management', 'Water Conservation'],
                'housing': ['Affordable Housing', 'Social Housing'],
                'healthcare': ['Healthcare Facilities', 'Hospitals', 'Clinics', 'Telemedicine'],
                'education': ['Schools', 'Universities', 'Vocational Training', 'Educational Technology'],
                'agriculture': ['Sustainable Farming', 'Vertical Farming', 'Precision Agriculture'],
                'waste': ['Recycling Facilities', 'Waste-to-Energy', 'Composting Systems']
            }
            
            for general_key, project_list in general_project_mappings.items():
                if general_key in user_lower:
                    # For general categories, we'll use a list to match any of the subcategories
                    filters['Project_Type'] = project_list
                    break
        
        # Enhanced sector parsing
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
            'tech': 'Technology',
            'manufacturing': 'Manufacturing',
            'construction': 'Construction'
        }
        
        for sector_key, sector_value in sector_mappings.items():
            if sector_key in user_lower:
                filters['Sector'] = sector_value
                break
        
        # Enhanced SDG parsing
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
        
        # Enhanced status parsing
        status_mappings = {
            'completed': 'Completed',
            'finished': 'Completed',
            'operational': 'Operational',
            'running': 'Operational',
            'active': 'Operational',
            'in development': 'In Development',
            'developing': 'In Development',
            'under construction': 'In Development',
            'proposed': 'Proposed',
            'planned': 'Proposed'
        }
        
        for status_key, status_value in status_mappings.items():
            if status_key in user_lower:
                filters['Status'] = status_value
                break
        
        # Enhanced impact parsing
        if any(phrase in user_lower for phrase in ['high impact', 'maximum impact', 'strong impact', 'significant impact']):
            filters['Impact_Potential_Score'] = '>=8'
        elif any(phrase in user_lower for phrase in ['medium impact', 'moderate impact']):
            filters['Impact_Potential_Score'] = '>=6'
        elif any(phrase in user_lower for phrase in ['low impact', 'minimal impact']):
            filters['Impact_Potential_Score'] = '>=4'
        
        # Enhanced innovation parsing
        if any(phrase in user_lower for phrase in ['innovative', 'innovation', 'cutting edge', 'advanced', 'breakthrough']):
            filters['Innovation_Score'] = '>=70'
        
        # Enhanced scalability parsing
        if any(phrase in user_lower for phrase in ['scalable', 'scale up', 'expandable', 'replicable']):
            filters['Scalability_Score'] = '>=70'
        
        # Credit rating parsing
        credit_rating_patterns = [
            r'credit rating ([a-z]+\+?-?)',
            r'rating ([a-z]+\+?-?)',
            r'([a-z]+\+?-?) rated',
            r'([a-z]+\+?-?) credit'
        ]
        
        for pattern in credit_rating_patterns:
            rating_match = re.search(pattern, user_lower)
            if rating_match:
                rating = rating_match.group(1).upper()
                if rating in ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-', 'BB+', 'BB', 'BB-', 'B+', 'B', 'B-']:
                    filters['Credit_Rating'] = rating
                break
        
        # Investment grade parsing
        if any(phrase in user_lower for phrase in ['investment grade', 'high grade', 'top rated']):
            filters['Credit_Rating'] = ['AAA', 'AA+', 'AA', 'AA-', 'A+', 'A', 'A-', 'BBB+', 'BBB', 'BBB-']
        
        print(f"🔍 Parsed {len(filters)} filters from user input: {filters}")
        return filters
    
    def explain_selection(self, df_selected, filters: Dict[str, Any]) -> str:
        """
        Generate enhanced explanation of project selection using real data
        
        Args:
            df_selected: DataFrame of selected projects
            filters: Applied filters dictionary
            
        Returns:
            Enhanced explanation string with comprehensive statistics
        """
        if df_selected.empty:
            return "No projects were selected based on the given criteria."
        
        num_projects = len(df_selected)
        total_investment = df_selected['Total_Investment_USD'].sum()
        avg_esg_score = df_selected['Overall_ESG_Score'].mean()
        
        explanation = f"Selected {num_projects} projects with total investment of ${total_investment:,.0f}. "
        explanation += f"Average ESG score: {avg_esg_score:.1f}. "
        
        # Enhanced impact metrics
        total_co2_reduction = df_selected['CO2_Reduction_Tonnes_Annual'].sum()
        total_jobs = df_selected['Jobs_Created_Total'].sum()
        avg_roi = df_selected['Expected_ROI_Percent'].mean()
        total_beneficiaries = df_selected['Beneficiaries_Direct'].sum()
        
        explanation += f"Expected impact: {total_co2_reduction:,.0f} tonnes CO2 reduction annually, "
        explanation += f"{total_jobs:,.0f} jobs created, {avg_roi:.1f}% average ROI, "
        explanation += f"{total_beneficiaries:,.0f} direct beneficiaries. "
        
        # Credit rating distribution
        if 'Credit_Rating' in df_selected.columns:
            top_ratings = df_selected['Credit_Rating'].value_counts().head(3)
            explanation += f"Top credit ratings: {', '.join([f'{rating} ({count})' for rating, count in top_ratings.items()])}."
        
        return explanation
