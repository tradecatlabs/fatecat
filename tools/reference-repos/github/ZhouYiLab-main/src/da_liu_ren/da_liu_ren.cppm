// C++23 Module - 大六壬排盘系统
export module ZhouYi.DaLiuRen;

// 导入第三方库模块
import fmt;
import nlohmann.json;

// 导入自定义通用模块
import ZhouYi.BaZiBase;      // 八字基础数据结构（Pillar, BaZi）
import ZhouYi.GanZhi;        // 干支系统（包含地支关系）
import ZhouYi.WuXingUtils;   // 五行工具
import ZhouYi.tyme;          // 时间模块
import ZhouYi.DaLiuRen.ShenSha;  // 神煞系统

// 导入标准库模块（最后）
import std;

/**
 * @brief 大六壬命名空间
 * 
 * 大六壬是中国古代占卜术之一，与奇门遁甲、太乙神数并称三式。
 * 主要用于预测事物的发展趋势和吉凶。
 */
export namespace ZhouYi::DaLiuRen {

// 使用通用命名空间
using namespace ZhouYi::BaZiBase;
using namespace ZhouYi::GanZhi;
using namespace ZhouYi::WuXingUtils;
namespace Mapper = ZhouYi::GanZhi::Mapper;

// ==================== 月将对照表 ====================

/**
 * @brief 月将枚举
 * 
 * 大六壬中的十二月将，对应十二地支
 */
enum class YueJiang {
    DengMing = 0,   // 登明（亥）- 正月
    HeKui = 1,      // 河魁（戌）- 二月
    ChuanSong = 2,  // 传送（酉）- 三月
    XiaoJi = 3,     // 小吉（申）- 四月
    ShengGuang = 4, // 胜光（未）- 五月
    TaiYi = 5,      // 太乙（午）- 六月
    TianGang = 6,   // 天罡（巳）- 七月
    TaiChong = 7,   // 太冲（辰）- 八月
    GongCao = 8,    // 功曹（卯）- 九月
    DaJi = 9,       // 大吉（寅）- 十月
    ShenHou = 10,   // 神后（丑）- 十一月
    YinYang = 11    // 阴阳（子）- 十二月
};

/**
 * @brief 根据太阳黄经（气中换将）确定月将
 *
 * 算法说明：
 * 本函数严格按照传统历法歌诀实现月将的精确计算。
 * 月将的切换不是简单的按月份，而是根据太阳在黄道上的实际位置，
 * 在特定节气的特定时刻进行切换。
 *
 * 历法歌诀（写于此处，便于校对公式）：
 * 雨水前日卯初刻，太阳入卫用登明；(亥)  - 雨水前1日，卯时初刻（5:00）-> 登明(亥)
 * 春分后二巳一刻，入鲁河魁作将明；(戌)  - 春分后2日，巳时一刻（9:15）-> 河魁(戌)
 * 谷雨后四亥初刻，入赵从魁用可称；(酉)  - 谷雨后4日，亥时初刻（21:00）-> 从魁(酉)
 * 小满后五酉三刻，入晋还须传送兵；(申)  - 小满后5日，酉时三刻（17:45）-> 传送(申)
 * 夏至后四未一刻，入秦小吉用其名；(未)  - 夏至后4日，未时一刻（13:15）-> 小吉(未)
 * 大暑后三巳一刻，入周先用胜光灵；(午)  - 大暑后3日，巳时一刻（9:15）-> 胜光(午)
 * 处暑后三巳二刻，入楚还当太乙迎；(巳)  - 处暑后3日，巳时二刻（9:30）-> 太乙(巳)
 * 秋分后七寅三刻，入郑天罡用去亨；(辰)  - 秋分后7日，寅时三刻（3:45）-> 天罡(辰)
 * 霜降后九丑三刻，太冲运动宋州城；(卯)  - 霜降后9日，丑时三刻（1:45）-> 太冲(卯)
 * 小雪后七戌一刻，功曹将领入燕京；(寅)  - 小雪后7日，戌时一刻（19:15）-> 功曹(寅)
 * 冬至后四亥一刻，入吴大吉便休停；(丑)  - 冬至后4日，亥时一刻（21:15）-> 大吉(丑)
 * 大寒当日酉三刻，入齐神后岁功成。(子)  - 大寒当日，酉时三刻（17:45）-> 神后(子)
 *
 * 算法流程：
 * 1. 定义12个月将切换规则（对应12个节气切换点）
 * 2. 计算前后三年的所有切换时刻（确保覆盖当前时间）
 * 3. 按时间排序所有切换点
 * 4. 去重（避免重复的切换点）
 * 5. 找到最后一个不超过当前时间的切换点，其对应的月将即为当前月将
 *
 * @param solar_time 公历时刻
 * @return DiZhi 月将地支
 */
inline DiZhi get_yue_jiang(const tyme::SolarTime& solar_time) {
    /**
     * @brief 月将切换规则结构体
     * 
     * 每个规则定义一个月将的切换时刻：
     * - term_name: 基准节气名称
     * - day_offset: 相对于节气的日期偏移（负数表示前，正数表示后，0表示当日）
     * - trigger_branch: 触发时辰的地支（如"卯初刻"中的"卯"）
     * - trigger_minutes: 触发时刻的分钟数（如"一刻"=15分钟，"三刻"=45分钟）
     * - result: 切换后的月将地支
     */
    struct YueJiangRule {
        const char* term_name;      // 基准节气名称
        int day_offset;              // 日期偏移（相对于节气日）
        DiZhi trigger_branch;        // 触发时辰的地支
        int trigger_minutes;         // 触发时刻的分钟数（0/15/30/45）
        DiZhi result;                // 切换后的月将地支
    };

    /**
     * 12个月将切换规则表
     */
    constexpr std::array<YueJiangRule, 12> rules = {{
        {"雨水", -1, DiZhi::Mao, 0, DiZhi::Hai},      // 雨水前1日，卯初刻（5:00）-> 登明(亥)
        {"春分", 2, DiZhi::Si, 15, DiZhi::Xu},        // 春分后2日，巳一刻（9:15）-> 河魁(戌)
        {"谷雨", 4, DiZhi::Hai, 0, DiZhi::You},       // 谷雨后4日，亥初刻（21:00）-> 从魁(酉)
        {"小满", 5, DiZhi::You, 45, DiZhi::Shen},     // 小满后5日，酉三刻（17:45）-> 传送(申)
        {"夏至", 4, DiZhi::Wei, 15, DiZhi::Wei},      // 夏至后4日，未一刻（13:15）-> 小吉(未)
        {"大暑", 3, DiZhi::Si, 15, DiZhi::Wu},        // 大暑后3日，巳一刻（9:15）-> 胜光(午)
        {"处暑", 3, DiZhi::Si, 30, DiZhi::Si},        // 处暑后3日，巳二刻（9:30）-> 太乙(巳)
        {"秋分", 7, DiZhi::Yin, 45, DiZhi::Chen},     // 秋分后7日，寅三刻（3:45）-> 天罡(辰)
        {"霜降", 9, DiZhi::Chou, 45, DiZhi::Mao},     // 霜降后9日，丑三刻（1:45）-> 太冲(卯)
        {"小雪", 7, DiZhi::Xu, 15, DiZhi::Yin},       // 小雪后7日，戌一刻（19:15）-> 功曹(寅)
        {"冬至", 4, DiZhi::Hai, 15, DiZhi::Chou},     // 冬至后4日，亥一刻（21:15）-> 大吉(丑)
        {"大寒", 0, DiZhi::You, 45, DiZhi::Zi}        // 大寒当日，酉三刻（17:45）-> 神后(子)
    }};

    /**
     * @brief 地支转时辰（24小时制）
     * 
     */
    const auto to_branch_hour = [](DiZhi branch) -> int {
        switch (branch) {
            case DiZhi::Zi: return 23;    // 子时起始：23:00
            case DiZhi::Chou: return 1;   // 丑时起始：01:00
            case DiZhi::Yin: return 3;    // 寅时起始：03:00
            case DiZhi::Mao: return 5;    // 卯时起始：05:00
            case DiZhi::Chen: return 7;   // 辰时起始：07:00
            case DiZhi::Si: return 9;     // 巳时起始：09:00
            case DiZhi::Wu: return 11;    // 午时起始：11:00
            case DiZhi::Wei: return 13;   // 未时起始：13:00
            case DiZhi::Shen: return 15;  // 申时起始：15:00
            case DiZhi::You: return 17;   // 酉时起始：17:00
            case DiZhi::Xu: return 19;    // 戌时起始：19:00
            case DiZhi::Hai: return 21;   // 亥时起始：21:00
        }
        return 23;  // 默认返回子时
    };

    /**
     * 步骤1：使用 Ranges 计算前后三年的所有月将切换时刻
     * 
     * 为什么要计算三年？
     * - 当前时间可能在年初或年末，需要确保覆盖到所有可能的切换点
     * - 例如：如果当前是1月，需要包含上一年的"大寒"切换点
     * - 如果当前是12月，需要包含下一年的"雨水"切换点
     * 
     * 使用 Ranges 管道：
     * 1. 生成年份偏移范围 [-1, 0, 1]
     * 2. 与规则表进行笛卡尔积（cartesian product）
     * 3. 使用 transform 将每个组合转换为切换时刻
     * 4. 收集到 vector 中
     */
    const int base_year = solar_time.get_year();
    constexpr std::array<int, 3> year_offsets = {-1, 0, 1};
    
    auto transitions = year_offsets
        | std::views::transform([&](int year_offset) {
            return std::views::all(rules) 
                | std::views::transform([&, year_offset](const YueJiangRule& rule) {
                    // 获取基准节气（使用tyme库精确计算节气时刻）
                    const int term_year = base_year + year_offset;
                    const auto term = tyme::SolarTerm::from_name(term_year, std::string(rule.term_name));
                    
                    // 获取节气所在日期
                    const auto term_day = term.get_julian_day().get_solar_time().get_solar_day();
                    
                    // 计算切换日期：节气日 + 日期偏移
                    // 例如："雨水前1日" = 雨水日 + (-1) = 雨水前1日
                    const auto trigger_day = term_day.next(rule.day_offset);
                    
                    // 将地支转换为24小时制的小时数
                    // 例如："卯初刻"中的"卯" -> 5点
                    const int trigger_hour = to_branch_hour(rule.trigger_branch);
                    
                    // 构造精确的切换时刻
                    // 例如："卯初刻" = 5点0分，"巳一刻" = 9点15分
                    auto trigger_time = tyme::SolarTime::from_ymd_hms(
                        trigger_day.get_year(),
                        trigger_day.get_month(),
                        trigger_day.get_day(),
                        trigger_hour,
                        rule.trigger_minutes,  // 分钟数：0（初刻）、15（一刻）、30（二刻）、45（三刻）
                        0                      // 秒数固定为0
                    );
                    
                    // 返回切换时刻和对应的月将
                    return std::make_pair(trigger_time, rule.result);
                });
        })
        | std::views::join  // 展平嵌套的视图
        | std::ranges::to<std::vector>();  // 收集到 vector

    /**
     * 步骤2：使用 Ranges 按时间排序所有切换点
     * 
     * 排序规则：
     * 1. 首先按时间先后排序
     * 2. 如果时间相同，按月将地支的枚举值排序（确保结果稳定）
     */
    std::ranges::sort(
        transitions,
        [](const auto& lhs, const auto& rhs) {
            // 优先按时间排序
            if (lhs.first.is_before(rhs.first)) {
                return true;
            }
            if (lhs.first.is_after(rhs.first)) {
                return false;
            }
            // 时间相同时，按月将地支枚举值排序
            return static_cast<int>(lhs.second) < static_cast<int>(rhs.second);
        }
    );

    /**
     * 步骤3：使用 Ranges 去除重复的切换点
     * 
     * 可能产生重复的原因：
     * - 不同年份的同一规则可能计算出相同的时刻（理论上不应该，但为保险起见）
     * - 确保每个切换时刻只保留一个记录
     */
    auto unique_end = std::ranges::unique(
        transitions,
        [](const auto& lhs, const auto& rhs) {
            // 如果时间和月将都相同，则认为是重复的
            return lhs.first.equals(rhs.first) && lhs.second == rhs.second;
        }
    );
    transitions.erase(unique_end.begin(), unique_end.end());

    /**
     * 步骤4：使用 Ranges 查找当前时间对应的月将
     * 
     * 算法：找到最后一个不超过当前时间的切换点
     * - 使用 ranges::find_if 配合反向视图（因为已排序，从后往前找）
     * - 或者使用 ranges::partition_point 进行二分查找（O(log n) 复杂度）
     */
    // 使用反向视图查找最后一个 <= 当前时间的切换点
    auto reversed_transitions = transitions | std::views::reverse;
    auto it = std::ranges::find_if(
        reversed_transitions,
        [&](const auto& transition) {
            return !transition.first.is_after(solar_time);
        }
    );
    
    // 如果找到了，返回对应的月将
    if (it != reversed_transitions.end()) {
        return it->second;
    }

    // 如果没有找到（理论上不应该发生），返回默认值
    // 如果切换点列表为空，返回子（神后）
    // 否则返回最后一个切换点的月将（作为兜底）
    return transitions.empty() ? DiZhi::Zi : transitions.back().second;
}

// ==================== 干支课类 ====================

/**
 * @brief 干支课（包含天干或地支与地支的组合）
 * 
 * 大六壬中的"课"分为两种：
 * 1. 干支课：天干 + 地支（上神）
 * 2. 支辰课：地支（下神）+ 地支（上神）
 */
struct GanZhiKe {
    union {
        TianGan gan;          // 天干（用于干支课）
        DiZhi lower_zhi;      // 下神地支（用于支辰课）
    };
    DiZhi upper_zhi;          // 上神地支
    bool is_gan_zhi;          // true: 干支课, false: 支辰课
    
