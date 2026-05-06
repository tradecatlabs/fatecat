export const pipe = (headFn, ...restFns) => (...args) => restFns.reduce((value, fn) => fn(value), headFn(...args));

export const compose = (...fns) => pipe(...fns.reverse());

export const curry = (f, ...args) => args.length >= f.length ? f(...args) : (...next) => curry(f, ...args, ...next);
export const uncurry = f => (...args) => args.reduce((g, x) => (g = g(x), typeof g === "function" && g.length === 1 ? uncurry(g) : g), f);

export const zip = (arr, ...arrs) => arr.map((val, i) => arrs.reduce((a, arr) => [...a, arr[i]], [val]));
export const zipWith = (zipper, arr, ...arrs) => arr.map((val, i) => zipper(...arrs.reduce((a, arr) => [...a, arr[i]], [val])));

export const omap = (o, f) => Object.assign(...Object.keys(o).map(k => ({
    [k]: f(o[k])
})));
// NOTE:: ES7 version, Object.assign(...Object.entries(obj).map(([k, v]) => ({[k]: v * v})));
export const ozip = (obj, ...objs) => Object.assign(...Object.keys(obj).map(k => ({
    [k]: [obj[k]].concat(objs.map(o => o[k]))
})));
export const ozipWith = (zipper, obj, ...objs) => Object.assign(...Object.keys(obj).map(k => ({
    [k]: zipper(...[obj[k]].concat(objs.map(o => o[k])))
})));


export const memoize = fn => {
    let cache = {};
    return (...args) => {
        let stringifiedArgs = JSON.stringify(args);
        let result = cache[stringifiedArgs] = cache[stringifiedArgs] || fn(...args);
        return result;
    };
};

const check_builtin_type = typename => x => {
    if (typeof x === typename) return x;
    throw new TypeError("Except a " + typename + "!");
}

export const num = check_builtin_type("number");
export const str = check_builtin_type("string");
export const bool = check_builtin_type("boolean");
export const func = check_builtin_type("function");
export const undef = check_builtin_type("undefined");
export const obj = check_builtin_type("object");
// Asserts n is a signed 32-bit number
export const int32 = (n) => {
    if ((n | 0) !== n)
        throw new TypeError('Expected a 32-bit integer.');
    return n;
};
// Asserts int32 and nonnegative
export const nat32 = (n) => {
    if ((n | 0) !== n || n < 0)
        throw new TypeError('Expected a 32-bit natural.');
    return n;
};
