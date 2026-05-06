import { compose } from 'ramda';
import { PIE_UNIT_HALF } from '@/constants';

export const int = Math.trunc;

export const noop = () => {};

export const fixed =
  (decimals = 3) =>
  n => {
    const place = Math.pow(10, decimals);
    return int(n * place) / place;
  };

export const capitalize = s => s[0].toUpperCase() + s.slice(1);

export const gen_code_4 = () =>
  Math.floor((1 + Math.random()) * 0x10000)
    .toString(16)
    .substring(1);

export const gen_code_12 = () =>
  `${gen_code_4()}${gen_code_4()}${gen_code_4()}`;

export const rad_to_deg = rad => rad * (180 / Math.PI);
export const deg_to_rad = deg => deg * (Math.PI / 180);

export const normalize_degree = deg => ((deg % 360) + 360) % 360;
export const normalize_angle = normalize_degree;
export const normalize_radian = compose(
  deg_to_rad,
  normalize_degree,
  rad_to_deg
);

export const get_position = (rad, radius = 1, center = { x: 0, y: 0 }) => ({
  deg: normalize_degree(rad_to_deg(rad)),
  x: center.x + Math.cos(rad) * radius,
  y: center.y + Math.sin(rad) * radius,
});

// Compared to `get_position`, this function uses
// `Math.sin()` for `x`, and `Math.cos()` for `y`.
export const get_position_clock = (
  rad,
  radius = 1,
  center = { x: 0, y: 0 }
) => ({
  deg: normalize_degree(rad_to_deg(rad)),
  x: center.x + Math.sin(rad) * radius,
  y: center.y - Math.cos(rad) * radius,
});

export const euler_from_quaternion = (q = []) => {
  /*
   * alpha
   *  - Yew
   *  - Rotation around Z-axis (a ray coming out of your phone)
   *  - Screen-face rotation (like a car handle when driving)
   */
  const alpha = normalize_degree(
    rad_to_deg(
      Math.atan2(
        2 * q[0] * q[1] + 2 * q[2] * q[3],
        1 - 2 * q[1] * q[1] - 2 * q[2] * q[2]
      )
    )
  );

  /*
   * gamma
   *  - Roll
   *  - Rotation around Y-axis (phone's vertical axis)
   *  - Horizontal tilt (left-right tilt)
   */
  const gamma = normalize_degree(
    rad_to_deg(
      Math.atan2(
        2 * (q[3] * q[0] + q[1] * q[2]),
        1 - 2 * (q[0] * q[0] + q[1] * q[1])
      )
    )
  );

  return [alpha, gamma];
};

export const get_utc_offset_in_hours = dt =>
  int(Math.floor(dt.utcOffset() / 60));

export const str_to_hex = str => parseInt(str.slice(1), 16);

export const pad =
  (digits = 2) =>
  (n = 0) =>
    n.toString().padStart(digits, '0');

export const is_leap_year = year => {
  if (year % 4 == 0) {
    if (year % 100 == 0) {
      return year % 400 == 0;
    } else {
      return true;
    }
  } else {
    return false;
  }
};

export const is_iOS =
  navigator.userAgent.match(/(iPod|iPhone|iPad)/) &&
  navigator.userAgent.match(/AppleWebKit/);

let time = Date.now();

export const debounce = (f, delay) => {
  let timeout = null;
  let args = null;

  const g = () => {
    f.apply(null, args);
    time = Date.now();
  };

  return function () {
    args = arguments;

    if (Date.now() >= time + delay) {
      // Execute if the time has passed.
      g();
    } else {
      // Cancel the previous ones, and execute only the last one.
      !!timeout && clearTimeout(timeout);
      timeout = setTimeout(g, delay);
    }
  };
};
