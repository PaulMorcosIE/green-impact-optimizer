
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MapPin, DollarSign, Leaf, Users, TrendingUp } from 'lucide-react';

interface Project {
  Project_Name: string;
  Total_Investment_USD: number;
  Overall_ESG_Score: number;
  CO2_Reduction_Tonnes_Annual: number;
  Jobs_Created_Total: number;
  Region: string;
  Sector: string;
  Expected_ROI_Percent?: number;
  Beneficiaries_Direct?: number;
}

interface ProjectResultsProps {
  projects: Project[];
}

const ProjectResults = ({ projects }: ProjectResultsProps) => {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Selected Projects ({projects.length})</h3>
      </div>
      
      <div className="grid gap-4">
        {projects.map((project, index) => (
          <Card key={index} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <CardTitle className="text-lg">{project.Project_Name}</CardTitle>
                <Badge variant="secondary" className="ml-2">
                  ESG: {project.Overall_ESG_Score.toFixed(1)}
                </Badge>
              </div>
              <div className="flex items-center gap-4 text-sm text-gray-600">
                <div className="flex items-center gap-1">
                  <MapPin className="w-4 h-4" />
                  {project.Region}
                </div>
                <Badge variant="outline">{project.Sector}</Badge>
              </div>
            </CardHeader>
            
            <CardContent className="pt-0">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-green-600" />
                  <div>
                    <p className="text-sm font-medium">${(project.Total_Investment_USD / 1000000).toFixed(1)}M</p>
                    <p className="text-xs text-gray-500">Investment</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Leaf className="w-4 h-4 text-green-600" />
                  <div>
                    <p className="text-sm font-medium">{project.CO2_Reduction_Tonnes_Annual.toLocaleString()}</p>
                    <p className="text-xs text-gray-500">CO2 Reduction (t/year)</p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-blue-600" />
                  <div>
                    <p className="text-sm font-medium">{project.Jobs_Created_Total}</p>
                    <p className="text-xs text-gray-500">Jobs Created</p>
                  </div>
                </div>
                
                {project.Expected_ROI_Percent && (
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-purple-600" />
                    <div>
                      <p className="text-sm font-medium">{project.Expected_ROI_Percent}%</p>
                      <p className="text-xs text-gray-500">Expected ROI</p>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default ProjectResults;
