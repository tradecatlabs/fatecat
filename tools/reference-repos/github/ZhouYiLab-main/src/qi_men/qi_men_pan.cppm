// 奇门遁甲排盘算法实现
// 实现完整的排盘逻辑

export module ZhouYi.QiMen.Pan;

import ZhouYi.QiMen;
import ZhouYi.GanZhi;
import fmt;
import std;

/**
 * @brief 奇门排盘算法实现
 */
export namespace ZhouYi::QiMen {

/**
 * @brief 排盘器类
 * 
 * 负责生成完整的奇门盘
 */
class QiMenPanGenerator {
public:
    /**
     * @brief 生成奇门盘
     * 
     * @param solar_term 节气
     * @param tian_gan_day 日天干（0-9）
     * @param di_zhi_day 日地支（0-11）
     * @param tian_gan_hour 时天干（0-9）
     * @param di_zhi_hour 时地支（0-11）
     * @return 生成的奇门盘
     */
    [[nodiscard]] static auto generate_pan(
        SolarTerm solar_term,
        std::uint8_t tian_gan_day,
        std::uint8_t di_zhi_day,
        std::uint8_t tian_gan_hour,
        std::uint8_t di_zhi_hour
    ) -> std::expected<QiMenPan, std::string> {
        
        // 参数验证
        if (tian_gan_day >= 10) {
            return std::unexpected("日天干必须在 0-9 之间");
        }
        if (di_zhi_day >= 12) {
            return std::unexpected("日地支必须在 0-11 之间");
        }
        if (tian_gan_hour >= 10) {
            return std::unexpected("时天干必须在 0-9 之间");
        }
        if (di_zhi_hour >= 12) {
            return std::unexpected("时地支必须在 0-11 之间");
        }
        
        QiMenPan pan{};
        
        // 1. 确定阴阳遁
        pan.dun = get_dun_from_solar_term(solar_term);
        
        // 2. 根据日地支确定三元
        pan.yuan = get_yuan_from_di_zhi(di_zhi_day);
        
        // 3. 确定局数
        pan.ju = get_ju_from_solar_term_and_yuan(solar_term, pan.yuan);
        
        // 4. 记录节气
        pan.solar_term = solar_term;
        
        // 5. 排布地盘（地盘天干）
        arrange_di_pan(pan, pan.ju);
        
        // 6. 确定直符和直使
        determine_zhi_fu_and_zhi_shi(pan, tian_gan_day, di_zhi_day, tian_gan_hour, di_zhi_hour);
        
        // 7. 排布天盘（天盘天干）
        arrange_tian_pan(pan, tian_gan_hour, di_zhi_hour);
        
        // 7.5. 排布九星（转盘）
        arrange_jiu_xing(pan, tian_gan_hour);
        
        // 8. 排布人盘（人盘八门）
        arrange_ren_pan(pan, tian_gan_hour);
        
        // 9. 排布神盘（八神）
        arrange_shen_pan(pan);
        
        return pan;
    }

private:
    /**
     * @brief 排布地盘天干
     * 
     * 地盘天干按照戊己庚辛壬癸丁丙乙的顺序排列
     * 阳遁：戊从局数宫开始，按洛书顺序顺飞
     * 阴遁：戊从局数宫开始，按九宫数字逆飞
     */
    static void arrange_di_pan(QiMenPan& pan, std::uint8_t ju) {
        // 地盘干固定顺序：戊己庚辛壬癸丁丙乙
        auto gan_seq = get_tian_gan_sequence();
        
        // 初始化所有宫位的基本信息
        for (std::uint8_t i = 1; i <= 9; ++i) {
            Palace p = get_palace_from_number(i);
            auto& palace_info = pan.palaces[i - 1];
            palace_info.palace = p;
            palace_info.star = get_star_at_palace(p);
            palace_info.gate = get_gate_at_palace(p);
            palace_info.di_gan = 0;  // 先初始化
            palace_info.tian_gan = 0;
            palace_info.ren_gan = 0;
        }
        
        if (pan.dun == Dun::Yang) {
            // 阳遁：戊从局数宫开始，按洛书顺序顺飞
            // 洛书顺序：1→8→3→4→9→2→7→6
            auto luo_shu = get_luo_shu_order();
            
            // 处理局数为5的情况，中宫寄坤2宫
            std::uint8_t start_gong = (ju == 5) ? 2 : ju;
            
            // 找到起始宫在洛书顺序中的位置
            std::size_t start_idx = 0;
            for (std::size_t i = 0; i < luo_shu.size(); ++i) {
                if (luo_shu[i] == start_gong) {
                    start_idx = i;
                    break;
                }
            }
            
            // 按洛书顺序顺飞排布地盘干
            for (std::size_t i = 0; i < 8; ++i) {
                std::size_t gong_idx = (start_idx + i) % 8;
                std::uint8_t gong_num = luo_shu[gong_idx];
                pan.palaces[gong_num - 1].di_gan = gan_seq[i];
            }
            
            // 中宫寄坤2宫
            pan.palaces[4].di_gan = pan.palaces[1].di_gan;  // 中宫(5) = 坤2宫(2)
            
        } else {
            // 阴遁：戊从局数寫开始，按九宫数字递减
            // 阴遁顺序（以阴遁2局为例）：2→1→9→8→7→6→5→4→3
            std::uint8_t current_gong = ju;
            
            for (std::size_t i = 0; i < 9; ++i) {
                pan.palaces[current_gong - 1].di_gan = gan_seq[i];
                
                // 递减，遇到0后跳到9
                current_gong--;
                if (current_gong == 0) {
                    current_gong = 9;
                }
            }
        }
    }
    
