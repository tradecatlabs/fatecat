// C++23 Module - 六爻排盘系统
export module ZhouYi.LiuYao;

// 导入第三方库模块（优先）
import fmt;
import nlohmann.json;

// 导入自定义通用模块
import ZhouYi.BaZiBase;      // 八字基础数据结构（Pillar, BaZi）
import ZhouYi.GanZhi;        // 干支系统（包含地支关系）
import ZhouYi.WuXingUtils;   // 五行工具（包含旺衰计算）

// 导入标准库模块（最后）
import std;

// #define debug

// 导出所有公共接口
export namespace ZhouYi::LiuYao {

// 使用通用命名空间
using namespace ZhouYi::BaZiBase;
using namespace ZhouYi::GanZhi;
using namespace ZhouYi::WuXingUtils;

// 存储每一爻的详细信息 (结构优化)
// 存储每一爻的详细信息
struct YaoDetails
{
    int position; // 1-6

    // 本卦信息
    Pillar mainPillar; // 本卦纳甲干支
    std::string mainElement; // 本卦爻支五行 (string)
    std::string mainRelative; // 本卦六亲

    // 伏神信息
    Pillar hiddenPillar; // 伏神干支 (optional)
    std::string hiddenRelative; // 伏神六亲 (optional)
    std::string hiddenElement; // 伏神五行 (optional)

    // 变爻/变卦信息 (变卦)
    bool isChanging = false; // 是否为动爻
    Pillar changedPillar; // 变出之爻的干支 (按变卦独立纳甲) (optional)
    std::string changedElement; // 变出之爻地支五行 (optional string)
    std::string changedRelative; // 变出之爻六亲 (相对本卦宫位五行) (optional)

    // 其他辅助信息
    std::string spirit; // 六神 (string)
    std::string wangShuai; // 旺衰
    std::string shiYingMark; // 世/应标记 ("世", "应", " ")
    char mainYaoType; // 本卦爻阴阳 ('0'或'1')
    std::string changeMark = " "; // 动爻标记 ('X' 阴变, 'O' 阳变, " ")

    // JSON 序列化（手动定义，因为 NLOHMANN_DEFINE_TYPE_INTRUSIVE 在模块中不工作）
    friend void to_json(nlohmann::json& j, const YaoDetails& y) {
        j = {
            {"position", y.position},
            {"mainPillar", y.mainPillar},
            {"mainElement", y.mainElement},
            {"mainRelative", y.mainRelative},
            {"hiddenPillar", y.hiddenPillar},
            {"hiddenRelative", y.hiddenRelative},
            {"hiddenElement", y.hiddenElement},
            {"isChanging", y.isChanging},
            {"changedPillar", y.changedPillar},
            {"changedElement", y.changedElement},
            {"changedRelative", y.changedRelative},
            {"spirit", y.spirit},
            {"wangShuai", y.wangShuai},
            {"shiYingMark", y.shiYingMark},
            {"mainYaoType", y.mainYaoType},
            {"changeMark", y.changeMark}
        };
    }

    friend void from_json(const nlohmann::json& j, YaoDetails& y) {
        y.position = j["position"];
        y.mainPillar = j["mainPillar"];
        std::string me = j["mainElement"];
        std::string mr = j["mainRelative"];
        y.mainElement = me;
        y.mainRelative = mr;
        y.hiddenPillar = j["hiddenPillar"];
        std::string hr = j["hiddenRelative"];
        std::string he = j["hiddenElement"];
        y.hiddenRelative = hr;
        y.hiddenElement = he;
        y.isChanging = j["isChanging"];
        y.changedPillar = j["changedPillar"];
        std::string ce = j["changedElement"];
        std::string cr = j["changedRelative"];
        y.changedElement = ce;
        y.changedRelative = cr;
        std::string sp = j["spirit"];
        std::string ws = j["wangShuai"];
        std::string sm = j["shiYingMark"];
        y.spirit = sp;
        y.wangShuai = ws;
        y.shiYingMark = sm;
        // mainYaoType 是 char，需要特殊处理
        if (j.contains("mainYaoType")) {
            if (j["mainYaoType"].is_string()) {
                std::string myt = j["mainYaoType"];
                y.mainYaoType = myt.empty() ? '0' : myt[0];
            } else if (j["mainYaoType"].is_number()) {
                y.mainYaoType = static_cast<char>(j["mainYaoType"].get<int>() + '0');
            }
        }
        std::string cm = j["changeMark"];
        y.changeMark = cm;
    }