    // 构造函数：干支课
    GanZhiKe(TianGan g, DiZhi upper) 
        : gan(g), upper_zhi(upper), is_gan_zhi(true) {}
    
    // 构造函数：支辰课
    GanZhiKe(DiZhi lower, DiZhi upper) 
        : lower_zhi(lower), upper_zhi(upper), is_gan_zhi(false) {}
    
    /**
     * @brief 获取五行
     */
    WuXing get_wu_xing() const {
        if (is_gan_zhi) {
            return ZhouYi::GanZhi::get_wu_xing(gan);
        } else {
            return ZhouYi::GanZhi::get_wu_xing(lower_zhi);
        }
    }
    
    /**
     * @brief 判断是否为阳
     */
    bool is_yang() const {
        if (is_gan_zhi) {
            return ZhouYi::GanZhi::get_yin_yang(gan) == YinYang::Yang;
        } else {
            return ZhouYi::GanZhi::get_yin_yang(lower_zhi) == YinYang::Yang;
        }
    }
    
    /**
     * @brief 判断是否相等
     */
    bool operator==(const GanZhiKe& other) const {
        if (is_gan_zhi != other.is_gan_zhi) return false;
        if (upper_zhi != other.upper_zhi) return false;
        
        if (is_gan_zhi) {
            return gan == other.gan;
        } else {
            return lower_zhi == other.lower_zhi;
        }
    }
    
