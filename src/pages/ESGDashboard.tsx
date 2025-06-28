
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
      // Call the real Flask API
      const response = await fetch('http://localhost:5000/api/optimize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_text: userQuery,
          budget: budget,
          weights_dict: useCustomWeights ? convertWeightsToDecimal(customWeights) : null
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
      
      if (data.success) {
        toast({
          title: "Optimization Complete",
          description: `Found ${data.selected_count} optimal projects`,
        });
      } else {
        toast({
          title: "Optimization Failed",
          description: data.error || "Unknown error occurred",
          variant: "destructive"
        });
      }
    } catch (error) {
      console.error('API Error:', error);
      toast({
        title: "Connection Error",
        description: "Failed to connect to ESG optimization server. Make sure the Python API is running on port 5000.",
        variant: "destructive"
      });
      
      // Fallback to show connection instructions
      setResults({
        success: false,
        error: "Connection failed. Please start the Python API server by running: python src/api/server.py",
        user_query: userQuery,
        budget: budget,
        selected_count: 0,
        selected_projects: [],
        project_summary: null,
        explanation: "",
        optimization_summary: null,
        parsed_filters: {}
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Convert percentage weights to decimal for API
  const convertWeightsToDecimal = (weights: Record<string, number>) => {
    const converted: Record<string, number> = {};
    for (const [key, value] of Object.entries(weights)) {
      converted[key] = value / 100;
    }
    return converted;
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
          <p className="text-sm text-gray-500">
            Powered by 100,000 synthetic ESG projects with 80+ sustainability metrics
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
              {results.success && results.project_summary ? (
                <OptimizationSummary 
                  summary={results.project_summary}
                  optimization={results.optimization_summary}
                  budget={results.budget}
                />
              ) : (
                <Card className="border-red-200">
                  <CardContent className="pt-6">
                    <div className="flex items-center gap-2 text-red-600">
                      <AlertCircle className="w-5 h-5" />
                      <span className="font-medium">No Results Available</span>
                    </div>
                    <p className="text-red-700 mt-2">{results.error}</p>
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            <TabsContent value="projects">
              {results.success && results.selected_projects?.length > 0 ? (
                <ProjectResults projects={results.selected_projects} />
              ) : (
                <Card>
                  <CardContent className="pt-6">
                    <p className="text-gray-500">No projects selected</p>
                  </CardContent>
                </Card>
              )}
            </TabsContent>

            <TabsContent value="filters">
              <FilterPanel filters={results.parsed_filters || {}} />
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
                  <p className="text-gray-700 leading-relaxed">
                    {results.explanation || "No explanation available"}
                  </p>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        )}
      </div>
    </div>
  );
};

export default ESGDashboard;
