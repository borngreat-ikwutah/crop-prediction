import type { FC } from 'react';
import {
  AlertTriangle,
  Info,
  ShieldCheck,
  Percent,
} from 'lucide-react';
import { PredictionResponse } from '../lib/api';

interface ResultCardProps {
  data: PredictionResponse;
}

export const ResultCard: FC<ResultCardProps> = ({ data }) => {
  const isHealthy =
    data.disease.toLowerCase() === 'healthy' ||
    data.disease_name?.toLowerCase().includes('healthy');

  const confidenceValue = typeof data.confidence === 'number' ? data.confidence : parseFloat(data.confidence);

  return (
    <div className="w-full mt-6 bg-white rounded-2xl border border-green-200 shadow-lg overflow-hidden transition-all duration-300 animate-fadeIn">
      {/* Header status bar */}
      <div
        className={`px-6 py-4 flex items-center justify-between border-b ${
          isHealthy
            ? 'bg-[#e8f5e9] border-[#c8e6c9] text-[#1b5e20]'
            : 'bg-amber-50/80 border-amber-200 text-amber-900'
        }`}
      >
        <div className="flex items-center gap-2.5">
          {isHealthy ? (
            <ShieldCheck className="w-6 h-6 text-[#2e7d32]" />
          ) : (
            <AlertTriangle className="w-6 h-6 text-amber-600" />
          )}
          <span className="font-bold text-base">
            {isHealthy ? 'Diagnostic Result: Healthy Crop' : 'Diagnostic Result: Disease Detected'}
          </span>
        </div>

        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider ${
            isHealthy
              ? 'bg-[#2e7d32] text-white'
              : 'bg-amber-600 text-white'
          }`}
        >
          {data.crop || 'Crop Leaf'}
        </span>
      </div>

      <div className="p-6 space-y-5">
        {/* Core display matching legacy dashboard format:
            <b>Disease:</b> ${data.disease} <br>
            <b>Confidence:</b> ${data.confidence}% <br>
            <b>Treatment:</b> ${data.treatment}
        */}
        <div className="p-4 rounded-xl bg-gray-50 border border-gray-100 text-sm leading-relaxed text-gray-800 space-y-2">
          <div>
            <b>Disease:</b> <span className="text-gray-900 font-medium">{data.disease}</span>
            {data.disease_name && data.disease_name !== data.disease && (
              <span className="text-xs text-gray-500 block ml-0.5">
                ({data.disease_name})
              </span>
            )}
          </div>
          <div className="flex items-center gap-1.5">
            <b>Confidence:</b>
            <span className="font-semibold text-[#2e7d32]">{confidenceValue}%</span>
          </div>
          <div>
            <b>Treatment:</b>
            <div className="mt-1 whitespace-pre-line text-gray-700 font-normal">
              {data.treatment}
            </div>
          </div>
        </div>

        {/* Confidence Visual Meter */}
        <div className="space-y-1.5">
          <div className="flex justify-between items-center text-xs text-gray-600 font-medium">
            <span className="flex items-center gap-1">
              <Percent className="w-3.5 h-3.5 text-[#2e7d32]" />
              Model Confidence Rating
            </span>
            <span className="font-bold text-[#2e7d32]">{confidenceValue}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
            <div
              className={`h-2.5 rounded-full transition-all duration-700 ${
                confidenceValue >= 80
                  ? 'bg-[#2e7d32]'
                  : confidenceValue >= 60
                  ? 'bg-amber-500'
                  : 'bg-red-500'
              }`}
              style={{ width: `${Math.min(100, Math.max(5, confidenceValue))}%` }}
            />
          </div>
        </div>

        {/* Warnings for Blurry or Multi-Leaf captures */}
        {data.warnings && data.warnings.length > 0 && (
          <div className="p-4 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs space-y-1.5">
            <div className="flex items-center gap-2 font-semibold">
              <Info className="w-4 h-4 text-amber-600 flex-shrink-0" />
              <span>Image Quality Notice</span>
            </div>
            <ul className="list-disc list-inside space-y-1 pl-1">
              {data.warnings.map((warn, i) => (
                <li key={i}>{warn}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Multi-class probability breakdown if provided */}
        {data.all_probabilities && (
          <div className="pt-2 border-t border-gray-100">
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
              Class Distribution
            </p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              {Object.entries(data.all_probabilities).map(([cls, prob]) => (
                <div
                  key={cls}
                  className={`p-2 rounded-lg border ${
                    cls === data.disease
                      ? 'border-[#2e7d32] bg-[#e8f5e9]/50 font-semibold text-[#1b5e20]'
                      : 'border-gray-100 bg-gray-50 text-gray-600'
                  }`}
                >
                  <div className="truncate">{cls.replace(/_/g, ' ')}</div>
                  <div className="text-[11px] opacity-80">{prob}%</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
