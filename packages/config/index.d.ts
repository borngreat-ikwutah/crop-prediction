export declare const CROP_CLASSES: readonly [
  'Cassava_Mosaic',
  'Maize_Blight',
  'Tomato_Early_Blight',
  'Healthy'
];

export type CropClass = (typeof CROP_CLASSES)[number];

export declare const CROP_DISPLAY_NAMES: Record<CropClass, string>;

export declare const DEFAULT_API_URL: string;
export declare const DEFAULT_API_PORT: number;
export declare const DEFAULT_WEB_PORT: number;
export declare const MODEL_INPUT_SIZE: number;

export declare const THEME_COLORS: {
  readonly primary: string;
  readonly primaryDark: string;
  readonly primaryLight: string;
  readonly bgLight: string;
  readonly surface: string;
  readonly accent: string;
};