    /**
     * @brief 获取局数对应的起始宫位
     */
    static constexpr Palace get_palace_for_ju(std::uint8_t ju) noexcept {
        // 局数与起始宫位的对应关系
        // 这里简化处理，实际应根据具体的排盘规则
        switch (ju) {
            case 1: return Palace::North;
            case 2: return Palace::SouthWest;
            case 3: return Palace::East;
            case 4: return Palace::SouthEast;
            case 5: return Palace::Center;
            case 6: return Palace::NorthWest;
            case 7: return Palace::West;
            case 8: return Palace::NorthEast;
            case 9: return Palace::South;
            default: return Palace::Center;
        }
    }
    
    /**
     * @brief 确定直符和直使
     */
    static void determine_zhi_fu_and_zhi_shi(
        QiMenPan& pan,
        std::uint8_t tian_gan_day,
        std::uint8_t di_zhi_day,
        std::uint8_t tian_gan_hour,
        std::uint8_t di_zhi_hour
    ) {
        // 根据日干支确定旬首（时家奇门用日干支）
        JiaXun jia_xun = get_jia_xun_from_gan_zhi(tian_gan_day, di_zhi_day);
        
        // 获取旬首对应的六仪
        std::uint8_t liu_yi = get_liu_yi_from_jia_xun(jia_xun);
        
        // 在地盘上查找六仪的位置 = 值符宫
        std::uint8_t zhi_fu_gong = 0;
        for (std::size_t i = 0; i < 9; ++i) {
            if (pan.palaces[i].di_gan == liu_yi) {
                // 找到了旬首六仪在地盘上的位置
                zhi_fu_gong = get_number_from_palace(pan.palaces[i].palace);
                
                // 值符星 = 该宫位原位的九星
                pan.zhi_fu_star = get_star_at_palace(pan.palaces[i].palace);
                
                // 值使门 = 该宫位原位的八门
                pan.zhi_shi_gate = get_gate_at_palace(pan.palaces[i].palace);
                
                pan.zhi_fu_palace = pan.palaces[i].palace;
                break;
            }
        }
        
        // 如果没找到（理论上不应该发生），默认寄坤2宫
        if (zhi_fu_gong == 0) {
            zhi_fu_gong = 2;
            pan.zhi_fu_palace = Palace::SouthWest;
            pan.zhi_fu_star = get_star_at_palace(Palace::SouthWest);
            pan.zhi_shi_gate = get_gate_at_palace(Palace::SouthWest);
        }
    }
    