    friend std::ostream &operator<<(std::ostream &os, const YaoDetails &obj)
    {
        return os << "position: " << obj.position << " mainPillar: " << obj.mainPillar
                  << " mainElement: " << obj.mainElement << " mainRelative: " << obj.mainRelative
                  << " hiddenPillar: " << obj.hiddenPillar << " hiddenRelative: " << obj.hiddenRelative
                  << " hiddenElement: " << obj.hiddenElement << " isChanging: " << obj.isChanging
                  << " changedPillar: " << obj.changedPillar << " changedElement: " << obj.changedElement
                  << " changedRelative: " << obj.changedRelative << " spirit: " << obj.spirit
                  << " wangShuai: " << obj.wangShuai << " shiYingMark: " << obj.shiYingMark
                  << " mainYaoType: " << obj.mainYaoType << " changeMark: " << obj.changeMark;
    }
};

struct HexagramInfo
{
    std::string name; // 卦名 (使用 string_view)
    std::string meaning; // 简要含义 (使用 string_view)
    std::string fiveElement; // 五行属性 (使用 string_view)
    int shiYaoPosition; // 世爻位置 (1-6)
    int yingYaoPosition; // 应爻位置 (1-6)
    bool isYangHexagram; // 阳卦/阴卦
    std::string palaceType; // 所属宫位 (如 "乾", "坎"...) (使用 string_view)
    std::string innerHexagram; // 内卦
    std::string outerHexagram; // 外卦
    std::string structureType; // 卦结构类型 (如 "本宫", "游魂", "归魂", "" for others)
};

// 创建一个映射来关联数字串和卦象信息（const 在模块中自动 inline）
const std::unordered_map<std::string, HexagramInfo> hexagramMap = {
    // 乾宫（金）系列
    {"111111", {"乾为天", "刚健中正", "金", 6, 3, true, "乾", "乾", "乾", "本宫"}},
    {"011111", {"天风姤", "阴阳相遇", "金", 1, 4, true, "乾", "巽", "乾", ""}},
    {"001111", {"天山遁", "退避保全", "金", 2, 5, true, "乾", "艮", "乾", ""}},
    {"000111", {"天地否", "闭塞不通", "金", 3, 6, true, "乾", "坤", "乾", ""}},
    {"000011", {"风地观", "观察民情", "金", 4, 1, true, "乾", "坤", "巽", ""}},
    {"000001", {"山地剥", "阴盛阳衰", "金", 5, 2, true, "乾", "坤", "艮", ""}},
    {"000101", {"火地晋", "光明晋升", "金", 4, 1, true, "乾", "坤", "离", "游魂"}},
    {"111101", {"火天大有", "昌隆富有", "金", 3, 6, true, "乾", "乾", "离", "归魂"}},

    // 坎宫（水）系列
    {"010010", {"坎为水", "险陷重重", "水", 6, 3, true, "坎", "坎", "坎", "本宫"}},
    {"110010", {"水泽节", "节制有度", "水", 1, 4, true, "坎", "兑", "坎", ""}},
    {"100010", {"水雷屯", "初生艰难", "水", 2, 5, true, "坎", "震", "坎", ""}},
    {"101010", {"水火既济", "事已完成", "水", 3, 6, true, "坎", "离", "坎", ""}},
    {"101110", {"泽火革", "变革创新", "水", 4, 1, true, "坎", "离", "兑", ""}},
    {"101100", {"雷火丰", "盛大光明", "水", 5, 2, true, "坎", "离", "震", ""}},
    {"101000", {"地火明夷", "光明受伤", "水", 4, 1, true, "坎", "离", "坤", "游魂"}},
    {"010000", {"地水师", "兴师动众", "水", 3, 6, true, "坎", "坤", "坎", "归魂"}},

    // 艮宫（土）系列
    {"001001", {"艮为山", "静止不动", "土", 6, 3, true, "艮", "艮", "艮", "本宫"}},
    {"101001", {"山火贲", "文饰美化", "土", 1, 4, true, "艮", "离", "艮", ""}},
    {"111001", {"山天大畜", "积蓄力量", "土", 2, 5, true, "艮", "乾", "艮", ""}},
    {"110001", {"山泽损", "减损之道", "土", 3, 6, true, "艮", "兑", "艮", ""}},
    {"110101", {"火泽睽", "意见相左", "土", 4, 1, true, "艮", "兑", "离", ""}},
    {"110111", {"天泽履", "谨慎行事", "土", 5, 2, true, "艮", "兑", "乾", ""}},
    {"110011", {"风泽中孚", "诚信立身", "土", 4, 1, true, "艮", "兑", "巽", "游魂"}},
    {"001011", {"风山渐", "循序渐进", "土", 3, 6, true, "艮", "艮", "巽", "归魂"}},

    // 震宫（木）系列
    {"100100", {"震为雷", "震动奋发", "木", 6, 3, true, "震", "震", "震", "本宫"}},
    {"000100", {"雷地豫", "安乐警惕", "木", 1, 4, true, "震", "坤", "震", ""}},
    {"010100", {"雷水解", "解除困境", "木", 2, 5, true, "震", "坎", "震", ""}},
    {"011100", {"雷风恒", "恒久之道", "木", 3, 6, true, "震", "巽", "震", ""}},
    {"011000", {"地风升", "步步高升", "木", 4, 1, true, "震", "巽", "坤", ""}},
    {"011010", {"水风井", "滋养不穷", "木", 5, 2, true, "震", "巽", "坎", ""}},
    {"011110", {"泽风大过", "非常行动", "木", 4, 1, true, "震", "巽", "兑", "游魂"}},
    {"100110", {"泽雷随", "随从之道", "木", 3, 6, true, "震", "震", "兑", "归魂"}},

    // 巽宫（木）系列
    {"011011", {"巽为风", "谦逊柔顺", "木", 6, 3, false, "巽", "巽", "巽", "本宫"}},
    {"111011", {"风天小畜", "积蓄力量", "木", 1, 4, false, "巽", "乾", "巽", ""}},
    {"101011", {"风火家人", "家庭伦理", "木", 2, 5, false, "巽", "离", "巽", ""}},
    {"100011", {"风雷益", "增益之道", "木", 3, 6, false, "巽", "震", "巽", ""}},
    {"100111", {"天雷无妄", "不可妄为", "木", 4, 1, false, "巽", "乾", "震", ""}},
    {"100101", {"火雷噬嗑", "排除障碍", "木", 5, 2, false, "巽", "震", "离", ""}},
    {"100001", {"山雷颐", "颐养之道", "木", 4, 1, false, "巽", "震", "艮", "游魂"}},
    {"011001", {"山风蛊", "整治腐败", "木", 3, 6, false, "巽", "巽", "艮", "归魂"}},

    // 离宫（火）系列
    {"101101", {"离为火", "光明美丽", "火", 6, 3, false, "离", "离", "离", "本宫"}},
    {"001101", {"火山旅", "行旅之道", "火", 1, 4, false, "离", "艮", "离", ""}},
    {"011101", {"火风鼎", "稳重图新", "火", 2, 5, false, "离", "巽", "离", ""}},
    {"010101", {"火水未济", "事未完成", "火", 3, 6, false, "离", "坎", "离", ""}},
    {"010001", {"山水蒙", "启蒙教育", "火", 4, 1, false, "离", "坎", "艮", ""}},
    {"010011", {"风水涣", "涣散分离", "火", 5, 2, false, "离", "巽", "坎", ""}},
    {"010111", {"天水讼", "争讼纠纷", "火", 4, 1, false, "离", "乾", "坎", "游魂"}},
    {"101111", {"天火同人", "同心协力", "火", 3, 6, false, "离", "乾", "离", "归魂"}},

    // 坤宫（土）系列
    {"000000", {"坤为地", "厚德载物", "土", 6, 3, false, "坤", "坤", "坤", "本宫"}},
    {"100000", {"地雷复", "阳气复归", "土", 1, 4, false, "坤", "震", "坤", ""}},
    {"110000", {"地泽临", "督导视察", "土", 2, 5, false, "坤", "兑", "坤", ""}},
    {"111000", {"地天泰", "天地交泰", "土", 3, 6, false, "坤", "乾", "坤", ""}},
    {"111100", {"雷天大壮", "强盛壮大", "土", 4, 1, false, "坤", "乾", "震", ""}},
    {"111110", {"泽天夬", "果断决策", "土", 5, 2, false, "坤", "乾", "兑", ""}},
    {"111010", {"水天需", "耐心等待", "土", 4, 1, false, "坤", "乾", "坎", "游魂"}},
    {"000010", {"水地比", "亲和依附", "土", 3, 6, false, "坤", "坤", "坎", "归魂"}},

    // 兑宫（金）系列
    {"110110", {"兑为泽", "喜悦沟通", "金", 6, 3, false, "兑", "兑", "兑", "本宫"}},
    {"010110", {"泽水困", "困境求生", "金", 1, 4, false, "兑", "坎", "兑", ""}},
    {"000110", {"泽地萃", "人才荟萃", "金", 2, 5, false, "兑", "坤", "兑", ""}},
    {"001110", {"泽山咸", "感应相知", "金", 3, 6, false, "兑", "艮", "兑", ""}},
    {"001010", {"水山蹇", "艰难险阻", "金", 4, 1, false, "兑", "艮", "坎", ""}},
    {"001000", {"地山谦", "谦虚美德", "金", 5, 2, false, "兑", "艮", "坤", ""}},
    {"001100", {"雷山小过", "小有过失", "金", 4, 1, false, "兑", "艮", "震", "游魂"}},
    {"110100", {"雷泽归妹", "婚嫁之道", "金", 3, 6, false, "兑", "震", "兑", "归魂"}}};

// 地支序列（修正后）
const std::map<std::string, std::array<std::string, 6>> palaceBranchPatterns = {
    {"乾", {"子", "寅", "辰", "午", "申", "戌"}}, // 阳金（正确）
    {"坎", {"寅", "辰", "午", "申", "戌", "子"}}, // 阳水（正确）
    {"艮", {"辰", "午", "申", "戌", "子", "寅"}}, // 阳土（正确）
    {"震", {"子", "寅", "辰", "午", "申", "戌"}}, // 阳木（正确）
    {"巽", {"丑", "亥", "酉", "未", "巳", "卯"}}, // 阴木（修正：逆序）
    {"离", {"卯", "丑", "亥", "酉", "未", "巳"}}, // 阴火（修正：逆序）
    {"坤", {"未", "巳", "卯", "丑", "亥", "酉"}}, // 阴土（正确）
    {"兑", {"巳", "卯", "丑", "亥", "酉", "未"}} // 阴金（修正：逆序）
};

// 天干序列（修正后，默认冬至后）
const std::map<std::string, std::array<std::string, 6>> palaceStemPatterns = {
    {"乾", {"甲", "甲", "甲", "壬", "壬", "壬"}}, // 冬至后内甲外壬
    {"坎", {"戊", "戊", "戊", "戊", "戊", "戊"}}, // 内外均戊
    {"艮", {"丙", "丙", "丙", "丙", "丙", "丙"}}, // 内外均丙
    {"震", {"庚", "庚", "庚", "庚", "庚", "庚"}}, // 内外均庚
    {"巽", {"辛", "辛", "辛", "辛", "辛", "辛"}}, // 内外均辛
    {"离", {"己", "己", "己", "己", "己", "己"}}, // 内外均己
    {"坤", {"乙", "乙", "乙", "癸", "癸", "癸"}}, // 冬至后内乙外癸
    {"兑", {"丁", "丁", "丁", "丁", "丁", "丁"}} // 内外均丁
};

// 注：地支藏干、地支五行、五行索引已移至 ZhouYi.WuXingUtils 模块

// 日干到六神起始索引
const std::unordered_map<std::string, int> dayStemToSpiritStart = {
    {"甲", 0}, {"乙", 0}, {"丙", 1}, {"丁", 1}, {"戊", 2}, 
    {"己", 3}, {"庚", 4}, {"辛", 4}, {"壬", 5}, {"癸", 5}
};

// 注：地支六冲、六合、六害、相刑、三合已移至 ZhouYi.DiZhiRelations 模块
// 注：五行关系枚举和判断函数已移至 ZhouYi.WuXingUtils 模块

// 六神排列表 (string_view)
const std::array<std::string, 6> sixSpirits = {"青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"};

// 六亲
const std::array<std::string, 5> relativeNames = {"兄弟", "子孙", "妻财", "官鬼", "父母"};

// --- 辅助函数 ---

// 计算六亲关系 (使用 string_view)
inline std::string getRelative(const std::string &palaceElement, const std::string &yaoElement)
{
    if (palaceElement.empty() || yaoElement.empty() || !fiveElementIndex.contains(palaceElement) ||
        !fiveElementIndex.contains(yaoElement))
    {
        return "错误";
    }
    if (palaceElement == yaoElement) return relativeNames[0]; // 兄弟

    int palaceIdx = fiveElementIndex.at(palaceElement);
    int yaoIdx = fiveElementIndex.at(yaoElement);

    // palaceIdx: 我, yaoIdx: 爻
    // (yaoIdx - palaceIdx + 5) % 5: 0-同, 1-我生, 2-我克, 3-克我, 4-生我
    int diff = (yaoIdx - palaceIdx + 5) % 5;
    return relativeNames[diff];
}

// 旺衰计算函数已移至 ZhouYi.WuXingUtils 模块

/**
 * @brief 直接根据四柱和六个主卦爻支构建神煞汇总图。
 *
 * @param bazi 四柱八字信息。
 * @return std::map<std::string, std::vector<std::string>>
 * 一个 map，key 是神煞名称，value 是排序并去重后的地支列表。
 */
inline std::map<std::string, std::vector<std::string>> buildShenShaMap(const BaZi &bazi)
{
    // --- 神煞查找表 ---
    // 禄神 (日干查支)
    static const std::unordered_map<std::string, std::string> luShenMap = {
        {"甲", "寅"}, {"乙", "卯"}, {"丙", "巳"}, {"丁", "午"}, {"戊", "巳"},
        {"己", "午"}, {"庚", "申"}, {"辛", "酉"}, {"壬", "亥"}, {"癸", "子"}};
    // 羊刃 (日干查支)
    static const std::unordered_map<std::string, std::string> yangRenMap = {
        {"甲", "卯"}, {"乙", "辰"}, {"丙", "午"}, {"丁", "未"}, {"戊", "午"},
        {"己", "未"}, {"庚", "酉"}, {"辛", "戌"}, {"壬", "子"}, {"癸", "丑"}};
    // 桃花 (日/年支查支 - 优先日支)
    static const std::unordered_map<std::string, std::string> taoHuaMap = {
        {"寅", "卯"}, {"午", "卯"}, {"戌", "卯"}, // 寅午戌见卯
        {"申", "酉"}, {"子", "酉"}, {"辰", "酉"}, // 申子辰见酉
        {"亥", "子"}, {"卯", "子"}, {"未", "子"}, // 亥卯未见子
        {"巳", "午"}, {"酉", "午"}, {"丑", "午"} // 巳酉丑见午
    };
    // 驿马 (日/年支查支 - 优先日支)
    static const std::unordered_map<std::string, std::string> yiMaMap = {
        {"寅", "申"}, {"午", "申"}, {"戌", "申"}, // 寅午戌见申
        {"申", "寅"}, {"子", "寅"}, {"辰", "寅"}, // 申子辰见寅
        {"亥", "巳"}, {"卯", "巳"}, {"未", "巳"}, // 亥卯未见巳
        {"巳", "亥"}, {"酉", "亥"}, {"丑", "亥"} // 巳酉丑见亥
    };
    // 天乙贵人 (日干查支 - 简化日贵)
    static const std::unordered_map<std::string, std::vector<std::string>> guiRenMap = {
        {"甲", {"丑", "未"}}, {"戊", {"丑", "未"}}, {"庚", {"丑", "未"}}, // 甲戊庚牛羊
        {"乙", {"子", "申"}}, {"己", {"子", "申"}}, // 乙己鼠猴乡
        {"丙", {"亥", "酉"}}, {"丁", {"亥", "酉"}}, // 丙丁猪鸡位
        {"壬", {"巳", "卯"}}, {"癸", {"巳", "卯"}}, // 壬癸兔蛇藏
        {"辛", {"午", "寅"}} // 辛金马虎乡 (注意：传统上午、寅)
    };
    // 华盖 (日/年支查支 - 优先日支)
    static const std::unordered_map<std::string, std::string> huaGaiMap = {
        {"寅", "戌"}, {"午", "戌"}, {"戌", "戌"}, // 寅午戌见戌
        {"亥", "未"}, {"卯", "未"}, {"未", "未"}, // 亥卯未见未
        {"申", "辰"}, {"子", "辰"}, {"辰", "辰"}, // 申子辰见辰
        {"巳", "丑"}, {"酉", "丑"}, {"丑", "丑"} // 巳酉丑见丑
    };
    // 将星 (日/年支查支 - 优先日支)
    static const std::unordered_map<std::string, std::string> jiangXingMap = {
        {"寅", "午"}, {"午", "午"}, {"戌", "午"}, // 寅午戌见午
        {"亥", "卯"}, {"卯", "卯"}, {"未", "卯"}, // 亥卯未见卯
        {"申", "子"}, {"子", "子"}, {"辰", "子"}, // 申子辰见子
        {"巳", "酉"}, {"酉", "酉"}, {"丑", "酉"} // 巳酉丑见酉
    };
    // 劫煞 (日/年支查支 - 优先日支)
    static const std::unordered_map<std::string, std::string> jieShaMap = {
        {"寅", "亥"}, {"午", "亥"}, {"戌", "亥"}, // 寅午戌见亥
        {"申", "巳"}, {"子", "巳"}, {"辰", "巳"}, // 申子辰见巳
        {"亥", "申"}, {"卯", "申"}, {"未", "申"}, // 亥卯未见申
        {"巳", "寅"}, {"酉", "寅"}, {"丑", "寅"} // 巳酉丑见寅
    };
    // 灾煞 (日/年支查支 - 优先日支)
    static const std::unordered_map<std::string, std::string> zaiShaMap = {
        {"寅", "子"}, {"午", "子"}, {"戌", "子"}, // 寅午戌见子
        {"申", "午"}, {"子", "午"}, {"辰", "午"}, // 申子辰见午
        {"亥", "酉"}, {"卯", "酉"}, {"未", "酉"}, // 亥卯未见酉
        {"巳", "卯"}, {"酉", "卯"}, {"丑", "卯"} // 巳酉丑见卯
    };

    // 常用神煞名称列表 (用于汇总)
    static const std::array<std::string, 9> commonShenShaNames = {
        "驿马", "桃花", "日禄", "贵人", "文昌",
        "羊刃", "将星", "劫煞", "灾煞" // 还有 谋星, 华盖, 禄勋, 天医
                                       // 等，按需添加
    };

    // 文昌 (日干查支)
    static const std::unordered_map<std::string, std::string> wenChangMap = {
        {"甲", "巳"}, {"乙", "午"}, {"丙", "申"}, {"丁", "酉"}, {"戊", "申"},
        {"己", "酉"}, {"庚", "亥"}, {"辛", "子"}, {"壬", "寅"}, {"癸", "卯"}};

    // 天马 (月支查)
    static const std::unordered_map<std::string, std::string> tianMaMap = {
        {"寅", "午"}, {"申", "午"}, {"卯", "申"}, {"酉", "申"}, {"辰", "戌"}, {"戌", "戌"},
        {"巳", "子"}, {"亥", "子"}, {"午", "寅"}, {"子", "寅"}, {"未", "辰"}, {"丑", "辰"}};

    // 谋星 (日支查 - 按三合局)
    // 寅午戌(火局)辰, 申子辰(水局)酉, 巳酉丑(金局)未, 亥卯未(木局)丑
    static const std::unordered_map<std::string, std::string> mouXingMap = {
        {"寅", "辰"}, {"午", "辰"}, {"戌", "辰"},  // 火局  辰
        {"申", "酉"}, {"子", "酉"}, {"辰", "酉"},  // 水局  酉
        {"巳", "未"}, {"酉", "未"}, {"丑", "未"},  // 金局  未
        {"亥", "丑"}, {"卯", "丑"}, {"未", "丑"}   // 木局  丑
    };

    // 日德 (日干查 - 所有天干)
    // 甲寅、乙卯、丙巳、丁午、戊巳、己午、庚申、辛酉、壬亥、癸子
    static const std::unordered_map<std::string, std::string> riDeMap = {
        {"甲", "寅"}, {"乙", "卯"}, {"丙", "巳"}, {"丁", "午"}, {"戊", "巳"},
        {"己", "午"}, {"庚", "申"}, {"辛", "酉"}, {"壬", "亥"}, {"癸", "子"}
    };

    std::map<std::string, std::vector<std::string>> shenShaDefinitionMap;

    // **注意：** 根据您的要求，移除了对 bazi 输入有效性的检查。
    // **依赖调用者保证 bazi 数据的完整性和有效性。**

    const std::string dayStem = bazi.day.stem();       // 调用 stem() 方法
    const std::string dayBranch = bazi.day.branch();   // 调用 branch() 方法
    const std::string monthBranch = bazi.month.branch();  // 调用 branch() 方法
    const std::string yearBranch = bazi.year.branch();    // 调用 branch() 方法

    // --- 计算并填充 Map (直接使用 .at() 或 [], 依赖 key 存在) ---

    // 1. 基于年月日支本身 (假设非空)
    shenShaDefinitionMap["太岁"].push_back(yearBranch);
    shenShaDefinitionMap["月建"].push_back(monthBranch);
    shenShaDefinitionMap["日辰"].push_back(dayBranch);

    // 2. 基于冲合关系 - 使用 GanZhi 模块的函数计算
    // 计算月破（月支的冲支）
    auto monthZhiOpt = Mapper::from_zh_zhi(monthBranch);
    if (monthZhiOpt.has_value()) {
        DiZhi monthZhi = monthZhiOpt.value();
        DiZhi monthChong = static_cast<DiZhi>((static_cast<int>(monthZhi) + 6) % 12);
        shenShaDefinitionMap["月破"].push_back(std::string(Mapper::to_zh(monthChong)));
        
        // 计算月合（遍历查找与月支相合的地支）
        for (int i = 0; i < 12; ++i) {
            DiZhi testZhi = static_cast<DiZhi>(i);
            if (is_he(monthZhi, testZhi)) {
                shenShaDefinitionMap["月合"].push_back(std::string(Mapper::to_zh(testZhi)));
                break;
            }
        }
    }
    
    // 计算日破（日支的冲支）
    auto dayZhiOpt = Mapper::from_zh_zhi(dayBranch);
    if (dayZhiOpt.has_value()) {
        DiZhi dayZhi = dayZhiOpt.value();
        DiZhi dayChong = static_cast<DiZhi>((static_cast<int>(dayZhi) + 6) % 12);
        shenShaDefinitionMap["日破"].push_back(std::string(Mapper::to_zh(dayChong)));
        
        // 计算日合（遍历查找与日支相合的地支）
        for (int i = 0; i < 12; ++i) {
            DiZhi testZhi = static_cast<DiZhi>(i);
            if (is_he(dayZhi, testZhi)) {
                shenShaDefinitionMap["日合"].push_back(std::string(Mapper::to_zh(testZhi)));
                break;
            }
        }
    }
    // 日德（所有天干都有日德：甲寅、乙卯、丙巳、丁午、戊巳、己午、庚申、辛酉、壬亥、癸子）
    shenShaDefinitionMap["日德"].push_back(riDeMap.at(dayStem));

    // 3. 基于干支关系的神煞 (假设 key 存在)
    shenShaDefinitionMap["日禄"].push_back(luShenMap.at(dayStem));
    shenShaDefinitionMap["羊刃"].push_back(yangRenMap.at(dayStem));
    shenShaDefinitionMap["桃花"].push_back(taoHuaMap.at(dayBranch)); // 沿用日支优先
    shenShaDefinitionMap["驿马"].push_back(yiMaMap.at(dayBranch)); // 沿用日支优先
    shenShaDefinitionMap["天马"].push_back(tianMaMap.at(monthBranch)); // 天马 (基于月支)

    shenShaDefinitionMap["谋星"].push_back(mouXingMap.at(dayBranch));  // 按日支查（三合局）
    shenShaDefinitionMap["文昌"].push_back(wenChangMap.at(dayStem));
    shenShaDefinitionMap["华盖"].push_back(huaGaiMap.at(dayBranch)); // 沿用日支优先
    shenShaDefinitionMap["将星"].push_back(jiangXingMap.at(dayBranch)); // 沿用日支优先
    shenShaDefinitionMap["劫煞"].push_back(jieShaMap.at(dayBranch)); // 沿用日支优先
    shenShaDefinitionMap["灾煞"].push_back(zaiShaMap.at(dayBranch)); // 沿用日支优先

    // 天乙贵人 (假设 key 存在)
    const auto &nobles = guiRenMap.at(dayStem);
    shenShaDefinitionMap["贵人"].insert(shenShaDefinitionMap["贵人"].end(), nobles.begin(), nobles.end());

    // 排序贵人地支
    std::ranges::sort(shenShaDefinitionMap["贵人"]);

    // --- （可选）添加其他神煞计算逻辑 ---
    return shenShaDefinitionMap;
}

// 格式化爻象线条 (用于表格输出)
inline std::string formatYaoLine(char mainYaoType, std::string changeMark)
{
    std::string line = (mainYaoType == '1') ? "" : " ";
    std::string marker = std::string(changeMark); // Convert string_view to string if needed
    if (marker == " ")
    {
        return fmt::format("{:^7}", line); // 7 characters width seems appropriate
    }
    else
    {
        return fmt::format("{} {}", line, marker); // Add marker if changing
    }
}

// 初始化包含6个YaoDetails的向量，并设置position
inline std::vector<YaoDetails> initializeYaoDetailsVector(const HexagramInfo &mainInfo,
                                                          const std::vector<int> &changingLineIndices)
{
    std::vector<YaoDetails> yaoDetailsList(6);
    for (int i = 0; i < 6; ++i)
    {
        yaoDetailsList[i].position = i + 1;
        for (int idx : changingLineIndices)
        {
            if (idx == i + 1)
            {
                yaoDetailsList[i].isChanging = true;  // 修复：应该是 [i] 而不是 [i+1]
                break;
            }
        }
        if (i + 1 == mainInfo.shiYaoPosition)
        {
            yaoDetailsList[i].shiYingMark = "世";
        }
        else if (i + 1 == mainInfo.yingYaoPosition)
        {
            yaoDetailsList[i].shiYingMark = "应";
        }
        else
        {
            yaoDetailsList[i].shiYingMark = " ";
        }
    }
    return yaoDetailsList;
}

// 生成六个爻的天干地支
/**
 *
 * @param yaoDetailsList 六个爻位
 * @param hexagram 64卦的信息
 * @param typeYao 0 飞神 1 变卦 2伏神
 */
inline void generateTianGanAndDiZhi(std::vector<YaoDetails> &yaoDetailsList, const HexagramInfo &hexagram, int typeYao)
{
    const auto &innerStems = palaceStemPatterns.at(hexagram.innerHexagram);
    const auto &innerBranches = palaceBranchPatterns.at(hexagram.innerHexagram);
    const auto &outerStems = palaceStemPatterns.at(hexagram.outerHexagram);
    const auto &outerBranches = palaceBranchPatterns.at(hexagram.outerHexagram);

    // 内卦（0-2）  外卦（3-5）
    for (int i = 0, w = 3; i < 6; ++i)
    {
        YaoDetails &detailsList = yaoDetailsList.at(i);
        Pillar *pillar = nullptr;
        switch (typeYao)
        {
        case 0:
            pillar = &detailsList.mainPillar;
            break;
        case 1:
            pillar = &detailsList.changedPillar;
            break;
        case 2:
            pillar = &detailsList.hiddenPillar;
            break;
        default:
            std::println("{}", "generateTianGanAndDiZhi <UNK>");
        }

        // 使用字符串构造函数创建 Pillar（会自动转换为枚举）
        if (i < 3)
        {
            *pillar = Pillar(innerStems[i], innerBranches[i]);
        }
        else
        {
            *pillar = Pillar(outerStems[w], outerBranches[w]);
            ++w;
        }
    }
}

// --- 辅助函数：计算伏神信息 ---
// 使用 generateTianGanAndDiZhi 来获取本宫卦干支
inline void calculateHiddenGods(const HexagramInfo &pBasePalaceInfo, // 指向本宫卦信息
                                const std::string &mainPalaceElement, // 本卦已有六亲
                                std::vector<YaoDetails> &yaoList // (输入/输出) 要填充的爻列表
)
{
    generateTianGanAndDiZhi(yaoList, pBasePalaceInfo, 2);

    for (int i = 0; i < 6; ++i)
    {
        const std::string hiddenBranch = yaoList[i].hiddenPillar.branch();  // 调用 branch() 方法
        if (branchFiveElements.contains(hiddenBranch))
        {
            yaoList[i].hiddenElement = branchFiveElements.at(hiddenBranch); // 存储变爻五行
            // *** 关键：变爻六亲相对于【本卦】宫位五行 ***
            yaoList[i].hiddenRelative = getRelative(mainPalaceElement, yaoList[i].hiddenElement);
        }
        else
        {
            yaoList[i].changedElement = "未知";
            yaoList[i].changedRelative = "错误";
            std::print(std::cerr, "警告: 无法找到变爻地支 '{}' 的五行属性。\n", hiddenBranch);
        }
    }
}

/**
 * @brief 填充爻的五行和六亲信息
 */
inline void fillElementAndRelative(std::vector<YaoDetails> &yaoList, 
                                   const std::string &palaceElement,
                                   bool isMainHexagram) {
    for (int i = 0; i < 6; ++i) {
        const std::string &branch = isMainHexagram ? 
            yaoList[i].mainPillar.branch() : 
            yaoList[i].changedPillar.branch();
        
        if (branchFiveElements.contains(branch)) {
            const std::string &element = branchFiveElements.at(branch);
            const std::string &relative = getRelative(palaceElement, element);
            
            if (isMainHexagram) {
                yaoList[i].mainElement = element;
                yaoList[i].mainRelative = relative;
            } else {
                yaoList[i].changedElement = element;
                yaoList[i].changedRelative = relative;
            }
        } else {
            if (isMainHexagram) {
                yaoList[i].mainElement = "未知";
                yaoList[i].mainRelative = "错误";
            } else {
                yaoList[i].changedElement = "未知";
                yaoList[i].changedRelative = "错误";
            }
            std::print(std::cerr, "警告: 无法找到地支 '{}' 的五行属性。\n", branch);
        }
    }
}

// --- 主排盘函数 ---
inline std::pair<std::vector<YaoDetails>, nlohmann::json> sixYaoDivination(const std::string &mainHexagramCode,
                                                                           const BaZi &bazi,
                                                                           const std::vector<int> &changingLineIndices)
{
    nlohmann::json json;
    json["ba_zi"] = bazi;

    // ===== 第1步：初始化本卦信息 =====
    const HexagramInfo &mianInfo = hexagramMap.at(mainHexagramCode);
    std::vector<YaoDetails> LIU_YAO = initializeYaoDetailsVector(mianInfo, changingLineIndices);
    
    // 生成本卦天干地支（纳甲）
    generateTianGanAndDiZhi(LIU_YAO, mianInfo, 0);
    json["ben_gua_name"] = mianInfo.palaceType + "宫: " + mianInfo.name;

    // ===== 第2步：填充爻的阴阳类型 =====
    for (int i = 0; i < 6; ++i) {
        LIU_YAO[i].mainYaoType = mainHexagramCode[i]; // '0' 或 '1'
    }

    // ===== 第3步：标记动爻 =====
    for (int changeIdx : changingLineIndices) {
        if (changeIdx >= 1 && changeIdx <= 6) {
            int yaoIndex = changeIdx - 1; // 转换为 0-based index (修复bug)
            LIU_YAO[yaoIndex].isChanging = true;  // 修复：去掉 +1
            LIU_YAO[yaoIndex].changeMark = (LIU_YAO[yaoIndex].mainYaoType == '1') ? "O" : "X"; // 阳动O, 阴动X
        }
    }

    // ===== 第4步：计算本卦五行和六亲 =====
    const std::string &mainPalaceElement = mianInfo.fiveElement;
    fillElementAndRelative(LIU_YAO, mainPalaceElement, true);

#ifdef debug
    std::println("{}", "【本卦信息】");
    for (const auto &yaoDetails : LIU_YAO) {
        std::println("{}", yaoDetails);
    }
#endif

    // ===== 第5步：处理变卦（如果有动爻）=====
    if (!changingLineIndices.empty()) {
        // 生成变卦代码
        std::string changedHexagramCode = mainHexagramCode;
        for (int idx : changingLineIndices) {
            if (idx >= 1 && idx <= 6) {  // 修复：idx 是 1-6
                int arrayIndex = idx - 1;  // 转换为 0-5
                changedHexagramCode[arrayIndex] = (changedHexagramCode[arrayIndex] == '0' ? '1' : '0');
            } else {
                std::print(std::cerr, "警告: 动爻位置超出范围: {}\n", idx);
            }
        }

        // 获取变卦信息并生成纳甲
        const HexagramInfo &changedInfo = hexagramMap.at(changedHexagramCode);
        generateTianGanAndDiZhi(LIU_YAO, changedInfo, 1);
        json["bian_gua_name"] = changedInfo.palaceType + "宫: " + changedInfo.name;

        // 计算变卦五行和六亲（注意：变爻六亲相对于本卦宫位五行）
        fillElementAndRelative(LIU_YAO, mainPalaceElement, false);
    }

#ifdef debug
    std::println("{}", "\n【变卦信息】");
    for (const auto &yaoDetails : LIU_YAO) {
        std::println("{}", yaoDetails);
    }
#endif

    // ===== 第6步：计算伏神 =====
    // 获取本宫卦代码
    static const std::unordered_map<std::string, std::string> palaceCodeMap = {
        {"乾", "111111"}, {"坎", "010010"}, {"艮", "001001"}, {"震", "100100"},
        {"巽", "011011"}, {"离", "101101"}, {"坤", "000000"}, {"兑", "110110"}
    };
    
    const std::string &palaceType = mianInfo.palaceType;
    if (palaceCodeMap.contains(palaceType)) {
        const std::string &basePalaceCode = palaceCodeMap.at(palaceType);
        const auto &basePalaceInfo = hexagramMap.at(basePalaceCode);
        calculateHiddenGods(basePalaceInfo, mainPalaceElement, LIU_YAO);
    } else {
        std::print(std::cerr, "警告：未知的宫位类型: {}\n", palaceType);
    }

    // ===== 第7步：计算六神 =====
    const std::string dayStem = bazi.day.stem();
    if (!dayStem.empty() && dayStemToSpiritStart.contains(dayStem)) {
        int startIdx = dayStemToSpiritStart.at(dayStem);
        for (int i = 0; i < 6; ++i) {
            int spiritIdx = (startIdx + i) % 6;
            LIU_YAO[i].spirit = sixSpirits[spiritIdx];
        }
    } else {
        std::print(std::cerr, "警告：无法计算六神（日干: {}）\n", dayStem);
        for (int i = 0; i < 6; ++i) {
            LIU_YAO[i].spirit = dayStem.empty() ? "空" : "未知";
        }
    }

    // ===== 第8步：计算旺衰 =====
    const std::string &monthBranch = bazi.month.branch();
    for (int i = 0; i < 6; ++i) {
        LIU_YAO[i].wangShuai = getWangShuai(LIU_YAO[i].mainElement, monthBranch);
    }

    // ===== 第9步：计算神煞 =====
    std::map<std::string, std::vector<std::string>> shenShaMap = buildShenShaMap(bazi);
    json["shen_sa"] = shenShaMap;

#ifdef debug
    // 打印八字信息
    std::println("\n【八字信息】\n干支: {}年 {}月 {}日 {}时", 
                 bazi.year.to_string(),
                 bazi.month.to_string(), 
                 bazi.day.to_string(),
                 bazi.hour.to_string());
    
    // 打印神煞
    std::println("{}", "\n【神煞】");
    for (const auto &[name, branches] : shenShaMap) {
        std::string branchList;
        bool first = true;
        for (const auto& branch : branches) {
            if (!first) branchList += " ";
            branchList += branch;
            first = false;
        }
        std::println("{}: {}", name, branchList);
    }
#endif

    // ===== 第10步：输出排盘结果（调试模式）=====
#ifdef debug
    // 打印卦名
    std::println("\n【卦象】\n{}: {}{}\n", 
                 mianInfo.palaceType + "宫",
                 mianInfo.name,
                 mianInfo.structureType.empty() ? "" : fmt::format(" ({})", mianInfo.structureType));
    
    // 打印爻象表格
    auto get_yao_line_shape = [](char yaoType) -> std::string { 
        return (yaoType == '1') ? "" : " "; 
    };

    const int spirit_width = 4;
    const int fushen_width = 12;
    const int bengua_width = 22;
    const int biangua_width = 18;

    std::println("| {:<{}} | {:<{}} | {:<{}} | {:<{}} |", 
                 "六神", spirit_width, "伏神", fushen_width,
                 "本卦 (飞神)", bengua_width, "变卦", biangua_width);
    std::println("|{:-<{}}+{:-<{}}+{:-<{}}+{:-<{}}|", 
                 "", spirit_width + 1, "", fushen_width + 1, 
                 "", bengua_width + 1, "", biangua_width + 1);

    for (int i = 5; i >= 0; --i) {
        const auto &yao = LIU_YAO[i];

        // 六神列
        std::string spiritCol = yao.spirit;

        // 伏神列
        std::string fuShenCol = fmt::format("{}{}{}{}", 
                                           yao.hiddenRelative, 
                                           yao.hiddenPillar.stem(),
                                           yao.hiddenPillar.branch(), 
                                           yao.hiddenElement);

        // 本卦列
        std::string benGuaText = fmt::format("{}{}{}{}", 
                                            yao.mainRelative, 
                                            yao.mainPillar.stem(), 
                                            yao.mainPillar.branch(), 
                                            yao.mainElement);
        std::string changeMarker = (yao.changeMark == " ") ? " " : (" " + yao.changeMark);
        std::string shiYingMarker = (yao.shiYingMark == " ") ? "" : (" " + yao.shiYingMark);
        std::string benGuaCol = fmt::format("{}{}{}{}", 
                                           benGuaText, 
                                           " " + get_yao_line_shape(yao.mainYaoType), 
                                           changeMarker, 
                                           shiYingMarker);

        // 变卦列
        std::string changedText = fmt::format("{}{}{}{}", 
                                             yao.changedRelative, 
                                             yao.changedPillar.stem(), 
                                             yao.changedPillar.branch(),
                                             yao.changedElement);
        char finalYaoType = (yao.mainYaoType == '0' ? '1' : '0');
        std::string bianGuaCol = fmt::format("{} {}", changedText, get_yao_line_shape(finalYaoType));

        // 打印当前行
        std::println("| {:<{}} | {:<{}} | {:<{}} | {:<{}} |", 
                     spiritCol, spirit_width, 
                     fuShenCol, fushen_width, 
                     benGuaCol, bengua_width, 
                     bianGuaCol, biangua_width);
    }
    std::println("{}", "");
#endif

    // ===== 返回结果 =====
    json["yao"] = LIU_YAO;
    return {LIU_YAO, json};
}

/**
 * @brief 生成 AI 可读的 JSON 数据（中文 key）
 * 
 * @param yao_list 六爻详细信息列表
 * @param original_json 原始 JSON 数据（英文 key）
 * @return nlohmann::json AI 可读的 JSON（中文 key，爻编号格式为 "1爻"、"2爻" 等，确保所有字段都翻译）
 */
inline nlohmann::json aiSetSixYaoDivination(
    const std::vector<YaoDetails>& yao_list,
    const nlohmann::json& original_json
) {
    nlohmann::json ai_json;
    
    // 转换八字信息（完整翻译所有字段）
    if (original_json.contains("ba_zi")) {
        nlohmann::json ba_zi_cn;
        auto const& ba_zi = original_json["ba_zi"];
        ba_zi_cn["年柱"] = ba_zi["year"];
        ba_zi_cn["月柱"] = ba_zi["month"];
        ba_zi_cn["日柱"] = ba_zi["day"];
        ba_zi_cn["时柱"] = ba_zi["hour"];
        
        // 添加空亡信息
        if (ba_zi.contains("xun_kong_1")) {
            ba_zi_cn["旬空1"] = ba_zi["xun_kong_1"];
        }
        if (ba_zi.contains("xun_kong_2")) {
            ba_zi_cn["旬空2"] = ba_zi["xun_kong_2"];
        }
        
        ai_json["八字"] = ba_zi_cn;
    }
    
    // 转换本卦名称
    if (original_json.contains("ben_gua_name")) {
        ai_json["本卦名称"] = original_json["ben_gua_name"];
    }
    
    // 转换变卦名称
    if (original_json.contains("bian_gua_name")) {
        ai_json["变卦名称"] = original_json["bian_gua_name"];
    }
    
    // 转换神煞信息（神煞名称已经是中文，直接保留）
    if (original_json.contains("shen_sa")) {
        ai_json["神煞"] = original_json["shen_sa"];
    }
    
    // 转换六爻信息（完整翻译所有字段，使用 "1爻"、"2爻" 等格式）
    nlohmann::json liu_yao_cn;
    for (std::size_t i = 0z; i < yao_list.size(); ++i) {
        auto const& yao = yao_list[i];
        nlohmann::json yao_cn;
        
        // 基本信息
        yao_cn["爻位"] = yao.position;
        yao_cn["世应标记"] = yao.shiYingMark;
        yao_cn["六神"] = yao.spirit;
        yao_cn["旺衰"] = yao.wangShuai;
        
        // 本卦信息（完整翻译）
        nlohmann::json ben_gua_cn;
        ben_gua_cn["干支"] = yao.mainPillar.to_string();
        ben_gua_cn["天干"] = std::string{yao.mainPillar.stem()};
        ben_gua_cn["地支"] = std::string{yao.mainPillar.branch()};
        ben_gua_cn["五行"] = yao.mainElement;
        ben_gua_cn["六亲"] = yao.mainRelative;
        ben_gua_cn["爻性"] = (yao.mainYaoType == '1' || yao.mainYaoType == 49 ? "阳爻" : "阴爻");
        yao_cn["本卦"] = ben_gua_cn;
        
        // 伏神信息（完整翻译，如果存在）
        if (not yao.hiddenPillar.to_string().empty()) {
            nlohmann::json fu_shen_cn;
            fu_shen_cn["干支"] = yao.hiddenPillar.to_string();
            fu_shen_cn["天干"] = std::string{yao.hiddenPillar.stem()};
            fu_shen_cn["地支"] = std::string{yao.hiddenPillar.branch()};
            fu_shen_cn["五行"] = yao.hiddenElement;
            fu_shen_cn["六亲"] = yao.hiddenRelative;
            yao_cn["伏神"] = fu_shen_cn;
        }
        
        // 动爻信息（完整翻译）
        yao_cn["是否动爻"] = yao.isChanging;
        //yao_cn["动爻标记"] = yao.changeMark;
        
        // 变卦信息（完整翻译，始终包含）
        nlohmann::json bian_gua_cn;
        bian_gua_cn["干支"] = yao.changedPillar.to_string();
        bian_gua_cn["天干"] = std::string{yao.changedPillar.stem()};
        bian_gua_cn["地支"] = std::string{yao.changedPillar.branch()};
        bian_gua_cn["五行"] = yao.changedElement;
        bian_gua_cn["六亲"] = yao.changedRelative;
        bian_gua_cn["爻性"] = (yao.mainYaoType == '0' || yao.mainYaoType == 48 ? "阳爻" : "阴爻");  // 变卦爻性相反
        yao_cn["变卦"] = bian_gua_cn;
        
        // 使用 "1爻"、"2爻" 等格式作为 key
        auto yao_key = fmt::format("{}爻", yao.position);
        liu_yao_cn[yao_key] = yao_cn;
    }
    
    ai_json["六爻"] = liu_yao_cn;
    
    return ai_json;
}

/**
 * @brief 获取卦象映射表（供外部模块使用）
 */
inline const std::unordered_map<std::string, HexagramInfo>& get_hexagram_map() {
    return hexagramMap;
}

} // namespace ZhouYi::LiuYao