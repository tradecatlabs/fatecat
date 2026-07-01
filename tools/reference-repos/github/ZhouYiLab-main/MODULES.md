# ZhouYiLab 模块架构文档

## 模块层次结构

```

                应用层 (main.cpp)                 

                        

              功能模块层                          
       
   LiuYao    DaLiuRen  BaZi   ZiWei        
       
                                     
    QiMen                                      
                                     

                        

              通用模块层                          
     
   BaZiBase   WuXingUtils  DiZhiRelations   
     
     
    TianGan      DiZhi         GanZhi       
     
                    
   ZhMapper       Tyme                       
                    

                        

            第三方库 & 标准库层                   
      
   fmt  nlohmann.json   magic_enum         
      
                                
    import std                                
                                

```

## 模块详细说明

### 1. 通用基础模块 (Common Layer)

#### ZhouYi.BaZiBase
**文件**: `src/common/ba_zi_base.cppm`

**导出内容**:
- `struct Pillar` - 干支柱（天干地支组合）
- `struct BaZi` - 四柱八字

**依赖**:
```cpp
import nlohmann.json;  // JSON 序列化
import std;            // 标准库
```

**用途**: 被所有需要使用干支柱和八字的模块引用

---

#### ZhouYi.WuXingUtils
**文件**: `src/common/wu_xing_utils.cppm`

**导出内容**:
- `enum class ElementalRelation` - 五行关系枚举
- `branchFiveElements` - 地支五行映射表
- `fiveElementIndex` - 五行索引映射
- `hiddenStems` - 地支藏干映射
- `getElementalRelationship()` - 五行关系判断
- `relationToString()` - 五行关系转中文
- `getBranchElement()` - 获取地支五行

**依赖**:
```cpp
import std;  // 标准库
```

**用途**: 提供五行相关的所有工具函数和数据映射

---

#### ZhouYi.DiZhiRelations
**文件**: `src/common/di_zhi_relations.cppm`

**导出内容**:
- `clashMap` - 地支六冲映射
- `combineMap` - 地支六合映射
- `harmMap` - 地支六害映射
- `punishmentMap` - 地支相刑映射
- `sanHeMap` - 地支三合局映射
- `isClash()`, `isCombine()`, `isHarm()`, `isPunishment()` - 判断函数

**依赖**:
```cpp
import std;  // 标准库
```

**用途**: 提供地支关系的所有映射表和判断函数

---

#### ZhouYi.GanZhi
**文件**: `src/common/ganzhi.cppm`

**导出内容**:
- `enum class TianGan` - 天干枚举
- `enum class DiZhi` - 地支枚举
- `enum class WuXing` - 五行枚举
- `enum class YinYang` - 阴阳枚举
- 六十甲子相关函数
- 干支关系判断函数

**依赖**:
```cpp
import magic_enum;  // 枚举反射
import std;         // 标准库
```

---

#### ZhouYi.TianGan
**文件**: `src/common/example_module.cppm`

**导出内容**:
- `class TianGan` - 天干类
- `TianGan::Type` - 天干类型枚举
- `TianGanMapper` - 中英文映射

**依赖**:
```cpp
import magic_enum;  // 枚举反射
import std;         // 标准库
```

---

#### ZhouYi.DiZhi
**文件**: `src/common/dizhi_module.cppm`

**导出内容**:
- `class DiZhi` - 地支类
- `DiZhi::Type` - 地支类型枚举
- `DiZhiMapper` - 中英文映射

**依赖**:
```cpp
import magic_enum;  // 枚举反射
import std;         // 标准库
```

---

#### ZhouYi.ZhMapper
**文件**: `src/common/zh_mapper.cppm`

**导出内容**:
- `template<typename E> struct ZhMap` - 中文映射模板
- `to_zh()`, `from_zh()` - 枚举与中文互转
- `get_all_zh_names()` - 获取所有中文名
- `get_all_info()` - 获取枚举详细信息

**依赖**:
```cpp
import magic_enum;  // 枚举反射
import std;         // 标准库
```

---

### 2. 功能模块 (Feature Layer)

#### ZhouYi.BaZi
**文件**: `src/ba_zi/ba_zi.cppm`

**导出内容**:
- `struct BaZiResult` - 八字排盘结果
- `struct DaYun` - 大运信息
- `struct LiuNian` - 流年信息
- `struct LiuYue` - 流月信息
- `pai_pan_solar()` - 公历排盘
- `pai_pan_lunar()` - 农历排盘
- `get_da_yun_list()` - 获取大运列表
- `get_liu_nian()` - 获取流年
- `get_liu_yue_list()` - 获取流月列表

