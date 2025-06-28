
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';

interface WeightingPanelProps {
  weights: Record<string, number>;
  defaultWeights: Record<string, number>;
  onWeightsChange: (weights: Record<string, number>) => void;
}

const WeightingPanel = ({ weights, defaultWeights, onWeightsChange }: WeightingPanelProps) => {
  const handleWeightChange = (key: string, value: number[]) => {
    onWeightsChange({
      ...weights,
      [key]: value[0]
    });
  };

  const formatLabel = (key: string) => {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  const getCurrentWeight = (key: string) => {
    return weights[key] !== undefined ? weights[key] : defaultWeights[key];
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Scoring Weights (%)</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {Object.keys(defaultWeights).map((key) => (
          <div key={key} className="space-y-2">
            <div className="flex justify-between">
              <Label className="text-sm">{formatLabel(key)}</Label>
              <span className="text-sm font-medium">{getCurrentWeight(key)}%</span>
            </div>
            <Slider
              value={[getCurrentWeight(key)]}
              onValueChange={(value) => handleWeightChange(key, value)}
              max={50}
              min={0}
              step={1}
              className="w-full"
            />
          </div>
        ))}
        <div className="text-xs text-gray-500 mt-4">
          Total: {Object.values(weights).reduce((sum, val) => sum + (val || 0), 0) || 
                  Object.values(defaultWeights).reduce((sum, val) => sum + val, 0)}%
        </div>
      </CardContent>
    </Card>
  );
};

export default WeightingPanel;
