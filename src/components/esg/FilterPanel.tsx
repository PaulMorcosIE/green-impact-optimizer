
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Filter } from 'lucide-react';

interface FilterPanelProps {
  filters: Record<string, any>;
}

const FilterPanel = ({ filters }: FilterPanelProps) => {
  const formatFilterValue = (key: string, value: any) => {
    if (typeof value === 'string' && value.includes('<=')) {
      const amount = parseFloat(value.replace('<=', ''));
      return `≤ $${(amount / 1000000).toFixed(1)}M`;
    }
    if (typeof value === 'string' && value.includes('>=')) {
      const amount = parseFloat(value.replace('>=', ''));
      return `≥ ${amount}`;
    }
    return value;
  };

  const formatFilterKey = (key: string) => {
    return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Filter className="w-5 h-5" />
          Applied Filters
        </CardTitle>
      </CardHeader>
      <CardContent>
        {Object.keys(filters).length === 0 ? (
          <p className="text-gray-500">No specific filters were applied</p>
        ) : (
          <div className="space-y-3">
            {Object.entries(filters).map(([key, value]) => (
              <div key={key} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <span className="font-medium text-gray-700">{formatFilterKey(key)}</span>
                <Badge variant="secondary">{formatFilterValue(key, value)}</Badge>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FilterPanel;