    /**
     * @brief 根据天干地支确定旬首
     * 
     * 六十甲子分六旬：
     * - 甲子旬：甲子～癸酉（10个）
     * - 甲戌旬：甲戌～癸未（10个）
     * - 甲申旬：甲申～癸己（10个）
     * - 甲午旬：甲午～癸卯（10个）
     * - 甲辰旬：甲辰～癸丑（10个）
     * - 甲寅旬：甲寅～癸亥（10个）
     */
    static constexpr JiaXun get_jia_xun_from_gan_zhi(
        std::uint8_t tian_gan,
        std::uint8_t di_zhi
    ) noexcept {
        // 计算天干地支组合在六十甲子中的位置
        // 六十甲子索引 = (tian_gan * 6 + di_zhi * 5) % 60
        // 但更简单的方法是直接用 (tian_gan + di_zhi * 10) % 60
        // 或者根据地支判断旬首
        
        // 简化算法：根据地支除以 2 的余数分组
        // 甲子旬：地支为子(酉、子，地支 0-9
        // 甲戌旬：地支为戌亥，地支 10-11
        // 但这种方法不准确
        
        // 正确的方法：根据地支判断旬首
        // 每个旬首包含 10 个干支，地支每 2 个为一组
        switch (di_zhi) {
            case 0:  // 子
            case 1:  // 丑
                return JiaXun::JiaZi;
            case 2:  // 寅
            case 3:  // 卯
                return JiaXun::JiaYin;
            case 4:  // 辰
            case 5:  // 己
                return JiaXun::JiaChen;
            case 6:  // 午
            case 7:  // 未
                return JiaXun::JiaWu;
            case 8:  // 申
            case 9:  // 酉
                return JiaXun::JiaShen;
            case 10: // 戌
            case 11: // 亥
                return JiaXun::JiaXu;
            default:
                return JiaXun::JiaZi;
        }
    }
    
    /**
     * @brief 排布天盘天干（转盘法）
     * 
     * 天盘地盘整体从值符宫转动到时干落宫
     * 阳遁顺转，阴遁逆转
     */
    static void arrange_tian_pan(QiMenPan& pan, std::uint8_t tian_gan_hour, std::uint8_t di_zhi_hour) {
        // 1. 值符宫 = 旬首六仪在地盘上的位置（已在 determine_zhi_fu_and_zhi_shi 中确定）
        std::uint8_t zhi_fu_gong = get_number_from_palace(pan.zhi_fu_palace);
        
        // 2. 时干落宫 = 时干在地盘上的位置
        std::uint8_t shi_gan_gong = 0;
        
        // 如果时干为甲，甲隐于旬首六仪之下，落宫就是值符宫
        if (tian_gan_hour == 0) {  // 甲 = 0
            shi_gan_gong = zhi_fu_gong;
        } else {
            // 在地盘上查找时干的位置
            for (std::size_t i = 0; i < 9; ++i) {
                if (pan.palaces[i].di_gan == tian_gan_hour) {
                    shi_gan_gong = get_number_from_palace(pan.palaces[i].palace);
                    break;
                }
            }
            
            // 如果没找到（中宫的情况），寄坤2宫
            if (shi_gan_gong == 0) {
                shi_gan_gong = 2;
            }
        }
        
        // 3. 计算转动步数
        auto luo_shu = get_luo_shu_order();
        
        // 找到值符宫和时干落宫在洛书顺序中的位置
        std::size_t zhi_fu_idx = 0;
        std::size_t shi_gan_idx = 0;
        
        for (std::size_t i = 0; i < luo_shu.size(); ++i) {
            if (luo_shu[i] == zhi_fu_gong) {
                zhi_fu_idx = i;
            }
            if (luo_shu[i] == shi_gan_gong) {
                shi_gan_idx = i;
            }
        }
        
        // 计算步数
        std::size_t steps;
        if (pan.dun == Dun::Yang) {
            // 阳遁顺转
            steps = (shi_gan_idx - zhi_fu_idx + 8) % 8;
        } else {
            // 阴遁逆转
            steps = (zhi_fu_idx - shi_gan_idx + 8) % 8;
        }
        
        // 4. 天盘整体转动
        // 天盘干就是地盘干整体移动
        std::array<std::uint8_t, 9> temp_tian_gan;
        
        for (std::size_t i = 0; i < 8; ++i) {
            std::uint8_t di_pan_gong = luo_shu[i];
            std::uint8_t di_pan_gan = pan.palaces[di_pan_gong - 1].di_gan;
            
            std::size_t tian_pan_idx;
            if (pan.dun == Dun::Yang) {
                // 阳遁顺转
                tian_pan_idx = (i + steps) % 8;
            } else {
                // 阴遁逆转
                tian_pan_idx = (i - steps + 8) % 8;
            }
            
            std::uint8_t tian_pan_gong = luo_shu[tian_pan_idx];
            temp_tian_gan[tian_pan_gong - 1] = di_pan_gan;
        }
        
        // 中宫天盘干与2宫相同（寄坤宫）
        temp_tian_gan[4] = temp_tian_gan[1];  // 中宫(5) = 坤2宫(2)
        
        // 应用到宫位
        for (std::size_t i = 0; i < 9; ++i) {
            pan.palaces[i].tian_gan = temp_tian_gan[i];
        }
    }
    
