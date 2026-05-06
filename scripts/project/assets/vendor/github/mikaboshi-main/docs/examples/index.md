# Examples

[1. Example Rust + React Codes](#1-example-rust-react-codes)  
[2. Setups for WASM Apps in Webpack](#2-setups-for-wasm-apps-in-webpack)  
[3. Using WASM Apps from React](#3-using-wasm-apps-from-react)  
[4. Feng-Shui Examples](#4-feng-shui-examples)  
&nbsp; &nbsp; [4-1. `src/contexts/FengShui.js`](#4-1-srccontextsfengshuijs)  
&nbsp; &nbsp; [4-2. `src/components/fengshui/jiuxing.jsx`](#4-2-srccomponentsfengshuijiuxingjsx)  

## 1. Example Rust + React Codes

I picked up some files from one of the real-world projects of mine.
In this project, I have Rust codes in `src_for_wasm` and React codes in `src`.

Rust
- [src_for_wasm/Cargo.toml](./Cargo.toml)
- [src_for_wasm/lib.rs](./lib.rs)  
Acts like a proxy to all the public functions provided by _mikaboshi_.

React
- [src/contexts/FengShui.js](FengShui.js)  
A context provider set to the React app top, and delegates functions provided by `src_for_wasm/lib.rs`.
- [src/components/chart/chart.jsx](chart.jsx)  
Provides a layout for Feng-Shui chart which contains a several child components such as `src/components/fengshui/jiuxing.jsx`, `src/components/twentyfour.jsx`, and so forth.
- [src/components/fengshui/bagua_info.jsx](bagua_info.jsx)
- [src/pages/fengshui/bagua.jsx](bagua.jsx)
- [src/pages/fengshui/jiuxing.jsx](jiuxing.jsx)
- [src/pages/fengshui/north.jsx](north.jsx)
- [src/pages/fengshui/twentyfour_info.jsx](twentyfour_info.jsx)
- [src/pages/fengshui/twentyfour.jsx](twentyfour.jsx)
- [src/lib/utils.js](utils.js)


## 2. Setups for WASM Apps in Webpack

For how you can serve a WASM app, you may want to check out
one of my other projects,
_[perlin-experiment](https://github.com/minagawah/perlin-experiment)_.  
Setups are about the same.


## 3. Using WASM Apps from React

When using a WASM app from React, you need to first
asynchronously wait for the module to be ready.

```js
import React, { useContext, createContext, useEffect, useState } from 'react';
import init, { order_pizza } from 'wasm-pizza';

const WASM_PATH =
  NODE_ENV === 'production'
    ? 'wasm/wasm-pizza/wasm-pizza_bg.wasm'
    : void 0;

const PizzaContext = createContext({
  ready: false,
  orderPizza: () => {},
});

export const PizzaProvider = () => {
  const [ready, setReady] = useState(false);

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
  }, []);

  const orderPizza = params => {
    return order_pizza(params);
  };

  return (
    <PizzaContext.Provider
      value={{
        ready,
        orderPizza,
      }}
    />
};

export const usePizza = () => useContext(PizzaContext);
```

Notice that we import `init` from `wasm-pizza` which is a compiled WASM app
provided as a NPM module. As mentioned in the previous section,
[take a look at one of my projects](https://github.com/minagawah/perlin-experiment)
for it explains how.

Now, you may use the provider:

`src/App.jsx`

```js
ReactDOM.render(
  <PizzaProvider>
    <App />
  </PizzaProvider>,
  document.getElementById('root')
);
```

From one of your components, you call the method:

```js
import { usePizza } from '@/contexts/Pizza';

export const Order = () => {
  const { ready, orderPizza } = usePizza();
  const [pizza, setPizza] = useState(null);

  useEffect(() => {
    setPizza(
      orderPizza()
    );
  }, [ready])

  return <div>{pizza}</div>;
};
```

## 4. Feng-Shui Examples

For example files provided at the beginning,
I will explain key features found in the codes.
Although it is the usage from React,
I believe you will at least get ideas
when using _mikaboshi_ for your projects.


### 4-1. `src/contexts/FengShui.js`

Source: [src/contexts/FengShui.js](FengShui.js)

`src/contexts/FengShui.js` is a React context provider,
and it provides `FengShuiContext`.
For resources provided by `FengShuiContext`
will be accessible for any child components
when using `useFengShui()`.

```js
const FengShuiContext = createContext({
  ready: false,
  profile: null, // localtime, direction, sector
  bazi: null,
  lichun: null,
  unpan_xing: null, // 運盤星
  shan_xing: null, // 山星
  xiang_xing: null, // 向星
  update: noop,
  ...
  ...
  ...
});
```

`src/contexts/FengShui.js` loads a WASM app (`src_for_wasm/lib/rs`).
Since it loads the WASM app asynchronously,
components must wait for `ready` to become `true`
for all the features to become available.

For `profile` is not actually peculiar to `src/contexts/FengShui.js`,
but is something managed in another provider `src/contexts/Profiles.js`.
Since there is no way for 2 providers to communicate,
we run `useFengShuiSync()` somewhere in one of the components
to sync the contents of `profile`.

`_set()` runs when the content of `profile` changes:

```js
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
```

In the above, using _mikaboshi_'s `get_xiaguatu_from_unpan_index()`
to obtain 下卦図 (Xia-Gua-Tu). For 3 arguments required,
we already have `xiang_xing_direction` and `xiang_xing_sector`
in `profile`, but for `unpan_xing_center` needs a preparation.

For `unpan_xing_center`, we run `get_unpan_xing_index()`.
And, again, it requires another preparation for `lichun`,
and we run `get_lichun()` for `lichun`.


### 4-2. `src/components/fengshui/jiuxing.jsx`

Source: [src/components/fengshui/jiuxing.jsx](jiuxing.jsx)

`jiuxing.jsx` is one of the child components wrapped in `FengShuiContext` provider.
Here is how it starts:

```js
export const FengShuiJiuXing = () => {
  const { worldInfo: world } = useWorld();
  const deviceOrientation = useDeviceOrientation();
  const {
    ready,
    unpan_xing,
    shan_xing,
    xiang_xing,
    get_xiaguatu_from_unpan_index,
    get_jiuxing_dipan_positions_from_direction,
    get_twentyfour_direction_from_degrees,
    get_shengsi_mapping,
  } = useFengShui();
```

As mentioned, using `useFengShui()`, will get you an access
for resources provided by `FengShuiContext`.

Let's continue.

```js
  const { direction: curr_dir } = get_twentyfour_direction_from_degrees(
    360 - alpha
  );
```

Now, we are using `get_twentyfour_direction_from_degrees()`.

For a given angle (in degrees),
`get_twentyfour_direction_from_degrees()`
returns `direction` and `sector`.

`direction` is a compass direction represented
in a lower case string (e.g. `n`, `ne`, `e`, `se`, etc.).

`sector` is special concept unique to
[二十四山向 (Er-Shi-Si Shan-Xiang)](../compass.md).
For each compass direction is further divided into 3 sectors,
represented in a number `1`, `2`, or `3`.

Yet, for the above example, this time,
we are getting `direction` only,
and naming it: `curr_dir`

```js
      const u_id = unpan_xing.center;

      // When calculating for 下卦図 (Xia-Gua-Tu), not only
      // the current 運盤星 (Un-Pan Xing), but we also want
      // all 九星 (Jiu-Xing) in the 洛書 (Lo-Shu) order.
      // Although we have `JIU_XING_DI_PAN_POSITIONS`
      // which defines 洛書 (Lo-Shu) order, we want it
      // in re-arranged order for the current device rotation,
      // and that is what we pass for the second argument
      // of `get_xiaguatu_from_unpan_index()`.
      const u_order = get_jiuxing_dipan_positions_from_direction(curr_dir);

      // Now, calculate for 下卦図 (Xia-Gua-Tu).
      const xiagua = get_xiaguatu_from_unpan_index({
        unpan_xing_center: u_id,
        unpan_xing_order: u_order,
        xiang_xing_direction: xiang_xing.direction,
        xiang_xing_sector: xiang_xing.sector,
      });
```

As mentioned before, `unpan_xing` (運盤星; Un-Pan Xing)
is managed in `src/contexts/FengShui.js`,
and we simply want to refer to it.
The same goes for `shan_xing` (山星; Shan-Xing),
and `xiang_xing` (向星; Xiang-Xing),
and we expect that we already have the values
stored in `src/contexts/FengShui.js`.
