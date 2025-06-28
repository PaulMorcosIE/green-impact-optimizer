
"""
Main Pipeline for ESG Optimization Engine
Orchestrates the complete flow from natural language input to optimized project selection
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple
import json

from .llm_handler import LLMHandler
from .project_filter import ProjectFilter
from .project_scorer import ProjectScorer
from .optimizer import ProjectOptimizer

class ESGOptimizationPipeline:
    """Main pipeline orchestrator for ESG project optimization"""
    
    def __init__(self, df_esg: pd.DataFrame):
        """
        Initialize the ESG optimization pipeline
        
        Args:
            df_esg: ESG projects DataFrame with all 81 columns
        """
        self.df_esg = df_esg
        self.llm_handler = LLMHandler()
        self.project_filter = ProjectFilter()
        self.project_scorer = ProjectScorer()
        self.optimizer = ProjectOptimizer()
        
        # Initialize LLM
        self.llm_handler.load_llm_pipeline()
        
        # Default weights for scoring
        self.default_weights = {
            'Overall_ESG_Score': 0.25,
            'Impact_Potential_Score': 0.20,
            'CO2_Reduction_Tonnes_Annual': 0.15,
            'Jobs_Created_Total': 0.10,
            'Expected_ROI_Percent': 0.10,
            'Beneficiaries_Direct': 0.10,
            'Innovation_Score': 0.05,
            'Scalability_Score': 0.05
        }
    
    def run_pipeline(self, user_text: str, weights_dict: Optional[Dict[str, float]] = None, 
                    budget: float = 10000000, optimization_method: str = 'maximize_score') -> Dict[str, Any]:
        """
        Execute the complete ESG optimization pipeline
        
        Args:
            user_text: Natural language query from user
            weights_dict: Custom weights for scoring (optional)
            budget: Maximum budget for project selection
            optimization_method: Method for optimization ('maximize_score' or 'minimize_risk')
            
        Returns:
            Dictionary containing all pipeline results
        """
        print(f"Starting ESG optimization pipeline...")
        print(f"User query: {user_text}")
        print(f"Budget: ${budget:,.0f}")
        
        results = {
            'user_query': user_text,
            'budget': budget,
            'success': False,
            'error': None
        }
        
        try:
            # Step 1: Parse user input into structured filters
            print("Step 1: Parsing user input...")
            filters = self.llm_handler.parse_user_input(user_text)
            results['parsed_filters'] = filters
            print(f"Parsed filters: {filters}")
            
            # Step 2: Apply filters to dataset
            print("Step 2: Applying filters...")
            df_filtered = self.project_filter.apply_filters(self.df_esg, filters)
            results['filtered_count'] = len(df_filtered)
            print(f"Projects after filtering: {len(df_filtered)}")
            
            if df_filtered.empty:
                results['error'] = "No projects match the specified criteria"
                return results
            
            # Step 3: Score projects
            print("Step 3: Scoring projects...")
            weights = weights_dict if weights_dict else self.default_weights
            df_scored = self.project_scorer.score_projects(df_filtered, weights)
            results['scoring_weights'] = weights
            
            # Step 4: Optimize project selection
            print("Step 4: Optimizing project selection...")
            df_selected = self.optimizer.optimize_projects(
                df_scored, budget, method=optimization_method
            )
            results['selected_count'] = len(df_selected)
            print(f"Projects selected: {len(df_selected)}")
            
            if df_selected.empty:
                results['error'] = "No projects could be selected within budget constraints"
                return results
            
            # Step 5: Generate explanation
            print("Step 5: Generating explanation...")
            explanation = self.llm_handler.explain_selection(df_selected, filters)
            results['explanation'] = explanation
            
            # Step 6: Compile final results
            results['selected_projects'] = df_selected.to_dict('records')
            results['project_summary'] = self._generate_project_summary(df_selected)
            results['optimization_summary'] = self.optimizer.get_optimization_summary()
            results['success'] = True
            
            print("Pipeline completed successfully!")
            
        except Exception as e:
            print(f"Pipeline error: {e}")
            results['error'] = str(e)
        
        return results
    
    def _generate_project_summary(self, df_selected: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate summary statistics for selected projects
        
        Args:
            df_selected: DataFrame of selected projects
            
        Returns:
            Dictionary with summary statistics
        """
        if df_selected.empty:
            return {}
        
        summary = {
            'total_projects': len(df_selected),
            'total_investment': df_selected['Total_Investment_USD'].sum(),
            'average_esg_score': df_selected['Overall_ESG_Score'].mean(),
            'total_co2_reduction': df_selected['CO2_Reduction_Tonnes_Annual'].sum(),
            'total_jobs_created': df_selected['Jobs_Created_Total'].sum(),
            'total_beneficiaries': df_selected['Beneficiaries_Direct'].sum(),
            'average_roi': df_selected['Expected_ROI_Percent'].mean(),
            'sectors_represented': df_selected['Sector'].nunique() if 'Sector' in df_selected.columns else 0,
            'regions_represented': df_selected['Region'].nunique() if 'Region' in df_selected.columns else 0,
            'risk_distribution': df_selected['Financial_Risk_Level'].value_counts().to_dict() if 'Financial_Risk_Level' in df_selected.columns else {}
        }
        
        return summary
    
    def get_detailed_analysis(self, user_text: str, weights_dict: Optional[Dict[str, float]] = None, 
                            budget: float = 10000000) -> Dict[str, Any]:
        """
        Get detailed analysis including intermediate steps
        
        Args:
            user_text: Natural language query
            weights_dict: Custom scoring weights
            budget: Budget constraint
            
        Returns:
            Detailed analysis dictionary
        """
        # Run main pipeline
        results = self.run_pipeline(user_text, weights_dict, budget)
        
        if not results['success']:
            return results
        
        # Add detailed analysis
        filters = results['parsed_filters']
        df_filtered = self.project_filter.apply_filters(self.df_esg, filters)
        
        # Filter summary
        filter_summary = self.project_filter.get_filter_summary(
            self.df_esg, df_filtered, filters
        )
        results['filter_summary'] = filter_summary
        
        # Score distribution analysis
        if not df_filtered.empty:
            weights = weights_dict if weights_dict else self.default_weights
            df_scored = self.project_scorer.score_projects(df_filtered, weights)
            score_analysis = self.project_scorer.analyze_score_distribution(df_scored)
            results['score_analysis'] = score_analysis
            
            # Top projects analysis (before optimization)
            top_projects = self.project_scorer.get_top_projects(df_scored, n=10)
            results['top_projects_by_score'] = top_projects[['Project_Name', 'Composite_Score', 'Total_Investment_USD']].to_dict('records')
        
        return results
    
    def update_weights(self, new_weights: Dict[str, float]) -> None:
        """
        Update default scoring weights
        
        Args:
            new_weights: New weights dictionary
        """
        self.default_weights.update(new_weights)
        print(f"Updated weights: {self.default_weights}")
    
    def get_available_filters(self) -> Dict[str, Any]:
        """
        Get information about available filter columns and their possible values
        
        Returns:
            Dictionary with filter information
        """
        categorical_columns = ['Project_Type', 'Sector', 'Region', 'Country', 
                             'Financial_Risk_Level', 'Environmental_Risk_Level', 
                             'Social_Risk_Level', 'Governance_Risk_Level']
        
        filter_info = {}
        
        for col in categorical_columns:
            if col in self.df_esg.columns:
                filter_info[col] = {
                    'type': 'categorical',
                    'unique_values': self.df_esg[col].unique().tolist()
                }
        
        # Add numerical columns with ranges
        numerical_columns = ['Total_Investment_USD', 'Expected_ROI_Percent', 
                           'Overall_ESG_Score', 'Impact_Potential_Score',
                           'CO2_Reduction_Tonnes_Annual', 'Jobs_Created_Total']
        
        for col in numerical_columns:
            if col in self.df_esg.columns:
                filter_info[col] = {
                    'type': 'numerical',
                    'min': float(self.df_esg[col].min()),
                    'max': float(self.df_esg[col].max()),
                    'mean': float(self.df_esg[col].mean())
                }
        
        return filter_info
