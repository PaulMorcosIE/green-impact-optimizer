
"""
Project Scoring Module for ESG Optimization Engine
Handles scoring and ranking of ESG projects based on weighted KPIs
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from sklearn.preprocessing import MinMaxScaler

class ProjectScorer:
    """Handles scoring operations for ESG projects"""
    
    def __init__(self):
        self.scaler = MinMaxScaler()
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
    
    def score_projects(self, df: pd.DataFrame, weights: Optional[Dict[str, float]] = None) -> pd.DataFrame:
        """
        Calculate composite scores for ESG projects based on weighted KPIs
        
        Args:
            df: ESG projects DataFrame
            weights: Dictionary of column_name -> weight pairs
            
        Returns:
            DataFrame with added 'Composite_Score' column
        """
        if df.empty:
            return df
        
        # Use provided weights or defaults
        if weights is None:
            weights = self.default_weights
        
        # Create copy to avoid modifying original
        scored_df = df.copy()
        
        # Prepare scoring columns
        scoring_columns = []
        scoring_weights = []
        
        for column, weight in weights.items():
            if column in scored_df.columns:
                scoring_columns.append(column)
                scoring_weights.append(weight)
            else:
                print(f"Warning: Scoring column '{column}' not found in dataset")
        
        if not scoring_columns:
            print("No valid scoring columns found, using Overall_ESG_Score only")
            scored_df['Composite_Score'] = scored_df.get('Overall_ESG_Score', 0)
            return scored_df
        
        # Normalize scoring columns to 0-1 range
        normalized_data = pd.DataFrame()
        
        for column in scoring_columns:
            col_data = scored_df[column].fillna(0)  # Fill NaN with 0
            
            # Handle different column types appropriately
            if column in ['Financial_Risk_Level', 'Environmental_Risk_Level', 'Social_Risk_Level', 'Governance_Risk_Level']:
                # For risk levels, convert to numeric (Low=3, Medium=2, High=1)
                risk_mapping = {'Low': 3, 'Medium': 2, 'High': 1}
                col_data = col_data.map(risk_mapping).fillna(1)
            
            # Normalize to 0-1 range
            if col_data.max() > col_data.min():
                normalized_col = (col_data - col_data.min()) / (col_data.max() - col_data.min())
            else:
                normalized_col = pd.Series(np.ones(len(col_data)), index=col_data.index)
            
            normalized_data[column] = normalized_col
        
        # Calculate weighted composite score
        composite_scores = np.zeros(len(scored_df))
        total_weight = sum(scoring_weights)
        
        for i, (column, weight) in enumerate(zip(scoring_columns, scoring_weights)):
            normalized_weight = weight / total_weight if total_weight > 0 else 1 / len(scoring_columns)
            composite_scores += normalized_data[column] * normalized_weight
        
        scored_df['Composite_Score'] = composite_scores * 100  # Scale to 0-100
        
        return scored_df
    
    def rank_projects(self, df: pd.DataFrame, score_column: str = 'Composite_Score') -> pd.DataFrame:
        """
        Rank projects by score in descending order
        
        Args:
            df: DataFrame with scored projects
            score_column: Column name containing scores
            
        Returns:
            DataFrame sorted by score with rank column added
        """
        if score_column not in df.columns:
            print(f"Score column '{score_column}' not found")
            return df
        
        ranked_df = df.copy()
        ranked_df = ranked_df.sort_values(by=score_column, ascending=False)
        ranked_df['Rank'] = range(1, len(ranked_df) + 1)
        
        return ranked_df
    
    def get_top_projects(self, df: pd.DataFrame, n: int = 10, 
                        score_column: str = 'Composite_Score') -> pd.DataFrame:
        """
        Get top N projects by score
        
        Args:
            df: DataFrame with scored projects
            n: Number of top projects to return
            score_column: Column name containing scores
            
        Returns:
            DataFrame with top N projects
        """
        ranked_df = self.rank_projects(df, score_column)
        return ranked_df.head(n)
    
    def analyze_score_distribution(self, df: pd.DataFrame, 
                                 score_column: str = 'Composite_Score') -> Dict[str, float]:
        """
        Analyze the distribution of composite scores
        
        Args:
            df: DataFrame with scored projects
            score_column: Column name containing scores
            
        Returns:
            Dictionary with score statistics
        """
        if score_column not in df.columns:
            return {}
        
        scores = df[score_column]
        
        return {
            'mean': scores.mean(),
            'median': scores.median(),
            'std': scores.std(),
            'min': scores.min(),
            'max': scores.max(),
            'q25': scores.quantile(0.25),
            'q75': scores.quantile(0.75),
            'count': len(scores)
        }
