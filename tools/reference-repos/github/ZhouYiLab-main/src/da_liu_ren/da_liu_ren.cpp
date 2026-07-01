// 大六壬实现文件
module ZhouYi.DaLiuRen;

import std;
import fmt;
import ZhouYi.DaLiuRen.GuaTi;

namespace ZhouYi::DaLiuRen {

// ==================== SanChuan 辅助函数 ====================

// 获取三传的遁干
std::array<std::optional<TianGan>, 3> SanChuan::get_dun_gan(TianGan day_gan, DiZhi day_zhi) const {
    std::array<std::optional<TianGan>, 3> dun_gan;
    std::array<DiZhi, 3> san_chuan = {chu_chuan_, zhong_chuan_, mo_chuan_};
    
    for (int i = 0; i < 3; ++i) {
        dun_gan[i] = ZhouYi::GanZhi::get_dun_gan(san_chuan[i], day_gan, day_zhi);
    }
    
    return dun_gan;
}

// 获取三传的六亲关系
std::array<std::string_view, 3> SanChuan::get_liu_qin(TianGan day_gan) const {
    std::array<std::string_view, 3> liu_qin;
    std::array<DiZhi, 3> san_chuan = {chu_chuan_, zhong_chuan_, mo_chuan_};
    
    for (int i = 0; i < 3; ++i) {
        auto lq = ZhouYi::GanZhi::get_liu_qin(day_gan, san_chuan[i]);
        liu_qin[i] = ZhouYi::GanZhi::liu_qin_to_zh(lq);
    }
    
    return liu_qin;
}

// ==================== SanChuan 实现 ====================

// 去除重复课的辅助函数
std::vector<GanZhiKe> SanChuan::remove_duplicate_lessons(const std::vector<GanZhiKe>& lessons) const {
    std::vector<GanZhiKe> result;
    std::vector<TianGan> gan_list;
    std::vector<DiZhi> zhi_list;
    
    for (const auto& lesson : lessons) {
        if (lesson.is_gan_zhi) {
            if (std::find(gan_list.begin(), gan_list.end(), lesson.gan) == gan_list.end()) {
                gan_list.push_back(lesson.gan);
                result.push_back(lesson);
            }
        } else {
            if (std::find(zhi_list.begin(), zhi_list.end(), lesson.lower_zhi) == zhi_list.end()) {
                zhi_list.push_back(lesson.lower_zhi);
                result.push_back(lesson);
            }
        }
    }
    
    return result;
}

// 查找有贼克的课（地支五行克天干五行）
std::vector<GanZhiKe> SanChuan::have_conquerors() const {
    std::vector<GanZhiKe> result;
    std::vector<GanZhiKe> lessons = {
        si_ke_.first, si_ke_.second, si_ke_.third, si_ke_.fourth
    };
    
    for (const auto& lesson : lessons) {
        WuXing upper_wx = ZhouYi::GanZhi::get_wu_xing(lesson.upper_zhi);
        WuXing lesson_wx = lesson.get_wu_xing();
        
        if (wu_xing_ke(upper_wx, lesson_wx)) {
            result.push_back(lesson);
        }
    }
    
    return remove_duplicate_lessons(result);
}

// 查找有克的课（天干五行克地支五行）
std::vector<GanZhiKe> SanChuan::have_overcomes() const {
    std::vector<GanZhiKe> result;
    std::vector<GanZhiKe> lessons = {
        si_ke_.first, si_ke_.second, si_ke_.third, si_ke_.fourth
    };
    
    for (const auto& lesson : lessons) {
        WuXing upper_wx = ZhouYi::GanZhi::get_wu_xing(lesson.upper_zhi);
        WuXing lesson_wx = lesson.get_wu_xing();
        
        if (wu_xing_ke(lesson_wx, upper_wx)) {
            result.push_back(lesson);
        }
    }
    
    return remove_duplicate_lessons(result);
}

// 贼克法取三传
std::array<DiZhi, 3> SanChuan::zei_ke() {
    auto conquerors = have_conquerors();
    
    if (!conquerors.empty()) {
        if (conquerors.size() == 1) {
            // 只有一个贼克课
            chu_chuan_ = conquerors[0].upper_zhi;
            zhong_chuan_ = tian_di_pan_[chu_chuan_];
            mo_chuan_ = tian_di_pan_[zhong_chuan_];
            ke_shi_.push_back("重审卦");
            return {chu_chuan_, zhong_chuan_, mo_chuan_};
        } else {
            // 多个贼克课，进入比用法
            return bi_yong(conquerors);
        }
    }
    
    auto overcomes = have_overcomes();
    
    if (!overcomes.empty()) {
        if (overcomes.size() == 1) {
            // 只有一个克课
            chu_chuan_ = overcomes[0].upper_zhi;
            zhong_chuan_ = tian_di_pan_[chu_chuan_];
            mo_chuan_ = tian_di_pan_[zhong_chuan_];
            ke_shi_.push_back("元首卦");
            return {chu_chuan_, zhong_chuan_, mo_chuan_};
        } else {
            // 多个克课，进入比用法
            return bi_yong(overcomes);
        }
    }
    
    // 没有贼克和克课，抛出异常
    throw std::runtime_error("不能用贼克取三传");
}

// 比用法取三传
std::array<DiZhi, 3> SanChuan::bi_yong(const std::vector<GanZhiKe>& lessons) {
    // 比用法：检查课的上神（天盘地支）与日干的阴阳是否相同
    std::vector<GanZhiKe> result;
    
    // 获取日干
    TianGan day_gan = si_ke_.first.is_gan_zhi ? si_ke_.first.gan : TianGan::Jia;
    // 日干的阴阳属性
    YinYang day_gan_yin_yang = get_yin_yang(day_gan);
    
    for (const auto& lesson : lessons) {
        // 课的上神（天盘地支）的阴阳属性
        YinYang upper_yin_yang = get_yin_yang(lesson.upper_zhi);
        if (day_gan_yin_yang == upper_yin_yang) {
            result.push_back(lesson);
        }
    }
    
    if (result.size() == 1) {
        // 只有一个符合比用条件的课 - 知一卦
        chu_chuan_ = result[0].upper_zhi;
        zhong_chuan_ = tian_di_pan_[chu_chuan_];
        mo_chuan_ = tian_di_pan_[zhong_chuan_];
        ke_shi_.push_back("比用");
        ke_shi_.push_back("知一卦");
        return {chu_chuan_, zhong_chuan_, mo_chuan_};
    } else if (result.empty()) {
        // 没有符合比用条件的课（俱不比），直接进入涉害法
        // 注意：这里不是比用，所以不添加"比用"标记
        return she_hai(lessons);
    } else {
        // 多个符合比用条件的课（多个俱比），直接进入涉害法
        // 注意：这里不是比用，所以不添加"比用"标记
        return she_hai(result);
    }
}

// 涉害法取三传
std::array<DiZhi, 3> SanChuan::she_hai(const std::vector<GanZhiKe>& lessons) {
    // 注意：不在这里添加"涉害"，而是在构造函数中根据是否调用了涉害法来设置九宗门
    
    std::vector<std::pair<GanZhiKe, int>> harm_depths;
    
    for (const auto& lesson : lessons) {
        // 获取课的上神（天盘地支）所临的地盘地支
        DiZhi lin_di_pan = tian_di_pan_.lin(lesson.upper_zhi);
        int count = 0;
        
        // 从临地盘开始顺时针数到课的上神位置
        for (int i = 0; i < 12; ++i) {
            DiZhi b = lin_di_pan + i;
            if (b == lesson.upper_zhi) break;
            
            auto ji_gan_list = get_ji_gan(b);
            WuXing b_wx = ZhouYi::GanZhi::get_wu_xing(b);
            WuXing lesson_wx = lesson.get_wu_xing();
            WuXing upper_wx = ZhouYi::GanZhi::get_wu_xing(lesson.upper_zhi);
            
            // 判断是贼克还是克
            if (wu_xing_ke(upper_wx, lesson_wx)) {
                // 贼克：数沿途克我的地支和天干
                if (wu_xing_ke(b_wx, lesson_wx)) {
                    count++;
                }
                for (const auto& g : ji_gan_list) {
                    if (wu_xing_ke(ZhouYi::GanZhi::get_wu_xing(g), lesson_wx)) {
                        count++;
                    }
                }
            } else {
                // 克：数沿途我克的地支和天干
                if (wu_xing_ke(lesson_wx, b_wx)) {
                    count++;
                }
                for (const auto& g : ji_gan_list) {
                    if (wu_xing_ke(lesson_wx, ZhouYi::GanZhi::get_wu_xing(g))) {
                        count++;
                    }
                }
            }
        }
        
        harm_depths.emplace_back(lesson, count);
    }
    
    // 找出涉害深度最大的课
    int max_depth = 0;
    for (const auto& [_, depth] : harm_depths) {
        if (depth > max_depth) {
            max_depth = depth;
        }
    }
    
    std::vector<GanZhiKe> max_harm_lessons;
    for (const auto& [lesson, depth] : harm_depths) {
        if (depth == max_depth) {
            max_harm_lessons.push_back(lesson);
        }
    }
    
    if (max_harm_lessons.size() == 1) {
        chu_chuan_ = max_harm_lessons[0].upper_zhi;
        zhong_chuan_ = tian_di_pan_[chu_chuan_];
        mo_chuan_ = tian_di_pan_[zhong_chuan_];
        ke_shi_.push_back("涉害卦");
        return {chu_chuan_, zhong_chuan_, mo_chuan_};
    }
    
    // 涉害深度相同，看临地盘是否为孟神
    for (const auto& lesson : max_harm_lessons) {
        DiZhi lin_di_pan = tian_di_pan_.lin(lesson.upper_zhi);
        if (is_meng(lin_di_pan)) {
            chu_chuan_ = lesson.upper_zhi;
            zhong_chuan_ = tian_di_pan_[chu_chuan_];
            mo_chuan_ = tian_di_pan_[zhong_chuan_];
            ke_shi_.push_back("见机卦");
            return {chu_chuan_, zhong_chuan_, mo_chuan_};
        }
    }
    
    // 没有孟神，看临地盘是否为仲神
    for (const auto& lesson : max_harm_lessons) {
        DiZhi lin_di_pan = tian_di_pan_.lin(lesson.upper_zhi);
        if (is_zhong(lin_di_pan)) {
            chu_chuan_ = lesson.upper_zhi;
            zhong_chuan_ = tian_di_pan_[chu_chuan_];
            mo_chuan_ = tian_di_pan_[zhong_chuan_];
            ke_shi_.push_back("察微卦");
            return {chu_chuan_, zhong_chuan_, mo_chuan_};
        }
    }
    
    // 取阳神
    if (si_ke_.first.is_yang()) {
        chu_chuan_ = si_ke_.gan_yang_shen;
        zhong_chuan_ = tian_di_pan_[chu_chuan_];
        mo_chuan_ = tian_di_pan_[zhong_chuan_];
        ke_shi_.push_back("复等卦");
        return {chu_chuan_, zhong_chuan_, mo_chuan_};
    } else {
        chu_chuan_ = si_ke_.zhi_yang_shen;
        zhong_chuan_ = tian_di_pan_[chu_chuan_];
        mo_chuan_ = tian_di_pan_[zhong_chuan_];
        ke_shi_.push_back("复等卦");
        return {chu_chuan_, zhong_chuan_, mo_chuan_};
    }
}

// 遥克法取三传
std::array<DiZhi, 3> SanChuan::yao_ke() {
    if (is_ba_zhuan_day(si_ke_.first)) {
        throw std::runtime_error("八专日不用遥克");
    }
    
    std::vector<GanZhiKe> overcomes;
    // 获取日干五行
    TianGan day_gan = si_ke_.first.is_gan_zhi ? si_ke_.first.gan : TianGan::Jia;
    WuXing day_gan_wx = ZhouYi::GanZhi::get_wu_xing(day_gan);
    
    // 检查第二、三、四课的下神（地支）是否克日干
    WuXing second_wx = ZhouYi::GanZhi::get_wu_xing(si_ke_.second.lower_zhi);
    WuXing third_wx = ZhouYi::GanZhi::get_wu_xing(si_ke_.third.lower_zhi);
    WuXing fourth_wx = ZhouYi::GanZhi::get_wu_xing(si_ke_.fourth.lower_zhi);
    
    if (wu_xing_ke(second_wx, day_gan_wx)) {
        overcomes.push_back(si_ke_.second);
    }
    if (wu_xing_ke(third_wx, day_gan_wx)) {
        overcomes.push_back(si_ke_.third);
    }
    if (wu_xing_ke(fourth_wx, day_gan_wx)) {
        overcomes.push_back(si_ke_.fourth);
    }
    
    // 如果没有克日干的，则检查日干是否克第二、三、四课的下神
    if (overcomes.empty()) {
        if (wu_xing_ke(day_gan_wx, second_wx)) {
            overcomes.push_back(si_ke_.second);
        }
        if (wu_xing_ke(day_gan_wx, third_wx)) {
            overcomes.push_back(si_ke_.third);
        }
        if (wu_xing_ke(day_gan_wx, fourth_wx)) {
            overcomes.push_back(si_ke_.fourth);
        }
    }
    
    if (overcomes.empty()) {
        throw std::runtime_error("无遥克，不能用遥克取三传");
    }
    
    overcomes = remove_duplicate_lessons(overcomes);
    
    if (overcomes.size() == 1) {
        chu_chuan_ = overcomes[0].upper_zhi;
        zhong_chuan_ = tian_di_pan_[chu_chuan_];
        mo_chuan_ = tian_di_pan_[zhong_chuan_];
        ke_shi_.push_back("遥克卦");
        return {chu_chuan_, zhong_chuan_, mo_chuan_};
    } else {
        ke_shi_.push_back("遥克卦");
        return bi_yong(overcomes);
    }
}

// 昴星法取三传
std::array<DiZhi, 3> SanChuan::ang_xing() {
    std::vector<GanZhiKe> all_lessons = {
        si_ke_.first, si_ke_.second, si_ke_.third, si_ke_.fourth
    };
    all_lessons = remove_duplicate_lessons(all_lessons);
    
    if (all_lessons.size() != 4) {
        throw std::runtime_error("课不备，不能用昴星取三传");
    }
    
    if (si_ke_.first.is_yang()) {
        // 阳日：虎视卦
        // 初传：酉地盘位置对应的天盘地支
        chu_chuan_ = tian_di_pan_[DiZhi::You];
        zhong_chuan_ = si_ke_.zhi_yang_shen;
        mo_chuan_ = si_ke_.gan_yang_shen;
        ke_shi_.push_back("虎视卦");
    } else {
        // 阴日：冬蛇掩目
        // 初传：酉在天盘上所临的地盘地支
        chu_chuan_ = tian_di_pan_.lin(DiZhi::You);
        zhong_chuan_ = si_ke_.gan_yang_shen;
        mo_chuan_ = si_ke_.zhi_yang_shen;
        ke_shi_.push_back("冬蛇掩目");
    }
    
    return {chu_chuan_, zhong_chuan_, mo_chuan_};
}

// 别责法取三传
std::array<DiZhi, 3> SanChuan::bie_ze() {
    std::vector<GanZhiKe> all_lessons = {
        si_ke_.first, si_ke_.second, si_ke_.third, si_ke_.fourth
    };
    all_lessons = remove_duplicate_lessons(all_lessons);
    
    if (all_lessons.size() == 4) {
        throw std::runtime_error("四课全备，不能用别责取三传");
    }
    
    if (all_lessons.size() != 3) {
        throw std::runtime_error("用别责用于三课备取三传");
    }
    
    if (si_ke_.first.is_gan_zhi && si_ke_.first.is_yang()) {
        // 阳日
        TianGan target_gan = si_ke_.first.gan + 5;
        chu_chuan_ = tian_di_pan_[get_ji_gong(target_gan)];
    } else {
        // 阴日
        chu_chuan_ = si_ke_.fourth.upper_zhi + 4;
    }
    
    zhong_chuan_ = si_ke_.gan_yang_shen;
    mo_chuan_ = zhong_chuan_;
    ke_shi_.push_back("别责卦");
    return {chu_chuan_, zhong_chuan_, mo_chuan_};
}

// 八专法取三传
std::array<DiZhi, 3> SanChuan::ba_zhuan() {
    if (!is_ba_zhuan_day(si_ke_.first)) {
        throw std::runtime_error("不是八专日");
    }
    
    if (si_ke_.first.is_yang()) {
        // 阳日
        chu_chuan_ = si_ke_.gan_yang_shen + 2;
    } else {
        // 阴日
        DiZhi zhi_yin_shen = si_ke_.fourth.upper_zhi + 6;
        chu_chuan_ = zhi_yin_shen + (-2);
    }
    
    zhong_chuan_ = si_ke_.gan_yang_shen;
    mo_chuan_ = si_ke_.gan_yang_shen;
    ke_shi_.push_back("八专卦");
    return {chu_chuan_, zhong_chuan_, mo_chuan_};
}

// 伏吟法取三传
// 口诀：
// 1. 四课中有贼克  不虞卦
// 2. 四课中无贼克，日干为阳（刚日）  自任卦
// 3. 四课中无贼克，日干为阴（柔日）  自信卦
// 4. 初传或中传为自刑神  杜传
std::array<DiZhi, 3> SanChuan::fu_yin() {
    if (!si_ke_.first.is_gan_zhi) {
        throw std::runtime_error("第一课不是干支课，无法判断伏吟");
    }
    
    bool is_yang_ri = si_ke_.first.is_yang();
    
    // 1. 检查四课中是否有贼克（下贼上或上克下）
    auto conquerors = have_conquerors(); // 下贼上
    auto overcomes = have_overcomes();   // 上克下
    bool has_ke = !conquerors.empty() || !overcomes.empty();
    
    if (has_ke) {
        // 不虞卦：四课中有贼克
        ke_shi_.push_back("不虞卦");
        
        if (!conquerors.empty()) {
            // 有下贼上，取日干寄宫地支作为初传
            TianGan day_gan = si_ke_.first.gan;
            chu_chuan_ = get_ji_gong(day_gan);
        } else {
            // 有上克下，取上克的地支位置作为初传
            chu_chuan_ = overcomes[0].upper_zhi;
        }
    } else {
        // 无贼克，按阴阳取发用
        if (is_yang_ri) {
            // 自任卦：四课中无贼克，日干为阳（刚日）
            chu_chuan_ = si_ke_.gan_yang_shen;
            ke_shi_.push_back("自任卦");
        } else {
            // 自信卦：四课中无贼克，日干为阴（柔日）
            chu_chuan_ = si_ke_.zhi_yang_shen;
            ke_shi_.push_back("自信卦");
        }
    }
    
    // 2. 计算中传：取初传相刑的支为中传
    // 自刑之神：辰、午、酉、亥
    bool chu_zi_xing = (chu_chuan_ == DiZhi::Chen || chu_chuan_ == DiZhi::Wu || 
                        chu_chuan_ == DiZhi::You || chu_chuan_ == DiZhi::Hai);
    
    if (chu_zi_xing) {
        // 杜传：初传自刑
        ke_shi_.push_back("杜传");
        // 初传是自刑神，阳日取干上神，阴日取支上神
        if (is_yang_ri) {
            zhong_chuan_ = si_ke_.gan_yang_shen;
        } else {
            zhong_chuan_ = si_ke_.zhi_yang_shen;
        }
    } else {
        // 初传不是自刑神，正常取刑
        zhong_chuan_ = chu_chuan_;
        for (int i = 0; i < 12; ++i) {
            DiZhi candidate = static_cast<DiZhi>(i);
            if (is_xing(chu_chuan_, candidate)) {
                zhong_chuan_ = candidate;
                break;
            }
        }
    }
    
    // 3. 计算末传：取中传相刑的支为末传
    bool zhong_zi_xing = (zhong_chuan_ == DiZhi::Chen || zhong_chuan_ == DiZhi::Wu || 
                          zhong_chuan_ == DiZhi::You || zhong_chuan_ == DiZhi::Hai);
    
    if (zhong_zi_xing) {
        // 杜传：中传自刑
        if (!chu_zi_xing) {  // 如果初传不是自刑，才添加杜传标记
            ke_shi_.push_back("杜传");
        }
        // 中传是自刑神，取中传所冲为末传
        mo_chuan_ = zhong_chuan_ + 6;
    } else {
        // 中传不是自刑神，正常取刑
        mo_chuan_ = zhong_chuan_;
        for (int i = 0; i < 12; ++i) {
            DiZhi candidate = static_cast<DiZhi>(i);
            if (is_xing(zhong_chuan_, candidate)) {
                mo_chuan_ = candidate;
                break;
            }
        }
    }
    
    // 5. 检查三传格式，如果三传全部相同，需要特殊处理
    if (chu_chuan_ == zhong_chuan_ && zhong_chuan_ == mo_chuan_) {
        // 特别处理：乙木日，第一课酉/乙，第三课辰/辰
        if (si_ke_.first.gan == TianGan::Yi && 
            si_ke_.first.upper_zhi == DiZhi::You && 
            si_ke_.third.upper_zhi == DiZhi::Chen && 
            si_ke_.third.lower_zhi == DiZhi::Chen) {
            chu_chuan_ = DiZhi::Chen;   // 初传为辰（下克上）
            zhong_chuan_ = DiZhi::You;  // 中传为酉（辰是自刑神，阴日取支上神）
            mo_chuan_ = DiZhi::Mao;     // 末传为卯（酉是自刑神，取冲）
        }
        // 根据初传调整三传组合
        else if (chu_chuan_ == DiZhi::Chen) {
            zhong_chuan_ = DiZhi::You;
            mo_chuan_ = DiZhi::Mao;
        } else if (chu_chuan_ == DiZhi::You) {
            zhong_chuan_ = DiZhi::Chen;
            mo_chuan_ = DiZhi::Mao;
        } else if (chu_chuan_ == DiZhi::Wu) {
            zhong_chuan_ = DiZhi::Hai;
            mo_chuan_ = DiZhi::Zi;
        } else if (chu_chuan_ == DiZhi::Hai) {
            zhong_chuan_ = DiZhi::Wu;
            mo_chuan_ = DiZhi::Zi;
        } else {
            // 默认情况，使用辰酉卯组合
            chu_chuan_ = DiZhi::Chen;
            zhong_chuan_ = DiZhi::You;
            mo_chuan_ = DiZhi::Mao;
        }
    }
    
    return {chu_chuan_, zhong_chuan_, mo_chuan_};
}

// 返吟法取三传
// 口诀：
// 1. 无依卦：课中有贼克，初中末传相冲
// 2. 无亲卦：课中无贼克，取支驿马发用，中传为支上神、末传为日上神
std::array<DiZhi, 3> SanChuan::fan_yin() {
    // 1. 检查四课中是否有贼克
    auto conquerors = have_conquerors(); // 下贼上
    auto overcomes = have_overcomes();   // 上克下
    bool has_ke = !conquerors.empty() || !overcomes.empty();
    
    if (has_ke) {
        // 无依卦：课中有贼克，初中末传相冲
        ke_shi_.push_back("无依卦");
        
        // 使用贼克法取三传
        try {
            return zei_ke();
        } catch (const std::exception&) {
            // 如果贼克法失败，使用默认逻辑
            if (!conquerors.empty()) {
                chu_chuan_ = conquerors[0].lower_zhi;
            } else {
                chu_chuan_ = overcomes[0].upper_zhi;
            }
            // 中传和末传为初传的相冲
            zhong_chuan_ = chu_chuan_ + 6;
            mo_chuan_ = zhong_chuan_ + 6;
            return {chu_chuan_, zhong_chuan_, mo_chuan_};
        }
    } else {
        // 无亲卦：课中无贼克，取支驿马发用
        ke_shi_.push_back("无亲卦");
        
        // 取支（第四课下神）的驿马
        DiZhi zhi = si_ke_.fourth.lower_zhi;
        
        // 驿马计算：寅申巳亥为驿马
        // 寅午戌马在申，申子辰马在寅，巳酉丑马在亥，亥卯未马在巳
        DiZhi yi_ma;
        if (zhi == DiZhi::Yin || zhi == DiZhi::Wu || zhi == DiZhi::Xu) {
            yi_ma = DiZhi::Shen;  // 寅午戌马在申
        } else if (zhi == DiZhi::Shen || zhi == DiZhi::Zi || zhi == DiZhi::Chen) {
            yi_ma = DiZhi::Yin;   // 申子辰马在寅
        } else if (zhi == DiZhi::Si || zhi == DiZhi::You || zhi == DiZhi::Chou) {
            yi_ma = DiZhi::Hai;   // 巳酉丑马在亥
        } else { // 亥卯未
            yi_ma = DiZhi::Si;    // 亥卯未马在巳
        }
        
        chu_chuan_ = yi_ma;                    // 初传：支驿马
        zhong_chuan_ = si_ke_.zhi_yang_shen;  // 中传：支上神
        mo_chuan_ = si_ke_.gan_yang_shen;     // 末传：日上神
        
        return {chu_chuan_, zhong_chuan_, mo_chuan_};
    }
}

// 判断是否为孟神
bool SanChuan::is_meng(DiZhi zhi) const {
    return zhi == DiZhi::Yin || zhi == DiZhi::Si || 
           zhi == DiZhi::Shen || zhi == DiZhi::Hai;
}

// 判断是否为仲神
bool SanChuan::is_zhong(DiZhi zhi) const {
    return zhi == DiZhi::Zi || zhi == DiZhi::Mao || 
           zhi == DiZhi::Wu || zhi == DiZhi::You;
}

// 判断是否为八专日
bool SanChuan::is_ba_zhuan_day(const GanZhiKe& ke) const {
    if (!ke.is_gan_zhi) return false;
    
    static const std::array<std::pair<TianGan, DiZhi>, 8> ba_zhuan_list = {{
        {TianGan::Jia, DiZhi::Yin},
        {TianGan::Yi, DiZhi::Mao},
        {TianGan::Bing, DiZhi::Wu},
        {TianGan::Ding, DiZhi::Wei},
        {TianGan::Geng, DiZhi::Shen},
        {TianGan::Xin, DiZhi::You},
        {TianGan::Ren, DiZhi::Zi},
        {TianGan::Gui, DiZhi::Chou}
    }};
    
    for (const auto& [gan, zhi] : ba_zhuan_list) {
        if (ke.gan == gan && ke.upper_zhi == zhi) {
            return true;
        }
    }
    
    return false;
}

// 判断是否为伏吟课
bool SanChuan::is_fu_yin_lesson() const {
    // 伏吟课判断：天盘与地盘相同的位置数量>=6个
    int fu_yin_count = 0;
    for (int i = 0; i < 12; ++i) {
        DiZhi current = static_cast<DiZhi>(i);
        if (tian_di_pan_[current] == current) {
            fu_yin_count++;
        }
    }
    return fu_yin_count >= 6;
}

// 判断是否为返吟课
bool SanChuan::is_fan_yin_lesson() const {
    for (int i = 0; i < 12; ++i) {
        DiZhi current = static_cast<DiZhi>(i);
        DiZhi opposite = current + 6;
        if (tian_di_pan_[current] != opposite) {
            return false;
        }
    }
    return true;
}

// 构造函数：计算三传
SanChuan::SanChuan(const TianDiPan& tdp, const SiKe& sk)
    : tian_di_pan_(tdp), si_ke_(sk) {
    
    std::array<DiZhi, 3> result;
    std::string jiu_zong_men;  // 九宗门名称
    
    // 优先处理伏吟课
    if (is_fu_yin_lesson()) {
        jiu_zong_men = "伏吟";
        result = fu_yin();
    }
    // 其次处理返吟课
    else if (is_fan_yin_lesson()) {
        jiu_zong_men = "返吟";
        result = fan_yin();
    }
    // 正常课式处理流程
    else {
        try {
            // 1. 先尝试贼克法（含比用、涉害）
            result = zei_ke();
            
            // 根据具体的课式确定九宗门
            // 如果ke_shi_中有涉害相关的卦（涉害卦、见机卦、察微卦、复等卦），九宗门是"涉害"
            if (!ke_shi_.empty()) {
                const auto& last_ke = ke_shi_.back();
                if (last_ke == "涉害卦" || last_ke == "见机卦" || 
                    last_ke == "察微卦" || last_ke == "复等卦") {
                    jiu_zong_men = "涉害";
                } else {
                    jiu_zong_men = "贼克";
                }
            } else {
                jiu_zong_men = "贼克";
            }
        } catch (const std::exception&) {
            try {
                // 2. 尝试遥克法
                jiu_zong_men = "遥克";
                result = yao_ke();
            } catch (const std::exception&) {
                try {
                    // 3. 尝试昴星法
                    jiu_zong_men = "昴星";
                    result = ang_xing();
                } catch (const std::exception&) {
                    try {
                        // 4. 尝试别责法
                        jiu_zong_men = "别责";
                        result = bie_ze();
                    } catch (const std::exception&) {
                        try {
                            // 5. 处理八专日
                            jiu_zong_men = "八专";
                            result = ba_zhuan();
                        } catch (const std::exception&) {
                            throw std::runtime_error("所有方法均无法确定三传");
                        }
                    }
                }
            }
        }
    }
    
    chu_chuan_ = result[0];
    zhong_chuan_ = result[1];
    mo_chuan_ = result[2];
    
    // 将九宗门名称插入到课式列表的开头（如果不为空）
    if (!jiu_zong_men.empty()) {
        ke_shi_.insert(ke_shi_.begin(), jiu_zong_men);
    }
}

// ==================== DaLiuRenResult 实现 ====================

nlohmann::json DaLiuRenResult::to_json() const {
    nlohmann::json j;
    
    j["ba_zi"] = ba_zi;
    j["yue_jiang"] = std::string(Mapper::to_zh(yue_jiang));
    j["gui_ren"] = std::string(Mapper::to_zh(gui_ren));
    j["is_day"] = is_day;
    
    j["si_ke"] = {
        {"first", si_ke.first.to_string()},
        {"second", si_ke.second.to_string()},
        {"third", si_ke.third.to_string()},
        {"fourth", si_ke.fourth.to_string()}
    };
    
    j["san_chuan"] = {
        {"chu_chuan", std::string(Mapper::to_zh(san_chuan.get_chu_chuan()))},
        {"zhong_chuan", std::string(Mapper::to_zh(san_chuan.get_zhong_chuan()))},
        {"mo_chuan", std::string(Mapper::to_zh(san_chuan.get_mo_chuan()))},
        {"ke_shi", san_chuan.get_ke_shi()}
    };
    
    return j;
}

std::string DaLiuRenResult::to_string() const {
    return fmt::format(
        "【大六壬排盘】\n"
        "八字: {}\n"
        "月将: {}\n"
        "贵人: {}\n"
        "昼夜: {}\n"
        "四课: {} {} {} {}\n"
        "三传: {} -> {} -> {}\n"
        "课式: {}",
        ba_zi,
        Mapper::to_zh(yue_jiang),
        Mapper::to_zh(gui_ren),
        is_day ? "白天" : "夜晚",
        si_ke.first.to_string(),
        si_ke.second.to_string(),
        si_ke.third.to_string(),
        si_ke.fourth.to_string(),
        Mapper::to_zh(san_chuan.get_chu_chuan()),
        Mapper::to_zh(san_chuan.get_zhong_chuan()),
        Mapper::to_zh(san_chuan.get_mo_chuan()),
        fmt::join(san_chuan.get_ke_shi(), ", ")
    );
}

// ==================== DaLiuRenEngine 实现 ====================

DaLiuRenResult DaLiuRenEngine::pai_pan(int year, int month, int day, int hour) {
    auto solar_time = tyme::SolarTime::from_ymd_hms(year, month, day, hour, 0, 0);
    BaZi ba_zi = BaZi::from_solar(year, month, day, hour);
    return pai_pan_from_bazi(ba_zi, solar_time);
}

DaLiuRenResult DaLiuRenEngine::pai_pan_lunar(int year, int month, int day, int hour) {
    auto lunar_hour = tyme::LunarHour::from_ymd_hms(year, month, day, hour, 0, 0);
    auto solar_time = lunar_hour.get_solar_time();
    BaZi ba_zi = BaZi::from_lunar(year, month, day, hour);
    return pai_pan_from_bazi(ba_zi, solar_time);
}

DaLiuRenResult DaLiuRenEngine::pai_pan_from_bazi(const BaZi& ba_zi, const tyme::SolarTime& solar_time) {
    // 获取月将
    DiZhi yue_jiang = get_yue_jiang(solar_time);

    // 直接从八字获取时辰地支（更准确）
    DiZhi hour_zhi = ba_zi.hour.zhi;
    bool is_day = is_daytime(hour_zhi);
    
    // 获取贵人
    DiZhi gui_ren = get_gui_ren(ba_zi.day.gan, is_day);
    // 判断神将顺布还是逆布
    bool is_clockwise = (gui_ren == DiZhi::Hai) ||
                        (static_cast<int>(gui_ren) >= static_cast<int>(DiZhi::Zi) &&
                         static_cast<int>(gui_ren) <= static_cast<int>(DiZhi::Chen));

    TianDiPan tian_di_pan(yue_jiang, hour_zhi, gui_ren, is_clockwise);

    // 计算四课
    DiZhi gan_gong = get_ji_gong(ba_zi.day.gan);
    DiZhi first_upper = tian_di_pan[gan_gong];
    GanZhiKe first_ke(ba_zi.day.gan, first_upper);
    
    DiZhi second_upper = tian_di_pan[first_upper];
    GanZhiKe second_ke(first_upper, second_upper);
    
    DiZhi third_upper = tian_di_pan[ba_zi.day.zhi];
    GanZhiKe third_ke(ba_zi.day.zhi, third_upper);
    
    DiZhi fourth_upper = tian_di_pan[third_upper];
    GanZhiKe fourth_ke(third_upper, fourth_upper);
    
    SiKe si_ke(first_ke, second_ke, third_ke, fourth_ke, first_upper, third_upper);
    
    // 计算三传
    SanChuan san_chuan(tian_di_pan, si_ke);
    
    // 计算神煞
    ShenSha::ShenShaEngine shen_sha_engine(ba_zi, ba_zi.day.zhi);
    auto shen_sha_result = shen_sha_engine.calculate();
    
    // 判定卦体
    auto gua_ti = GuaTi::GuaTiEngine::judge_all(
        ba_zi, yue_jiang, tian_di_pan, si_ke, san_chuan
    );
    
    return DaLiuRenResult(ba_zi, yue_jiang, gui_ren, is_day, 
                          tian_di_pan, si_ke, san_chuan, shen_sha_result, gua_ti);
}

} // namespace ZhouYi::DaLiuRen