    /**
     * @brief 转换为字符串
     */
    std::string to_string() const {
        if (is_gan_zhi) {
            return std::format("{}{}", 
                Mapper::to_zh(gan), 
                Mapper::to_zh(upper_zhi));
        } else {
            return std::format("{}{}", 
                Mapper::to_zh(lower_zhi), 
                Mapper::to_zh(upper_zhi));
        }
    }
};

// ==================== 四课类 ====================

/**
 * @brief 四课
 * 
 * 大六壬的四课：
 * - 第一课（干上神）：日干寄宫的上神
 * - 第二课（干上神的上神）
 * - 第三课（日支的上神）
 * - 第四课（日支上神的上神）
 */
struct SiKe {
    GanZhiKe first;       // 第一课（干上神）
    GanZhiKe second;      // 第二课
    GanZhiKe third;       // 第三课（支上神）
    GanZhiKe fourth;      // 第四课
    DiZhi gan_yang_shen;  // 干阳神（第一课的上神）
    DiZhi zhi_yang_shen;  // 支阳神（第三课的上神）
    
    SiKe(const GanZhiKe& f, const GanZhiKe& s, 
         const GanZhiKe& t, const GanZhiKe& fo,
         DiZhi gys, DiZhi zys)
        : first(f), second(s), third(t), fourth(fo),
          gan_yang_shen(gys), zhi_yang_shen(zys) {}
    
