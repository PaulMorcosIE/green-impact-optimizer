
"""
Linear Optimization Module for ESG Project Selection
Uses scipy.optimize.linprog for optimal project portfolio selection
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy.optimize import linprog
import warnings

class ProjectOptimizer:
    """Handles linear optimization for ESG project selection"""
    
    def __init__(self):
        self.optimization_results = None
    
    def optimize_projects(self, df: pd.DataFrame, budget: float, 
                         score_column: str = 'Composite_Score',
                         cost_column: str = 'Total_Investment_USD',
                         method: str = 'maximize_score') -> pd.DataFrame:
        """
        Use linear programming to select optimal project portfolio
        
        Args:
            df: DataFrame with scored projects
            budget: Maximum budget constraint
            score_column: Column containing project scores
            cost_column: Column containing project costs
            method: Optimization method ('maximize_score' or 'minimize_risk')
            
        Returns:
            DataFrame with selected projects
        """
        if df.empty:
            return pd.DataFrame()
        
        if score_column not in df.columns or cost_column not in df.columns:
            print(f"Required columns not found: {score_column}, {cost_column}")
            return df
        
        # Prepare optimization data
        projects = df.copy()
        n_projects = len(projects)
        
        # Extract costs and scores
        costs = projects[cost_column].values
        scores = projects[score_column].values
        
        # Handle NaN values
        costs = np.nan_to_num(costs, nan=0)
        scores = np.nan_to_num(scores, nan=0)
        
        # Set up linear programming problem
        # Variables: binary selection for each project (0 or 1)
        
        if method == 'maximize_score':
            # Maximize total score subject to budget constraint
            # Convert to minimization problem by negating objective
            c = -scores  # Coefficients for objective function (negate for maximization)
        else:
            # Minimize risk (assume higher scores mean lower risk)
            c = scores
        
        # Inequality constraint: total cost <= budget
        A_ub = [costs]  # Constraint matrix
        b_ub = [budget]  # Constraint bounds
        
        # Bounds for variables (0 <= x_i <= 1 for binary/fractional selection)
        bounds = [(0, 1) for _ in range(n_projects)]
        
        try:
            # Solve linear programming problem
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
            
            if result.success:
                # Extract solution
                selection = result.x
                
                # For practical purposes, select projects with selection > 0.5
                # (or use integer programming for true binary selection)
                selected_indices = selection > 0.5
                
                # If no projects selected with threshold, select top projects within budget
                if not selected_indices.any():
                    selected_indices = self._greedy_selection(costs, scores, budget)
                
                selected_projects = projects[selected_indices].copy()
                selected_projects['Selection_Weight'] = selection[selected_indices]
                
                self.optimization_results = {
                    'success': True,
                    'total_cost': selected_projects[cost_column].sum(),
                    'total_score': selected_projects[score_column].sum(),
                    'budget_utilization': selected_projects[cost_column].sum() / budget,
                    'num_projects': len(selected_projects)
                }
                
                return selected_projects
            
            else:
                print(f"Optimization failed: {result.message}")
                # Fallback to greedy selection
                return self._greedy_fallback(df, budget, score_column, cost_column)
        
        except Exception as e:
            print(f"Optimization error: {e}")
            return self._greedy_fallback(df, budget, score_column, cost_column)
    
    def _greedy_selection(self, costs: np.ndarray, scores: np.ndarray, 
                         budget: float) -> np.ndarray:
        """
        Greedy selection based on score-to-cost ratio
        
        Args:
            costs: Array of project costs
            scores: Array of project scores
            budget: Available budget
            
        Returns:
            Boolean array indicating selected projects
        """
        n_projects = len(costs)
        selected = np.zeros(n_projects, dtype=bool)
        remaining_budget = budget
        
        # Calculate efficiency ratio (score per unit cost)
        efficiency = np.divide(scores, costs, out=np.zeros_like(scores), where=costs!=0)
        
        # Sort by efficiency (descending)
        sorted_indices = np.argsort(efficiency)[::-1]
        
        # Greedily select projects
        for idx in sorted_indices:
            if costs[idx] <= remaining_budget:
                selected[idx] = True
                remaining_budget -= costs[idx]
        
        return selected
    
    def _greedy_fallback(self, df: pd.DataFrame, budget: float, 
                        score_column: str, cost_column: str) -> pd.DataFrame:
        """
        Fallback greedy selection method
        
        Args:
            df: Projects DataFrame
            budget: Available budget
            score_column: Score column name
            cost_column: Cost column name
            
        Returns:
            Selected projects DataFrame
        """
        # Calculate efficiency and sort
        df_work = df.copy()
        df_work['Efficiency'] = df_work[score_column] / df_work[cost_column].replace(0, 1)
        df_work = df_work.sort_values('Efficiency', ascending=False)
        
        selected_projects = []
        remaining_budget = budget
        
        for _, project in df_work.iterrows():
            if project[cost_column] <= remaining_budget:
                selected_projects.append(project)
                remaining_budget -= project[cost_column]
        
        if selected_projects:
            result_df = pd.DataFrame(selected_projects)
            result_df['Selection_Weight'] = 1.0
            return result_df
        else:
            return pd.DataFrame()
    
    def optimize_with_constraints(self, df: pd.DataFrame, budget: float,
                                 additional_constraints: Optional[Dict[str, Dict]] = None,
                                 score_column: str = 'Composite_Score',
                                 cost_column: str = 'Total_Investment_USD') -> pd.DataFrame:
        """
        Optimize with additional constraints (e.g., sector diversity, risk limits)
        
        Args:
            df: Projects DataFrame
            budget: Budget constraint
            additional_constraints: Dictionary of additional constraints
            score_column: Score column name
            cost_column: Cost column name
            
        Returns:
            Optimized project selection DataFrame
        """
        # Start with basic optimization
        selected_df = self.optimize_projects(df, budget, score_column, cost_column)
        
        # Apply additional constraints if provided
        if additional_constraints and not selected_df.empty:
            for constraint_name, constraint_params in additional_constraints.items():
                selected_df = self._apply_constraint(selected_df, constraint_name, constraint_params)
        
        return selected_df
    
    def _apply_constraint(self, df: pd.DataFrame, constraint_name: str, 
                         constraint_params: Dict) -> pd.DataFrame:
        """
        Apply specific constraint to selected projects
        
        Args:
            df: Selected projects DataFrame
            constraint_name: Name of constraint to apply
            constraint_params: Parameters for the constraint
            
        Returns:
            DataFrame after applying constraint
        """
        if constraint_name == 'sector_diversity':
            # Ensure minimum number of different sectors
            min_sectors = constraint_params.get('min_sectors', 2)
            if 'Sector' in df.columns:
                unique_sectors = df['Sector'].nunique()
                if unique_sectors < min_sectors:
                    print(f"Warning: Only {unique_sectors} sectors in selection, minimum required: {min_sectors}")
        
        elif constraint_name == 'risk_limit':
            # Limit number of high-risk projects
            max_high_risk = constraint_params.get('max_high_risk', 2)
            if 'Financial_Risk_Level' in df.columns:
                high_risk_count = (df['Financial_Risk_Level'] == 'High').sum()
                if high_risk_count > max_high_risk:
                    # Remove excess high-risk projects (keep highest scoring ones)
                    high_risk_projects = df[df['Financial_Risk_Level'] == 'High']
                    low_risk_projects = df[df['Financial_Risk_Level'] != 'High']
                    
                    top_high_risk = high_risk_projects.nlargest(max_high_risk, 'Composite_Score')
                    df = pd.concat([low_risk_projects, top_high_risk])
        
        return df
    
    def get_optimization_summary(self) -> Optional[Dict]:
        """
        Get summary of last optimization results
        
        Returns:
            Dictionary with optimization statistics
        """
        return self.optimization_results
