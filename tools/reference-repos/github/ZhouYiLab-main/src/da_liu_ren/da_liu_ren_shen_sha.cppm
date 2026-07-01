// 大六壬神煞系统模块

export module ZhouYi.DaLiuRen.ShenSha;

import ZhouYi.GanZhi;
import ZhouYi.BaZiBase;
import nlohmann.json;
import std;

/**
 * @brief 大六壬神煞系统命名空间
 */
export namespace ZhouYi::DaLiuRen::ShenSha {

using namespace ZhouYi::GanZhi;
using namespace ZhouYi::BaZiBase;

// ==================== 神煞分类枚举 ====================

/**
 * @brief 神煞类别
 */
enum class ShenShaCategory {
    Ji,          // 吉神
    Xiong,       // 凶神
    DongBian,    // 动变
    LuMa,        // 禄马
    TaoHua,      // 桃花咸池
    KongWang,    // 空亡
    Sang,        // 丧煞
    XueGuang,    // 血光
    GuDu,        // 孤独
    YiXiang      // 医相
};

/**
 * @brief 神煞信息
 */
struct ShenShaInfo {
    std::string name;                              // 神煞名称
    std::optional<DiZhi> zhi;                     // 所在地支
    std::vector<ShenShaCategory> categories;      // 所属类别
};

// ==================== 神煞数据结构 ====================

/**
 * @brief 神煞结果
 */
struct ShenShaResult {
    // 基础神煞（年月日时相关）
    DiZhi tai_sui;                   // 太岁（年支）
    DiZhi yue_jian;                  // 月建（月支）
    DiZhi ri_jian;                   // 日建（日支）
    DiZhi yue_po;                    // 月破（月建对冲）
    DiZhi ri_po;                     // 日破（日建对冲）
    
    // 年神煞
    DiZhi nian_yi_ma;                // 年驿马
    DiZhi da_hao;                    // 大耗
    DiZhi xiao_hao;                  // 小耗
    DiZhi bing_fu;                   // 病符
    DiZhi sui_de;                    // 岁德
    DiZhi sui_xing;                  // 岁刑
    DiZhi sui_he;                    // 岁合
    DiZhi jie_sha;                   // 劫煞
    DiZhi fei_lian;                  // 飞廉
    DiZhi sang_men;                  // 丧门
    DiZhi diao_ke;                   // 吊客
    DiZhi wang_shen;                 // 亡神
    
    // 月神煞
    DiZhi yue_yi_ma;                 // 月驿马
    DiZhi huang_shu;                 // 皇书
    DiZhi huang_en;                  // 皇恩
    DiZhi tian_zhao;                 // 天诏
    DiZhi fei_hun;                   // 飞魂
    DiZhi tian_xi;                   // 天喜
    DiZhi sheng_qi;                  // 生气
    DiZhi tian_ma;                   // 天马
    DiZhi san_qiu;                   // 三丘
    DiZhi wu_mu;                     // 五墓
    DiZhi si_qi;                     // 死气
    DiZhi man_yu;                    // 谩语
    DiZhi gu_chen;                   // 孤辰
    DiZhi gua_su;                    // 寡宿
    DiZhi tian_yi;                   // 天医
    DiZhi di_yi;                     // 地医
    DiZhi tian_wu;                   // 天巫
    DiZhi di_wu;                     // 地巫
    DiZhi po_sui;                    // 破碎
    DiZhi yue_yan;                   // 月厌
    DiZhi xue_zhi;                   // 血支
    DiZhi xue_ji;                    // 血忌
    DiZhi sang_che;                  // 丧车
    DiZhi xin_shen;                  // 信神
    DiZhi tian_ji;                   // 天鸡
    DiZhi sang_hun;                  // 丧魂
    DiZhi tian_gui;                  // 天鬼
    DiZhi da_shi;                    // 大时
    DiZhi xiao_shi;                  // 小时
    DiZhi yue_he;                    // 月合
    DiZhi yue_xing;                  // 月刑
    DiZhi huo_gui;                   // 火鬼
    DiZhi tian_mu;                   // 天目
    DiZhi jian_shen;                 // 奸神
    DiZhi jian_men;                  // 奸门
    DiZhi yao_shen;                  // 钥神
    DiZhi fei_huo;                   // 飞祸
    DiZhi hong_wan;                  // 红弯
    