    /**
     * @brief 排布九星（转盘法）
     * 
     * 九星按洛书顺序从值符宫整体转动到时干落宫
     * 天禽寄坤2宫，中宫不显示九星或与坤宫同
     */
    static void arrange_jiu_xing(QiMenPan& pan, std::uint8_t tian_gan_hour) {
        // 1. 值符宫 = 旬首六仪在地盘上的位置
        std::uint8_t zhi_fu_gong = get_number_from_palace(pan.zhi_fu_palace);
        
        // 2. 时干落宫 = 时干在地盘上的位置
        std::uint8_t shi_gan_gong = 0;
        
        // 如果时干为甲，甲隐于旬首六仪之下，落宫就是值符宫
        if (tian_gan_hour == 0) {  // 甲 = 0
            shi_gan_gong = zhi_fu_gong;
        } else {
            // 在地盘上查找时干的位置
            for (std::size_t i = 0; i < 9; ++i) {
                if (pan.palaces[i].di_gan == tian_gan_hour) {
                    shi_gan_gong = get_number_from_palace(pan.palaces[i].palace);
                    break;
                }
            }
            
            // 如果没找到（中宫的情况），寄坤2宫
            if (shi_gan_gong == 0) {
                shi_gan_gong = 2;
            }
        }
        
        // 3. 计算转动步数
        auto luo_shu = get_luo_shu_order();
        
        // 找到值符宫和时干落宫在洛书顺序中的位置
        std::size_t zhi_fu_idx = 0;
        std::size_t shi_gan_idx = 0;
        
        for (std::size_t i = 0; i < luo_shu.size(); ++i) {
            if (luo_shu[i] == zhi_fu_gong) {
                zhi_fu_idx = i;
            }
            if (luo_shu[i] == shi_gan_gong) {
                shi_gan_idx = i;
            }
        }
        
        // 计算步数（九星总是顺转）
        std::size_t steps = (shi_gan_idx - zhi_fu_idx + 8) % 8;
        
        // 4. 九星整体转动
        std::array<Star, 9> temp_stars;
        
        for (std::size_t i = 0; i < 8; ++i) {
            std::uint8_t original_gong = luo_shu[i];
            Palace original_palace = get_palace_from_number(original_gong);
            Star original_star = get_star_at_palace(original_palace);
            
            // 转动后的宫位
            std::size_t new_idx = (i + steps) % 8;
            std::uint8_t new_gong = luo_shu[new_idx];
            
            temp_stars[new_gong - 1] = original_star;
        }
        
        // 天禽在中寫，中宫不显示九星（或与坤2宫同）
        temp_stars[4] = temp_stars[1];  // 中宫(5) = 坤2宫(2)
        
        // 应用到宫位
        for (std::size_t i = 0; i < 9; ++i) {
            pan.palaces[i].star = temp_stars[i];
        }
    }
    
