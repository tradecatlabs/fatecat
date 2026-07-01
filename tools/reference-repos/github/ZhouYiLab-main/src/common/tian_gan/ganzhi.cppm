// 干支系统模块 - 天干地支核心功能
// 整合自旧代码，提供完整的天干地支功能

export module ZhouYi.GanZhi;

// 导入反射库
import magic_enum;

// 导入标准库（最后）
import std;

/**
 * @brief 干支系统命名空间
 * 
 * 提供天干地支的核心定义和相关功能
 */
export namespace ZhouYi::GanZhi {

// ==================== 枚举定义 ====================

/**
 * @brief 天干枚举
 */
enum class TianGan {
    Jia = 0,   // 甲
    Yi,        // 乙
    Bing,      // 丙
    Ding,      // 丁
    Wu,        // 戊
    Ji,        // 己
    Geng,      // 庚
    Xin,       // 辛
    Ren,       // 壬
    Gui        // 癸
};

/**
 * @brief 地支枚举
 */
enum class DiZhi {
    Zi = 0,    // 子
    Chou,      // 丑
    Yin,       // 寅
    Mao,       // 卯
    Chen,      // 辰
    Si,        // 巳
    Wu,        // 午
    Wei,       // 未
    Shen,      // 申
    You,       // 酉
    Xu,        // 戌
    Hai        // 亥
};

/**
 * @brief 五行枚举
 */
enum class WuXing {
    Mu = 1,    // 木
    Huo = 2,   // 火
    Tu = 3,    // 土
    Jin = 4,   // 金
    Shui = 5   // 水
};

/**
 * @brief 阴阳枚举
 */
enum class YinYang {
    Yin = 0,   // 阴
    Yang = 1   // 阳
};

// ==================== 运算符重载 ====================

/**
 * @brief 天干加法运算
 */
constexpr TianGan operator+(TianGan gan, int num) {
    int value = static_cast<int>(gan) + num;
    return static_cast<TianGan>((value % 10 + 10) % 10);
}

/**
 * @brief 地支加法运算
 */
constexpr DiZhi operator+(DiZhi zhi, int num) {
    int value = static_cast<int>(zhi) + num;
    return static_cast<DiZhi>((value % 12 + 12) % 12);
}

/**
 * @brief 地支减法运算（获取相距数）
 */
constexpr int operator-(DiZhi left, DiZhi right) {
    return (static_cast<int>(left) - static_cast<int>(right) + 12) % 12;
}

/**
 * @brief 地支前置自增
 */
constexpr DiZhi& operator++(DiZhi& zhi) {
    zhi = static_cast<DiZhi>((static_cast<int>(zhi) + 1) % 12);
    return zhi;
}

/**
 * @brief 地支前置自减
 */
constexpr DiZhi& operator--(DiZhi& zhi) {
    zhi = static_cast<DiZhi>((static_cast<int>(zhi) - 1 + 12) % 12);
    return zhi;
}

// ==================== 中文名称映射 ====================

namespace Mapper {
    // 天干中文名称
    constexpr auto to_zh(TianGan gan) -> std::string_view {
        constexpr std::array<std::string_view, 10> names = {
            "甲", "乙", "丙", "丁", "戊", 
            "己", "庚", "辛", "壬", "癸"
        };
        return names[static_cast<int>(gan)];
    }
    
    // 地支中文名称
    constexpr auto to_zh(DiZhi zhi) -> std::string_view {
        constexpr std::array<std::string_view, 12> names = {
            "子", "丑", "寅", "卯", "辰", "巳",
            "午", "未", "申", "酉", "戌", "亥"
        };
        return names[static_cast<int>(zhi)];
    }
    
    // 五行中文名称
    constexpr auto to_zh(WuXing wx) -> std::string_view {
        constexpr std::array<std::string_view, 5> names = {
            "木", "火", "土", "金", "水"
        };
        return names[static_cast<int>(wx) - 1];
    }
    
    // 阴阳中文名称
    constexpr auto to_zh(YinYang yy) -> std::string_view {
        return yy == YinYang::Yang ? "阳" : "阴";
    }
    
    // 生肖名称
    constexpr auto sheng_xiao_zh(DiZhi zhi) -> std::string_view {
        constexpr std::array<std::string_view, 12> names = {
            "鼠", "牛", "虎", "兔", "龙", "蛇",
            "马", "羊", "猴", "鸡", "狗", "猪"
        };
        return names[static_cast<int>(zhi)];
    }
    
    // 从中文查找天干
    constexpr auto from_zh_gan(std::string_view zh_name) -> std::optional<TianGan> {
        constexpr std::array<std::string_view, 10> names = {
            "甲", "乙", "丙", "丁", "戊", 
            "己", "庚", "辛", "壬", "癸"
        };
        
        for (std::size_t i = 0; i < names.size(); ++i) {
            if (names[i] == zh_name) {
                return static_cast<TianGan>(i);
            }
        }
        return std::nullopt;
    }
    
