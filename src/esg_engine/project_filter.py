
"""
Project Filtering Module for ESG Optimization Engine
Handles filtering of ESG projects based on structured criteria
"""

import pandas as pd
from typing import Dict, Any, List
import numpy as np

class ProjectFilter:
    """Handles filtering operations on ESG project datasets"""
    
    @staticmethod
    def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply structured filters to ESG project DataFrame
        
        Args:
            df: ESG projects DataFrame
            filters: Dictionary of column_name -> filter_value pairs
            
        Returns:
            Filtered DataFrame
        """
        if not filters:
            return df.copy()
        
        filtered_df = df.copy()
        
        for column, filter_value in filters.items():
            # Skip if column doesn't exist in DataFrame
            if column not in filtered_df.columns:
                print(f"Warning: Column '{column}' not found in dataset, skipping filter")
                continue
            
            try:
                # Handle string filter values with operators
                if isinstance(filter_value, str):
                    if filter_value.startswith('>='):
                        threshold = float(filter_value[2:])
                        filtered_df = filtered_df[filtered_df[column] >= threshold]
                    elif filter_value.startswith('<='):
                        threshold = float(filter_value[2:])
                        filtered_df = filtered_df[filtered_df[column] <= threshold]
                    elif filter_value.startswith('>'):
                        threshold = float(filter_value[1:])
                        filtered_df = filtered_df[filtered_df[column] > threshold]
                    elif filter_value.startswith('<'):
                        threshold = float(filter_value[1:])
                        filtered_df = filtered_df[filtered_df[column] < threshold]
                    elif filter_value.startswith('=='):
                        value = filter_value[2:]
                        # Try to convert to numeric if possible
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                        filtered_df = filtered_df[filtered_df[column] == value]
                    else:
                        # Direct string match for categorical columns
                        filtered_df = filtered_df[filtered_df[column] == filter_value]
                
                # Handle list of values (OR condition)
                elif isinstance(filter_value, list):
                    filtered_df = filtered_df[filtered_df[column].isin(filter_value)]
                
                # Handle direct numeric values
                elif isinstance(filter_value, (int, float)):
                    filtered_df = filtered_df[filtered_df[column] == filter_value]
                
                # Handle boolean values
                elif isinstance(filter_value, bool):
                    filtered_df = filtered_df[filtered_df[column] == filter_value]
                
            except Exception as e:
                print(f"Error applying filter for column '{column}' with value '{filter_value}': {e}")
                continue
        
        return filtered_df
    
    @staticmethod
    def get_filter_summary(df_original: pd.DataFrame, df_filtered: pd.DataFrame, 
                          filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate summary of filtering results
        
        Args:
            df_original: Original DataFrame before filtering
            df_filtered: DataFrame after filtering
            filters: Applied filters
            
        Returns:
            Summary dictionary with filtering statistics
        """
        summary = {
            'original_count': len(df_original),
            'filtered_count': len(df_filtered),
            'reduction_percent': (1 - len(df_filtered) / len(df_original)) * 100,
            'applied_filters': filters,
            'total_investment_original': df_original['Total_Investment_USD'].sum(),
            'total_investment_filtered': df_filtered['Total_Investment_USD'].sum() if not df_filtered.empty else 0,
            'avg_esg_score_original': df_original['Overall_ESG_Score'].mean(),
            'avg_esg_score_filtered': df_filtered['Overall_ESG_Score'].mean() if not df_filtered.empty else 0
        }
        
        return summary
    
    @staticmethod
    def validate_filters(filters: Dict[str, Any], available_columns: List[str]) -> Dict[str, Any]:
        """
        Validate filter dictionary against available columns
        
        Args:
            filters: Filter dictionary to validate
            available_columns: List of available column names
            
        Returns:
            Validated filter dictionary with invalid entries removed
        """
        validated_filters = {}
        
        for column, value in filters.items():
            if column in available_columns:
                validated_filters[column] = value
            else:
                print(f"Warning: Filter column '{column}' not available, skipping")
        
        return validated_filters
