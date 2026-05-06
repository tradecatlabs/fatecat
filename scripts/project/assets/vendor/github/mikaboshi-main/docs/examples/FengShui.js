/**
 * A context provider to load a WASM app ("voi-feng-shui" in our case).
 * Once `FengShuiContext` is set in the parent component, you can use
 * `useFengShui` in child components to access the given properties.
 * To start with, it requies data in `profile`, however, `profile`
 * is managed in `ProfilesProvider`. For two providers cannot
 * communicate to each other, we have `useFengShuiSync`
 * to serve the purpose. For any components handling `profile`,
 * we run `useFengShuiSync` in there, and it will automatically
 * @namespace FengShui
 */

import React, {
  useContext,
  createContext,
  useEffect,
  useState,
  useCallback,
  useRef,
} from 'react';

import moment from 'moment';
import init, {
  // 八卦 (Ba-Gua)
  get_gua_compass_order as wasm_get_gua_compass_order,
  // 二十四山向 (Er-Shi Si-Shan Xiang)
  get_twentyfour_direction_from_index as wasm_get_twentyfour_direction_from_index,
  get_twentyfour_direction_from_degrees as wasm_get_twentyfour_direction_from_degrees,
  get_twentyfour_data_from_index as wasm_get_twentyfour_data_from_index,
  get_twentyfour_data_from_direction as wasm_get_twentyfour_data_from_direction,
  // 干支 (Gan-Zhi)
  get_bazi as wasm_get_bazi,
  get_lichun as wasm_get_lichun,
  // 九星 (Jiu-Xings)
  get_jiuxing_from_index as wasm_get_jiuxing_from_index,
  get_unpan_xing_index as wasm_get_unpan_xing_index,
  get_xiaguatu_from_unpan_index as wasm_get_xiaguatu_from_unpan_index,
  get_jiuxing_dipan_positions_from_direction as wasm_get_jiuxing_dipan_positions_from_direction,
  // 生死衰旺 (Sheng-Si Shuai-Wang)
  get_shengsi_mapping as wasm_get_shengsi_mapping,
} from 'voi-feng-shui';

import { DATETIME_FORMAT, BAZI_TYPE_KEYS, GANZHI_TYPE_KEYS } from '@/constants';
import { int, noop, get_utc_offset_in_hours } from '@/lib/utils';

import {
  useProfiles,
  get_first_valid_profile_from_profiles,
} from '@/contexts/Profiles';

const WASM_PATH =
  NODE_ENV === 'production'
    ? 'wasm/voi-feng-shui/voi-feng-shui_bg.wasm'
    : void 0;

const DATETIME_KEYS = Object.keys(DATETIME_FORMAT);
const DATE_KEYS = DATETIME_KEYS.filter(
  key =>
    key.indexOf('year') > -1 ||
    key.indexOf('month') > -1 ||
    key.indexOf('day') > -1
);

/** @public */
export const has_valid_profile = (p = {}) =>
  p.localtime && p.direction && p.sector;

// ----------------------------------------------------------------
// FengShuiContext
// ----------------------------------------------------------------

/**
 * @typedef FengShui.FengShuiContext
 * @property {boolean} ready
 * @property {Object} profile
 * @property {Object} bazi
 * @property {Object} lichun
 * @property {Object} unpan_xing
 * @property {Object} shan_xing
 * @property {Object} xiang_xing
 * @property {Function} update
 * @property {FengShui.FengShuiContext.get_gua_compass_order}
 * @property {FengShui.FengShuiContext.get_direction_positions_in_chart} - NOT IN USE
 * @property {FengShui.FengShuiContext.get_opposite_direction} - NOT IN USE
 * @property {FengShui.FengShuiContext.get_twentyfour_direction_from_index}
 * @property {FengShui.FengShuiContext.get_twentyfour_direction_from_degrees}
 * @property {FengShui.FengShuiContext.get_twentyfour_data_from_index}
 * @property {FengShui.FengShuiContext.get_twentyfour_data_from_direction}
 * @property {FengShui.FengShuiContext.get_bazi} get_bazi
 * @property {FengShui.FengShuiContext.get_lichun} get_lichun
 * @property {FengShui.FengShuiContext.get_unpan_xing_index}
 * @property {FengShui.FengShuiContext.get_jiuxing_from_index}
 * @property {FengShui.FengShuiContext.get_xiaguatu_from_unpan_index}
 * @property {FengShui.FengShuiContext.get_jiuxing_dipan_positions_from_direction}
 * @property {FengShui.FengShuiContext.get_shengsi_mapping}
 */