    /**
     * @brief 排布人盘八门（转盘法）
     * 
     * 八门按洛书顺序从值符宫整体转动到时干落宫
     * 转动步数是九星的2倍
     * 阳遁顺转，阴遁逆转
     */
    static void arrange_ren_pan(QiMenPan& pan, std::uint8_t tian_gan_hour) {
        // 1. 值符宫 = 旬首六仪在地盘上的位置
        std::uint8_t zhi_fu_gong = get_number_from_palace(pan.zhi_fu_palace);
        
        // 2. 时干落宫 = 时干在地盘上的位置
        std::uint8_t shi_gan_gong = 0;
        
        // 如果时干为甲，甲隐于旬首六仪之下，落宫就是值符宫
        if (tian_gan_hour == 0) {  // 甲 = 0
            shi_gan_gong = zhi_fu_gong;
        } else {
            // 在地盘上查找时干的位置
            for (std::size_t i = 0; i < 9; ++i) {
                if (pan.palaces[i].di_gan == tian_gan_hour) {
                    shi_gan_gong = get_number_from_palace(pan.palaces[i].palace);
                    break;
                }
            }
            
            // 如果没找到（中宫的情况），寄坤2宫
            if (shi_gan_gong == 0) {
                shi_gan_gong = 2;
            }
        }
        
        // 3. 计算转动步数
        auto luo_shu = get_luo_shu_order();
        
        // 找到值符宫和时干落宫在洛书顺序中的位置
        std::size_t zhi_fu_idx = 0;
        std::size_t shi_gan_idx = 0;
        
        for (std::size_t i = 0; i < luo_shu.size(); ++i) {
            if (luo_shu[i] == zhi_fu_gong) {
                zhi_fu_idx = i;
            }
            if (luo_shu[i] == shi_gan_gong) {
                shi_gan_idx = i;
            }
        }
        
        // 计算基础步数（与九星相同）
        std::size_t base_steps = (shi_gan_idx - zhi_fu_idx + 8) % 8;
        
        // 八门转动步数是九星的2倍
        std::size_t steps = (base_steps * 2) % 8;
        
        // 4. 八门整体转动
        std::array<Gate, 9> temp_gates;
        
        for (std::size_t i = 0; i < 8; ++i) {
            std::uint8_t original_gong = luo_shu[i];
            Palace original_palace = get_palace_from_number(original_gong);
            Gate original_gate = get_gate_at_palace(original_palace);
            
            // 转动后的宫位
            std::size_t new_idx;
            if (pan.dun == Dun::Yang) {
                // 阳遁顺转
                new_idx = (i + steps) % 8;
            } else {
                // 阴遁逆转
                new_idx = (i - steps + 8) % 8;
            }
            
            std::uint8_t new_gong = luo_shu[new_idx];
            temp_gates[new_gong - 1] = original_gate;
        }
        
        // 中宫无门
        temp_gates[4] = Gate::Jing_Center;  // 中宫(5)无门
        
        // 应用到宫位
        for (std::size_t i = 0; i < 9; ++i) {
            pan.palaces[i].gate = temp_gates[i];
        }
    }
    
