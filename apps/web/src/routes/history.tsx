import { useState, useEffect } from 'react';
import { createFileRoute, Link } from '@tanstack/react-router';
import {
  History as HistoryIcon,
  Trash2,
  Sprout,
  ShieldCheck,
  AlertTriangle,
  ArrowRight,
  Calendar,
} from 'lucide-react';
import {
  getPredictionHistory,
  clearPredictionHistory,
  HistoryItem,
} from '../lib/api';

export const Route = createFileRoute('/history')({
  component: HistoryComponent,
});

function HistoryComponent() {
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    setHistory(getPredictionHistory());
  }, []);

  const handleClear = () => {
    if (confirm('Are you sure you want to clear your prediction history?')) {
      clearPredictionHistory();
      setHistory([]);
    }
  };

  const formatDate = (isoString: string) => {
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return isoString;
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 py-4">
      {/* Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-gray-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-[#2e7d32] mb-1">
            <HistoryIcon className="w-5 h-5" />
            <h2 className="text-xl sm:text-2xl font-bold text-gray-900">
              Prediction History
            </h2>
          </div>
          <p className="text-xs text-gray-500">
            Stored locally in your browser/device session
          </p>
        </div>

        {history.length > 0 && (
          <button
            type="button"
            onClick={handleClear}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold text-red-700 bg-red-50 hover:bg-red-100 border border-red-200 transition-colors self-start sm:self-auto cursor-pointer"
          >
            <Trash2 className="w-3.5 h-3.5" />
            Clear History
          </button>
        )}
      </div>

      {/* History Items List */}
      {history.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-gray-100 shadow-sm space-y-4">
          <div className="w-16 h-16 rounded-full bg-[#e8f5e9] flex items-center justify-center text-[#2e7d32] mx-auto">
            <Sprout className="w-8 h-8" />
          </div>
          <div>
            <h3 className="text-base font-bold text-gray-800">
              No Past Predictions Yet
            </h3>
            <p className="text-xs text-gray-500 mt-1 max-w-sm mx-auto">
              Diagnose your first crop leaf on the home page. Results will automatically be saved here.
            </p>
          </div>
          <Link
            to="/"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-[#2e7d32] hover:bg-[#1b5e20] text-white text-xs font-bold shadow-md transition-colors"
          >
            <span>Scan Leaf Now</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item) => {
            const isHealthy =
              item.disease.toLowerCase() === 'healthy' ||
              item.disease_name?.toLowerCase().includes('healthy');

            return (
              <div
                key={item.id}
                className="bg-white rounded-2xl border border-gray-100 p-5 shadow-sm hover:border-green-200 transition-all flex flex-col sm:flex-row gap-4"
              >
                {/* Thumbnail or Icon */}
                <div className="w-full sm:w-28 sm:h-28 rounded-xl bg-gray-100 overflow-hidden flex-shrink-0 flex items-center justify-center border border-gray-200">
                  {item.imageUrl ? (
                    <img
                      src={item.imageUrl}
                      alt={item.disease}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <Sprout className="w-8 h-8 text-[#2e7d32]/50" />
                  )}
                </div>

                {/* Details */}
                <div className="flex-1 space-y-2">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      {isHealthy ? (
                        <ShieldCheck className="w-4 h-4 text-[#2e7d32]" />
                      ) : (
                        <AlertTriangle className="w-4 h-4 text-amber-600" />
                      )}
                      <span className="font-bold text-sm sm:text-base text-gray-900">
                        {item.disease_name || item.disease}
                      </span>
                    </div>

                    <span
                      className={`text-xs px-2.5 py-0.5 rounded-full font-semibold ${
                        isHealthy
                          ? 'bg-[#e8f5e9] text-[#1b5e20]'
                          : 'bg-amber-50 text-amber-800 border border-amber-200'
                      }`}
                    >
                      {item.confidence}% confidence
                    </span>
                  </div>

                  <div className="text-xs text-gray-600 line-clamp-2">
                    <b>Treatment:</b> {item.short_treatment || item.treatment}
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-gray-50 text-[11px] text-gray-400">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {formatDate(item.timestamp)}
                    </span>
                    <span>{item.filename}</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
