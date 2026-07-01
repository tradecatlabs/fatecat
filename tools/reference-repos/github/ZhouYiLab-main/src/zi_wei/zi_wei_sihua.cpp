// 紫微斗数四化系统模块（实现）
module ZhouYi.ZiWei.SiHua;

import ZhouYi.GanZhi;
import ZhouYi.ZiWei.Constants;
import ZhouYi.ZiWei.Star;
import fmt;
import std;
import ZhouYi.ZhMapper;

namespace ZhouYi::ZiWei {
    using namespace std;
    using namespace ZhouYi::GanZhi;
    using namespace ZhouYi::Mapper;

    // ============= 辅助函数 =============

    string SiHuaInfo::to_string() const {
        return fmt::format("{}{} -> 第{}宫",
            star_name,
            string(to_zh(type)),
            gong_index);
    }

    string GongGanSiHua::to_string() const {
        string result = fmt::format("第{}宫 [{}干] 四化：\n", gong_index, string(to_zh(gong_gan)));
        for (const auto& si_hua : si_hua_list) {
            if (!si_hua.star_name.empty()) {
                result += "  " + si_hua.to_string() + "\n";
            }
        }
        return result;
    }

    string ZiHuaInfo::to_string() const {
        string result = fmt::format("第{}宫自化：", gong_index);
        for (const auto& type : zi_hua_types) {
            result += string(to_zh(type)) + " ";
        }
        return result;
    }

    string FeiHuaRelation::to_string() const {
        return fmt::format("第{}宫[{}干] {} 飞化 -> 第{}宫",
            from_gong,
            string(to_zh(from_gan)),
            star_name + string(to_zh(si_hua_type)),
            to_gong);
    }

    string FeiHuaChain::to_string() const {
        string result = "飞化链：";
        for (size_t i = 0; i < chain.size(); ++i) {
            if (i > 0) result += "  ";
            result += fmt::format("第{}宫", chain[i].from_gong);
        }
        if (!chain.empty()) {
            result += fmt::format("  第{}宫", chain.back().to_gong);
        }
        if (is_hui_ben) {
            result += " (回本宫)";
        }
        return result;
    }

    // ============= 获取天干对应的四化星 =============

    array<optional<ZhuXing>, 4> get_si_hua_stars(TianGan gan) {
        array<optional<ZhuXing>, 4> result = {nullopt, nullopt, nullopt, nullopt};
        
        switch (gan) {
            case TianGan::Jia:
                result[0] = ZhuXing::LianZhen;  // 化禄
                result[1] = ZhuXing::PoJun;     // 化权
                result[2] = ZhuXing::WuQu;      // 化科
                result[3] = ZhuXing::TaiYang;   // 化忌
                break;
            case TianGan::Yi:
                result[0] = ZhuXing::TianJi;
                result[1] = ZhuXing::TianLiang;
                result[2] = ZhuXing::ZiWei;
                result[3] = ZhuXing::TaiYin;
                break;
            case TianGan::Bing:
                result[0] = ZhuXing::TianTong;
                result[1] = ZhuXing::TianJi;
                result[3] = ZhuXing::LianZhen;
                break;
            case TianGan::Ding:
                result[0] = ZhuXing::TaiYin;
                result[1] = ZhuXing::TianTong;
                result[2] = ZhuXing::TianJi;
                result[3] = ZhuXing::JuMen;
                break;
            case TianGan::Wu:
                result[0] = ZhuXing::TanLang;
                result[1] = ZhuXing::TaiYin;
                result[3] = ZhuXing::TianJi;
                break;
            case TianGan::Ji:
                result[0] = ZhuXing::WuQu;
                result[1] = ZhuXing::TanLang;
                result[2] = ZhuXing::TianLiang;
                break;
            case TianGan::Geng:
                result[0] = ZhuXing::TaiYang;
                result[1] = ZhuXing::WuQu;
                result[2] = ZhuXing::TaiYin;
                result[3] = ZhuXing::TianTong;
                break;
            case TianGan::Xin:
                result[0] = ZhuXing::JuMen;
                result[1] = ZhuXing::TaiYang;
                break;
            case TianGan::Ren:
                result[0] = ZhuXing::TianLiang;
                result[1] = ZhuXing::ZiWei;
                result[3] = ZhuXing::WuQu;
                break;
            case TianGan::Gui:
                result[0] = ZhuXing::PoJun;
                result[1] = ZhuXing::JuMen;
                result[2] = ZhuXing::TaiYin;
                result[3] = ZhuXing::TanLang;
                break;
        }
        
        return result;
    }