    /**
     * @brief 排布神盘八神
     * 
     * 八神根据直符宫和阴阳遁进行排列
     * 阳遁：从值符宫开始顺时针排列
     * 阴遁：从值符宫开始逆时针排列
     */
    static void arrange_shen_pan(QiMenPan& pan) {
        // 八神顺序：值符、腾蛇、太阴、六合、白虎、玄武、九地、九天
        std::array<Spirit, 8> spirit_seq = {
            Spirit::ZhiFu, Spirit::TengShe, Spirit::TaiYin, Spirit::LiuHe,
            Spirit::BaiHu, Spirit::XuanWu, Spirit::JiuDi, Spirit::JiuTian
        };
        
        // 获取值符宫的数字
        std::uint8_t zhi_fu_gong = get_number_from_palace(pan.zhi_fu_palace);
        
        // 根据阴阳遁选择排列方向
        std::array<std::uint8_t, 8> gong_order;
        if (pan.dun == Dun::Yang) {
            // 阳遁顺时针：1→8→3→4→9→2→7→6
            gong_order = get_luo_shu_order();
        } else {
            // 阴遁逆时针：1→6→7→2→9→4→3→8
            gong_order = get_luo_shu_reverse_order();
        }
        
        // 找到值符宫在宫位顺序中的位置
        std::size_t zhi_fu_idx = 0;
        for (std::size_t i = 0; i < gong_order.size(); ++i) {
            if (gong_order[i] == zhi_fu_gong) {
                zhi_fu_idx = i;
                break;
            }
        }
        
        // 按顺序排列八神
        std::array<Spirit, 9> temp_spirits;
        
        for (std::size_t i = 0; i < 8; ++i) {
            std::size_t gong_idx = (zhi_fu_idx + i) % 8;
            std::uint8_t gong_num = gong_order[gong_idx];
            temp_spirits[gong_num - 1] = spirit_seq[i];
        }
        
        // 中宫无神
        temp_spirits[4] = Spirit::ZhiFu;  // 中宫使用默认值
        
        // 应用到宫位
        for (std::size_t i = 0; i < 9; ++i) {
            pan.palaces[i].spirit = temp_spirits[i];
        }
    }
};

/**
 * @brief 格式化输出奇门盘
 */
[[nodiscard]] inline auto format_qi_men_pan(const QiMenPan& pan) -> std::string {
    using namespace ZhouYi::GanZhi;
    
    std::string result;
    
    result += fmt::format("奇门遁甲排盘\n");
    result += fmt::format("节气: {}\n", solar_term_name(pan.solar_term));
    result += fmt::format("阴阳遁: {}\n", pan.dun == Dun::Yang ? "阳遁" : "阴遁");
    result += fmt::format("三元: ");
    switch (pan.yuan) {
        case Yuan::Shang: result += "上元"; break;
        case Yuan::Zhong: result += "中元"; break;
        case Yuan::Xia: result += "下元"; break;
    }
    result += fmt::format("\n局数: {}\n", pan.ju);
    result += fmt::format("直符: {}\n", star_name(pan.zhi_fu_star));
    result += fmt::format("直使: {}\n", gate_name(pan.zhi_shi_gate));
    
    result += "\n══════════════════════════\n";
    result += "九宫排盘：\n";
    result += "══════════════════════════\n";
    
    // 九宫格布局：西北(6) 北(1) 东北(8)
    //             西(7)   中(5)  东(3)
    //             西南(2) 南(9) 东南(4)
    std::array<std::uint8_t, 9> gong_layout = {6, 1, 8, 7, 5, 3, 2, 9, 4};
    
    // 输出九宫格
    for (std::size_t row = 0; row < 3; ++row) {
        // 每个宫位显示5行信息
        
        // 第1行：宫名 + 九星
        for (std::size_t col = 0; col < 3; ++col) {
            std::uint8_t gong_num = gong_layout[row * 3 + col];
            const auto& info = pan.palaces[gong_num - 1];
            auto palace_str = std::string(palace_name(info.palace));
            auto star_str = std::string(star_name(info.star));
            // 宫名固定4个字符宽度，九星固定4个字符宽度
            result += fmt::format("║{:<4}{:>4}", palace_str, star_str);
        }
        result += "║\n";
        
        // 第2行：八门
        for (std::size_t col = 0; col < 3; ++col) {
            std::uint8_t gong_num = gong_layout[row * 3 + col];
            const auto& info = pan.palaces[gong_num - 1];
            auto gate_str = std::string(gate_name(info.gate));
            result += fmt::format("║ {:<7}", gate_str);
        }
        result += "║\n";
        
        // 第3行：八神
        for (std::size_t col = 0; col < 3; ++col) {
            std::uint8_t gong_num = gong_layout[row * 3 + col];
            const auto& info = pan.palaces[gong_num - 1];
            auto spirit_str = std::string(spirit_name(info.spirit));
            result += fmt::format("║ {:<7}", spirit_str);
        }
        result += "║\n";
        
        // 第4行：地盘干
        for (std::size_t col = 0; col < 3; ++col) {
            std::uint8_t gong_num = gong_layout[row * 3 + col];
            const auto& info = pan.palaces[gong_num - 1];
            auto di_gan_str = std::string(Mapper::to_zh(static_cast<TianGan>(info.di_gan)));
            result += fmt::format("║地:{:<6}", di_gan_str);
        }
        result += "║\n";
        
        // 第5行：天盘干
        for (std::size_t col = 0; col < 3; ++col) {
            std::uint8_t gong_num = gong_layout[row * 3 + col];
            const auto& info = pan.palaces[gong_num - 1];
            auto tian_gan_str = std::string(Mapper::to_zh(static_cast<TianGan>(info.tian_gan)));
            result += fmt::format("║天:{:<6}", tian_gan_str);
        }
        result += "║\n";
        
        // 行分隔线
        if (row < 2) {
            result += "╠════════╬════════╬════════╣\n";
        }
    }
    
    result += "══════════════════════════\n";
    
    return result;
}

}  // namespace ZhouYi::QiMen
