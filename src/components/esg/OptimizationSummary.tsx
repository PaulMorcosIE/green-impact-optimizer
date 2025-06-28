
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, Target, DollarSign, Award } from 'lucide-react';

interface OptimizationSummaryProps {
  summary: {
    total_projects: number;
    total_investment: number;
    average_esg_score: number;
    total_co2_reduction: number;
    total_jobs_created: number;
    total_beneficiaries: number;
    average_roi: number;
    sectors_represented: number;
    regions_represented: number;
  };
  optimization: {
    total_cost: number;
    budget_utilization: number;
    num_projects: number;
  };
  budget: number;
}

const OptimizationSummary = ({ summary, optimization, budget }: OptimizationSummaryProps) => {
  const metrics = [
    {
      title: "Total Investment",
      value: `$${(summary.total_investment / 1000000).toFixed(1)}M`,
      icon: DollarSign,
      color: "text-green-600"
    },
    {
      title: "Average ESG Score",
      value: summary.average_esg_score.toFixed(1),
      icon: Award,
      color: "text-blue-600"
    },
    {
      title: "CO2 Reduction",
      value: `${summary.total_co2_reduction.toLocaleString()} t/year`,
      icon: TrendingUp,
      color: "text-green-600"
    },
    {
      title: "Jobs Created",
      value: summary.total_jobs_created.toLocaleString(),
      icon: Target,
      color: "text-purple-600"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map((metric, index) => (
          <Card key={index}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{metric.title}</p>
                  <p className="text-2xl font-bold">{metric.value}</p>
                </div>
                <metric.icon className={`w-8 h-8 ${metric.color}`} />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Detailed Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Portfolio Overview</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span>Budget Utilization</span>
                <span>{(optimization.budget_utilization * 100).toFixed(1)}%</span>
              </div>
              <Progress value={optimization.budget_utilization * 100} />
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-600">Projects Selected</p>
                <p className="font-semibold">{summary.total_projects}</p>
              </div>
              <div>
                <p className="text-gray-600">Avg ROI</p>
                <p className="font-semibold">{summary.average_roi.toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-gray-600">Sectors</p>
                <p className="font-semibold">{summary.sectors_represented}</p>
              </div>
              <div>
                <p className="text-gray-600">Regions</p>
                <p className="font-semibold">{summary.regions_represented}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Impact Metrics</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Direct Beneficiaries</span>
                <span className="font-semibold">{summary.total_beneficiaries.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Annual CO2 Reduction</span>
                <span className="font-semibold">{summary.total_co2_reduction.toLocaleString()} tonnes</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Total Jobs Created</span>
                <span className="font-semibold">{summary.total_jobs_created.toLocaleString()}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Investment per Job</span>
                <span className="font-semibold">
                  ${Math.round(summary.total_investment / summary.total_jobs_created).toLocaleString()}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default OptimizationSummary;