    // 从中文查找地支
    constexpr auto from_zh_zhi(std::string_view zh_name) -> std::optional<DiZhi> {
        constexpr std::array<std::string_view, 12> names = {
            "子", "丑", "寅", "卯", "辰", "巳",
            "午", "未", "申", "酉", "戌", "亥"
        };
        
        for (std::size_t i = 0; i < names.size(); ++i) {
            if (names[i] == zh_name) {
                return static_cast<DiZhi>(i);
            }
        }
        return std::nullopt;
    }
}

// ==================== 五行属性 ====================

/**
 * @brief 获取天干五行
 */
constexpr WuXing get_wu_xing(TianGan gan) {
    constexpr std::array<WuXing, 10> elements = {
        WuXing::Mu, WuXing::Mu,     // 甲乙木
        WuXing::Huo, WuXing::Huo,   // 丙丁火
        WuXing::Tu, WuXing::Tu,     // 戊己土
        WuXing::Jin, WuXing::Jin,   // 庚辛金
        WuXing::Shui, WuXing::Shui  // 壬癸水
    };
    return elements[static_cast<int>(gan)];
}

/**
 * @brief 获取地支五行
 */
constexpr WuXing get_wu_xing(DiZhi zhi) {
    constexpr std::array<WuXing, 12> elements = {
        WuXing::Shui,               // 子水
        WuXing::Tu,                 // 丑土
        WuXing::Mu, WuXing::Mu,     // 寅卯木
        WuXing::Tu,                 // 辰土
        WuXing::Huo, WuXing::Huo,   // 巳午火
        WuXing::Tu,                 // 未土
        WuXing::Jin, WuXing::Jin,   // 申酉金
        WuXing::Tu,                 // 戌土
        WuXing::Shui                // 亥水
    };
    return elements[static_cast<int>(zhi)];
}

// ==================== 阴阳属性 ====================

/**
 * @brief 获取天干阴阳
 */
constexpr YinYang get_yin_yang(TianGan gan) {
    // 甲丙戊庚壬为阳，乙丁己辛癸为阴
    return (static_cast<int>(gan) % 2 == 0) ? YinYang::Yang : YinYang::Yin;
}

/**
 * @brief 获取地支阴阳
 */
constexpr YinYang get_yin_yang(DiZhi zhi) {
    // 子寅辰午申戌为阳，丑卯巳未酉亥为阴
    return (static_cast<int>(zhi) % 2 == 0) ? YinYang::Yang : YinYang::Yin;
}

// ==================== 五行生克关系 ====================

/**
 * @brief 判断五行相生（x生y）
 * 
 * 五行相生规律：
 * - 木生火：木材燃烧生火，火赖木生
 * - 火生土：火焚木成灰土，土赖火生
 * - 土生金：土中蕴藏金矿，金赖土生
 * - 金生水：金属融化成水，水赖金生（又说金寒生水）
 * - 水生木：水滋润树木生长，木赖水生
 * 
 * 生我者为母，我生者为子，故称"母子相生"
 * 
 * @param x 生者（母）
 * @param y 被生者（子）
 * @return true 如果 x 生 y
 */
constexpr bool wu_xing_sheng(WuXing x, WuXing y) {
    int ix = static_cast<int>(x);
    int iy = static_cast<int>(y);
    return (ix == 1 && iy == 2) ||  // 木(1)生火(2)
           (ix == 2 && iy == 3) ||  // 火(2)生土(3)
           (ix == 3 && iy == 4) ||  // 土(3)生金(4)
           (ix == 4 && iy == 5) ||  // 金(4)生水(5)
           (ix == 5 && iy == 1);    // 水(5)生木(1)
}

/**
 * @brief 判断五行相克（x克y）
 * 
 * 五行相克规律：
 * - 木克土：树木扎根于土，木能疏土（木胜土）
 * - 土克水：土能防水、吸水，水来土掩（土胜水）
 * - 水克火：水能灭火，水火不容（水胜火）
 * - 火克金：火能熔金，烈火炼真金（火胜金）
 * - 金克木：金属可以砍伐树木，金刚克木（金胜木）
 * 
 * 克我者为所不胜，我克者为所胜，故称"克制相胜"
 * 
 * @param x 克者（所胜）
 * @param y 被克者（所不胜）
 * @return true 如果 x 克 y
 */
constexpr bool wu_xing_ke(WuXing x, WuXing y) {
    int ix = static_cast<int>(x);
    int iy = static_cast<int>(y);
    return (ix == 1 && iy == 3) ||  // 木(1)克土(3)
           (ix == 3 && iy == 5) ||  // 土(3)克水(5)
           (ix == 5 && iy == 2) ||  // 水(5)克火(2)
           (ix == 2 && iy == 4) ||  // 火(2)克金(4)
           (ix == 4 && iy == 1);    // 金(4)克木(1)
}

// ==================== 地支关系 ====================

/**
 * @brief 判断地支相冲（六冲）
 * 
 * 地支六冲，又称"六位相冲"，是地支相距六位的对冲关系。
 * 相冲代表对立、冲突、动荡、变化，主破坏之力。
 * 
 * 六冲对照：
 * - 子午冲：水火相冲（子水 vs 午火），北方与南方相冲
 * - 丑未冲：土土相冲（丑土 vs 未土），东北与西南相冲  
 * - 寅申冲：木金相冲（寅木 vs 申金），东北与西南相冲
 * - 卯酉冲：木金相冲（卯木 vs 酉金），东方与西方相冲，日出与日落
 * - 辰戌冲：土土相冲（辰土 vs 戌土），东南与西北相冲
 * - 巳亥冲：火水相冲（巳火 vs 亥水），东南与西北相冲
 * 
 * 规律：地支相距六位即相冲（180度对冲）
 * 影响：主变动、搬迁、离散、破坏、疾病等
 * 
 * @param zhi1 第一个地支
 * @param zhi2 第二个地支
 * @return true 如果两地支相冲
 */
constexpr bool is_chong(DiZhi zhi1, DiZhi zhi2) {
    return (static_cast<int>(zhi1) + 6) % 12 == static_cast<int>(zhi2);
}

/**
 * @brief 判断地支相刑
 * 
 * 地支相刑是地支之间的刑罚关系，代表刑伤、灾祸、官非、病痛。
 * 刑分为四种类型：
 * 
 * 1. 无礼之刑（子卯刑）：
 *    - 子刑卯、卯刑子
 *    - 子为水，卯为木，水生木，本为相生，但因过度则为刑
 *    - 主无礼、淫乱、犯上、礼教败坏
 *    - 子卯为桃花，相刑主感情纠葛、桃色事件
 * 
 * 2. 无恩之刑（寅巳申三刑）：
 *    - 寅刑巳、巳刑申、申刑寅（循环相刑）
 *    - 寅木、巳火、申金，三者既相生又相克，恩中藏害
 *    - 主忘恩负义、恩将仇报、背信弃义
 *    - 又称"持势之刑"，刑罚最重
 * 
 * 3. 恃势之刑（丑戌未三刑）：
 *    - 丑刑戌、戌刑未、未刑丑（循环相刑）
 *    - 三者皆为土，土旺则相刑，主霸道、恃强凌弱
 *    - 主自以为是、仗势欺人、专横跋扈
 *    - 又称"倚势之刑"、"土刑"
 * 
 * 4. 自刑（辰辰、午午、酉酉、亥亥）：
 *    - 自己刑自己，即同一地支相见则刑
 *    - 辰辰自刑：辰为天罡，水土相战
 *    - 午午自刑：午为阳火，火过旺则自焚
 *    - 酉酉自刑：酉为金，金刚过盛则自损
 *    - 亥亥自刑：亥为水，水漫过头则自困
 *    - 主自我矛盾、内耗、自残、自寻烦恼
 * 
 * 影响：主刑伤、官非、牢狱、疾病、灾祸、是非
 * 
 * @param zhi1 第一个地支
 * @param zhi2 第二个地支
 * @return true 如果两地支相刑
 */
constexpr bool is_xing(DiZhi zhi1, DiZhi zhi2) {
    int i1 = static_cast<int>(zhi1);
    int i2 = static_cast<int>(zhi2);
    
    // 无礼之刑：子卯相刑
    if ((i1 == 0 && i2 == 3) || (i1 == 3 && i2 == 0)) return true;
    
    // 无恩之刑：寅巳申三刑（循环相刑）
    if ((i1 == 2 && i2 == 5) || (i1 == 5 && i2 == 9) || (i1 == 9 && i2 == 2)) return true;
    
    // 恃势之刑：丑戌未三刑（循环相刑）
    if ((i1 == 1 && i2 == 10) || (i1 == 10 && i2 == 7) || (i1 == 7 && i2 == 1)) return true;
    
    // 自刑：辰辰、午午、酉酉、亥亥（同一地支相见）
    if (i1 == i2 && (i1 == 4 || i1 == 6 || i1 == 9 || i1 == 11)) return true;
    
    return false;
}

/**
 * @brief 判断地支相合（六合）
 * 
 * 地支六合是地支之间的合化关系，代表和谐、亲密、合作、喜庆。
 * 相合主吉祥、团结、婚姻、缘分，力量较三合为弱。
 * 
 * 六合对照及合化五行：
 * - 子丑合化土：子水配丑土，阴阳相合，水土相济，北方合（鼠牛合）
 * - 寅亥合化木：寅木配亥水，木得水生，木旺相生，东北合（虎猪合）
 * - 卯戌合化火：卯木配戌土，木火通明，文明之合，东西合（兔狗合）
 * - 辰酉合化金：辰土配酉金，土生金旺，金玉良缘，东南西合（龙鸡合）
 * - 巳申合化水：巳火配申金，火金相融，水火既济，南西合（蛇猴合）
 * - 午未合化土：午火配未土，火土相生，中正之合，南方合（马羊合）
 * 
 * 合化条件（一般需要）：
 * 1. 有化神当令（月令临合化之五行）
 * 2. 有化神透干（天干透出合化五行）  
 * 3. 无强烈冲刑破害
 * 
 * 规律特点：
 * - 阴阳相配：阳支合阴支（子阳丑阴、寅阳亥阴等）
 * - 方位对应：多为东西、南北或对角方位相合
 * - 五行和谐：合化后五行多与双方有生助关系
 * 
 * 影响：主婚姻美满、合作愉快、贵人相助、喜庆吉利
 * 
 * @param zhi1 第一个地支
 * @param zhi2 第二个地支
 * @return true 如果两地支相合
 */
constexpr bool is_he(DiZhi zhi1, DiZhi zhi2) {
    constexpr std::array<std::pair<int, int>, 6> he_pairs = {{
        {0, 1},   // 子(0)丑(1)合化土
        {2, 11},  // 寅(2)亥(11)合化木
        {3, 10},  // 卯(3)戌(10)合化火
        {4, 9},   // 辰(4)酉(9)合化金
        {5, 8},   // 巳(5)申(8)合化水
        {6, 7}    // 午(6)未(7)合化土
    }};
    
    int i1 = static_cast<int>(zhi1);
    int i2 = static_cast<int>(zhi2);
    
    for (const auto& [a, b] : he_pairs) {
        if ((i1 == a && i2 == b) || (i1 == b && i2 == a)) {
            return true;
        }
    }
    return false;
}

/**
 * @brief 判断地支相害（六害）
 * 
 * 地支六害，又称"六穿"、"相穿"，是地支之间的破坏关系。
 * 相害是因为破坏了相合关系而产生的，代表暗中伤害、小人陷害。
 * 害比冲、刑的力量弱，但其作用隐蔽，不易察觉，更加阴险。
 * 
 * 六害对照及成因：
 * - 子未害：子丑合，未冲丑，故子未相害（穿六合）
 *   子水克未土，未为木库，水土交战，主被人拖累
 * 
 * - 丑午害：丑子合，午未合，午冲子，故丑午相害
 *   丑土晦午火，午火伤丑金，主损耗、消磨
 * 
 * - 寅巳害：寅亥合，巳申合，寅巳刑，故寅巳相害（无恩之害）
 *   寅木生巳火，巳火反制寅木，主恩中带害、养虎为患
 * 
 * - 卯辰害：卯戌合，辰酉合，卯辰相邻，故卯辰相害
 *   卯木克辰土，辰为湿土，主阴湿、暗昧、抑郁
 * 
 * - 申亥害：申巳合，亥寅合，申亥相穿，故申亥相害
 *   申金克亥中甲木，亥水生申金中气，主互相伤害
 * 
 * - 酉戌害：酉辰合，戌卯合，酉戌相邻，故酉戌相害
 *   酉金克戌中丁火，戌土生酉金，主暗害、背叛
 * 
 * 规律特点：
 * - 相害是因破坏六合而成，合中带害
 * - 相害之地支往往与第三方有刑冲合的关系
 * - 六害主小人、暗害、牵连、拖累
 * 
 * 影响：主小人陷害、暗箭伤人、拖累牵连、明合暗斗、
 *       感情不和、疾病缠身、小灾小难
 * 
 * @param zhi1 第一个地支
 * @param zhi2 第二个地支
 * @return true 如果两地支相害
 */
constexpr bool is_hai(DiZhi zhi1, DiZhi zhi2) {
    constexpr std::array<std::pair<int, int>, 6> hai_pairs = {{
        {0, 7},   // 子(0)未(7)害
        {1, 6},   // 丑(1)午(6)害
        {2, 5},   // 寅(2)巳(5)害
        {3, 4},   // 卯(3)辰(4)害
        {8, 11},  // 申(8)亥(11)害
        {9, 10}   // 酉(9)戌(10)害
    }};
    
    int i1 = static_cast<int>(zhi1);
    int i2 = static_cast<int>(zhi2);
    
    for (const auto& [a, b] : hai_pairs) {
        if ((i1 == a && i2 == b) || (i1 == b && i2 == a)) {
            return true;
        }
    }
    return false;
}

/**
 * @brief 判断地支三合
 * 
 * 地支三合局是三个地支合化成一个五行的组合，力量最强。
 * 三合局按照五行的"生、旺、墓"三个阶段组成，代表从生到旺到归藏的完整循环。
 * 
 * 四组三合局及其组成（生旺墓）：
 * 
 * 1. 申子辰合水局：
 *    - 申（长生）：水长生于申，申为水的起源
 *    - 子（帝旺）：子为水之本位，水最旺盛
 *    - 辰（墓库）：辰为水库，水归藏之地
 *    - 方位：西  北  东，跨越三方
 *    - 季节：秋末  冬  春初，水气旺盛之时
 * 
 * 2. 亥卯未合木局：
 *    - 亥（长生）：木长生于亥，水生木之始
 *    - 卯（帝旺）：卯为木之本位，木最旺盛
 *    - 未（墓库）：未为木库，木归藏之地
 *    - 方位：北  东  南，顺时针三合
 *    - 季节：冬末  春  夏初，木气生发之时
 * 
 * 3. 寅午戌合火局：
 *    - 寅（长生）：火长生于寅，木生火之始
 *    - 午（帝旺）：午为火之本位，火最旺盛
 *    - 戌（墓库）：戌为火库，火归藏之地
 *    - 方位：东  南  西，三合成局
 *    - 季节：春末  夏  秋初，火气炎盛之时
 * 
 * 4. 巳酉丑合金局：
 *    - 巳（长生）：金长生于巳，火炼金成
 *    - 酉（帝旺）：酉为金之本位，金最旺盛
 *    - 丑（墓库）：丑为金库，金归藏之地
 *    - 方位：南  西  北，逆时针三合
 *    - 季节：夏末  秋  冬初，金气肃杀之时
 * 
 * 规律特点：
 * - 三合局相距四位（120度），形成等边三角形
 * - 生旺墓三者齐全，力量最强，可改变原有五行属性
 * - 即使缺一，只要有两个也有一定的合力
 * - 三合局以"旺"为主导，有旺支则合局有力
 * 
 * 合化条件：
 * 1. 三支齐全（完美三合）
 * 2. 月令当旺（月令临合化之五行）
 * 3. 无强烈冲破（冲克旺支或生支）
 * 4. 有化神透干（天干透出合化五行更佳）
 * 
 * 影响：主力量强大、成就事业、团结合作、势力庞大、
 *       聚财聚势、贵人相助、婚姻美满（比六合更稳固）
 * 
 * @param zhi1 第一个地支
 * @param zhi2 第二个地支  
 * @param zhi3 第三个地支
 * @return pair<bool, WuXing> - 是否三合，合化的五行
 */
constexpr auto is_san_he(DiZhi zhi1, DiZhi zhi2, DiZhi zhi3) -> std::pair<bool, WuXing> {
    std::array<int, 3> arr = {
        static_cast<int>(zhi1),
        static_cast<int>(zhi2),
        static_cast<int>(zhi3)
    };
    std::ranges::sort(arr);
    
    // 申子辰合水局：申(8长生) + 子(0帝旺) + 辰(4墓库)
    if (arr[0] == 0 && arr[1] == 4 && arr[2] == 8) return {true, WuXing::Shui};
    
    // 亥卯未合木局：亥(11长生) + 卯(3帝旺) + 未(7墓库)
    if (arr[0] == 3 && arr[1] == 7 && arr[2] == 11) return {true, WuXing::Mu};
    
    // 寅午戌合火局：寅(2长生) + 午(6帝旺) + 戌(10墓库)
    if (arr[0] == 2 && arr[1] == 6 && arr[2] == 10) return {true, WuXing::Huo};
    
    // 巳酉丑合金局：巳(5长生) + 酉(9帝旺) + 丑(1墓库)
    if (arr[0] == 1 && arr[1] == 5 && arr[2] == 9) return {true, WuXing::Jin};
    
    return {false, WuXing::Mu};  // 未合局
}

// ==================== 天干寄宫 ====================

/**
 * @brief 获取天干寄宫地支
 * 
 * 大六壬十天干寄宫口诀：
 *   甲课寅兮乙课辰，
 *   丙戊课巳不须论，
 *   丁己课未庚申上，
 *   辛戌壬亥是其真，
 *   癸课原来丑宫坐，
 *   分明不用四正神。
 * 
 * 规则：
 *   1. 阳干（甲丙戊庚壬）寄禄位，如甲禄在寅
 *   2. 阴干（乙丁己辛癸）寄冠带位，如乙冠带在辰
 *   3. 丙戊同寄巳，丁己同寄未
 *   4. 子午卯酉四正位不参与寄宫
 */
constexpr DiZhi get_ji_gong(TianGan gan) {
    constexpr std::array<DiZhi, 10> palaces = {
        DiZhi::Yin,    // 甲寄寅（阳干寄禄）
        DiZhi::Chen,   // 乙寄辰（阴干寄冠带）
        DiZhi::Si,     // 丙寄巳（阳干寄禄）
        DiZhi::Wei,    // 丁寄未（阴干寄冠带）
        DiZhi::Si,     // 戊寄巳（阳干寄禄，与丙同宫）
        DiZhi::Wei,    // 己寄未（阴干寄冠带，与丁同宫）
        DiZhi::Shen,   // 庚寄申（阳干寄禄）
        DiZhi::Xu,     // 辛寄戌（阴干寄冠带）
        DiZhi::Hai,    // 壬寄亥（阳干寄禄）
        DiZhi::Chou    // 癸寄丑（阴干寄冠带）
    };
    return palaces[static_cast<int>(gan)];
}

/**
 * @brief 获取地支中寄居的天干
 */
inline auto get_ji_gan(DiZhi zhi) -> std::vector<TianGan> {
    switch (zhi) {
    case DiZhi::Yin:
        return {TianGan::Jia};
    case DiZhi::Chen:
        return {TianGan::Yi};
    case DiZhi::Si:
        return {TianGan::Bing, TianGan::Wu};
    case DiZhi::Wei:
        return {TianGan::Ding, TianGan::Ji};
    case DiZhi::Shen:
        return {TianGan::Geng};
    case DiZhi::Xu:
        return {TianGan::Xin};
    case DiZhi::Hai:
        return {TianGan::Ren};
    case DiZhi::Chou:
        return {TianGan::Gui};
    default:
        // 子、卯、午、酉无天干寄宫
        return {};
    }
}

// ==================== 贵人表 ====================

/**
 * @brief 获取天干贵人地支
 * @param is_day true为阳贵人（昼），false为阴贵人（夜）
 */
constexpr DiZhi get_gui_ren(TianGan gan, bool is_day) {
    // 贵人歌诀：甲戊庚牛羊，乙己鼠猴乡，丙丁猪鸡位，壬癸蛇兔藏，六辛逢马虎
    constexpr std::array<std::pair<DiZhi, DiZhi>, 10> table = {{
        {DiZhi::Chou, DiZhi::Wei},  // 甲 - 丑/未（牛/羊）
        {DiZhi::Zi, DiZhi::Shen},   // 乙 - 子/申（鼠/猴）
        {DiZhi::Hai, DiZhi::You},   // 丙 - 亥/酉（猪/鸡）
        {DiZhi::Hai, DiZhi::You},   // 丁 - 亥/酉（猪/鸡）
        {DiZhi::Chou, DiZhi::Wei},  // 戊 - 丑/未（牛/羊）
        {DiZhi::Zi, DiZhi::Shen},   // 己 - 子/申（鼠/猴）
        {DiZhi::Chou, DiZhi::Wei},  // 庚 - 丑/未（牛/羊）
        {DiZhi::Wu, DiZhi::Yin},    // 辛 - 午/寅（马/虎）
        {DiZhi::Si, DiZhi::Mao},    // 壬 - 巳/卯（蛇/兔）
        {DiZhi::Si, DiZhi::Mao}     // 癸 - 巳/卯（蛇/兔）
    }};
    
    auto [yang, yin] = table[static_cast<int>(gan)];
    return is_day ? yang : yin;
}

/**
 * @brief 判断是否为白天（卯时到申时）
 */
constexpr bool is_daytime(DiZhi hour) {
    int idx = static_cast<int>(hour);
    return (idx >= 3 && idx <= 8); // 3=卯, 8=申
}

// ==================== 地支藏干 ====================

/**
 * @brief 藏干数据结构（最多3个天干）
 */
struct CangGanData {
    std::array<TianGan, 3> gans;
    std::size_t count;
    
