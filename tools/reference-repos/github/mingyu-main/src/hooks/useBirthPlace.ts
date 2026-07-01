import {
  useCallback,
  useEffect,
  useMemo,
  useState,
  type Dispatch,
  type SetStateAction,
} from 'react';
import type { PersonRole } from '@/lib/input-labels';
import type { QueryInputState } from '@/lib/query-state';
import { resolveBirthPlaceLatitude } from '@/utils/core/birthPlaceCoordinates';

type BirthPlaceCascadeModule = typeof import('@/utils/core/birthPlaceCascade');

const SELF_PLACE_KEYS = {
  birthPlace: 'birthPlace',
  birthLongitude: 'birthLongitude',
  birthLatitude: 'birthLatitude',
} as const;

const PARTNER_PLACE_KEYS = {
  birthPlace: 'partnerBirthPlace',
  birthLongitude: 'partnerBirthLongitude',
  birthLatitude: 'partnerBirthLatitude',
} as const;

function getPlaceFieldKey(role: PersonRole, key: keyof typeof SELF_PLACE_KEYS) {
  return role === 'self' ? SELF_PLACE_KEYS[key] : PARTNER_PLACE_KEYS[key];
}

export interface UseBirthPlaceOptions {
  form: QueryInputState;
  setForm: Dispatch<SetStateAction<QueryInputState>>;
}

