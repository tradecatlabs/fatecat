/**
 * 省市县三级联动选择组件
 *
 * 'use client' 标记说明：
 * - 使用 useState 管理选择状态
 * - 包含交互式下拉选择
 */
'use client';

import { useState, useMemo, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';

interface Region {
    name: string;
    children?: Region[];
}

interface RegionPickerProps {
    value: string;
    onChange: (value: string) => void;
}

// 从 JSON 加载地区数据
let regionsCache: Region[] | null = null;

async function loadRegions(): Promise<Region[]> {
    if (regionsCache) return regionsCache;
    const res = await fetch('/data/china-regions.json');
    const data = await res.json();
    regionsCache = data;
    return regionsCache!;
}

export function RegionPicker({ value, onChange }: RegionPickerProps) {
    const [regions, setRegions] = useState<Region[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadRegions().then(setRegions).finally(() => setLoading(false));
    }, []);
    // 解析当前值为省/市/区
    const parseValue = (val: string): [string, string, string] => {
        if (!val) return ['', '', ''];
        const parts = val.split(/[,，\s]+/).filter(Boolean);
        return [parts[0] || '', parts[1] || '', parts[2] || ''];
    };

    const [province, city, district] = parseValue(value);
    const [selectedProvince, setSelectedProvince] = useState(province);
    const [selectedCity, setSelectedCity] = useState(city);
    const [selectedDistrict, setSelectedDistrict] = useState(district);

    // 同步外部值变化（使用条件更新代替 useEffect）
    const [lastValue, setLastValue] = useState(value);
    if (value !== lastValue) {
        const [p, c, d] = parseValue(value);
        setSelectedProvince(p);
        setSelectedCity(c);
        setSelectedDistrict(d);
        setLastValue(value);
    }

    // 获取当前省份的城市列表
    const cities = useMemo(() => {
        if (!selectedProvince) return [];
        const prov = regions.find(r => r.name === selectedProvince);
        return prov?.children || [];
    }, [selectedProvince, regions]);

    // 获取当前城市的区县列表
    const districts = useMemo(() => {
        if (!selectedCity || !cities.length) return [];
        const city = cities.find(c => c.name === selectedCity);
        return city?.children || [];
    }, [selectedCity, cities]);

    // 构建完整地址并通知父组件
    const updateValue = (prov: string, city: string, dist: string) => {
        const parts = [prov, city, dist].filter(Boolean);
        onChange(parts.join(' '));
    };

    // 处理省份变化
    const handleProvinceChange = (prov: string) => {
        setSelectedProvince(prov);
        setSelectedCity('');
        setSelectedDistrict('');
        updateValue(prov, '', '');
    };

    // 处理城市变化
    const handleCityChange = (city: string) => {
        setSelectedCity(city);
        setSelectedDistrict('');
        updateValue(selectedProvince, city, '');
    };

    // 处理区县变化
    const handleDistrictChange = (dist: string) => {
        setSelectedDistrict(dist);
        updateValue(selectedProvince, selectedCity, dist);
    };

    return (
        <div className="grid grid-cols-3 gap-2">
            {/* 省份选择 */}
            <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-foreground/50 mb-1">省/直辖市</label>
                <div className="relative">
                    <select
                        value={selectedProvince}
                        onChange={(e) => handleProvinceChange(e.target.value)}
                        className="w-full px-2 py-2 pr-6 border border-border rounded-md bg-background text-sm text-foreground
                            focus:outline-none focus:ring-2 focus:ring-[#2383e2]/10 focus:border-[#2383e2]
                            appearance-none cursor-pointer"
                    >
                        <option value="">省份</option>
                        {!loading && regions.map((region) => (
                            <option key={region.name} value={region.name}>
                                {region.name}
                            </option>
                        ))}
                    </select>
                    <ChevronDown className="absolute right-1 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30 pointer-events-none" />
                </div>
            </div>

            {/* 城市选择 */}
            <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-foreground/50 mb-1">市/区</label>
                <div className="relative">
                    <select
                        value={selectedCity}
                        onChange={(e) => handleCityChange(e.target.value)}
                        disabled={cities.length === 0}
                        className="w-full px-2 py-2 pr-6 border border-border rounded-md bg-background text-sm text-foreground
                            focus:outline-none focus:ring-2 focus:ring-[#2383e2]/10 focus:border-[#2383e2]
                            appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <option value="">城市</option>
                        {cities.map((city) => (
                            <option key={city.name} value={city.name}>
                                {city.name}
                            </option>
                        ))}
                    </select>
                    <ChevronDown className="absolute right-1 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30 pointer-events-none" />
                </div>
            </div>

            {/* 区县选择 */}
            <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-foreground/50 mb-1">区/县</label>
                <div className="relative">
                    <select
                        value={selectedDistrict}
                        onChange={(e) => handleDistrictChange(e.target.value)}
                        disabled={districts.length === 0}
                        className="w-full px-2 py-2 pr-6 border border-border rounded-md bg-background text-sm text-foreground
                            focus:outline-none focus:ring-2 focus:ring-[#2383e2]/10 focus:border-[#2383e2]
                            appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <option value="">区县</option>
                        {districts.map((dist) => (
                            <option key={dist.name} value={dist.name}>
                                {dist.name}
                            </option>
                        ))}
                    </select>
                    <ChevronDown className="absolute right-1 top-1/2 -translate-y-1/2 w-4 h-4 text-foreground/30 pointer-events-none" />
                </div>
            </div>
        </div>
    );
}