    // Getter 方法（用于卦体判定）
    TianGan get_gan() const { return first.is_gan_zhi ? first.gan : TianGan::Jia; }
    DiZhi get_zhi() const { return third.lower_zhi; }
    DiZhi get_gan_yang_shen() const { return gan_yang_shen; }
    DiZhi get_gan_yin_shen() const { return second.upper_zhi; }
    DiZhi get_zhi_yang_shen() const { return zhi_yang_shen; }
    DiZhi get_zhi_yin_shen() const { return fourth.upper_zhi; }
};

// ==================== 天地盘类 ====================

/**
 * @brief 天地盘
 * 
 * 包含：
 * - 地盘：固定的十二地支（子丑寅卯辰巳午未申酉戌亥）
 * - 天盘：从月将开始顺布的地支
 * - 十二神将：从贵人开始顺或逆布
 */
class TianDiPan {
private:
    std::array<DiZhi, 12> di_pan_;        // 地盘（固定）
    std::array<DiZhi, 12> tian_pan_;      // 天盘
    std::array<DiZhi, 12> shen_jiang_;    // 十二神将位置
    
public:
    /**
     * @brief 构造函数
     * 
     * @param yue_jiang 月将地支
     * @param hour_zhi 时辰地支
     * @param gui_ren 贵人地支
     * @param is_clockwise 神将是否顺布
     */
    TianDiPan(DiZhi yue_jiang, DiZhi hour_zhi, DiZhi gui_ren, bool is_clockwise) {
        // 初始化地盘（固定）
        for (int i = 0; i < 12; ++i) {
            di_pan_[i] = static_cast<DiZhi>(i);
        }
        
        // 初始化天盘（月将落在时辰位置，然后顺布）
        int hour_offset = static_cast<int>(hour_zhi);
        for (int i = 0; i < 12; ++i) {
            int tian_index = (hour_offset + i) % 12;  // 从时辰开始的位置
            int yue_jiang_offset = (static_cast<int>(yue_jiang) + i) % 12;  // 从月将开始递增
            tian_pan_[tian_index] = static_cast<DiZhi>(yue_jiang_offset);
        }
         
        // 初始化神将（从贵人开始顺布或逆布）
        int gui_ren_idx = static_cast<int>(gui_ren);
        int step = is_clockwise ? 1 : -1;  // 阳贵顺布（+1），阴贵逆布（-1）
        for (int i = 0; i < 12; ++i) {
            int pos = (gui_ren_idx + i * step + 12) % 12;
            shen_jiang_[i] = static_cast<DiZhi>(pos);
        }
    }
    
