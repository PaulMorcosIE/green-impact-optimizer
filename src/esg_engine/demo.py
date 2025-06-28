
"""
Demo script showcasing the ESG Optimization Engine with synthetic dataset
"""

from .pipeline import ESGOptimizationPipeline

def run_demo():
    """Run demonstration of ESG optimization engine with various queries"""
    
    print("🚀 ESG Optimization Engine Demo")
    print("=" * 50)
    
    # Initialize pipeline (this will generate the 100K synthetic dataset)
    pipeline = ESGOptimizationPipeline()
    
    # Display dataset statistics
    print("\n📊 Dataset Statistics:")
    stats = pipeline.get_dataset_statistics()
    print(f"Total Projects: {stats['total_projects']:,}")
    print(f"Total Investment: ${stats['investment_range']['total']:,.0f}")
    print(f"Sectors: {', '.join(stats['sector_distribution'].keys())}")
    print(f"Regions: {', '.join(stats['region_distribution'].keys())}")
    
    # Demo queries
    demo_queries = [
        {
            "query": "Find low-risk renewable energy projects in Africa under $10M with high impact",
            "budget": 50000000,
            "description": "Low-risk renewable energy focus in Africa"
        },
        {
            "query": "Show me completed projects in Kenya aligned with SDG 7 that created more than 500 jobs and have an ROI above 10%",
            "budget": 25000000,
            "description": "Kenya SDG 7 projects with high job creation and ROI"
        },
        {
            "query": "Water management projects in Asia with innovation score above 70 and scalable solutions",
            "budget": 30000000,
            "description": "Innovative water projects in Asia"
        }
    ]
    
    for i, demo in enumerate(demo_queries, 1):
        print(f"\n🔍 Demo Query {i}: {demo['description']}")
        print(f"Query: '{demo['query']}'")
        print(f"Budget: ${demo['budget']:,.0f}")
        print("-" * 60)
        
        # Run optimization
        results = pipeline.run_pipeline(
            user_text=demo['query'],
            budget=demo['budget']
        )
        
        if results['success']:
            print(f"✅ Success! Found {results['selected_count']} optimal projects")
            print(f"📋 Applied {len(results['parsed_filters'])} filters")
            print(f"🎯 Selected from {results['filtered_count']:,} filtered projects")
            
            # Display key metrics
            summary = results['project_summary']
            print(f"\n📈 Portfolio Summary:")
            print(f"  • Total Investment: ${summary['total_investment']:,.0f}")
            print(f"  • Average ESG Score: {summary['average_esg_score']:.1f}")
            print(f"  • Jobs Created: {summary['total_jobs_created']:,}")
            print(f"  • CO2 Reduction: {summary['total_co2_reduction']:,.0f} tonnes/year")
            print(f"  • Beneficiaries: {summary['total_beneficiaries']:,}")
            print(f"  • Expected ROI: {summary['average_roi']:.1f}%")
            print(f"  • Sectors: {summary['sectors_represented']}")
            print(f"  • Regions: {summary['regions_represented']}")
            
            # Display AI explanation
            print(f"\n🧠 AI Explanation:")
            print(f"  {results['explanation']}")
            
            # Show top 3 selected projects
            if results['selected_projects']:
                print(f"\n🏆 Top 3 Selected Projects:")
                for j, project in enumerate(results['selected_projects'][:3], 1):
                    print(f"  {j}. {project['Project_Name']}")
                    print(f"     Investment: ${project['Total_Investment_USD']:,.0f}")
                    print(f"     ESG Score: {project['Overall_ESG_Score']:.1f}")
                    print(f"     Sector: {project['Sector']} | Region: {project['Region']}")
                    print(f"     Jobs: {project['Jobs_Created_Total']:,} | CO2: {project['CO2_Reduction_Tonnes_Annual']:,.0f} tonnes")
        else:
            print(f"❌ Failed: {results['error']}")
        
        print()
    
    print("🎉 Demo completed!")
    
    # Additional functionality showcase
    print("\n🔧 Additional Features:")
    print("1. Text-based project search")
    search_results = pipeline.search_projects_by_text("high innovation solar projects", max_results=5)
    print(f"   Found {len(search_results)} projects matching 'high innovation solar projects'")
    
    print("2. Custom weight optimization")
    custom_weights = {
        'Overall_ESG_Score': 0.30,
        'Innovation_Score': 0.25,
        'Expected_ROI_Percent': 0.20,
        'Impact_Potential_Score': 0.15,
        'Jobs_Created_Total': 0.10
    }
    custom_results = pipeline.run_pipeline(
        user_text="Renewable energy projects with high innovation",
        weights_dict=custom_weights,
        budget=20000000
    )
    if custom_results['success']:
        print(f"   Custom weighted optimization found {custom_results['selected_count']} projects")

if __name__ == "__main__":
    run_demo()