const FengShuiContext = createContext({
  ready: false,
  profile: null, // localtime, direction, sector
  bazi: null,
  lichun: null,
  unpan_xing: null, // 運盤星
  shan_xing: null, // 山星
  xiang_xing: null, // 向星
  update: noop,

  // 八卦 (Ba-Gua)
  get_gua_compass_order: noop,

  // 二十四山向 (Er-Shi Si-Shan Xiang)
  get_twentyfour_direction_from_index: noop,
  get_twentyfour_direction_from_degrees: noop,
  get_twentyfour_data_from_index: noop,
  get_twentyfour_data_from_direction: noop,

  // 干支 (Gan-Zhi)
  get_bazi: noop,
  get_lichun: noop,

  // 九星 (Jiu-Xings)
  unpan_xing_index: noop,
  get_xiaguatu_from_unpan_index: noop,
  get_jiuxing_dipan_positions_from_direction: noop,

  // 生死衰旺 (Sheng-Si Shuai-Wang)
  get_shengsi_mapping: noop,
});

// ----------------------------------------------------------------
// FengShuiProvider
// ----------------------------------------------------------------

/**
 * @typedef FengShui.FengShuiProvider
 * @function
 */
export const FengShuiProvider = props => {
  const [ready, setReady] = useState(false);
  const [profile, setProfile] = useState(null);
  const [bazi, setBazi] = useState(null);
  const [lichun, setLiChun] = useState(null);
  const [unpan_xing, setUnPanXing] = useState(null);
  const [shan_xing, setShanXing] = useState(null);
  const [xiang_xing, setXiangXing] = useState(null);

  // ================================================================
  // 八卦 (Bagua)
  // ================================================================

  /**
   * A simple accessor for values stored in `BAGUA_START_NORTH`.
   * @typedef FengShui.FengShuiContext.get_gua_compass_order
   * @function
   */

  /**
   * @type {FengShui.FengShuiContext.get_gua_compass_order}
   */
  const get_gua_compass_order = useCallback(
    dir => {
      return ready && wasm_get_gua_compass_order(dir);
    },
    [ready]
  );

  // ================================================================
  // 二十四山向 (Er-Shi Si-Shan Xiang)
  // ================================================================

  /**
   * From the index, returns `Direction`.
   * @typedef FengShui.FengShuiContext.get_twentyfour_direction_from_index
   * @function
   * @param {number} [index]
   * @returns {Object} - { direction, sector }
   */

  /**
   * @type {FengShui.FengShuiContext.get_twentyfour_direction_from_index}
   */
  const get_twentyfour_direction_from_index = useCallback(
    index => {
      return ready && wasm_get_twentyfour_direction_from_index(index);
    },
    [ready]
  );

  /**
   * From `degrees`, returns `Direction` (for 二十四山向; Er-Shi Si-Shan Xiang).
   * @typedef FengShui.FengShuiContext.get_twentyfour_direction_from_degrees
   * @function
   * @param {number} [degrees=0]
   * @returns {Object} - { direction, sector }
   */

  /**
   * @type {FengShui.FengShuiContext.get_twentyfour_direction_from_degrees}
   */
  const get_twentyfour_direction_from_degrees = useCallback(
    degrees => {
      return ready && wasm_get_twentyfour_direction_from_degrees(degrees);
    },
    [ready]
  );

  /**
   * From index, returns `TwentyFourType`.
   * @typedef FengShui.FengShuiContext.get_twentyfour_data_from_index
   * @function
   * @param {number} [index]
   * @returns {Bagua|Stem|Branch} - TwentyFourType
   */

  /**
   * @type {FengShui.FengShuiContext.get_twentyfour_data_from_index}
   */
  const get_twentyfour_data_from_index = useCallback(
    index => {
      return ready && wasm_get_twentyfour_data_from_index(index);
    },
    [ready]
  );

  /**
   * From `direction`, returns `TwentyFourType`.
   * @typedef FengShui.FengShuiContext.get_twentyfour_data_from_direction
   * @function
   * @param {number} [index]
   * @returns {Bagua|Stem|Branch} - TwentyFourType
   */

  /**
   * @type {FengShui.FengShuiContext.get_twentyfour_data_from_direction}
   */
  const get_twentyfour_data_from_direction = useCallback(
    (dir, sec) => {
      return ready && wasm_get_twentyfour_data_from_direction(dir, sec);
    },
    [ready]
  );

  // ================================================================
  // 干支 (Gan-Zhi)
  // ================================================================

  /**
   * From `t` (localtime), calculates for 八字 (Bazi).
   * Internally mapped to: get_bazi
   * @typedef FengShui.FengShuiContext.get_bazi
   * @function
   * @param {Object} [t] - localtime (as a momemt object)
   * @returns {Object} - Bazi
   */

  /** @type {FengShui.FengShuiContext.get_bazi} */
  const get_bazi = useCallback(
    t => {
      return (
        ready &&
        normalize_bazi_data(wasm_get_bazi(datetime_params_from_localtime(t)))
      );
    },
    [ready]
  );

  /**
   * From `year`, calculates for 立春 (Li-Chun).
   * Internally mapped to: get_lichun
   * @typedef FengShui.FengShuiContext.get_lichun
   * @function
   * @param {number} [y] - year
   * @returns {string} - Li-Chun
   */

  /** @type {FengShui.FengShuiContext.get_lichun} */
  const get_lichun = useCallback(
    y => {
      return ready && y && wasm_get_lichun(~~y);
    },
    [ready]
  );

  // ================================================================
  // 九星 (Jiu-Xing)
  // ================================================================

  /**
   * A simple accessor for values stored in `JIU_XING`.
   * @typedef FengShui.FengShuiContext.get_jiuxing_from_index
   * @function
   * @param {Object} [index] - Jiu-Xing index
   * @returns {Object} - JiuXing
   */

  /** @type {FengShui.FengShuiContext.get_jiuxing_from_index} */
  const get_jiuxing_from_index = useCallback(
    index => {
      return ready && wasm_get_jiuxing_from_index(index);
    },
    [ready]
  );

  /**
   * From: (1) `current` (current localtime), and
   * (2) `lichun` (立春 (Li-Chun) for the year),
   * returns 運盤星 (Un-Pan Xing) index.
   * @typedef FengShui.FengShuiContext.get_unpan_xing_index
   * @function
   * @param {Object} [current] - Current localtime
   * @param {Object} [lichun] - Li-Chun (for the year)
   * @returns {number} - Un-Pan Xing index
   */

  /** @type {FengShui.FengShuiContext.get_unpan_xing_index} */
  const get_unpan_xing_index = useCallback(
    params => {
      const { current, lichun } = params;
      return (
        ready &&
        wasm_get_unpan_xing_index(
          date_params_from_localtime(current),
          date_params_from_localtime(lichun)
        )
      );
    },
    [ready]
  );

  /**
   * Takes 運盤星 (Un-Pan Xing) information and 向星 (Xiang-Xing)
   * information, and returns 下卦図 (Xia-Gua-Tu).
   * For 運盤星 (Un-Pan Xing), we need 2 kinds: 運盤 (Un-Pan)
   * which is currently in the center, and 洛書 (Lo-Shu) order
   * in its re-arranged form. For 向星 (Xiang-Xing),
   * we want `direction` and `sector`.
   * @typedef FengShui.FengShuiContext.get_xiaguatu_from_unpan_index
   * @function
   * @param {Object} arg
   * @param {number} arg.unpan_xing_center - 運盤星 (Un-Pan Xing) index
   * @param {Array} arg.unpan_xing_order - Jiu-Xing Order
   * @param {string} arg.xiang_xing_direction - Direction for 向星 (Xiang-Xing)
   * @param {number} arg.xiang_xing_sector - Sector for both 山星 (Shan-Xing) and 向星 (Xiang-Xing)
   * @returns {Object}
   */

  /** @type {FengShui.FengShuiContext.get_xiaguatu_from_unpan_index} */
  const get_xiaguatu_from_unpan_index = useCallback(
    params => {
      return (
        ready &&
        wasm_get_xiaguatu_from_unpan_index({
          ...params,
          unpan_xing_order: params.unpan_xing_order || [
            5, 0, 7, 6, 4, 2, 1, 8, 3,
          ],
        })
      );
    },
    [ready]
  );

  /**
   * A simple accessor for values stored in `JIU_XING_DI_PAN_POSITIONS`.
   * @type {FengShui.FengShuiContext.get_jiuxing_dipan_positions_from_direction}
   */
  const get_jiuxing_dipan_positions_from_direction = useCallback(
    dir => {
      return ready && wasm_get_jiuxing_dipan_positions_from_direction(dir);
    },
    [ready]
  );

  // ================================================================
  // 生死衰旺 (Sheng-Si Shuai-Wang)
  // ================================================================

  /**
   * When provided with 運盤 (Un-Pan) index and the current chart,
   * returns the corresponding 生死衰旺 (Sheng-Si Shuai-Wang).
   * @typedef FengShui.FengShuiContext.get_shengsi_mapping
   * @function
   * @param {Object} arg
   * @param {number} arg.unpan_id - 運盤星 (Un-Pan Xing) index
   * @param {Array} arg.unpan_xing_chart - 運盤星 (Un-Pan Xing) index
   * @returns {Object}
   */

  /** @type {FengShui.FengShuiContext.get_shengsi_mapping} */
  const get_shengsi_mapping = useCallback(
    params => {
      return (
        ready &&
        wasm_get_shengsi_mapping({
          ...params,
          unpan_xing_chart: params.unpan_xing_chart || [
            5, 0, 7, 6, 4, 2, 1, 8, 3,
          ],
        })
      );
    },
    [ready]
  );

  // ================================================================
  // MAIN FOR THE CONTEXT PROVIDER
  // ================================================================

  /** @private */
  const _set = useCallback(
    (prof = {}) => {
      const { localtime: current, direction, sector } = prof;

      if (ready && current && direction) {
        const lichun_0 = get_lichun(current.year());
        const lichun = moment(lichun_0);
        const center = get_unpan_xing_index({ current, lichun });

        const xgtu = get_xiaguatu_from_unpan_index({
          unpan_xing_center: center,
          xiang_xing_direction: direction,
          xiang_xing_sector: sector,
        });

        setBazi(
          normalize_bazi_data(
            wasm_get_bazi(datetime_params_from_localtime(current))
          )
        );
        setLiChun(lichun);
        setUnPanXing(xgtu.unpan_xing);
        setShanXing(xgtu.shan_xing);
        setXiangXing(xgtu.xiang_xing);
      }
    },
    [ready, profile?.locatltime, profile?.direction]
  );

  /**
   * @typedef FengShui.FengShuiContext.update
   * @function
   */

  /** @type {FengShui.FengShuiContext.update} */
  const update = useCallback(
    prof => {
      if (ready) {
        if (!has_valid_profile(prof)) {
          throw new Error(
            '[FengShuiContext] Need a valid profile for the argument'
          );
        }
        setProfile(prof);
        _set(prof);
      }
    },
    [ready, _set]
  );

  useEffect(() => {
    if (ready !== true) {
      init(WASM_PATH)
        .then(() => {
          setReady(true);
        })
        .catch(err => {
          throw err;
        });
    }
  }, [props?.localtime, props?.direction]);

  return (
    <FengShuiContext.Provider
      value={{
        ready,
        profile,
        bazi,
        lichun,
        unpan_xing,
        shan_xing,
        xiang_xing,
        update,
        get_gua_compass_order,
        get_twentyfour_direction_from_index,
        get_twentyfour_direction_from_degrees,
        get_twentyfour_data_from_index,
        get_twentyfour_data_from_direction,
        get_bazi,
        get_lichun,
        get_jiuxing_from_index,
        get_unpan_xing_index,
        get_xiaguatu_from_unpan_index,
        get_jiuxing_dipan_positions_from_direction,
        get_shengsi_mapping,
      }}
      {...props}
    />
  );
};