    constexpr CangGanData(TianGan g1) 
        : gans{g1, TianGan::Jia, TianGan::Jia}, count(1) {}
    
    constexpr CangGanData(TianGan g1, TianGan g2) 
        : gans{g1, g2, TianGan::Jia}, count(2) {}
    
    constexpr CangGanData(TianGan g1, TianGan g2, TianGan g3) 
        : gans{g1, g2, g3}, count(3) {}
    
    constexpr auto get_span() const -> std::span<const TianGan> {
        return std::span<const TianGan>(gans.data(), count);
    }
    
    constexpr auto operator[](std::size_t idx) const -> TianGan {
        return gans[idx];
    }
};

// 藏干数据表（编译时常量）
inline constexpr std::array<CangGanData, 12> cang_gan_table = {{
    CangGanData{TianGan::Gui},                            // 子：癸
    CangGanData{TianGan::Ji, TianGan::Gui, TianGan::Xin}, // 丑：己癸辛
    CangGanData{TianGan::Jia, TianGan::Bing, TianGan::Wu}, // 寅：甲丙戊
    CangGanData{TianGan::Yi},                             // 卯：乙
    CangGanData{TianGan::Wu, TianGan::Yi, TianGan::Gui},  // 辰：戊乙癸
    CangGanData{TianGan::Bing, TianGan::Wu, TianGan::Geng}, // 巳：丙戊庚
    CangGanData{TianGan::Ding, TianGan::Ji},              // 午：丁己
    CangGanData{TianGan::Ji, TianGan::Ding, TianGan::Yi}, // 未：己丁乙
    CangGanData{TianGan::Geng, TianGan::Ren, TianGan::Wu}, // 申：庚壬戊
    CangGanData{TianGan::Xin},                            // 酉：辛
    CangGanData{TianGan::Wu, TianGan::Xin, TianGan::Ding}, // 戌：戊辛丁
    CangGanData{TianGan::Ren, TianGan::Jia}               // 亥：壬甲
}};

/**
 * @brief 获取地支藏干（主气、中气、余气）
 * @return std::vector 包含藏干的向量
 */
inline auto get_cang_gan(DiZhi zhi) -> std::vector<TianGan> {
    const auto& data = cang_gan_table[static_cast<int>(zhi)];
    return std::vector<TianGan>(data.gans.begin(), data.gans.begin() + data.count);
}

// ==================== 六十甲子 ====================

/**
 * @brief 六十甲子类
 */
class LiuShiJiaZi {
public:
    TianGan gan;
    DiZhi zhi;
    
