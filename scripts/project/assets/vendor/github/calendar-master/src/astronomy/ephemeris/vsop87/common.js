import * as std from '../../../basic';
import * as Decimal from '../../../math/decimal';

const decimal=Decimal.decimal;

export const alphaMAX = 5; //最高階數 0 1 2 3 4 5
export const coordMAX = 6; //最大坐標分量數 橢圓坐標6分量 直角/球面坐標3分量

// In VSOP files, the index of celestial objects starts from 1 
// special cases: an index has different meanings among different versions.
// 3: Earth for the versions A-E and Earth-Moon Barycenter for the main version
// 9: Earth-Moon barycenter for the version A and Sun for the version E

// zh-cn: VSOP文件内行星的序号从1开始 
// 两个特例：版本间含义不同
// 3: 版本A-E中指Earth(地球)，主版本中指Earth-Moon Barycenter(地月质心)
// 9: 版本A中指Earth-Moon Barycenter(地月质心)，版本E中指Sun(太阳)
const celestial_objects=std.zip(
    ["Placeholder", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Earth-Moon barycenter", "Sun"],
    ["0","0.6e-8", "2.5e-8", "2.5e-8", "10.0e-8", "35.0e-8", "70.0e-8", "8.0e-8", "42.0e-8", "2.5e-8", "2.5e-8"],
    ["0","0.3871", "0.7233", "1.0000", "1.5237", "5.2026", "9.5547", "19.2181", "30.1096", "1.0000", "1.0000" ],
    [-1, 4, 4, 4, 4, 2, 2, 6, 6, 4, 4] // thousand years
).map(x=>({
    name: x[0],
    eps:x[1],
    semimajor_axis:x[2],
    span: x[3]
}));
// fix special index
const index=(idx, ver)=>{
    if(ver===0 && idx===3) return 9; //Earth-Moon Barycenter
    if(ver===5 && idx===9 ) return 10; //Sun
    return idx;
}
// celestial object name, 行星名
export const name=(idx, ver)=>celestial_objects[index(idx,ver)].name;
// celestial object standard error, 行星标准误差
export const eps=(idx, ver)=>decimal(celestial_objects[index(idx,ver)].eps);
// celestial object semi-major axis length, 行星半长轴长度
export const semimajor_axis=(idx, ver)=>decimal(celestial_objects[index(idx,ver)].semimajor_axis);
// span of ±thousand years with controllable errors（since J2000）,误差可控的时间范围，±千年數（自J2000）
export const span=(idx,ver)=>celestial_objects[index(idx,ver)].semimajor_axis;

const coordinates=["elliptic","descartes","spherical","descartes","spherical","descartes"];
// VSOP87, start from 1
const components={
    "elliptic":["au","rad","rad","rad","rad","rad"], // semi-major axis : au
    "descartes":["au","au","au"], // x, y, z
    "spherical":["rad","rad","au"] // λ, β, δ
};
export const coordinate=(ver)=>components[coordinates[ver]];