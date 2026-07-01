/**
 * @file da_liu_ren_guati.cpp
 * @brief 大六壬卦体判定实现
 */

module ZhouYi.DaLiuRen.GuaTi;

namespace ZhouYi::DaLiuRen::GuaTi {

// ==================== 主判定函数 ====================

std::vector<std::string> GuaTiEngine::judge_all(
    const BaZi& ba_zi,
    DiZhi yue_jiang,
    const TianDiPan& tian_di_pan,
    const SiKe& si_ke,
    const SanChuan& san_chuan
) {
    std::vector<std::string> gua_ti_list;
    
    // 基础卦体
    if (is_fu_yin(si_ke)) {
        gua_ti_list.push_back("伏吟卦");
    }
    if (is_fan_yin(si_ke)) {
        gua_ti_list.push_back("返吟卦");
    }
    
    // 吉卦
    if (is_long_de(ba_zi, yue_jiang, san_chuan)) {
        gua_ti_list.push_back("龙德卦");
    }
    if (is_san_qi(ba_zi, san_chuan)) {
        gua_ti_list.push_back("三奇卦");
    }
    if (is_liu_yi(ba_zi, san_chuan)) {
        gua_ti_list.push_back("六仪卦");
    }
    if (is_zhu_yin(tian_di_pan, san_chuan)) {
        gua_ti_list.push_back("铸印卦");
    }
    if (is_zhuo_lun(tian_di_pan, si_ke, san_chuan)) {
        gua_ti_list.push_back("斫轮卦");
    }
    if (is_xuan_gai(ba_zi, san_chuan)) {
        gua_ti_list.push_back("轩盖卦");
    }
    if (is_guan_jue(ba_zi, san_chuan)) {
        gua_ti_list.push_back("官爵卦");
    }
    
    // 凶卦
    if (is_jiu_chou(si_ke)) {
        gua_ti_list.push_back("九丑卦");
    }
    if (is_luo_wang(si_ke, san_chuan)) {
        gua_ti_list.push_back("罗网卦");
    }
    
    // 其他卦体
    if (is_lian_zhu(san_chuan)) {
        gua_ti_list.push_back("连珠卦");
    }
    if (is_lian_ru(san_chuan)) {
        gua_ti_list.push_back("连茹卦");
    }
    
    return gua_ti_list;
}

// ==================== 基础卦体实现 ====================

bool GuaTiEngine::is_fu_yin(const SiKe& si_ke) {
    // 伏吟：支上神与支相同
    return si_ke.get_zhi_yang_shen() == si_ke.get_zhi();
}

bool GuaTiEngine::is_fan_yin(const SiKe& si_ke) {
    // 返吟：支上神与支相冲（六冲）
    DiZhi zhi = si_ke.get_zhi();
    DiZhi zhi_yang_shen = si_ke.get_zhi_yang_shen();
    return zhi_yang_shen == (zhi + 6);
}

// ==================== 吉卦实现 ====================

bool GuaTiEngine::is_long_de(
    const BaZi& ba_zi,
    DiZhi yue_jiang,
    const SanChuan& san_chuan
) {
    // 龙德卦：初传为月将，太岁支在三传中
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    DiZhi tai_sui = ba_zi.year.zhi;
    
    if (chu != yue_jiang) {
        return false;
    }
    
    return tai_sui == chu || tai_sui == zhong || tai_sui == mo;
}

bool GuaTiEngine::is_san_qi(
    const BaZi& ba_zi,
    const SanChuan& san_chuan
) {
    // 三奇卦：旬奇在三传中
    DiZhi xun_qi = calc_xun_qi(ba_zi.day.gan, ba_zi.day.zhi);
    
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    
    return xun_qi == chu || xun_qi == zhong || xun_qi == mo;
}

bool GuaTiEngine::is_liu_yi(
    const BaZi& ba_zi,
    const SanChuan& san_chuan
) {
    // 六仪卦：旬首在三传中
    DiZhi xun_shou = get_xun_shou(ba_zi.day.gan, ba_zi.day.zhi);
    
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    
    return xun_shou == chu || xun_shou == zhong || xun_shou == mo;
}

bool GuaTiEngine::is_zhu_yin(
    const TianDiPan& tian_di_pan,
    const SanChuan& san_chuan
) {
    // 铸印卦：巳上见戌，且巳、戌、卯俱在三传中
    if (tian_di_pan[DiZhi::Si] != DiZhi::Xu) {
        return false;
    }
    
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    
    bool has_si = (chu == DiZhi::Si || zhong == DiZhi::Si || mo == DiZhi::Si);
    bool has_xu = (chu == DiZhi::Xu || zhong == DiZhi::Xu || mo == DiZhi::Xu);
    bool has_mao = (chu == DiZhi::Mao || zhong == DiZhi::Mao || mo == DiZhi::Mao);
    
    return has_si && has_xu && has_mao;
}

bool GuaTiEngine::is_zhuo_lun(
    const TianDiPan& tian_di_pan,
    const SiKe& si_ke,
    const SanChuan& san_chuan
) {
    // 斫轮卦：初传为卯
    DiZhi chu = san_chuan.get_chu_chuan();
    if (chu != DiZhi::Mao) {
        return false;
    }
    
    // 条件1：干上神为卯且干为庚辛
    DiZhi gan_yang_shen = si_ke.get_gan_yang_shen();
    TianGan gan = si_ke.get_gan();
    if (gan_yang_shen == DiZhi::Mao && (gan == TianGan::Geng || gan == TianGan::Xin)) {
        return true;
    }
    
    // 条件2：卯临申或酉
    DiZhi mao_lin = tian_di_pan.lin(DiZhi::Mao);
    if (mao_lin == DiZhi::Shen || mao_lin == DiZhi::You) {
        return true;
    }
    
    return false;
}

bool GuaTiEngine::is_xuan_gai(
    const BaZi& ba_zi,
    const SanChuan& san_chuan
) {
    // 轩盖卦（高盖卦）：子、卯、天马（午）俱在三传中
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    
    DiZhi tian_ma = calc_tian_ma(ba_zi.month.zhi);
    
    bool has_zi = (chu == DiZhi::Zi || zhong == DiZhi::Zi || mo == DiZhi::Zi);
    bool has_mao = (chu == DiZhi::Mao || zhong == DiZhi::Mao || mo == DiZhi::Mao);
    bool has_tian_ma = (chu == tian_ma || zhong == tian_ma || mo == tian_ma);
    
    return has_zi && has_mao && has_tian_ma;
}

bool GuaTiEngine::is_guan_jue(
    const BaZi& ba_zi,
    const SanChuan& san_chuan
) {
    // 官爵卦：戌在三传中
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    
    bool has_xu = (chu == DiZhi::Xu || zhong == DiZhi::Xu || mo == DiZhi::Xu);
    if (!has_xu) {
        return false;
    }
    
    // 简化版：不检查太常和驿马（需要天将盘信息）
    // 只检查戌在三传中
    return true;
}

// ==================== 凶卦实现 ====================

bool GuaTiEngine::is_jiu_chou(const SiKe& si_ke) {
    // 九丑卦：特定干支日，支上神为丑
    TianGan gan = si_ke.get_gan();
    DiZhi zhi = si_ke.get_zhi();
    DiZhi zhi_yang_shen = si_ke.get_zhi_yang_shen();
    
    // 干为乙、戊、己、辛、壬
    bool gan_match = (gan == TianGan::Yi || gan == TianGan::Wu || 
                      gan == TianGan::Ji || gan == TianGan::Xin || 
                      gan == TianGan::Ren);
    
    // 支为子、卯、午、酉
    bool zhi_match = (zhi == DiZhi::Zi || zhi == DiZhi::Mao || 
                      zhi == DiZhi::Wu || zhi == DiZhi::You);
    
    // 支上神为丑
    bool yang_shen_match = (zhi_yang_shen == DiZhi::Chou);
    
    return gan_match && zhi_match && yang_shen_match;
}

bool GuaTiEngine::is_luo_wang(
    const SiKe& si_ke,
    const SanChuan& san_chuan
) {
    // 罗网卦：辰戌丑未四墓全在四课三传中
    std::array<DiZhi, 7> all_zhi = {
        si_ke.get_gan_yang_shen(),
        si_ke.get_gan_yin_shen(),
        si_ke.get_zhi_yang_shen(),
        si_ke.get_zhi_yin_shen(),
        san_chuan.get_chu_chuan(),
        san_chuan.get_zhong_chuan(),
        san_chuan.get_mo_chuan()
    };
    
    bool has_chen = false, has_xu = false, has_chou = false, has_wei = false;
    
    for (DiZhi z : all_zhi) {
        if (z == DiZhi::Chen) has_chen = true;
        if (z == DiZhi::Xu) has_xu = true;
        if (z == DiZhi::Chou) has_chou = true;
        if (z == DiZhi::Wei) has_wei = true;
    }
    
    return has_chen && has_xu && has_chou && has_wei;
}

// ==================== 其他卦体实现 ====================

bool GuaTiEngine::is_lian_zhu(const SanChuan& san_chuan) {
    // 连珠卦：三传地支连续（如子丑寅、寅卯辰等）
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    
    int chu_val = static_cast<int>(chu);
    int zhong_val = static_cast<int>(zhong);
    int mo_val = static_cast<int>(mo);
    
    // 顺序递增
    return (zhong_val == (chu_val + 1) % 12) && (mo_val == (zhong_val + 1) % 12);
}

bool GuaTiEngine::is_lian_ru(const SanChuan& san_chuan) {
    // 连茹卦：三传地支连续递减（如寅丑子、辰卯寅等）
    DiZhi chu = san_chuan.get_chu_chuan();
    DiZhi zhong = san_chuan.get_zhong_chuan();
    DiZhi mo = san_chuan.get_mo_chuan();
    
    int chu_val = static_cast<int>(chu);
    int zhong_val = static_cast<int>(zhong);
    int mo_val = static_cast<int>(mo);
    
    // 顺序递减
    return (zhong_val == (chu_val - 1 + 12) % 12) && (mo_val == (zhong_val - 1 + 12) % 12);
}

// ==================== 辅助函数实现 ====================

DiZhi GuaTiEngine::calc_xun_qi(TianGan day_gan, DiZhi day_zhi) {
    // 计算旬奇
    auto kong_wang = get_kong_wang(day_gan, day_zhi);
    DiZhi xun_shou = kong_wang[1] + 1;
    
    // 根据旬首计算旬奇
    if (xun_shou == DiZhi::Xu || xun_shou == DiZhi::Zi) {
        return DiZhi::Chou;
    }
    if (xun_shou == DiZhi::Shen || xun_shou == DiZhi::Wu) {
        return DiZhi::Zi;
    }
    if (xun_shou == DiZhi::Yin || xun_shou == DiZhi::Chen) {
        return DiZhi::Hai;
    }
    
    return DiZhi::Chou;  // 默认
}

DiZhi GuaTiEngine::calc_tian_ma(DiZhi month_zhi) {
    // 天马（月内天马）计算：午 + (月建 - 寅) * 2
    int month_offset = (static_cast<int>(month_zhi) - static_cast<int>(DiZhi::Yin) + 12) % 12;
    return DiZhi::Wu + (month_offset * 2);
}

DiZhi GuaTiEngine::calc_yi_ma(DiZhi zhi) {
    // 驿马计算：申子辰马在寅，寅午戌马在申，巳酉丑马在亥，亥卯未马在巳
    DiZhi temp = zhi;
    for (int i = 0; i < 3; ++i) {
        // 找到孟神
        if (temp == DiZhi::Yin || temp == DiZhi::Si || 
            temp == DiZhi::Shen || temp == DiZhi::Hai) {
            break;
        }
        temp = temp + 4;
    }
    return temp + 6;  // 驿马在孟神对冲位置
}

} // namespace ZhouYi::DaLiuRen::GuaTi