    /**
     * @brief 获取地支对应的天盘地支
     */
    DiZhi operator[](DiZhi zhi) const {
        int index = static_cast<int>(zhi);
        return tian_pan_[index];
    }
    
    /**
     * @brief 获取地盘
     */
    const std::array<DiZhi, 12>& get_di_pan() const { return di_pan_; }
    
    /**
     * @brief 获取天盘
     */
    const std::array<DiZhi, 12>& get_tian_pan() const { return tian_pan_; }
    
    /**
     * @brief 获取神将
     */
    const std::array<DiZhi, 12>& get_shen_jiang() const { return shen_jiang_; }
    
    /**
     * @brief 获取地支对应的神将
     */
    DiZhi get_shen_jiang_at(DiZhi zhi) const {
        int index = static_cast<int>(zhi);
        return shen_jiang_[index];
    }
    
    /**
     * @brief 反向查找：给定天盘地支，找到它所临的地盘地支
     * 
     * @param tian_zhi 天盘地支
     * @return 对应的地盘地支
     */
    DiZhi lin(DiZhi tian_zhi) const {
        for (int i = 0; i < 12; ++i) {
            if (tian_pan_[i] == tian_zhi) {
                return di_pan_[i];
            }
        }
        // 理论上不会到达这里
        return DiZhi::Zi;
    }
};

// ==================== 三传类 ====================

/**
 * @brief 三传
 * 
 * 大六壬的核心：初传、中传、末传
 */
class SanChuan {
private:
    const TianDiPan& tian_di_pan_;
    const SiKe& si_ke_;
    DiZhi chu_chuan_;      // 初传
    DiZhi zhong_chuan_;    // 中传
    DiZhi mo_chuan_;       // 末传
    std::vector<std::string> ke_shi_;  // 课式名称
    
    // ==================== 辅助函数 ====================
    
    /**
     * @brief 去除重复课（相同天干的课）
     */
    std::vector<GanZhiKe> remove_duplicate_lessons(const std::vector<GanZhiKe>& lessons) const;
    
    /**
     * @brief 查找有贼克的课（地支五行克天干五行）
     */
    std::vector<GanZhiKe> have_conquerors() const;
    
    /**
     * @brief 查找有克的课（天干五行克地支五行）
     */
    std::vector<GanZhiKe> have_overcomes() const;
    
    /**
     * @brief 贼克法取三传
     */
    std::array<DiZhi, 3> zei_ke();
    
    /**
     * @brief 比用法取三传
     */
    std::array<DiZhi, 3> bi_yong(const std::vector<GanZhiKe>& lessons);
    
    /**
     * @brief 涉害法取三传
     */
    std::array<DiZhi, 3> she_hai(const std::vector<GanZhiKe>& lessons);
    
    /**
     * @brief 遥克法取三传
     */
    std::array<DiZhi, 3> yao_ke();
    
    /**
     * @brief 昴星法取三传
     */
    std::array<DiZhi, 3> ang_xing();
    