    optional<SiHua> get_star_si_hua_type(TianGan gan, ZhuXing star) {
        auto si_hua_stars = get_si_hua_stars(gan);
        
        for (size_t i = 0; i < 4; ++i) {
            if (si_hua_stars[i].has_value() && si_hua_stars[i].value() == star) {
                return static_cast<SiHua>(i);  // 0=禄, 1=权, 2=科, 3=忌
            }
        }
        
        return nullopt;
    }

    // ============= SiHuaSystem 实现 =============

    SiHuaSystem::SiHuaSystem(
        const array<pair<TianGan, DiZhi>, 12>& gong_gan_zhi,
        const array<vector<string>, 12>& stars_in_gong
    ) : stars_in_gong_(stars_in_gong) {
        calculate_gong_gan_si_hua(gong_gan_zhi);
    }

    void SiHuaSystem::calculate_gong_gan_si_hua(
        const array<pair<TianGan, DiZhi>, 12>& gong_gan_zhi
    ) {
        for (int i = 0; i < 12; ++i) {
            auto [gan, zhi] = gong_gan_zhi[i];
            gong_gan_si_hua_[i].gong_index = i;
            gong_gan_si_hua_[i].gong_gan = gan;
            
            // 获取该天干的四化星
            auto si_hua_stars = get_si_hua_stars(gan);
            
            // 查找四化星所在的宫位
            for (int si_hua_idx = 0; si_hua_idx < 4; ++si_hua_idx) {
                if (!si_hua_stars[si_hua_idx].has_value()) {
                    gong_gan_si_hua_[i].si_hua_list[si_hua_idx] = SiHuaInfo{
                        .type = static_cast<SiHua>(si_hua_idx),
                        .star_name = "",
                        .gong_index = -1
                    };
                    continue;
                }
                
                auto star = si_hua_stars[si_hua_idx].value();
                string star_name = string(to_zh(star));
                
                // 在12个宫位中查找该星
                int star_gong = -1;
                for (int j = 0; j < 12; ++j) {
                    if (find(stars_in_gong_[j].begin(), stars_in_gong_[j].end(), star_name) 
                        != stars_in_gong_[j].end()) {
                        star_gong = j;
                        break;
                    }
                }
                
                gong_gan_si_hua_[i].si_hua_list[si_hua_idx] = SiHuaInfo{
                    .type = static_cast<SiHua>(si_hua_idx),
                    .star_name = star_name,
                    .gong_index = star_gong
                };
            }
        }
    }

    bool SiHuaSystem::has_zi_hua(int gong_index) const {
        gong_index = fix_index(gong_index);
        const auto& gong_si_hua = gong_gan_si_hua_[gong_index];
        
        for (const auto& si_hua : gong_si_hua.si_hua_list) {
            if (si_hua.gong_index == gong_index && !si_hua.star_name.empty()) {
                return true;  // 化星在本宫，即为自化
            }
        }
        
        return false;
    }

    bool SiHuaSystem::has_zi_hua_type(int gong_index, SiHua type) const {
        gong_index = fix_index(gong_index);
        const auto& gong_si_hua = gong_gan_si_hua_[gong_index];
        
        for (const auto& si_hua : gong_si_hua.si_hua_list) {
            if (si_hua.type == type && 
                si_hua.gong_index == gong_index && 
                !si_hua.star_name.empty()) {
                return true;
            }
        }
        
        return false;
    }

    vector<ZiHuaInfo> SiHuaSystem::get_all_zi_hua() const {
        vector<ZiHuaInfo> result;
        
        for (int i = 0; i < 12; ++i) {
            ZiHuaInfo zi_hua_info{.gong_index = i, .zi_hua_types = {}};
            
            const auto& gong_si_hua = gong_gan_si_hua_[i];
            for (const auto& si_hua : gong_si_hua.si_hua_list) {
                if (si_hua.gong_index == i && !si_hua.star_name.empty()) {
                    zi_hua_info.zi_hua_types.push_back(si_hua.type);
                }
            }
            
            if (!zi_hua_info.zi_hua_types.empty()) {
                result.push_back(zi_hua_info);
            }
        }
        
        return result;
    }

    bool SiHuaSystem::flies_to(int from_gong, int to_gong, SiHua si_hua_type) const {
        from_gong = fix_index(from_gong);
        to_gong = fix_index(to_gong);
        
        const auto& gong_si_hua = gong_gan_si_hua_[from_gong];
        
        for (const auto& si_hua : gong_si_hua.si_hua_list) {
            if (si_hua.type == si_hua_type && si_hua.gong_index == to_gong) {
                return true;
            }
        }
        
        return false;
    }

