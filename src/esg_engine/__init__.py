
"""
ESG Optimization Engine

A comprehensive system for ESG project filtering, scoring, and optimization
using natural language processing and linear programming.
"""

from .llm_handler import LLMHandler
from .project_filter import ProjectFilter
from .project_scorer import ProjectScorer
from .optimizer import ProjectOptimizer
from .pipeline import ESGOptimizationPipeline

__version__ = "1.0.0"
__all__ = [
    'LLMHandler',
    'ProjectFilter', 
    'ProjectScorer',
    'ProjectOptimizer',
    'ESGOptimizationPipeline'
]
