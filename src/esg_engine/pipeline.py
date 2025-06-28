
"""
Main Pipeline for ESG Optimization Engine
Orchestrates the complete flow from natural language input to optimized project selection
"""

import pandas as pd
from typing import Dict, Any, Optional, Tuple
import json

from .data_generator import generate_synthetic_esg_data, get_column_info
from .llm_handler import LLMHandler
from .project_filter import ProjectFilter
from .project_scorer import ProjectScorer
from .optimizer import ProjectOptimizer

class ESGOptimizationPipeline:
    """Main pipeline orchestrator for ESG project optimization"""
    
    def __init__(self, use_cached_data: bool = True):
        """
        Initialize the ESG optimization pipeline
        
        Args:
            use_cached_data: Whether to use cached dataset or generate new one
        """
        # Generate or load the synthetic ESG dataset
        print("🚀 Initializing ESG Optimization Pipeline...")
        self.df_esg = generate_synthetic_esg_data(n_rows=100000)
        self.column_info = get_column_info(self.df_esg)
        
        # Initialize components
        self.llm_handler = LLMHandler()
        self.project_filter = ProjectFilter()
        self.project_scorer = ProjectScorer()
        self.optimizer = ProjectOptimizer()
        
        # Initialize LLM
        print("🧠 Loading LLM pipeline...")
        self.llm_handler.load_llm_pipeline()
        
        # Enhanced default weights for comprehensive scoring
        self.default_weights = {
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
        
        print(f"✅ Pipeline initialized with {len(self.df_esg):,} ESG projects")
        print(f"📊 Dataset contains {self.column_info['total_columns']} columns:")
        print(f"   • {len(self.column_info['numerical_columns'])} numerical columns")
        print(f"   • {len(self.column_info['categorical_columns'])} categorical columns")
        print(f"   • {len(self.column_info['boolean_columns'])} boolean columns")
    
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
        print(f"🔍 Starting ESG optimization pipeline...")
        print(f"📝 User query: {user_text}")
        print(f"💰 Budget: ${budget:,.0f}")
        
        results = {
            'user_query': user_text,
            'budget': budget,
            'dataset_size': len(self.df_esg),
            'success': False,
            'error': None
        }
        
        try:
            # Step 1: Parse user input into structured filters
            print("1️⃣ Parsing user input...")
            filters = self.llm_handler.parse_user_input(user_text)
            results['parsed_filters'] = filters
            print(f"   📋 Parsed filters: {filters}")
            
            # Step 2: Apply filters to dataset
            print("2️⃣ Applying filters to 100K projects...")
            df_filtered = self.project_filter.apply_filters(self.df_esg, filters)
            results['filtered_count'] = len(df_filtered)
            print(f"   ✅ Projects after filtering: {len(df_filtered):,}")
            
            if df_filtered.empty:
                results['error'] = "No projects match the specified criteria"
                return results
            
            # Step 3: Score projects
            print("3️⃣ Scoring filtered projects...")
            weights = weights_dict if weights_dict else self.default_weights
            df_scored = self.project_scorer.score_projects(df_filtered, weights)
            results['scoring_weights'] = weights
            print(f"   📊 Applied weighted scoring with {len(weights)} criteria")
            
            # Step 4: Optimize project selection
            print("4️⃣ Optimizing project portfolio...")
            df_selected = self.optimizer.optimize_projects(
                df_scored, budget, method=optimization_method
            )
            results['selected_count'] = len(df_selected)
            print(f"   🎯 Projects selected: {len(df_selected)}")
            
            if df_selected.empty:
                results['error'] = "No projects could be selected within budget constraints"
                return results
            
            # Step 5: Generate explanation
            print("5️⃣ Generating AI explanation...")
            explanation = self.llm_handler.explain_selection(df_selected, filters)
            results['explanation'] = explanation
            
            # Step 6: Compile final results with real data
            print("6️⃣ Compiling results...")
            results['selected_projects'] = df_selected.to_dict('records')
            results['project_summary'] = self._generate_project_summary(df_selected)
            results['optimization_summary'] = self.optimizer.get_optimization_summary()
            results['filter_analysis'] = self._analyze_filter_impact(df_filtered, filters)
            results['success'] = True
            
            print("✅ Pipeline completed successfully!")
            
        except Exception as e:
            print(f"❌ Pipeline error: {e}")
            results['error'] = str(e)
        
        return results
    
    def _generate_project_summary(self, df_selected: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics for selected projects
        
        Args:
            df_selected: DataFrame of selected projects
            
        Returns:
            Dictionary with detailed summary statistics
        """
        if df_selected.empty:
            return {}
        
        summary = {
            'total_projects': len(df_selected),
            'total_investment': float(df_selected['Total_Investment_USD'].sum()),
            'average_esg_score': float(df_selected['Overall_ESG_Score'].mean()),
            'total_co2_reduction': float(df_selected['CO2_Reduction_Tonnes_Annual'].sum()),
            'total_jobs_created': int(df_selected['Jobs_Created_Total'].sum()),
            'total_beneficiaries': int(df_selected['Beneficiaries_Direct'].sum()),
            'average_roi': float(df_selected['Expected_ROI_Percent'].mean()),
            'sectors_represented': int(df_selected['Sector'].nunique()),
            'regions_represented': int(df_selected['Region'].nunique()),
            'countries_represented': int(df_selected['Country'].nunique()),
            'risk_distribution': df_selected['Financial_Risk_Level'].value_counts().to_dict(),
            'status_distribution': df_selected['Status'].value_counts().to_dict(),
            'sdg_alignment': {
                'primary_sdgs': df_selected['Primary_SDG'].value_counts().head(5).to_dict(),
                'total_sdgs_covered': df_selected['Primary_SDG'].nunique()
            },
            'impact_metrics': {
                'avg_impact_score': float(df_selected['Impact_Potential_Score'].mean()),
                'avg_innovation_score': float(df_selected['Innovation_Score'].mean()),
                'avg_scalability_score': float(df_selected['Scalability_Score'].mean()),
                'total_renewable_capacity': float(df_selected['Renewable_Energy_Capacity_MW'].sum()),
                'total_water_savings': float(df_selected['Water_Savings_m3_Annual'].sum())
            }
        }
        
        return summary
    
    def _analyze_filter_impact(self, df_filtered: pd.DataFrame, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the impact of applied filters on the dataset
        
        Args:
            df_filtered: Filtered DataFrame
            filters: Applied filters
            
        Returns:
            Analysis of filter effectiveness
        """
        original_size = len(self.df_esg)
        filtered_size = len(df_filtered)
        
        analysis = {
            'original_dataset_size': original_size,
            'filtered_dataset_size': filtered_size,
            'reduction_percentage': ((original_size - filtered_size) / original_size) * 100,
            'filters_applied': len(filters),
            'most_restrictive_filter': None
        }
        
        # Find most restrictive filter by testing each individually
        if filters:
            filter_impacts = {}
            for filter_name, filter_value in filters.items():
                single_filter = {filter_name: filter_value}
                single_filtered = self.project_filter.apply_filters(self.df_esg, single_filter)
                filter_impacts[filter_name] = len(single_filtered)
            
            if filter_impacts:
                most_restrictive = min(filter_impacts, key=filter_impacts.get)
                analysis['most_restrictive_filter'] = {
                    'column': most_restrictive,
                    'remaining_projects': filter_impacts[most_restrictive]
                }
        
        return analysis
    
    def search_projects_by_text(self, search_text: str, max_results: int = 50) -> pd.DataFrame:
        """
        Search projects using natural language text matching
        
        Args:
            search_text: Text to search for in project names and descriptions
            max_results: Maximum number of results to return
            
        Returns:
            DataFrame with matching projects
        """
        # Parse the search text into filters
        filters = self.llm_handler.parse_user_input(search_text)
        
        # Apply filters and return top matches
        filtered_df = self.project_filter.apply_filters(self.df_esg, filters)
        
        if not filtered_df.empty:
            # Score the filtered projects
            scored_df = self.project_scorer.score_projects(filtered_df, self.default_weights)
            # Return top scoring projects
            return scored_df.nlargest(max_results, 'Composite_Score')
        
        return pd.DataFrame()
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the synthetic dataset
        
        Returns:
            Dictionary with dataset statistics
        """
        stats = {
            'total_projects': len(self.df_esg),
            'total_columns': len(self.df_esg.columns),
            'investment_range': {
                'min': float(self.df_esg['Total_Investment_USD'].min()),
                'max': float(self.df_esg['Total_Investment_USD'].max()),
                'mean': float(self.df_esg['Total_Investment_USD'].mean()),
                'total': float(self.df_esg['Total_Investment_USD'].sum())
            },
            'sector_distribution': self.df_esg['Sector'].value_counts().to_dict(),
            'region_distribution': self.df_esg['Region'].value_counts().to_dict(),
            'status_distribution': self.df_esg['Status'].value_counts().to_dict(),
            'risk_distribution': self.df_esg['Financial_Risk_Level'].value_counts().to_dict(),
            'impact_summary': {
                'total_co2_reduction': float(self.df_esg['CO2_Reduction_Tonnes_Annual'].sum()),
                'total_jobs': int(self.df_esg['Jobs_Created_Total'].sum()),
                'total_beneficiaries': int(self.df_esg['Beneficiaries_Direct'].sum()),
                'avg_esg_score': float(self.df_esg['Overall_ESG_Score'].mean())
            },
            'column_info': self.column_info
        }
        
        return stats

    # ... keep existing code (update_weights, get_available_filters, get_detailed_analysis methods)
