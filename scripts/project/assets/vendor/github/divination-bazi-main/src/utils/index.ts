/**
 * 获取assets静态资源，路径为assets
 * @param url 图片名称
 * @returns
 */
export const getAssetsFile = (url: string): string => {
    return new URL(`../assets/${url}`, import.meta.url).href
}

// 根据最大数字生成随机数 取下标 0 - max-1
export const getRandomNumber = (max: number): number => {
    return (Math.floor(Math.random() * max) + 1) % max
}

/**
 * 深拷贝
 * @param obj 要拷贝的对象
 * @param map 已经拷贝的对象
 * @returns
 */
export const deepClone = (obj, map = new WeakMap()) => {
    // 如果是基本数据类型，则直接返回
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }

    // 如果已经拷贝过该对象，则直接返回拷贝后的对象
    if (map.has(obj)) {
        return map.get(obj)!;
    }

    // 根据对象的类型进行深拷贝
    const clone = Array.isArray(obj) ? [] : {};

    // 将当前对象和对应的拷贝存储到map中
    map.set(obj, clone);

    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            clone[key] = deepClone(obj[key], map);
        }
    }

    return clone;
}

/**
 * 防抖函数
 */
let debounceTimer;
export const debounce = (fn: Function, delay: number = 500) => {
    if (debounceTimer) clearInterval(debounceTimer)
    debounceTimer = window.setTimeout(() => {
        fn()
    }, delay);
}

/**
 * 节流函数 点击之后一段时间不会再触发
 * @param fn
 * @param still 持续间隔时间
 */
let throttleTimer;
export const throttle = (fn: Function, still = 300) => {
    if (!throttleTimer) {
        fn();
        throttleTimer = setTimeout(() => {
            if (throttleTimer) clearTimeout(throttleTimer)
            throttleTimer = null;
        }, still);
    }
}

/**
 * 强制清除节流
 */
export const clearAllThrottle = () => {
    if (throttleTimer) clearTimeout(throttleTimer);
}