    // 日神煞
    DiZhi ri_yi_ma;                  // 日驿马
    DiZhi xun_qi;                    // 旬奇
    DiZhi ri_qi;                     // 日奇
    DiZhi xun_yi;                    // 旬仪（旬首）
    DiZhi zhi_yi;                    // 支仪
    DiZhi ri_de;                     // 日德（地支）
    DiZhi ri_lu;                     // 日禄（地支）
    DiZhi xun_ding;                  // 旬丁
    DiZhi cheng_shen;                // 成神
    DiZhi tao_hua;                   // 桃花
    DiZhi xian_chi;                  // 咸池
    DiZhi zei_fu;                    // 贼符
    DiZhi si_fu;                     // 死符
    DiZhi si_shen;                   // 死神
    DiZhi zhi_de;                    // 支德
    DiZhi yang_ren;                  // 阳刃
    DiZhi jie_shen;                  // 解神
    
    // 地支到神煞的映射（每个地支上的神煞列表）
    std::map<DiZhi, std::vector<std::string>> zhi_to_shensha_map;
    
    // 神煞信息列表（包含分类）
    std::vector<ShenShaInfo> shen_sha_list;
    
    /**
     * @brief 构建地支到神煞的映射
     */
    void build_zhi_mapping();
    
    /**
     * @brief 获取某个地支上的神煞列表
     * 
     * @param zhi 地支
     * @return 该地支上的神煞名称列表
     */
    std::vector<std::string> get_shensha_on_zhi(DiZhi zhi) const;
    
    /**
     * @brief 转换为可读字符串
     */
    std::string to_string() const;
    
    /**
     * @brief 转换为 JSON
     */
    nlohmann::json to_json() const;
};

// ==================== 神煞计算类 ====================

/**
 * @brief 神煞计算引擎
 */
class ShenShaEngine {
private:
    const BaZi& ba_zi_;
    DiZhi day_zhi_;  // 日支
    
    // 辅助函数：查找孟位（寅巳申亥）
    static DiZhi find_meng_zhi(DiZhi start_zhi);
    
    // 辅助函数：查找仲位（子卯午酉）
    static DiZhi find_zhong_zhi(DiZhi start_zhi);
    
public:
    /**
     * @brief 构造函数
     * 
     * @param ba_zi 八字
     * @param day_zhi 日支
     */
    ShenShaEngine(const BaZi& ba_zi, DiZhi day_zhi);
    
    /**
     * @brief 计算所有神煞
     */
    ShenShaResult calculate() const;
    
    // ==================== 年神煞计算 ====================
    
    /**
     * @brief 计算年驿马
     */
    DiZhi calc_nian_yi_ma() const;
    
    /**
     * @brief 计算大耗
     */
    DiZhi calc_da_hao() const;
    
    /**
     * @brief 计算小耗
     */
    DiZhi calc_xiao_hao() const;
    
    /**
     * @brief 计算病符
     */
    DiZhi calc_bing_fu() const;
    
    // ==================== 月神煞计算 ====================
    
    /**
     * @brief 计算月驿马
     */
    DiZhi calc_yue_yi_ma() const;
    
    /**
     * @brief 计算皇书
     */
    DiZhi calc_huang_shu() const;
    
    /**
     * @brief 计算皇恩
     */
    DiZhi calc_huang_en() const;
    
    /**
     * @brief 计算天诏/飞魂
     */
    DiZhi calc_tian_zhao_fei_hun() const;
    
    /**
     * @brief 计算天喜
     */
    DiZhi calc_tian_xi() const;
    
    /**
     * @brief 计算生气
     */
    DiZhi calc_sheng_qi() const;
    
    /**
     * @brief 计算天马
     */
    DiZhi calc_tian_ma() const;
    
    /**
     * @brief 计算三丘
     */
    DiZhi calc_san_qiu() const;
    
    /**
     * @brief 计算五墓
     */
    DiZhi calc_wu_mu() const;
    
    /**
     * @brief 计算死气/谩语
     */
    DiZhi calc_si_qi_man_yu() const;
    
    /**
     * @brief 计算孤辰
     */
    DiZhi calc_gu_chen() const;
    
    /**
     * @brief 计算寡宿
     */
    DiZhi calc_gua_su() const;
    
    /**
     * @brief 计算天医
     */
    DiZhi calc_tian_yi() const;
    
    /**
     * @brief 计算地医
     */
    DiZhi calc_di_yi() const;
    
    /**
     * @brief 计算破碎
     */
    DiZhi calc_po_sui() const;
    
