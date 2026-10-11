import { useState, useEffect } from 'react';
import { createFileRoute } from '@tanstack/react-router';
import { Sprout, AlertCircle, Sparkles } from 'lucide-react';
import { ImageUploader } from '../components/ImageUploader';
import { Preview } from '../components/Preview';
import { ResultCard } from '../components/ResultCard';
import {
  predictCropDisease,
  savePredictionToHistory,
  type PredictionResponse,
} from '../lib/api';

export const Route = createFileRoute('/')({
  component: HomeComponent,
});

function HomeComponent() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);

  // Handle file selection and object URL generation
  const handleSelectImage = (file: File) => {
    // Revoke previous object URL if any to free memory
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    setResult(null);
    setErrorMsg(null);
  };

  // Clear selected file
  const handleClearImage = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setErrorMsg(null);
  };

  // Clean up object URL on unmount
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  // Main Analyze action
  const handleAnalyze = async () => {
    // Exact requirement: Frontend handles "Select image first" alert if no file
    if (!selectedFile) {
      alert('Select image first');
      setErrorMsg('Please select or capture a crop leaf image first.');
      return;
    }

    setIsLoading(true);
    setErrorMsg(null);

    try {
      const data = await predictCropDisease(selectedFile);
      setResult(data);

      // Save to localStorage history
      savePredictionToHistory({
        ...data,
        filename: selectedFile.name,
        imageUrl: previewUrl || undefined,
      });
    } catch (err: any) {
      console.error('Prediction failed:', err);
      const message =
        err?.response?.data?.error ||
        err?.message ||
        'Unable to connect to Flask server. Ensure the backend is running at http://localhost:5000.';
      setErrorMsg(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full flex flex-col items-center justify-center py-4">
      {/* Centered card with max-width 600px - matching user dashboard specification */}
      <div className="w-full max-w-[600px] bg-white rounded-3xl shadow-md border border-gray-100 overflow-hidden">
        {/* Card Header */}
        <div className="bg-[#2e7d32] text-white p-6 sm:p-7">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-white/15 flex items-center justify-center border border-white/20">
              <Sprout className="w-7 h-7 text-green-200" />
            </div>
            <div>
              <h2 className="text-xl font-bold tracking-tight">
                Crop Disease Diagnosis
              </h2>
              <p className="text-xs text-green-100 mt-0.5">
                AI leaf analysis for Cassava, Maize, and Tomato
              </p>
            </div>
          </div>
        </div>

        {/* Card Body */}
        <div className="p-6 sm:p-8 space-y-6">
          {/* Target Crops Badge Bar */}
          <div className="flex flex-wrap gap-2 text-xs">
            <span className="px-2.5 py-1 rounded-full bg-[#e8f5e9] text-[#1b5e20] font-medium border border-green-200">
              Cassava (CMD)
            </span>
            <span className="px-2.5 py-1 rounded-full bg-[#e8f5e9] text-[#1b5e20] font-medium border border-green-200">
              Maize (Blight)
            </span>
            <span className="px-2.5 py-1 rounded-full bg-[#e8f5e9] text-[#1b5e20] font-medium border border-green-200">
              Tomato (Early Blight)
            </span>
            <span className="px-2.5 py-1 rounded-full bg-[#e8f5e9] text-[#1b5e20] font-medium border border-green-200">
              Healthy
            </span>
          </div>

          {/* Upload or Preview Display */}
          {!previewUrl || !selectedFile ? (
            <ImageUploader
              onImageSelected={handleSelectImage}
              disabled={isLoading}
            />
          ) : (
            <Preview
              previewUrl={previewUrl}
              file={selectedFile}
              onClear={handleClearImage}
              disabled={isLoading}
            />
          )}

          {/* Error message alert */}
          {errorMsg && (
            <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Analyze Button */}
          <div className="pt-2">
            <button
              type="button"
              onClick={handleAnalyze}
              disabled={isLoading}
              className="w-full py-3.5 px-6 rounded-xl font-bold text-white text-base bg-[#2e7d32] hover:bg-[#1b5e20] active:scale-[0.99] transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 cursor-pointer"
            >
              {isLoading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>Analyzing Leaf with MobileNetV2...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5 text-green-200" />
                  <span>Analyze Leaf Image</span>
                </>
              )}
            </button>
          </div>

          {/* Result Card Display */}
          {result && (
            <div className="pt-2 border-t border-gray-100">
              <ResultCard data={result} />

              <div className="mt-4 flex justify-center">
                <button
                  type="button"
                  onClick={handleClearImage}
                  className="text-xs font-semibold text-[#2e7d32] hover:text-[#1b5e20] underline transition-colors cursor-pointer"
                >
                  Analyze another leaf photo
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