    constexpr LiuShiJiaZi(TianGan g, DiZhi z) : gan(g), zhi(z) {}
    
    /**
     * @brief 从索引创建（0-59）
     */
    static constexpr LiuShiJiaZi from_index(int index) {
        index = ((index % 60) + 60) % 60;
        return LiuShiJiaZi(
            static_cast<TianGan>(index % 10),
            static_cast<DiZhi>(index % 12)
        );
    }
    
    /**
     * @brief 获取索引（0-59）
     */
    constexpr int to_index() const {
        // 使用中国剩余定理求解
        int g = static_cast<int>(gan);
        int z = static_cast<int>(zhi);
        
        // 寻找满足条件的索引
        for (int i = g; i < 60; i += 10) {
            if (i % 12 == z) {
                return i;
            }
        }
        return 0;
    }
    
    /**
     * @brief 获取中文名称
     */
    std::string to_string() const {
        return std::string(Mapper::to_zh(gan)) + std::string(Mapper::to_zh(zhi));
    }
    
    /**
     * @brief 获取纳音五行
     */
    constexpr WuXing get_na_yin() const {
        // 纳音五行表
        constexpr std::array<WuXing, 60> na_yin_table = {
            WuXing::Jin, WuXing::Jin,   // 甲子乙丑海中金
            WuXing::Huo, WuXing::Huo,   // 丙寅丁卯炉中火
            WuXing::Mu, WuXing::Mu,     // 戊辰己巳大林木
            WuXing::Jin, WuXing::Jin,   // 庚午辛未路旁土
            WuXing::Tu, WuXing::Tu,     // 壬申癸酉剑锋金
            WuXing::Shui, WuXing::Shui, // 甲戌乙亥山头火
            WuXing::Huo, WuXing::Huo,   // 丙子丁丑涧下水
            WuXing::Tu, WuXing::Tu,     // 戊寅己卯城头土
            WuXing::Mu, WuXing::Mu,     // 庚辰辛巳白蜡金
            WuXing::Jin, WuXing::Jin,   // 壬午癸未杨柳木
            WuXing::Shui, WuXing::Shui, // 甲申乙酉泉中水
            WuXing::Tu, WuXing::Tu,     // 丙戌丁亥屋上土
            WuXing::Mu, WuXing::Mu,     // 戊子己丑霹雳火
            WuXing::Huo, WuXing::Huo,   // 庚寅辛卯松柏木
            WuXing::Jin, WuXing::Jin,   // 壬辰癸巳长流水
            WuXing::Tu, WuXing::Tu,     // 甲午乙未沙中金
            WuXing::Shui, WuXing::Shui, // 丙申丁酉山下火
            WuXing::Huo, WuXing::Huo,   // 戊戌己亥平地木
            WuXing::Mu, WuXing::Mu,     // 庚子辛丑壁上土
            WuXing::Jin, WuXing::Jin,   // 壬寅癸卯金箔金
            WuXing::Tu, WuXing::Tu,     // 甲辰乙巳佛灯火
            WuXing::Shui, WuXing::Shui, // 丙午丁未天河水
            WuXing::Huo, WuXing::Huo,   // 戊申己酉大驿土
            WuXing::Mu, WuXing::Mu,     // 庚戌辛亥钗钏金
            WuXing::Jin, WuXing::Jin,   // 壬子癸丑桑柘木
            WuXing::Tu, WuXing::Tu,     // 甲寅乙卯大溪水
            WuXing::Shui, WuXing::Shui, // 丙辰丁巳沙中土
            WuXing::Huo, WuXing::Huo,   // 戊午己未天上火
            WuXing::Mu, WuXing::Mu,     // 庚申辛酉石榴木
            WuXing::Jin, WuXing::Jin    // 壬戌癸亥大海水
        };
        
        return na_yin_table[to_index()];
    }
};

/**
 * @brief 获取完整的六十甲子表
 */
inline auto get_liu_shi_jia_zi() -> std::vector<LiuShiJiaZi> {
    std::vector<LiuShiJiaZi> result;
    result.reserve(60);
    
    for (int i = 0; i < 60; ++i) {
        result.push_back(LiuShiJiaZi::from_index(i));
    }
    
    return result;
}

// ==================== 十二长生 ====================

/**
 * @brief 十二长生枚举
 * 
 * 表示天干在十二地支中的生命状态
 * 用于判断五行的旺衰
 */
enum class ShiErChangSheng {
    ChangSheng = 0,  // 长生 - 如婴儿出生，开始生长
    MuYu = 1,        // 沐浴 - 如婴儿沐浴，易受侵害
    GuanDai = 2,     // 冠带 - 如成人加冠，渐趋成熟
    LinGuan = 3,     // 临官 - 如人临官得位，兴旺发达
    DiWang = 4,      // 帝旺 - 如人壮盛，达到顶峰
    Shuai = 5,       // 衰 - 如人衰老，开始衰退
    Bing = 6,        // 病 - 如人患病，气力衰弱
    Si = 7,          // 死 - 如人死亡，生机断绝
    Mu = 8,          // 墓 - 如人入墓，归于寂静（又称"库"）
    Jue = 9,         // 绝 - 如形体灭绝，无气之地
    Tai = 10,        // 胎 - 如受胎孕育，开始孕育
    Yang = 11        // 养 - 如婴儿养育，生命延续
};

/**
 * @brief 十二长生中文映射命名空间
 */
namespace ShiErChangShengMapper {
    /**
     * @brief 转换为中文名称
     */
    constexpr auto to_zh(ShiErChangSheng cs) -> std::string_view {
        constexpr std::array<std::string_view, 12> names = {
            "长生", "沐浴", "冠带", "临官", "帝旺", "衰",
            "病", "死", "墓", "绝", "胎", "养"
        };
        return names[static_cast<int>(cs)];
    }