    /**
     * @brief 别责法取三传
     */
    std::array<DiZhi, 3> bie_ze();
    
    /**
     * @brief 八专法取三传
     */
    std::array<DiZhi, 3> ba_zhuan();
    
    /**
     * @brief 伏吟法取三传
     */
    std::array<DiZhi, 3> fu_yin();
    
    /**
     * @brief 返吟法取三传
     */
    std::array<DiZhi, 3> fan_yin();
    
    /**
     * @brief 判断是否为孟神（寅巳申亥）
     */
    bool is_meng(DiZhi zhi) const;
    
    /**
     * @brief 判断是否为仲神（子卯午酉）
     */
    bool is_zhong(DiZhi zhi) const;
    
    /**
     * @brief 判断是否为八专日
     */
    bool is_ba_zhuan_day(const GanZhiKe& ke) const;
    
    /**
     * @brief 判断是否为伏吟课
     */
    bool is_fu_yin_lesson() const;
    
    /**
     * @brief 判断是否为返吟课
     */
    bool is_fan_yin_lesson() const;
    
public:
    /**
     * @brief 构造函数
     * 
     * 根据四课和天地盘计算三传
     */
    SanChuan(const TianDiPan& tdp, const SiKe& sk);
    
    /**
     * @brief 获取初传
     */
    DiZhi get_chu_chuan() const { return chu_chuan_; }
    
    /**
     * @brief 获取中传
     */
    DiZhi get_zhong_chuan() const { return zhong_chuan_; }
    
    /**
     * @brief 获取末传
     */
    DiZhi get_mo_chuan() const { return mo_chuan_; }
    
    /**
     * @brief 获取课式
     */
    const std::vector<std::string>& get_ke_shi() const { return ke_shi_; }
    
    /**
     * @brief 获取三传的遁干
     * @param day_gan 日干
     * @param day_zhi 日支
     * @return 三个天干，对应初传、中传、末传。空亡时返回空optional
     */
    std::array<std::optional<TianGan>, 3> get_dun_gan(TianGan day_gan, DiZhi day_zhi) const;
    
    /**
     * @brief 获取三传的六亲关系
     * @param day_gan 日干
     * @return 三个六亲名称，对应初传、中传、末传
     */
    std::array<std::string_view, 3> get_liu_qin(TianGan day_gan) const;
};

// ==================== 大六壬排盘结果 ====================

/**
 * @brief 大六壬排盘结果
 */
struct DaLiuRenResult {
    BaZi ba_zi;                            // 八字信息
    DiZhi yue_jiang;                       // 月将
    DiZhi gui_ren;                         // 贵人
    bool is_day;                           // 是否白天
    TianDiPan tian_di_pan;                 // 天地盘
    SiKe si_ke;                            // 四课
    SanChuan san_chuan;                    // 三传
    ShenSha::ShenShaResult shen_sha;       // 神煞
    std::vector<std::string> gua_ti;       // 卦体
    
    DaLiuRenResult(const BaZi& bz, DiZhi yj, DiZhi gr, bool id,
                   const TianDiPan& tdp, const SiKe& sk, const SanChuan& sc,
                   const ShenSha::ShenShaResult& ss, const std::vector<std::string>& gt)
        : ba_zi(bz), yue_jiang(yj), gui_ren(gr), is_day(id),
          tian_di_pan(tdp), si_ke(sk), san_chuan(sc), shen_sha(ss), gua_ti(gt) {}
    
    /**
     * @brief 转换为 JSON
     */
    nlohmann::json to_json() const;
    
    /**
     * @brief 格式化输出
     */
    std::string to_string() const;
};

// ==================== 大六壬排盘引擎 ====================

/**
 * @brief 大六壬排盘引擎
 * 
 * 提供大六壬的排盘功能
 */
class DaLiuRenEngine {
public:
    /**
     * @brief 从公历日期时间排盘
     * 
     * @param year 公历年
     * @param month 公历月
     * @param day 公历日
     * @param hour 公历时
     * @return DaLiuRenResult 排盘结果
     */
    static DaLiuRenResult pai_pan(int year, int month, int day, int hour);
    
    /**
     * @brief 从农历日期时间排盘
     */
    static DaLiuRenResult pai_pan_lunar(int year, int month, int day, int hour);
    
    /**
     * @brief 从八字与公历时刻排盘
     */
    static DaLiuRenResult pai_pan_from_bazi(const BaZi& ba_zi, const tyme::SolarTime& solar_time);
};

} // namespace ZhouYi::DaLiuRen