// ----------------------------------------------------------------
// useFengShui
// ----------------------------------------------------------------

/**
 * @typedef FengShui.useFengShui
 * @function
 */
export const useFengShui = () => useContext(FengShuiContext);

// ----------------------------------------------------------------
// useFengShuiSync (hook)
// ----------------------------------------------------------------

/**
 * Syncing the latest primary profile to FengShuiContext.profile
 * @typedef FengShui.useFengShuiSync
 * @function
 */
export const useFengShuiSync = () => {
  const { profiles } = useProfiles();
  const { ready, update } = useFengShui();
  const [hasProfile, setHasProfile] = useState(false);

  useEffect(() => {
    const p = get_first_valid_profile_from_profiles(profiles);
    if (p) {
      const t = p.localtime.format('YYYY-MM-DD');
      const dir = `${p.direction}${p.sector}`;
      setHasProfile(true);
      update(p);
    } else {
      setHasProfile(false);
    }
  }, [ready, profiles]);

  return hasProfile;
};

// ----------------------------------------------------------------
// All the others
// ----------------------------------------------------------------

/**
 * @private
 * @param {Object} t - Moment object in localtime + explicit UTC offset
 */
function date_params_from_localtime(t) {
  if (!t) throw new Error("No 'localtime' specified for FengShui");

  return {
    ...DATE_KEYS.reduce((acc, key) => {
      acc[key] = int(t.format(DATETIME_FORMAT[key]));
      return acc;
    }, {}),
  };
}