    vector<FeiHuaRelation> SiHuaSystem::get_fei_hua_from(int gong_index) const {
        vector<FeiHuaRelation> result;
        gong_index = fix_index(gong_index);
        
        const auto& gong_si_hua = gong_gan_si_hua_[gong_index];
        
        for (const auto& si_hua : gong_si_hua.si_hua_list) {
            if (si_hua.gong_index >= 0 && !si_hua.star_name.empty()) {
                result.push_back(FeiHuaRelation{
                    .from_gong = gong_index,
                    .from_gan = gong_si_hua.gong_gan,
                    .to_gong = si_hua.gong_index,
                    .si_hua_type = si_hua.type,
                    .star_name = si_hua.star_name
                });
            }
        }
        
        return result;
    }

    vector<FeiHuaRelation> SiHuaSystem::get_fei_hua_to(int gong_index) const {
        vector<FeiHuaRelation> result;
        gong_index = fix_index(gong_index);
        
        for (int i = 0; i < 12; ++i) {
            const auto& gong_si_hua = gong_gan_si_hua_[i];
            
            for (const auto& si_hua : gong_si_hua.si_hua_list) {
                if (si_hua.gong_index == gong_index && !si_hua.star_name.empty()) {
                    result.push_back(FeiHuaRelation{
                        .from_gong = i,
                        .from_gan = gong_si_hua.gong_gan,
                        .to_gong = gong_index,
                        .si_hua_type = si_hua.type,
                        .star_name = si_hua.star_name
                    });
                }
            }
        }
        
        return result;
    }

    vector<FeiHuaChain> SiHuaSystem::get_fei_hua_chains(
        int start_gong,
        SiHua si_hua_type,
        int max_depth
    ) const {
        vector<FeiHuaChain> result;
        vector<FeiHuaRelation> current_chain;
        set<int> visited;
        
        max_depth = min(max_depth, 4);  // 最多4层
        
        find_chains_recursive(start_gong, si_hua_type, 0, max_depth, current_chain, visited, result);
        
        return result;
    }

    void SiHuaSystem::find_chains_recursive(
        int current_gong,
        SiHua si_hua_type,
        int current_depth,
        int max_depth,
        vector<FeiHuaRelation>& current_chain,
        set<int>& visited,
        vector<FeiHuaChain>& result
    ) const {
        if (current_depth >= max_depth) {
            return;
        }
        
        const auto& gong_si_hua = gong_gan_si_hua_[current_gong];
        
        // 查找指定类型的四化
        for (const auto& si_hua : gong_si_hua.si_hua_list) {
            if (si_hua.type == si_hua_type && si_hua.gong_index >= 0 && !si_hua.star_name.empty()) {
                FeiHuaRelation relation{
                    .from_gong = current_gong,
                    .from_gan = gong_si_hua.gong_gan,
                    .to_gong = si_hua.gong_index,
                    .si_hua_type = si_hua_type,
                    .star_name = si_hua.star_name
                };
                
                current_chain.push_back(relation);
                
                // 检查是否回到起始宫
                bool is_hui_ben = false;
                if (!current_chain.empty() && si_hua.gong_index == current_chain[0].from_gong) {
                    is_hui_ben = true;
                }
                
                // 保存当前链
                result.push_back(FeiHuaChain{
                    .chain = current_chain,
                    .is_hui_ben = is_hui_ben
                });
                
                // 如果没有回本宫且没有访问过，继续递归
                if (!is_hui_ben && visited.find(si_hua.gong_index) == visited.end()) {
                    visited.insert(si_hua.gong_index);
                    find_chains_recursive(si_hua.gong_index, si_hua_type, current_depth + 1, 
                                         max_depth, current_chain, visited, result);
                    visited.erase(si_hua.gong_index);
                }
                
                current_chain.pop_back();
            }
        }
    }

    vector<FeiHuaChain> SiHuaSystem::find_hui_ben_chains(int start_gong) const {
        vector<FeiHuaChain> all_chains;
        
        // 对每种四化类型查找回本宫的链
        for (int i = 0; i < 4; ++i) {
            auto chains = get_fei_hua_chains(start_gong, static_cast<SiHua>(i), 4);
            for (const auto& chain : chains) {
                if (chain.is_hui_ben) {
                    all_chains.push_back(chain);
                }
            }
        }
        
        return all_chains;
    }

} // namespace ZhouYi::ZiWei

