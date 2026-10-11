import { useEffect, useState } from 'react';
import {
  createRootRoute,
  Link,
  Outlet,
  useRouterState,
} from '@tanstack/react-router';
import {
  Sprout,
  History as HistoryIcon,
  Info,
  Home as HomeIcon,
  Wifi,
  WifiOff,
} from 'lucide-react';
import { checkBackendHealth, API_BASE_URL } from '../lib/api';

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  const [backendStatus, setBackendStatus] = useState<
    'checking' | 'connected' | 'offline'
  >('checking');
  const routerState = useRouterState();
  const currentPath = routerState.location.pathname;

  useEffect(() => {
    let isMounted = true;
    checkBackendHealth()
      .then(() => {
        if (isMounted) setBackendStatus('connected');
      })
      .catch(() => {
        if (isMounted) setBackendStatus('offline');
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#f4f7f4] text-gray-800">
      {/* Top Banner Navigation */}
      <header className="sticky top-0 z-50 bg-[#2e7d32] text-white shadow-md">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo & Project Title */}
            <Link
              to="/"
              className="flex items-center gap-2.5 hover:opacity-95 transition-opacity"
            >
              <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center border border-white/20">
                <Sprout className="w-6 h-6 text-green-200" />
              </div>
              <div>
                <h1 className="font-bold text-base sm:text-lg leading-tight">
                  CropDisease Detection
                </h1>
                <p className="text-[11px] text-green-100 font-light">
                  Enugu Focus • Cassava, Maize, Tomato
                </p>
              </div>
            </Link>

            {/* Navigation Links */}
            <nav className="flex items-center gap-1 sm:gap-2">
              <Link
                to="/"
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                  currentPath === '/'
                    ? 'bg-white/20 text-white shadow-inner'
                    : 'text-green-100 hover:bg-white/10 hover:text-white'
                }`}
              >
                <HomeIcon className="w-4 h-4" />
                <span className="hidden sm:inline">Home</span>
              </Link>

              <Link
                to="/history"
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                  currentPath === '/history'
                    ? 'bg-white/20 text-white shadow-inner'
                    : 'text-green-100 hover:bg-white/10 hover:text-white'
                }`}
              >
                <HistoryIcon className="w-4 h-4" />
                <span className="hidden sm:inline">History</span>
              </Link>

              <Link
                to="/about"
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors ${
                  currentPath === '/about'
                    ? 'bg-white/20 text-white shadow-inner'
                    : 'text-green-100 hover:bg-white/10 hover:text-white'
                }`}
              >
                <Info className="w-4 h-4" />
                <span className="hidden sm:inline">About</span>
              </Link>
            </nav>
          </div>
        </div>

        {/* Backend connectivity indicator badge */}
        <div className="bg-[#1b5e20] px-4 py-1 text-[11px] text-green-100 flex items-center justify-between max-w-5xl mx-auto">
          <span>Final Year Project • Enugu State Agricultural Diagnostics</span>
          <div className="flex items-center gap-1.5">
            {backendStatus === 'connected' ? (
              <>
                <Wifi className="w-3 h-3 text-emerald-300" />
                <span className="text-emerald-300 font-medium">Flask API Online</span>
              </>
            ) : backendStatus === 'offline' ? (
              <>
                <WifiOff className="w-3 h-3 text-amber-300" />
                <span className="text-amber-300 font-medium">
                  API Offline ({API_BASE_URL})
                </span>
              </>
            ) : (
              <span className="text-green-300">Checking API...</span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content View */}
      <main className="flex-1 max-w-5xl w-full mx-auto px-4 py-6 sm:px-6 sm:py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-6 text-center text-xs text-gray-500">
        <p className="max-w-md mx-auto px-4">
          Developed for smallholder farmers in Enugu State. Powered by MobileNetV2 Transfer Learning &amp; TFLite edge deployment.
        </p>
      </footer>
    </div>
  );
}
