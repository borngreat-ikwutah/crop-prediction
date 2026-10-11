import { createFileRoute } from '@tanstack/react-router';
import {
  Sprout,
  Smartphone,
  Cpu,
  MapPin,
} from 'lucide-react';

export const Route = createFileRoute('/about')({
  component: AboutComponent,
});

function AboutComponent() {
  return (
    <div className="max-w-3xl mx-auto space-y-6 py-4">
      {/* Hero Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-gray-100">
        <div className="flex items-center gap-3 text-[#2e7d32] mb-3">
          <MapPin className="w-5 h-5" />
          <span className="text-xs font-bold uppercase tracking-wider">
            Enugu Agricultural Focus • Final Year Project
          </span>
        </div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900 tracking-tight">
          CropDisease Detection System
        </h2>
        <p className="mt-3 text-sm text-gray-600 leading-relaxed">
          An automated computer vision and deep learning diagnostic system designed to assist
          smallholder farmers, agricultural extension agents, and agronomists across Enugu State,
          Nigeria. The system identifies foliar diseases on vital food crops and provides practical,
          FAO-approved field treatments.
        </p>
      </div>

      {/* Target Crops & Pathologies */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-gray-100">
        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
          <Sprout className="w-5 h-5 text-[#2e7d32]" />
          Target Crop Pathologies
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-4 rounded-2xl bg-[#e8f5e9]/50 border border-green-200 space-y-1.5">
            <span className="font-bold text-[#1b5e20] text-sm block">
              1. Cassava Mosaic Disease (CMD)
            </span>
            <p className="text-gray-700">
              Major threat to cassava tubers in Eastern Nigeria. Transmitted by whiteflies (<em>Bemisia tabaci</em>) and infected stems.
            </p>
            <p className="text-[#2e7d32] font-medium pt-1">
              • Treatment: Resistant TMS 30572 cuttings, roguing, neem vector control.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#e8f5e9]/50 border border-green-200 space-y-1.5">
            <span className="font-bold text-[#1b5e20] text-sm block">
              2. Maize Leaf Blight
            </span>
            <p className="text-gray-700">
              Fungal disease (<em>Exserohilum turcicum</em>) causing elongated cigar lesions, drying corn leaves prematurely.
            </p>
            <p className="text-[#2e7d32] font-medium pt-1">
              • Treatment: Crop rotation with cowpea/soybean, Oba Super hybrids, Mancozeb.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#e8f5e9]/50 border border-green-200 space-y-1.5">
            <span className="font-bold text-[#1b5e20] text-sm block">
              3. Tomato Early Blight
            </span>
            <p className="text-gray-700">
              Fungal pathogen (<em>Alternaria solani</em>) producing distinctive concentric rings on lower leaves and stems.
            </p>
            <p className="text-[#2e7d32] font-medium pt-1">
              • Treatment: Bottom pruning, straw mulching, copper oxychloride sprays.
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-[#e8f5e9]/50 border border-green-200 space-y-1.5">
            <span className="font-bold text-[#1b5e20] text-sm block">
              4. Healthy Crop Foliage
            </span>
            <p className="text-gray-700">
              Normal vegetative growth without active lesions, maintaining baseline calibration for field scouting.
            </p>
            <p className="text-[#2e7d32] font-medium pt-1">
              • Advice: Routine scouting every 3-5 days, balanced NPK fertilizer.
            </p>
          </div>
        </div>
      </div>

      {/* Model & Architecture Details */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-gray-100 space-y-4">
        <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
          <Cpu className="w-5 h-5 text-[#2e7d32]" />
          Deep Learning Pipeline & Edge Architecture
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-100">
            <span className="font-semibold text-gray-900 block mb-1">
              MobileNetV2 Backbone
            </span>
            <p className="text-gray-600">
              Lightweight inverted residual blocks with depthwise separable convolutions optimized for mobile edge devices.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-100">
            <span className="font-semibold text-gray-900 block mb-1">
              TFLite Conversion
            </span>
            <p className="text-gray-600">
              Quantized model export under 10MB, enabling low-latency inference on low-cost smartphones without cloud GPU.
            </p>
          </div>

          <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-100">
            <span className="font-semibold text-gray-900 block mb-1">
              Enugu Farm Data
            </span>
            <p className="text-gray-600">
              Trained on PlantVillage and augmented with actual smartphone photos captured on local farms in Enugu.
            </p>
          </div>
        </div>
      </div>

      {/* Testing On Mobile Guide */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-sm border border-gray-100 space-y-3">
        <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
          <Smartphone className="w-5 h-5 text-[#2e7d32]" />
          Field Testing on Tecno / Android Phone
        </h3>
        <p className="text-xs text-gray-600 leading-relaxed">
          The Flask backend is configured to listen on <code className="bg-gray-100 px-1 py-0.5 rounded">0.0.0.0:5000</code>.
          To test from your smartphone:
        </p>
        <ol className="list-decimal list-inside text-xs text-gray-700 space-y-1.5 pl-1">
          <li>Connect both your laptop and Android phone to the same Wi-Fi network (or phone hotspot).</li>
          <li>Find your laptop's local IP address (e.g. <code>192.168.1.100</code>).</li>
          <li>Set <code className="bg-gray-100 px-1 py-0.5 rounded">VITE_API_URL=http://&lt;YOUR_IP&gt;:5000</code> in your environment.</li>
          <li>Open your phone browser and navigate to <code className="bg-gray-100 px-1 py-0.5 rounded">http://&lt;YOUR_IP&gt;:3000</code>.</li>
        </ol>
      </div>
    </div>
  );
}
