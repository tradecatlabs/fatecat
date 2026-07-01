// 紫微斗数常量定义模块
export module ZhouYi.ZiWei.Constants;

import std;
import ZhouYi.GanZhi;
import ZhouYi.ZhMapper;

export namespace ZhouYi::ZiWei {
    using namespace std;

    /**
     * @brief 十二宫名称（从命宫开始）
     */
    enum class GongWei {
        MingGong = 0,    // 命宫
        XiongDiGong,     // 兄弟宫
        FuQiGong,        // 夫妻宫
        ZiNvGong,        // 子女宫
        CaiBoGong,       // 财帛宫
        JiBingGong,      // 疾厄宫
        QianYiGong,      // 迁移宫
        NuPuGong,        // 奴仆宫（交友宫）
        GuanLuGong,      // 官禄宫（事业宫）
        TianZhaiGong,    // 田宅宫
        FuDeGong,        // 福德宫
        FuMuGong,        // 父母宫
        COUNT = 12
    };

    /**
     * @brief 五行局（纳音五行）
     * 紫微斗数用于定紫微星位置和起运年龄
     */
    enum class WuXingJu {
        ShuiErJu = 2,    // 水二局
        MuSanJu = 3,     // 木三局
        JinSiJu = 4,     // 金四局
        TuWuJu = 5,      // 土五局
        HuoLiuJu = 6     // 火六局
    };

    /**
     * @brief 主星（十四正曜）
     */
    enum class ZhuXing {
        // 北斗星系（紫微星系）
        ZiWei = 0,       // 紫微星（帝座）
        TianJi,          // 天机星（智慧）
        TaiYang,         // 太阳星（权贵）
        WuQu,            // 武曲星（财富）
        TianTong,        // 天同星（福星）
        LianZhen,        // 廉贞星（桃花）
        
        // 南斗星系（天府星系）
        TianFu,          // 天府星（财库）
        TaiYin,          // 太阴星（财富）
        TanLang,         // 贪狼星（欲望）
        JuMen,           // 巨门星（口舌）
        TianXiang,       // 天相星（印绶）
        TianLiang,       // 天梁星（荫庇）
        QiSha,           // 七杀星（将星）
        PoJun,           // 破军星（耗星）
        
        COUNT
    };

    /**
     * @brief 辅星（左辅右弼等）
     */
    enum class FuXing {
        ZuoFu = 0,       // 左辅
        YouBi,           // 右弼
        WenChang,        // 文昌
        WenQu,           // 文曲
        TianKui,         // 天魁
        TianYue,         // 天钺
        COUNT
    };

    /**
     * @brief 煞星
     */
    enum class ShaXing {
        QingYang = 0,    // 擎羊
        TuoLuo,          // 陀罗
        HuoXing,         // 火星
        LingXing,        // 铃星
        DiKong,          // 地空
        DiJie,           // 地劫
        COUNT
    };

    /**
     * @brief 禄权科忌（四化）
     */
    enum class SiHua {
        Lu = 0,          // 化禄
        Quan,            // 化权
        Ke,              // 化科
        Ji,              // 化忌
        COUNT
    };

    /**
     * @brief 长生十二神
     */
    enum class ChangSheng12 {
        ChangSheng = 0,  // 长生
        MuYu,            // 沐浴
        GuanDai,         // 冠带
        LinGuan,         // 临官
        DiWang,          // 帝旺
        Shuai,           // 衰
        Bing,            // 病
        Si,              // 死
        Mu,              // 墓
        Jue,             // 绝
        Tai,             // 胎
        Yang,            // 养
        COUNT = 12
    };

    /**
     * @brief 星耀亮度
     */
    enum class LiangDu {
        Miao = 0,        // 庙（最亮）
        Wang,            // 旺
        De,              // 得
        Ping,            // 平
        Xian,            // 陷
        Bu,              // 不
        Li,              // 利
        COUNT
    };

    // 添加杂耀
    enum class ZaYao {
        // 桃花星
        HongLuan = 0,    // 红鸾
        TianXi,          // 天喜
        TianYao,         // 天姚
        XianChi,         // 咸池
        
        // 贵人星
        JieShen,         // 解神
        TianWu,          // 天巫
        TianGuan,        // 天官
        TianFu2,         // 天福
        TianChu,         // 天厨
        TianMa,          // 天马
        
