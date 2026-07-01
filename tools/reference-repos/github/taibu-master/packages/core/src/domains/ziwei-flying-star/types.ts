import type {
  BirthTimeInput,
  FlyingStarActualFlight,
  FlyingStarQuery,
  Gender,
  MutagedPlaceInfo,
  SurroundedPalaceInfo
} from '../shared/types.js';

// ===== 紫微飞星类型 =====

export interface ZiweiFlyingStarInput extends BirthTimeInput {
  gender: Gender;
  longitude?: number;
  queries: FlyingStarQuery[];
}

export interface ZiweiFlyingStarOutput {
  results: FlyingStarResult[];
}

export interface FlyingStarResult {
  queryIndex: number;
  type: string;
  result: boolean | MutagedPlaceInfo[] | SurroundedPalaceInfo;
  queryTarget?: {
    fromPalace?: string;
    toPalace?: string;
    palace?: string;
    mutagens?: string[];
  };
  sourcePalaceGanZhi?: string;
  actualFlights?: FlyingStarActualFlight[];
}
