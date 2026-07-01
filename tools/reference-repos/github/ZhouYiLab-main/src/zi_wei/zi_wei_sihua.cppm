// 紫微斗数四化系统模块（接口）
export module ZhouYi.ZiWei.SiHua;

import std;
import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZhMapper;

export namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;

    /**
     * @brief 四化信息结构
     */
    struct SiHuaInfo {
        SiHua type;           // 四化类型（禄权科忌）
        string star_name;     // 化星名称
        int gong_index;       // 化星所在宫位
        
        string to_string() const;
    };

    /**
     * @brief 宫干四化数据
     * 每个宫位的天干都会产生四化，飞入其他宫位
     */
    struct GongGanSiHua {
        int gong_index;                    // 宫位索引
        TianGan gong_gan;                  // 宫位天干
        array<SiHuaInfo, 4> si_hua_list;   // 四化列表（禄权科忌）
        
        /**
         * @brief 获取指定四化类型的信息
         */
        optional<SiHuaInfo> get_si_hua(SiHua type) const {
            for (const auto& info : si_hua_list) {
                if (info.type == type) {
                    return info;
                }
            }
            return nullopt;
        }
        
        string to_string() const;
    };

    /**
     * @brief 自化信息
     * 当宫位天干四化的星耀恰好在本宫，称为"自化"
     */
    struct ZiHuaInfo {
        int gong_index;              // 宫位索引
        vector<SiHua> zi_hua_types;  // 自化类型列表
        
        bool has_zi_hua() const {
            return !zi_hua_types.empty();
        }
        
        bool has_zi_hua_type(SiHua type) const {
            return find(zi_hua_types.begin(), zi_hua_types.end(), type) != zi_hua_types.end();
        }
        
        string to_string() const;
    };

    /**
     * @brief 飞化关系
     * 从某宫飞化到另一宫的关系
     */
    struct FeiHuaRelation {
        int from_gong;          // 起飞宫位
        TianGan from_gan;       // 起飞宫天干
        int to_gong;            // 落宫
        SiHua si_hua_type;      // 四化类型
        string star_name;       // 化星名称
        
        string to_string() const;
    };

    /**
     * @brief 多层飞化链
     * 支持飞化之飞化（最多4层）
     */
    struct FeiHuaChain {
        vector<FeiHuaRelation> chain;  // 飞化链
        bool is_hui_ben;               // 是否回本宫（最后回到起始宫）
        
        int get_depth() const {
            return static_cast<int>(chain.size());
        }
        
        string to_string() const;
    };

    /**
     * @brief 四化系统管理器
     */
    class SiHuaSystem {
    public:
        /**
         * @brief 构造函数
         * @param gong_wei_data 十二宫数据（需包含天干地支）
         * @param stars_in_gong 每个宫位的星耀列表
         */
        SiHuaSystem(
            const array<pair<TianGan, DiZhi>, 12>& gong_gan_zhi,
            const array<vector<string>, 12>& stars_in_gong
        );
        
        /**
         * @brief 获取所有宫位的宫干四化
         */
        const array<GongGanSiHua, 12>& get_all_gong_gan_si_hua() const {
            return gong_gan_si_hua_;
        }
        
        /**
         * @brief 获取指定宫位的宫干四化
         */
        const GongGanSiHua& get_gong_gan_si_hua(int gong_index) const {
            return gong_gan_si_hua_[fix_index(gong_index)];
        }
        
        /**
         * @brief 判断某宫是否有自化
         */
        bool has_zi_hua(int gong_index) const;
        
        /**
         * @brief 判断某宫是否有指定类型的自化
         */
        bool has_zi_hua_type(int gong_index, SiHua type) const;
        
        /**
         * @brief 获取所有自化宫位
         */
        vector<ZiHuaInfo> get_all_zi_hua() const;
        
        /**
         * @brief 判断是否从某宫飞化到另一宫
         */
        bool flies_to(int from_gong, int to_gong, SiHua si_hua_type) const;
        
        /**
         * @brief 获取从某宫飞出的所有四化
         */
        vector<FeiHuaRelation> get_fei_hua_from(int gong_index) const;
        
        /**
         * @brief 获取飞入某宫的所有四化
         */
        vector<FeiHuaRelation> get_fei_hua_to(int gong_index) const;
        
        /**
         * @brief 获取多层飞化链（最多4层）
         * @param start_gong 起始宫位
         * @param si_hua_type 四化类型
         * @param max_depth 最大深度（1-4）
         */
        vector<FeiHuaChain> get_fei_hua_chains(
            int start_gong,
            SiHua si_hua_type,
            int max_depth = 4
        ) const;
        
        /**
         * @brief 查找飞化回本宫的链（四化回本宫）
         */
        vector<FeiHuaChain> find_hui_ben_chains(int start_gong) const;
        
    private:
        array<GongGanSiHua, 12> gong_gan_si_hua_;     // 12宫的宫干四化
        array<vector<string>, 12> stars_in_gong_;     // 每宫的星耀列表
        
        /**
         * @brief 计算宫干四化
         */
        void calculate_gong_gan_si_hua(const array<pair<TianGan, DiZhi>, 12>& gong_gan_zhi);
        
        /**
         * @brief 递归查找飞化链
         */
        void find_chains_recursive(
            int current_gong,
            SiHua si_hua_type,
            int current_depth,
            int max_depth,
            vector<FeiHuaRelation>& current_chain,
            set<int>& visited,
            vector<FeiHuaChain>& result
        ) const;
    };

    /**
     * @brief 获取天干对应的四化星
     * 
     * @param gan 天干
     * @return 四化星数组（禄权科忌顺序）
     */
    array<optional<ZhuXing>, 4> get_si_hua_stars(TianGan gan);

    /**
     * @brief 判断某星在指定天干下的四化类型
     * 
     * @param gan 天干
     * @param star 主星
     * @return 四化类型（如果不化则返回nullopt）
     */
    optional<SiHua> get_star_si_hua_type(TianGan gan, ZhuXing star);

} // namespace ZhouYi::ZiWei

