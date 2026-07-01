import rawBirthPlaceTree from '@/data/chinaBirthPlaceTree.json';

export interface BirthPlaceDistrictOption {
  id: string;
  label: string;
  displayName: string;
  pinyin: string;
  longitude: number;
}

export interface BirthPlaceCityOption {
  id: string;
  label: string;
  displayName: string;
  pinyin: string;
  longitude: number;
  districts: BirthPlaceDistrictOption[];
}

export interface BirthPlaceProvinceOption {
  id: string;
  label: string;
  pinyin: string;
  longitude: number;
  cities: BirthPlaceCityOption[];
}

interface BirthPlaceCascadePath {
  province: BirthPlaceProvinceOption;
  city: BirthPlaceCityOption;
  district: BirthPlaceDistrictOption;
}

const birthPlaceTree = rawBirthPlaceTree as BirthPlaceProvinceOption[];

const districtPathById = new Map<string, BirthPlaceCascadePath>();
const districtPathByDisplayName = new Map<string, BirthPlaceCascadePath>();

for (const province of birthPlaceTree) {
  for (const city of province.cities) {
    for (const district of city.districts) {
      const path = { province, city, district };
      districtPathById.set(district.id, path);
      districtPathByDisplayName.set(district.displayName, path);
    }
  }
}

export function getBirthPlaceProvinceOptions(): BirthPlaceProvinceOption[] {
  return birthPlaceTree;
}

export function getBirthPlaceCityOptions(provinceId: string): BirthPlaceCityOption[] {
  return birthPlaceTree.find((province) => province.id === provinceId)?.cities || [];
}

export function getBirthPlaceDistrictOptions(cityId: string): BirthPlaceDistrictOption[] {
  for (const province of birthPlaceTree) {
    const city = province.cities.find((item) => item.id === cityId);
    if (city) {
      return city.districts;
    }
  }

  return [];
}

export function findBirthPlaceCascadeByDistrictId(
  districtId: string,
): BirthPlaceCascadePath | null {
  return districtPathById.get(districtId) || null;
}

export function findBirthPlaceCascadeByDisplayName(
  displayName: string,
): BirthPlaceCascadePath | null {
  return districtPathByDisplayName.get(displayName) || null;
}
