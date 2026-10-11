import { useRef, useState, type FC } from 'react';
import { UploadCloud, Camera, Image as ImageIcon } from 'lucide-react';

interface ImageUploaderProps {
  onImageSelected: (file: File) => void;
  disabled?: boolean;
}

export const ImageUploader: FC<ImageUploaderProps> = ({
  onImageSelected,
  disabled = false,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Please upload a valid image file (JPEG, PNG, WebP).');
      return;
    }
    onImageSelected(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  return (
    <div className="w-full">
      {/* Standard file picker input */}
      <input
        type="file"
        ref={fileInputRef}
        accept="image/*"
        className="hidden"
        disabled={disabled}
        onChange={(e) => {
          if (e.target.files && e.target.files.length > 0) {
            handleFile(e.target.files[0]);
          }
        }}
      />

      {/* Direct mobile camera capture input for Tecno / Android */}
      <input
        type="file"
        ref={cameraInputRef}
        accept="image/*"
        capture="environment"
        className="hidden"
        disabled={disabled}
        onChange={(e) => {
          if (e.target.files && e.target.files.length > 0) {
            handleFile(e.target.files[0]);
          }
        }}
      />

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => !disabled && fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-2xl p-6 md:p-8 text-center transition-all cursor-pointer ${
          isDragging
            ? 'border-[#2e7d32] bg-[#e8f5e9]/80 scale-[1.01]'
            : 'border-green-200 hover:border-[#2e7d32] bg-[#e8f5e9]/30 hover:bg-[#e8f5e9]/50'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <div className="flex flex-col items-center justify-center space-y-3">
          <div className="w-16 h-16 rounded-full bg-white shadow-sm flex items-center justify-center text-[#2e7d32]">
            <UploadCloud className="w-8 h-8" />
          </div>

          <div>
            <p className="text-base font-semibold text-gray-800">
              Upload leaf image or drop here
            </p>
            <p className="text-xs text-gray-500 mt-1">
              Supports JPG, PNG, WebP • Max 10MB
            </p>
          </div>

          <div className="flex items-center gap-3 pt-2">
            <button
              type="button"
              disabled={disabled}
              onClick={(e) => {
                e.stopPropagation();
                fileInputRef.current?.click();
              }}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-white border border-gray-200 text-gray-700 shadow-sm hover:bg-gray-50"
            >
              <ImageIcon className="w-3.5 h-3.5 text-[#2e7d32]" />
              Browse Gallery
            </button>

            <button
              type="button"
              disabled={disabled}
              onClick={(e) => {
                e.stopPropagation();
                cameraInputRef.current?.click();
              }}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-[#2e7d32] text-white shadow-sm hover:bg-[#1b5e20]"
            >
              <Camera className="w-3.5 h-3.5" />
              Take Photo (Phone)
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
