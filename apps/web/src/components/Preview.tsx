import type { FC } from 'react';
import { X, RefreshCw } from 'lucide-react';

interface PreviewProps {
  previewUrl: string;
  file: File;
  onClear: () => void;
  disabled?: boolean;
}

export const Preview: FC<PreviewProps> = ({
  previewUrl,
  file,
  onClear,
  disabled = false,
}) => {
  const formatSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="w-full relative rounded-2xl overflow-hidden border border-green-200 bg-white shadow-sm">
      <div className="relative aspect-[4/3] w-full max-h-[360px] bg-black/5 flex items-center justify-center overflow-hidden">
        <img
          src={previewUrl}
          alt="Selected crop leaf preview"
          className="w-full h-full object-contain"
        />

        {!disabled && (
          <button
            type="button"
            onClick={onClear}
            aria-label="Remove image"
            className="absolute top-3 right-3 p-1.5 rounded-full bg-black/60 text-white hover:bg-black/80 transition-colors shadow-md backdrop-blur-sm cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="px-4 py-3 bg-[#e8f5e9]/40 border-t border-green-100 flex items-center justify-between text-xs text-gray-700">
        <div className="truncate pr-2">
          <span className="font-semibold text-gray-900 block truncate">
            {file.name}
          </span>
          <span className="text-gray-500">{formatSize(file.size)}</span>
        </div>

        {!disabled && (
          <button
            type="button"
            onClick={onClear}
            className="inline-flex items-center gap-1 text-[#2e7d32] hover:text-[#1b5e20] font-medium transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            Change
          </button>
        )}
      </div>
    </div>
  );
};