        // 吉星
        SanTai,          // 三台
        BaZuo,           // 八座
        EnGuang,         // 恩光
        TianGui,         // 天贵
        LongChi,         // 龙池
        FengGe,          // 凤阁
        TianCai,         // 天才
        TianShou,        // 天寿
        TaiFu,           // 台辅
        FengGao,         // 封诰
        HuaGai,          // 华盖
        TianYue2,        // 天月
        TianDe,          // 天德
        YueDe,           // 月德
        
        // 凶星
        GuChen,          // 孤辰
        GuaSu,           // 寡宿
        FeiLian,         // 蜚廉
        PoSui,           // 破碎
        TianXing,        // 天刑
        YinSha,          // 阴煞
        TianKong2,       // 天空
        XunKong,         // 旬空
        JieLu,           // 截路
        KongWang,        // 空亡
        TianKu,          // 天哭
        TianXu,          // 天虚
        TianShi,         // 天使
        TianShang,       // 天伤
        NianJie,         // 年解
        DaHao,           // 大耗（生年）
        LongDe2,         // 龙德（生年）
        
        COUNT
    };


    /**
     * @brief 五行局对应的起运年龄（虚岁）
     */
    constexpr int get_qi_yun_age(WuXingJu ju) {
        return static_cast<int>(ju);
    }

    /**
     * @brief 流年岁前12神
     */
    enum class SuiQian12 {
        SuiJian = 0,     // 岁建
        HuiQi,           // 晦气
        SangMen,         // 丧门
        GuanSuo,         // 贯索
        GuanFu,          // 官符
        XiaoHao,         // 小耗
        DaHao,           // 大耗
        LongDe,          // 龙德
        BaiHu,           // 白虎
        TianDe2,         // 天德
        DiaoKe,          // 吊客
        BingFu,          // 病符
        COUNT = 12
    };

    /**
     * @brief 流年将前12神
     */
    enum class JiangQian12 {
        JiangXing = 0,   // 将星
        PanAn,           // 攀鞍
        SuiYi,           // 岁驿
        XiShen,          // 息神
        HuaGai2,         // 华盖
        JieSha,          // 劫煞
        ZaiSha,          // 灾煞
        TianSha,         // 天煞
        ZhiBei,          // 指背
        XianChi2,        // 咸池
        YueSha,          // 月煞
        WangShen,        // 亡神
        COUNT = 12
    };

    /**
     * @brief 博士12神
     */
    enum class BoShi12 {
        BoShi = 0,       // 博士
        LiShi,           // 力士
        QingLong,        // 青龙
        XiaoHao2,        // 小耗
        JiangJun,        // 将军
        ZouShu,          // 奏书
        FeiLian2,        // 飞廉
        XiShen2,         // 喜神
        BingFu2,         // 病符
        DaHao2,          // 大耗
        FuBing,          // 伏兵
        GuanFu2,         // 官府
        COUNT = 12
    };

    /**
     * @brief 天地人三盘类型
     */
    enum class PanType {
        Tian = 0,        // 天盘（本命盘）
        Di,              // 地盘（身宫起命）
        Ren,             // 人盘（福德宫起命）
        COUNT
    };

    /**
     * @brief 修正索引（确保在0-11范围内）
     */
    constexpr int fix_index(int index, int size = 12) {
        index %= size;
        if (index < 0) {
            index += size;
        }
        return index;
    }

} // namespace ZhouYi::ZiWei

// ZhMapper 特化定义
namespace ZhouYi::Mapper {
    using namespace ZhouYi::ZiWei;

    // 宫位中文映射
    template<>
    struct ZhMap<GongWei> {
        static constexpr auto get_map() {
            return std::array{
                "命宫"sv, "兄弟宫"sv, "夫妻宫"sv, "子女宫"sv,
                "财帛宫"sv, "疾厄宫"sv, "迁移宫"sv, "奴仆宫"sv,
                "官禄宫"sv, "田宅宫"sv, "福德宫"sv, "父母宫"sv
            };
        }
    };

    // 主星中文映射
    template<>
    struct ZhMap<ZhuXing> {
        static constexpr auto get_map() {
            return std::array{
                "紫微"sv, "天机"sv, "太阳"sv, "武曲"sv, "天同"sv, "廉贞"sv,
                "天府"sv, "太阴"sv, "贪狼"sv, "巨门"sv, "天相"sv, "天梁"sv,
                "七杀"sv, "破军"sv
            };
        }
    };