    /**
     * @brief 从中文名称查找
     */
    constexpr auto from_zh(std::string_view name) -> std::optional<ShiErChangSheng> {
        constexpr std::array<std::string_view, 12> names = {
            "长生", "沐浴", "冠带", "临官", "帝旺", "衰",
            "病", "死", "墓", "绝", "胎", "养"
        };
        
        for (std::size_t i = 0; i < names.size(); ++i) {
            if (names[i] == name) {
                return static_cast<ShiErChangSheng>(i);
            }
        }
        return std::nullopt;
    }
}

/**
 * @brief 获取天干在指定地支的十二长生状态
 * 
 * @param gan 天干
 * @param zhi 地支
 * @return 十二长生状态
 * 
 * 规则说明：
 * - 阳干（甲丙戊庚壬）顺行十二长生
 * - 阴干（乙丁己辛癸）逆行十二长生
 * 
 * 长生起点：
 * - 甲木长生在亥，乙木长生在午
 * - 丙火长生在寅，丁火长生在酉
 * - 戊土长生在寅，己土长生在酉（土同火）
 * - 庚金长生在巳，辛金长生在子
 * - 壬水长生在申，癸水长生在卯
 * 
 * @example
 * auto cs = get_shi_er_chang_sheng(TianGan::Jia, DiZhi::Hai); // 返回 ShiErChangSheng::ChangSheng
 */
inline auto get_shi_er_chang_sheng(TianGan gan, DiZhi zhi) -> ShiErChangSheng {
    // 长生地支索引（从子=0开始）
    static constexpr std::array<int, 10> chang_sheng_start = {
        11,  // 甲 - 亥 (11)
        6,   // 乙 - 午 (6)
        2,   // 丙 - 寅 (2)
        9,   // 丁 - 酉 (9)
        2,   // 戊 - 寅 (2)（土同火）
        9,   // 己 - 酉 (9)（土同火）
        5,   // 庚 - 巳 (5)
        0,   // 辛 - 子 (0)
        8,   // 壬 - 申 (8)
        3    // 癸 - 卯 (3)
    };
    
    int gan_idx = static_cast<int>(gan);
    int zhi_idx = static_cast<int>(zhi);
    int start = chang_sheng_start[gan_idx];
    
    int offset;
    
    // 阳干顺行，阴干逆行
    if (gan_idx % 2 == 0) {
        // 阳干：甲丙戊庚壬（索引为偶数）
        offset = (zhi_idx - start + 12) % 12;
    } else {
        // 阴干：乙丁己辛癸（索引为奇数）
        offset = (start - zhi_idx + 12) % 12;
    }
    
    return static_cast<ShiErChangSheng>(offset);
}

/**
 * @brief 判断天干在指定地支是否为长生状态
 */
inline bool is_chang_sheng(TianGan gan, DiZhi zhi) {
    return get_shi_er_chang_sheng(gan, zhi) == ShiErChangSheng::ChangSheng;
}

/**
 * @brief 判断天干在指定地支是否为帝旺状态
 */
inline bool is_di_wang(TianGan gan, DiZhi zhi) {
    return get_shi_er_chang_sheng(gan, zhi) == ShiErChangSheng::DiWang;
}

/**
 * @brief 判断天干在指定地支是否为墓库状态
 */
inline bool is_mu_ku(TianGan gan, DiZhi zhi) {
    return get_shi_er_chang_sheng(gan, zhi) == ShiErChangSheng::Mu;
}

/**
 * @brief 判断天干在指定地支是否为绝地状态
 */
inline bool is_jue_di(TianGan gan, DiZhi zhi) {
    return get_shi_er_chang_sheng(gan, zhi) == ShiErChangSheng::Jue;
}

/**
 * @brief 获取天干的长生地支
 * 
 * @param gan 天干
 * @return 长生地支
 */
inline auto get_chang_sheng_zhi(TianGan gan) -> DiZhi {
    static constexpr std::array<DiZhi, 10> chang_sheng_map = {
        DiZhi::Hai,   // 甲木长生在亥
        DiZhi::Wu,    // 乙木长生在午
        DiZhi::Yin,   // 丙火长生在寅
        DiZhi::You,   // 丁火长生在酉
        DiZhi::Yin,   // 戊土长生在寅
        DiZhi::You,   // 己土长生在酉
        DiZhi::Si,    // 庚金长生在巳
        DiZhi::Zi,    // 辛金长生在子
        DiZhi::Shen,  // 壬水长生在申
        DiZhi::Mao    // 癸水长生在卯
    };
    
    return chang_sheng_map[static_cast<int>(gan)];
}

/**
 * @brief 获取天干的帝旺地支
 * 
 * @param gan 天干
 * @return 帝旺地支
 */
inline auto get_di_wang_zhi(TianGan gan) -> DiZhi {
    // 帝旺 = 长生 + 4（阳干顺行）或 长生 - 4（阴干逆行）
    auto chang_sheng = get_chang_sheng_zhi(gan);
    int cs_idx = static_cast<int>(chang_sheng);
    int gan_idx = static_cast<int>(gan);
    
    int di_wang_idx;
    if (gan_idx % 2 == 0) {
        // 阳干顺行
        di_wang_idx = (cs_idx + 4) % 12;
    } else {
        // 阴干逆行
        di_wang_idx = (cs_idx - 4 + 12) % 12;
    }
    
    return static_cast<DiZhi>(di_wang_idx);
}

/**
 * @brief 获取天干的墓库地支
 * 
 * @param gan 天干
 * @return 墓库地支
 */
inline auto get_mu_ku_zhi(TianGan gan) -> DiZhi {
    // 墓库 = 长生 + 8（阳干顺行）或 长生 - 8（阴干逆行）
    auto chang_sheng = get_chang_sheng_zhi(gan);
    int cs_idx = static_cast<int>(chang_sheng);
    int gan_idx = static_cast<int>(gan);
    
    int mu_ku_idx;
    if (gan_idx % 2 == 0) {
        // 阳干顺行
        mu_ku_idx = (cs_idx + 8) % 12;
    } else {
        // 阴干逆行
        mu_ku_idx = (cs_idx - 8 + 12) % 12;
    }
    
    return static_cast<DiZhi>(mu_ku_idx);
}

// ==================== 六亲系统 ====================

/**
 * @brief 六亲枚举
 * 
 * 用于描述五行之间的六亲关系
 */
enum class LiuQin {
    FuMu,      // 父母（生我者）
    XiongDi,   // 兄弟（比和者）
    ZiSun,     // 子孙（我生者）
    QiCai,     // 妻财（我克者）
    GuanGui    // 官鬼（克我者）
};

/**
 * @brief 获取六亲关系
 * 
 * @param self_gan 日干（我）
 * @param other_zhi 他支
 * @return 六亲关系
 */
constexpr LiuQin get_liu_qin(TianGan self_gan, DiZhi other_zhi) {
    WuXing self_wx = get_wu_xing(self_gan);
    WuXing other_wx = get_wu_xing(other_zhi);
    
    if (wu_xing_sheng(other_wx, self_wx)) {
        return LiuQin::FuMu;  // 生我者为父母
    } else if (wu_xing_sheng(self_wx, other_wx)) {
        return LiuQin::ZiSun;  // 我生者为子孙
    } else if (wu_xing_ke(self_wx, other_wx)) {
        return LiuQin::QiCai;  // 我克者为妻财
    } else if (wu_xing_ke(other_wx, self_wx)) {
        return LiuQin::GuanGui;  // 克我者为官鬼
    } else {
        return LiuQin::XiongDi;  // 比和为兄弟
    }
}

/**
 * @brief 获取六亲中文名称
 */
constexpr std::string_view liu_qin_to_zh(LiuQin lq) {
    constexpr std::array<std::string_view, 5> names = {
        "父母", "兄弟", "子孙", "妻财", "官鬼"
    };
    return names[static_cast<int>(lq)];
}

// ==================== 十神系统 ====================

/**
 * @brief 十神枚举
 */
enum class ShiShen {
    BiJian,     // 比肩
    JieCai,     // 劫财
    ShiShen,    // 食神
    ShangGuan,  // 伤官
    PianCai,    // 偏财
    ZhengCai,   // 正财
    QiSha,      // 七杀
    ZhengGuan,  // 正官
    PianYin,    // 偏印
    ZhengYin    // 正印
};

/**
 * @brief 获取十神关系
 * 
 * @param self_gan 日干（我）
 * @param other_gan 他干
 * @return 十神关系
 */
constexpr ShiShen get_shi_shen(TianGan self_gan, TianGan other_gan) {
    WuXing self_wx = get_wu_xing(self_gan);
    WuXing other_wx = get_wu_xing(other_gan);
    YinYang self_yy = get_yin_yang(self_gan);
    YinYang other_yy = get_yin_yang(other_gan);
    bool same_yy = (self_yy == other_yy);
    
    if (self_wx == other_wx) {
        // 比和
        return same_yy ? ShiShen::BiJian : ShiShen::JieCai;
    } else if (wu_xing_sheng(self_wx, other_wx)) {
        // 我生者
        return same_yy ? ShiShen::ShiShen : ShiShen::ShangGuan;
    } else if (wu_xing_ke(self_wx, other_wx)) {
        // 我克者
        return same_yy ? ShiShen::PianCai : ShiShen::ZhengCai;
    } else if (wu_xing_ke(other_wx, self_wx)) {
        // 克我者
        return same_yy ? ShiShen::QiSha : ShiShen::ZhengGuan;
    } else {
        // 生我者
        return same_yy ? ShiShen::PianYin : ShiShen::ZhengYin;
    }
}

/**
 * @brief 获取十神中文名称
 */
constexpr std::string_view shi_shen_to_zh(ShiShen ss) {
    constexpr std::array<std::string_view, 10> names = {
        "比肩", "劫财", "食神", "伤官", "偏财",
        "正财", "七杀", "正官", "偏印", "正印"
    };
    return names[static_cast<int>(ss)];
}

// ==================== 地支遁干系统 ====================

/**
 * @brief 计算旬首地支
 * 
 * @param day_gan 日干
 * @param day_zhi 日支
 * @return 旬首地支
 */
constexpr DiZhi get_xun_shou(TianGan day_gan, DiZhi day_zhi) {
    int gan_idx = static_cast<int>(day_gan);
    int zhi_idx = static_cast<int>(day_zhi);
    int xun_shou_idx = (zhi_idx - gan_idx + 12) % 12;
    return static_cast<DiZhi>(xun_shou_idx);
}

/**
 * @brief 计算地支遁干
 * 
 * @param zhi 地支
 * @param day_gan 日干
 * @param day_zhi 日支
 * @return 遁干，如果空亡则返回 std::nullopt
 */
constexpr std::optional<TianGan> get_dun_gan(DiZhi zhi, TianGan day_gan, DiZhi day_zhi) {
    DiZhi xun_shou = get_xun_shou(day_gan, day_zhi);
    int zhi_delta = (static_cast<int>(zhi) - static_cast<int>(xun_shou) + 12) % 12;
    
    // 如果是10或11（戌或亥位置），则为空亡
    if (zhi_delta == 10 || zhi_delta == 11) {
        return std::nullopt;
    }
    
    // 从甲开始加偏移量
    return static_cast<TianGan>((static_cast<int>(TianGan::Jia) + zhi_delta) % 10);
}

/**
 * @brief 判断地支是否空亡
 * 
 * @param zhi 地支
 * @param day_gan 日干
 * @param day_zhi 日支
 * @return 是否空亡
 */
constexpr bool is_kong_wang(DiZhi zhi, TianGan day_gan, DiZhi day_zhi) {
    return !get_dun_gan(zhi, day_gan, day_zhi).has_value();
}

/**
 * @brief 获取旬空（空亡）的两个地支
 * 
 * @param day_gan 日干
 * @param day_zhi 日支
 * @return 旬空的两个地支
 */
constexpr std::array<DiZhi, 2> get_kong_wang(TianGan day_gan, DiZhi day_zhi) {
    DiZhi xun_shou = get_xun_shou(day_gan, day_zhi);
    int xs_idx = static_cast<int>(xun_shou);
    return {
        static_cast<DiZhi>((xs_idx - 2 + 12) % 12),
        static_cast<DiZhi>((xs_idx - 1 + 12) % 12)
    };
}

} // namespace ZhouYi::GanZhi