**依赖**:
```cpp
import ZhouYi.BaZiBase;        // 八字基础
import ZhouYi.GanZhi;          // 干支系统
import ZhouYi.Tyme;            // 农历历法
import std;                    // 标准库
```

**使用示例**:
```cpp
import ZhouYi.BaZiController;

using namespace ZhouYi::BaZiController;

// 公历排盘
auto result = pai_pan_solar(2000, 7, 15, 16, 30, true);
const auto& ba_zi = result.ba_zi;
std::println("年柱：{}", ba_zi.year.to_string());
```

---

#### ZhouYi.DaLiuRen
**文件**: `src/da_liu_ren/da_liu_ren.cppm`

**导出内容**:
- `struct DaLiuRenResult` - 大六壬排盘结果
- `struct SiKe` - 四课信息
- `struct SanChuan` - 三传信息
- `struct TianDiPan` - 天地盘信息
- `pai_pan()` - 公历排盘
- `pai_pan_lunar()` - 农历排盘

**依赖**:
```cpp
import ZhouYi.GanZhi;          // 干支系统
import ZhouYi.Tyme;            // 农历历法
import nlohmann.json;          // JSON 序列化
import std;                    // 标准库
```

**使用示例**:
```cpp
import ZhouYi.DaLiuRen.Controller;

using namespace ZhouYi::DaLiuRen;

auto result = DaLiuRenEngine::pai_pan(2024, 10, 13, 14);
std::println("月将: {}", result.yue_jiang);
```

---

#### ZhouYi.QiMen
**文件**: `src/qi_men/qi_men.cppm`, `src/qi_men/qi_men_pan.cppm`, `src/qi_men/qi_men_controller.cppm`

**导出内容**:
- `struct QiMenPan` - 奇门盘信息
- `enum class Dun` - 阴阳遁枚举
- `enum class Palace` - 九宫枚举
- `enum class SolarTerm` - 二十四节气枚举
- `pai_pan_solar()` - 公历排盘
- `pai_pan_lunar()` - 农历排盘
- `get_summary()` - 获取排盘摘要
- `analyze_auspiciousness()` - 分析宫位吉凶

**依赖**:
```cpp
import ZhouYi.GanZhi;          // 干支系统
import ZhouYi.Tyme;            // 农历历法
import std;                    // 标准库
```

**使用示例**:
```cpp
import ZhouYi.QiMen.Controller;

using namespace ZhouYi::QiMen;

// 公历排盘
auto result = QiMenController::pai_pan_solar(2011, 6, 18, 3, 56);
if (result) {
    const auto& pan = result.value();
    std::println("阴阳遁：{}", pan.dun == Dun::Yang ? "阳遁" : "阴遁");
    std::println("局数：第{}局", pan.ju);
}
```

---

#### ZhouYi.LiuYao
**文件**: `src/liu_yao/liu_yao.cppm`

**导出内容**:
- `struct YaoDetails` - 爻详细信息
- `struct HexagramInfo` - 卦象信息
- `hexagramMap` - 六十四卦信息映射
- `palaceBranchPatterns` - 宫位地支序列
- `palaceStemPatterns` - 宫位天干序列
- `sixYaoDivination()` - 六爻排盘主函数
- `buildShenShaMap()` - 神煞计算
- `analyzeXingChongKeHaiHe()` - 关系分析

**依赖**:
```cpp
import fmt;                    // 格式化输出
import nlohmann.json;          // JSON 序列化
import ZhouYi.BaZiBase;        // 八字基础
import ZhouYi.WuXingUtils;     // 五行工具
import ZhouYi.DiZhiRelations;  // 地支关系
import std;                    // 标准库
```

**使用示例**:
```cpp
import ZhouYi.LiuYao;

using namespace ZhouYi::LiuYao;

BaZi bazi{...};
auto [yaoList, json] = sixYaoDivination("111111", bazi, {1, 4});
```

---

## 模块依赖关系

### BaZi 依赖树

```
ZhouYi.BaZi
 ZhouYi.BaZiBase
    nlohmann.json
    std
 ZhouYi.GanZhi
    magic_enum
    std
 ZhouYi.Tyme
    std
 std
```

### DaLiuRen 依赖树