    /**
     * @brief 计算月厌
     */
    DiZhi calc_yue_yan() const;
    
    /**
     * @brief 计算血支
     */
    DiZhi calc_xue_zhi() const;
    
    /**
     * @brief 计算血忌
     */
    DiZhi calc_xue_ji() const;
    
    /**
     * @brief 计算丧车
     */
    DiZhi calc_sang_che() const;
    
    /**
     * @brief 计算信神
     */
    DiZhi calc_xin_shen() const;
    
    /**
     * @brief 计算天鸡
     */
    DiZhi calc_tian_ji() const;
    
    /**
     * @brief 计算丧魂
     */
    DiZhi calc_sang_hun() const;
    
    /**
     * @brief 计算天鬼
     */
    DiZhi calc_tian_gui() const;
    
    /**
     * @brief 计算大时
     */
    DiZhi calc_da_shi() const;
    
    /**
     * @brief 计算小时
     */
    DiZhi calc_xiao_shi() const;
    
    /**
     * @brief 计算月合
     */
    DiZhi calc_yue_he() const;
    
    /**
     * @brief 计算月刑
     */
    DiZhi calc_yue_xing() const;
    
    /**
     * @brief 计算火鬼
     */
    DiZhi calc_huo_gui() const;
    
    /**
     * @brief 计算天目
     */
    DiZhi calc_tian_mu() const;
    
    /**
     * @brief 计算奸神
     */
    DiZhi calc_jian_shen() const;
    
    /**
     * @brief 计算奸门
     */
    DiZhi calc_jian_men() const;
    
    /**
     * @brief 计算钥神
     */
    DiZhi calc_yao_shen() const;
    
    /**
     * @brief 计算飞祸
     */
    DiZhi calc_fei_huo() const;
    
    /**
     * @brief 计算红弯
     */
    DiZhi calc_hong_wan() const;
    
    // ==================== 年神煞（补充） ====================
    
    /**
     * @brief 计算岁德
     */
    DiZhi calc_sui_de() const;
    
    /**
     * @brief 计算岁刑
     */
    DiZhi calc_sui_xing() const;
    
    /**
     * @brief 计算岁合
     */
    DiZhi calc_sui_he() const;
    
    /**
     * @brief 计算劫煞
     */
    DiZhi calc_jie_sha() const;
    
    /**
     * @brief 计算飞廉
     */
    DiZhi calc_fei_lian() const;
    
    /**
     * @brief 计算丧门
     */
    DiZhi calc_sang_men() const;
    
    /**
     * @brief 计算吊客
     */
    DiZhi calc_diao_ke() const;
    
    /**
     * @brief 计算亡神
     */
    DiZhi calc_wang_shen() const;
    
    // ==================== 日神煞计算 ====================
    
    /**
     * @brief 计算日驿马
     */
    DiZhi calc_ri_yi_ma() const;
      
    /**
     * @brief 计算旬奇
     */
    DiZhi calc_xun_qi() const;
    
    /**
     * @brief 计算日奇
     */
    DiZhi calc_ri_qi() const;
    
    /**
     * @brief 计算旬仪
     */
    DiZhi calc_xun_yi() const;
    
    /**
     * @brief 计算支仪
     */
    DiZhi calc_zhi_yi() const;
    
    /**
     * @brief 计算日德（地支）
     */
    DiZhi calc_ri_de() const;
    
    /**
     * @brief 计算日禄（地支）
     */
    DiZhi calc_ri_lu() const;
    
    /**
     * @brief 计算旬丁
     */
    DiZhi calc_xun_ding() const;
    
    /**
     * @brief 计算成神
     */
    DiZhi calc_cheng_shen() const;
    
    /**
     * @brief 计算桃花
     */
    DiZhi calc_tao_hua() const;
    
    /**
     * @brief 计算咸池
     */
    DiZhi calc_xian_chi() const;
    
    /**
     * @brief 计算贼符
     */
    DiZhi calc_zei_fu() const;
    
    /**
     * @brief 计算死符
     */
    DiZhi calc_si_fu() const;
    
    /**
     * @brief 计算死神
     */
    DiZhi calc_si_shen() const;
    
    /**
     * @brief 计算支德
     */
    DiZhi calc_zhi_de() const;
    
    /**
     * @brief 计算阳刃
     */
    DiZhi calc_yang_ren() const;
    
    /**
     * @brief 计算解神
     */
    DiZhi calc_jie_shen() const;
};

} // namespace ZhouYi::DaLiuRen::ShenSha