    // 辅星中文映射
    template<>
    struct ZhMap<FuXing> {
        static constexpr auto get_map() {
            return std::array{
                "左辅"sv, "右弼"sv, "文昌"sv, "文曲"sv, "天魁"sv, "天钺"sv
            };
        }
    };

    // 煞星中文映射
    template<>
    struct ZhMap<ShaXing> {
        static constexpr auto get_map() {
            return std::array{
                "擎羊"sv, "陀罗"sv, "火星"sv, "铃星"sv, "地空"sv, "地劫"sv
            };
        }
    };

    // 四化中文映射
    template<>
    struct ZhMap<SiHua> {
        static constexpr auto get_map() {
            return std::array{
                "化禄"sv, "化权"sv, "化科"sv, "化忌"sv
            };
        }
    };

    // 长生12神中文映射
    template<>
    struct ZhMap<ChangSheng12> {
        static constexpr auto get_map() {
            return std::array{
                "长生"sv, "沐浴"sv, "冠带"sv, "临官"sv, "帝旺"sv, "衰"sv,
                "病"sv, "死"sv, "墓"sv, "绝"sv, "胎"sv, "养"sv
            };
        }
    };

    // 亮度中文映射
    template<>
    struct ZhMap<LiangDu> {
        static constexpr auto get_map() {
            return std::array{
                "庙"sv, "旺"sv, "得"sv, "平"sv, "陷"sv, "不"sv, "利"sv
            };
        }
    };

    // 五行局中文映射
    template<>
    struct ZhMap<WuXingJu> {
        static constexpr auto get_map() {
            return std::array{
                "水二局"sv, "木三局"sv, "金四局"sv, "土五局"sv, "火六局"sv
            };
        }
    };

    // 杂耀中文映射
    template<>
    struct ZhMap<ZaYao> {
        static constexpr auto get_map() {
            return std::array{
                "红鸾"sv, "天喜"sv, "天姚"sv, "咸池"sv,
                "解神"sv, "天巫"sv, "天官"sv, "天福"sv, "天厨"sv, "天马"sv,
                "三台"sv, "八座"sv, "恩光"sv, "天贵"sv, "龙池"sv, "凤阁"sv,
                "天才"sv, "天寿"sv, "台辅"sv, "封讼"sv, "华盖"sv, "天月"sv,
                "天德"sv, "月德"sv,
                "孤辰"sv, "寡宿"sv, "蜚廉"sv, "破碎"sv, "天刑"sv, "阴煞"sv,
                "天空"sv, "旬空"sv, "截路"sv, "空亡"sv, "天哭"sv, "天虚"sv,
                "天使"sv, "天伤"sv, "年解"sv, "大耗"sv, "龙德"sv
            };
        }
    };

    // 岁前12神中文映射
    template<>
    struct ZhMap<SuiQian12> {
        static constexpr auto get_map() {
            return std::array{
                "岁建"sv, "晦气"sv, "丧门"sv, "贯索"sv, "官符"sv, "小耗"sv,
                "大耗"sv, "龙德"sv, "白虎"sv, "天德"sv, "吊客"sv, "病符"sv
            };
        }
    };

    // 将前12神中文映射
    template<>
    struct ZhMap<JiangQian12> {
        static constexpr auto get_map() {
            return std::array{
                "将星"sv, "攀鞍"sv, "岁驿"sv, "息神"sv, "华盖"sv, "劫煞"sv,
                "灾煞"sv, "天煞"sv, "指背"sv, "咸池"sv, "月煞"sv, "亡神"sv
            };
        }
    };

    // 博士12神中文映射
    template<>
    struct ZhMap<BoShi12> {
        static constexpr auto get_map() {
            return std::array{
                "博士"sv, "力士"sv, "青龙"sv, "小耗"sv, "将军"sv, "奏书"sv,
                "飞廉"sv, "喜神"sv, "病符"sv, "大耗"sv, "伏兵"sv, "官府"sv
            };
        }
    };

    // 三盘类型中文映射
    template<>
    struct ZhMap<PanType> {
        static constexpr auto get_map() {
            return std::array{
                "天盘"sv, "地盘"sv, "人盘"sv
            };
        }
    };

} // namespace ZhouYi::Mapper