```
ZhouYi.DaLiuRen
 ZhouYi.GanZhi
    magic_enum
    std
 ZhouYi.Tyme
    std
 nlohmann.json
 std
```

### QiMen 依赖树

```
ZhouYi.QiMen
 ZhouYi.GanZhi
    magic_enum
    std
 ZhouYi.Tyme
    std
 std
```

### LiuYao 依赖树

```
ZhouYi.LiuYao
 ZhouYi.BaZiBase
    nlohmann.json
    std
 ZhouYi.WuXingUtils
    std
 ZhouYi.DiZhiRelations
    std
 fmt
 nlohmann.json
 std
```

### 通用模块依赖树

```
ZhouYi.BaZiBase
 nlohmann.json
 std

ZhouYi.WuXingUtils
 std

ZhouYi.DiZhiRelations
 std

ZhouYi.GanZhi
 magic_enum
 std

ZhouYi.TianGan
 magic_enum
 std

ZhouYi.DiZhi
 magic_enum
 std

ZhouYi.ZhMapper
 magic_enum
 std
```

## 模块使用原则

### 1. 分层原则
- **应用层** 只调用功能模块层
- **功能模块层** 可以调用通用模块层和第三方库
- **通用模块层** 只能调用其他通用模块和第三方库
- **禁止循环依赖**

### 2. 命名规范
- 模块名使用 `ZhouYi.` 前缀
- 子模块使用驼峰命名法（如 `BaZiBase`）
- 文件名使用下划线命名法（如 `ba_zi_base.cppm`）

### 3. 导入顺序
```cpp
// 1. 第三方库模块
import fmt;
import nlohmann.json;
import magic_enum;

// 2. 自定义模块
import ZhouYi.BaZiBase;
import ZhouYi.WuXingUtils;

// 3. 标准库模块（最后）
import std;
```

### 4. 导出规范
```cpp
export module ZhouYi.ModuleName;

// 导入其他模块...

export namespace ZhouYi::ModuleName {
    // 导出的内容
}
```

## 编译配置

### CMakeLists.txt 配置

```cmake
file(GLOB_RECURSE MODULE_FILES 
    "src/*.cppm"           # C++23 module 接口文件（递归搜索所有子目录）
    "src/*.ixx"            # MSVC module 接口文件
    "common/tyme/*.cppm"   # common/tyme 模块文件
)

target_sources(ZhouYiLab
    PUBLIC
    FILE_SET cxx_modules TYPE CXX_MODULES FILES
    ${MODULE_FILES}
    ${CMAKE_CURRENT_SOURCE_DIR}/3rdparty/magic_enum/module/magic_enum.cppm
)
```

### 编译器要求

- **Clang**: 17+ (with libc++)
- **GCC**: 14+ (with libstdc++)
- **MSVC**: 19.36+ (Visual Studio 2022 17.6+)
- **CMake**: 4.0+

## 最佳实践

### 1. 模块设计
-  单一职责：每个模块只负责一个明确的功能领域
-  高内聚：相关功能放在同一个模块中
-  低耦合：模块之间依赖关系清晰简单
-  可复用：通用功能抽取到 common 层

### 2. 性能优化
-  使用 `inline const` 替代 `static const` 全局变量
-  使用 `constexpr` 标记编译期常量
-  使用 `std::string_view` 传递字符串参数
-  使用 `auto` 和 `decltype` 简化代码

### 3. C++23 特性
-  使用 `import std` 替代传统头文件
-  使用 `<=>` 三路比较运算符
-  使用 `= default` 生成默认函数
-  使用 `std::ranges` 进行范围操作

## 已实现模块

已完成的功能模块：

1.  **ZhouYi.BaZi** - 八字排盘系统（完整实现）
2.  **ZhouYi.DaLiuRen** - 大六壬排盘系统（完整实现）
3.  **ZhouYi.QiMen** - 奇门遁甲排盘系统（完整实现）
4.  **ZhouYi.LiuYao** - 六爻排盘系统（完整实现）
5.  **ZhouYi.ZiWei** - 紫微斗数排盘系统（完整实现）

## 未来扩展

计划添加的模块：

1. **ZhouYi.FengShui** - 风水计算系统
2. **ZhouYi.MeiHua** - 梅花易数系统
3. **ZhouYi.TaiYi** - 太乙神数系统

所有新模块都应该：
- 遵循相同的命名和组织规范
- 复用 common 层的通用功能
- 提供完整的文档和示例
- 使用 C++23 模块系统

## 许可证

本项目采用 MIT 许可证。