/**
 * @private
 * @param {Object} t - Moment object in localtime + explicit UTC offset
 */
function datetime_params_from_localtime(t) {
  if (!t) throw new Error("No 'localtime' specified for FengShui");

  return {
    ...DATETIME_KEYS.reduce((acc, key) => {
      acc[key] = int(t.format(DATETIME_FORMAT[key]));
      return acc;
    }, {}),
    zone: get_utc_offset_in_hours(t),
  };
}

/**
 * @private
 */
function normalize_bazi_data(orig) {
  const hash = { __orig: { ...orig } };

  // 'year', 'month', 'hour', 'day'
  BAZI_TYPE_KEYS.forEach(bazi_key => {
    hash[bazi_key] = {
      __obj: orig[bazi_key][bazi_key],
    };

    // 'stem', 'branch'
    GANZHI_TYPE_KEYS.forEach(ganzhi_key => {
      hash[bazi_key][ganzhi_key] = {
        kanji: orig[bazi_key][ganzhi_key].name.zh_cn.alphabet,
        yomi: orig[bazi_key][ganzhi_key].name.ja.alphabet,
      };
    });

    hash[
      bazi_key
    ].kanji = `${hash[bazi_key].stem.kanji}${hash[bazi_key].branch.kanji}`;
    hash[
      bazi_key
    ].yomi = `${hash[bazi_key].stem.yomi}${hash[bazi_key].branch.yomi}`;
  });

  return hash;
}