export function useBirthPlace({ form, setForm }: UseBirthPlaceOptions) {
  const [isBirthPlaceModalOpen, setIsBirthPlaceModalOpen] = useState(false);
  const [activeBirthPlaceTarget, setActiveBirthPlaceTarget] = useState<PersonRole>('self');
  const [birthPlaceSearch, setBirthPlaceSearch] = useState('');
  const [draftProvinceId, setDraftProvinceId] = useState('');
  const [draftCityId, setDraftCityId] = useState('');
  const [draftDistrictId, setDraftDistrictId] = useState('');
  const [birthPlaceCascadeModule, setBirthPlaceCascadeModule] =
    useState<BirthPlaceCascadeModule | null>(null);
  const [isBirthPlaceDataLoading, setIsBirthPlaceDataLoading] = useState(false);

  const provinceOptions = useMemo(
    () => birthPlaceCascadeModule?.getBirthPlaceProvinceOptions() ?? [],
    [birthPlaceCascadeModule],
  );
  const cityOptions = useMemo(
    () => birthPlaceCascadeModule?.getBirthPlaceCityOptions(draftProvinceId) ?? [],
    [birthPlaceCascadeModule, draftProvinceId],
  );
  const districtOptions = useMemo(
    () => birthPlaceCascadeModule?.getBirthPlaceDistrictOptions(draftCityId) ?? [],
    [birthPlaceCascadeModule, draftCityId],
  );

  const ensureBirthPlaceCascadeModule = useCallback(async () => {
    if (birthPlaceCascadeModule) {
      return birthPlaceCascadeModule;
    }

    setIsBirthPlaceDataLoading(true);
    try {
      const module = await import('@/utils/core/birthPlaceCascade');
      setBirthPlaceCascadeModule(module);
      return module;
    } finally {
      setIsBirthPlaceDataLoading(false);
    }
  }, [birthPlaceCascadeModule]);

  useEffect(() => {
    if (!isBirthPlaceModalOpen || birthPlaceCascadeModule) {
      return;
    }

    void ensureBirthPlaceCascadeModule();
  }, [birthPlaceCascadeModule, ensureBirthPlaceCascadeModule, isBirthPlaceModalOpen]);

  useEffect(() => {
    if (!birthPlaceCascadeModule) {
      return;
    }

    const placeKey = getPlaceFieldKey(activeBirthPlaceTarget, 'birthPlace');
    const birthPlace = String(form[placeKey] || '');
    const matched = birthPlace
      ? birthPlaceCascadeModule.findBirthPlaceCascadeByDisplayName(birthPlace)
      : null;

    setDraftProvinceId(matched?.province.id || '');
    setDraftCityId(matched?.city.id || '');
    setDraftDistrictId(matched?.district.id || '');
  }, [activeBirthPlaceTarget, birthPlaceCascadeModule, form]);

  useEffect(() => {
    if (!isBirthPlaceModalOpen || birthPlaceSearch) {
      return;
    }

    const timer = window.setTimeout(() => {
      document
        .getElementById(`birth-place-province-${draftProvinceId}`)
        ?.scrollIntoView({ block: 'center', inline: 'nearest' });
      document
        .getElementById(`birth-place-city-${draftCityId}`)
        ?.scrollIntoView({ block: 'center', inline: 'nearest' });
      document
        .getElementById(`birth-place-district-${draftDistrictId}`)
        ?.scrollIntoView({ block: 'center', inline: 'nearest' });
    }, 30);

    return () => window.clearTimeout(timer);
  }, [birthPlaceSearch, draftCityId, draftDistrictId, draftProvinceId, isBirthPlaceModalOpen]);

  const filteredDistrictResults = useMemo(() => {
    const query = birthPlaceSearch.trim().toLowerCase();
    if (!query) {
      return [];
    }

    const results: Array<{
      districtId: string;
      provinceLabel: string;
      cityLabel: string;
      districtLabel: string;
    }> = [];

    for (const province of provinceOptions) {
      for (const city of province.cities) {
        for (const district of city.districts) {
          const text = [
            province.label,
            city.label,
            district.label,
            district.displayName,
            district.pinyin,
          ]
            .join('|')
            .toLowerCase();

          if (!text.includes(query)) {
            continue;
          }

          results.push({
            districtId: district.id,
            provinceLabel: province.label,
            cityLabel: city.label,
            districtLabel: district.label,
          });

          if (results.length >= 60) {
            return results;
          }
        }
      }
    }

    return results;
  }, [birthPlaceSearch, provinceOptions]);

  function openBirthPlaceModal(role: PersonRole) {
    setActiveBirthPlaceTarget(role);
    setBirthPlaceSearch('');
    setIsBirthPlaceModalOpen(true);
    void ensureBirthPlaceCascadeModule();
  }

  function closeBirthPlaceModal() {
    setBirthPlaceSearch('');
    setIsBirthPlaceModalOpen(false);
  }

  function handleProvinceSelect(provinceId: string) {
    setDraftProvinceId(provinceId);
    setDraftCityId('');
    setDraftDistrictId('');
  }

  function handleCitySelect(cityId: string) {
    setDraftCityId(cityId);
    setDraftDistrictId('');
  }

  function handleDistrictSelect(districtId: string) {
    setDraftDistrictId(districtId);
  }

  function selectDistrictFromSearch(districtId: string) {
    const matched = birthPlaceCascadeModule?.findBirthPlaceCascadeByDistrictId(districtId) ?? null;
    if (!matched) {
      return;
    }

    setDraftProvinceId(matched.province.id);
    setDraftCityId(matched.city.id);
    setDraftDistrictId(matched.district.id);
    setBirthPlaceSearch('');
  }

  function confirmBirthPlaceSelection() {
    const matched =
      draftDistrictId && birthPlaceCascadeModule
        ? birthPlaceCascadeModule.findBirthPlaceCascadeByDistrictId(draftDistrictId)
        : null;
    if (!matched) {
      return;
    }

    setForm((current) => {
      const next = { ...current };
      const placeKey = getPlaceFieldKey(activeBirthPlaceTarget, 'birthPlace');
      const longitudeKey = getPlaceFieldKey(activeBirthPlaceTarget, 'birthLongitude');
      const latitudeKey = getPlaceFieldKey(activeBirthPlaceTarget, 'birthLatitude');
      next[placeKey] = matched.district.displayName as never;
      next[longitudeKey] = String(matched.district.longitude) as never;
      next[latitudeKey] = String(resolveBirthPlaceLatitude(matched.district.id)) as never;
      return next;
    });
    closeBirthPlaceModal();
  }

  const draftSummary = `${provinceOptions.find((item) => item.id === draftProvinceId)?.label || '未选择省份'} / ${
    cityOptions.find((item) => item.id === draftCityId)?.label || '未选择城市'
  } / ${districtOptions.find((item) => item.id === draftDistrictId)?.label || '未选择区县'}`;

  return {
    isBirthPlaceModalOpen,
    isBirthPlaceDataLoading,
    birthPlaceSearch,
    setBirthPlaceSearch,
    draftProvinceId,
    draftCityId,
    draftDistrictId,
    provinceOptions,
    cityOptions,
    districtOptions,
    filteredDistrictResults,
    draftSummary,
    openBirthPlaceModal,
    closeBirthPlaceModal,
    handleProvinceSelect,
    handleCitySelect,
    handleDistrictSelect,
    selectDistrictFromSearch,
    confirmBirthPlaceSelection,
  };
}
