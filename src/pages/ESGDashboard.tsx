
import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AlertCircle, CheckCircle, Loader2, TrendingUp } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import ProjectResults from '@/components/esg/ProjectResults';
import FilterPanel from '@/components/esg/FilterPanel';
import WeightingPanel from '@/components/esg/WeightingPanel';
import OptimizationSummary from '@/components/esg/OptimizationSummary';

interface ESGResults {
  success: boolean;
  error?: string;
  user_query: string;
  budget: number;
  selected_count: number;
  selected_projects: any[];
  project_summary: any;
  explanation: string;
  optimization_summary: any;
  parsed_filters: any;
}

const ESGDashboard = () => {
  const [userQuery, setUserQuery] = useState('');
  const [budget, setBudget] = useState(10000000);
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState<ESGResults | null>(null);
  const [customWeights, setCustomWeights] = useState<Record<string, number>>({});
  const [useCustomWeights, setUseCustomWeights] = useState(false);
  const { toast } = useToast();

  const defaultWeights = {
    'Overall_ESG_Score': 25,
    'Impact_Potential_Score': 20,
    'CO2_Reduction_Tonnes_Annual': 15,
    'Jobs_Created_Total': 10,
    'Expected_ROI_Percent': 10,
    'Beneficiaries_Direct': 10,
    'Innovation_Score': 5,
    'Scalability_Score': 5
  };

  const handleOptimization = async () => {
    if (!userQuery.trim()) {
      toast({
        title: "Input Required",
        description: "Please enter your ESG project requirements",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      // Simulate API call to Python backend
      // In production, this would call your Flask/FastAPI endpoint
      const response = await simulateESGOptimization({
        user_text: userQuery,
        budget: budget,
        weights_dict: useCustomWeights ? customWeights : null
      });

      setResults(response);
      
      if (response.success) {
        toast({
          title: "Optimization Complete",
          description: `Found ${response.selected_count} optimal projects`,
        });
      } else {
        toast({
          title: "Optimization Failed",
          description: response.error || "Unknown error occurred",
          variant: "destructive"
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to connect to optimization engine",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Simulate the ESG optimization process
  const simulateESGOptimization = async (params: any): Promise<ESGResults> => {
    // This would normally call your Python backend
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    return {
      success: true,
      user_query: params.user_text,
      budget: params.budget,
      selected_count: 12,
      selected_projects: [
        {
          Project_Name: "Solar Farm Development - Ghana",
          Total_Investment_USD: 2500000,
          Overall_ESG_Score: 92.5,
          CO2_Reduction_Tonnes_Annual: 15000,
          Jobs_Created_Total: 150,
          Region: "Africa",
          Sector: "Energy"
        },
        {
          Project_Name: "Water Purification System - Kenya",
          Total_Investment_USD: 1800000,
          Overall_ESG_Score: 89.2,
          CO2_Reduction_Tonnes_Annual: 5000,
          Jobs_Created_Total: 80,
          Region: "Africa",
          Sector: "Water"
        }
      ],
      project_summary: {
        total_projects: 12,
        total_investment: 8950000,
        average_esg_score: 87.3,
        total_co2_reduction: 45000,
        total_jobs_created: 680,
        total_beneficiaries: 125000,
        average_roi: 12.8,
        sectors_represented: 4,
        regions_represented: 2
      },
      explanation: "Selected 12 high-impact renewable energy and water projects across Africa. These projects offer strong ESG scores while maintaining low financial risk. The portfolio emphasizes CO2 reduction and job creation in underserved communities.",
      optimization_summary: {
        total_cost: 8950000,
        total_score: 1047.6,
        budget_utilization: 0.895,
        num_projects: 12
      },
      parsed_filters: {
        Region: "Africa",
        Total_Investment_USD: "<=10000000",
        Financial_Risk_Level: "Low"
      }
    };
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-4">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-gray-900">ESG Project Optimizer</h1>
          <p className="text-lg text-gray-600">
            Find and optimize ESG projects using AI-powered natural language processing
          </p>
        </div>

        {/* Main Input Section */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Project Requirements
            </CardTitle>
            <CardDescription>
              Describe your ESG project requirements in natural language
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="query">What kind of ESG projects are you looking for?</Label>
              <Textarea
                id="query"
                placeholder="e.g., Find low-risk renewable energy projects in Africa under $10M with high impact"
                value={userQuery}
                onChange={(e) => setUserQuery(e.target.value)}
                className="min-h-20"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="budget">Maximum Budget (USD)</Label>
                <Input
                  id="budget"
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(Number(e.target.value))}
                />
                <p className="text-sm text-gray-500">
                  ${budget.toLocaleString()}
                </p>
              </div>

              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <Switch
                    id="custom-weights"
                    checked={useCustomWeights}
                    onCheckedChange={setUseCustomWeights}
                  />
                  <Label htmlFor="custom-weights">Use Custom Scoring Weights</Label>
                </div>
              </div>
            </div>

            {useCustomWeights && (
              <WeightingPanel
                weights={customWeights}
                defaultWeights={defaultWeights}
                onWeightsChange={setCustomWeights}
              />
            )}

            <Button 
              onClick={handleOptimization} 
              disabled={isLoading}
              className="w-full"
              size="lg"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Optimizing Projects...
                </>
              ) : (
                "Find Optimal Projects"
              )}
            </Button>
          </CardContent>
        </Card>

        {/* Results Section */}
        {results && (
          <Tabs defaultValue="summary" className="w-full">
            <TabsList className="grid w-full grid-cols-4">
              <TabsTrigger value="summary">Summary</TabsTrigger>
              <TabsTrigger value="projects">Selected Projects</TabsTrigger>
              <TabsTrigger value="filters">Applied Filters</TabsTrigger>
              <TabsTrigger value="explanation">AI Explanation</TabsTrigger>
            </TabsList>

            <TabsContent value="summary" className="space-y-4">
              <OptimizationSummary 
                summary={results.project_summary}
                optimization={results.optimization_summary}
                budget={results.budget}
              />
            </TabsContent>

            <TabsContent value="projects">
              <ProjectResults projects={results.selected_projects} />
            </TabsContent>

            <TabsContent value="filters">
              <FilterPanel filters={results.parsed_filters} />
            </TabsContent>

            <TabsContent value="explanation">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    AI Explanation
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed">{results.explanation}</p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        )}

        {results && !results.success && (
          <Card className="border-red-200">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-red-600">
                <AlertCircle className="w-5 h-5" />
                <span className="font-medium">Optimization Failed</span>
              </div>
              <p className="text-red-700 mt-2">{results.error}</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default ESGDashboard;
