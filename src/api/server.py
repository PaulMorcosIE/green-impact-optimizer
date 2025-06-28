"""
Flask API Server for ESG Optimization Pipeline
Exposes the ESG pipeline as REST endpoints for the React frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the parent directory to the path to import esg_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from esg_engine.pipeline import ESGOptimizationPipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize the ESG pipeline once at startup
print("🚀 Initializing ESG Pipeline...")
pipeline = ESGOptimizationPipeline()
print("✅ ESG Pipeline ready!")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'dataset_size': len(pipeline.df_esg),
        'message': 'ESG Optimization API is running'
    })

@app.route('/api/optimize', methods=['POST'])
def optimize_projects():
    """
    Main optimization endpoint
    Accepts user query and budget, returns optimized project selection
    """
    try:
        data = request.get_json()
        
        # Extract parameters
        user_text = data.get('user_text', '')
        budget = data.get('budget', 10000000)
        weights_dict = data.get('weights_dict', None)
        optimization_method = data.get('optimization_method', 'maximize_score')
        
        if not user_text.strip():
            return jsonify({
                'success': False,
                'error': 'User query is required'
            }), 400
        
        # Run the pipeline
        results = pipeline.run_pipeline(
            user_text=user_text,
            weights_dict=weights_dict,
            budget=budget,
            optimization_method=optimization_method
        )
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/dataset/stats', methods=['GET'])
def get_dataset_stats():
    """Get comprehensive dataset statistics"""
    try:
        stats = pipeline.get_dataset_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({
            'error': f'Failed to get dataset statistics: {str(e)}'
        }), 500

@app.route('/api/search', methods=['POST'])
def search_projects():
    """Search projects using natural language text matching"""
    try:
        data = request.get_json()
        search_text = data.get('search_text', '')
        max_results = data.get('max_results', 50)
        
        if not search_text.strip():
            return jsonify({
                'error': 'Search text is required'
            }), 400
        
        results_df = pipeline.search_projects_by_text(search_text, max_results)
        
        return jsonify({
            'success': True,
            'count': len(results_df),
            'projects': results_df.to_dict('records') if not results_df.empty else []
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Search failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🌐 Starting Flask API server...")
    print("📊 Dataset loaded with 500,000 ESG projects")
    print("🔗 API endpoints available:")
    print("   - GET  /api/health")
    print("   - POST /api/optimize")
    print("   - GET  /api/dataset/stats")
    print("   - POST /api/search")
    app.run(debug=True, host='0.0.0.0', port=5000)
