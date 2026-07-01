// C++23 Module - 大六壬控制器
export module ZhouYi.DaLiuRen.Controller;

// 导入第三方库
import fmt;
import nlohmann.json;

// 导入大六壬模块
import ZhouYi.DaLiuRen;
import ZhouYi.BaZiBase;
import ZhouYi.GanZhi;

// 导入标准库
import std;

/**
 * @brief 大六壬控制器命名空间
 * 
 * 提供大六壬的交互式界面和批处理功能
 */
export namespace ZhouYi::DaLiuRen::Controller {

using namespace ZhouYi::DaLiuRen;
using namespace ZhouYi::BaZiBase;
using namespace ZhouYi::GanZhi;
namespace Mapper = ZhouYi::GanZhi::Mapper;

/**
 * @brief 大六壬控制器类
 * 
 * 提供用户交互和结果展示功能
 */
class DaLiuRenController {
public:
    /**
     * @brief 交互式排盘
     * 
     * 从控制台读取日期时间，进行大六壬排盘
     */
    static void interactive_pai_pan();
    
    /**
     * @brief 从公历日期排盘（非交互式）
     * 
     * @param year 公历年
     * @param month 公历月
     * @param day 公历日
     * @param hour 公历时
     * @return DaLiuRenResult 排盘结果
     */
    static DaLiuRenResult pai_pan_solar(int year, int month, int day, int hour);
    
    /**
     * @brief 从农历日期排盘（非交互式）
     * 
     * @param year 农历年
     * @param month 农历月
     * @param day 农历日
     * @param hour 农历时
     * @return DaLiuRenResult 排盘结果
     */
    static DaLiuRenResult pai_pan_lunar(int year, int month, int day, int hour);
    
    /**
     * @brief 显示排盘结果（控制台）
     * 
     * @param result 排盘结果
     */
    static void display_result(const DaLiuRenResult& result);
    
    /**
     * @brief 显示排盘结果（详细版）
     * 
     * 包含天地盘、四课、三传等详细信息
     * 
     * @param result 排盘结果
     */
    static void display_result_detailed(const DaLiuRenResult& result);
    
    
    /**
     * @brief 显示天地盘（图形化）
     * 
     * @param tian_di_pan 天地盘
     * @param day_gan 日干
     * @param day_zhi 日支
     */
    static void display_tian_di_pan(const TianDiPan& tian_di_pan, TianGan day_gan, DiZhi day_zhi);
    
    /**
     * @brief 显示四课信息
     * 
     * @param si_ke 四课
     */
    static void display_si_ke(const SiKe& si_ke);
    
    /**
     * @brief 显示三传信息
     * 
     * @param san_chuan 三传
     */
    static void display_san_chuan(const SanChuan& san_chuan, TianGan day_gan, DiZhi day_zhi);

private:
    /**
     * @brief 获取用户输入的日期
     * 
     * @param year 年份（输出）
     * @param month 月份（输出）
     * @param day 日期（输出）
     * @param hour 时辰（输出）
     * @param is_lunar 是否为农历（输出）
     */
    static void get_date_input(int& year, int& month, int& day, int& hour, bool& is_lunar);
    
    /**
     * @brief 格式化显示天地盘（圆形布局）
     */
    static std::string format_pan_circular(const TianDiPan& tdp);
};

} // namespace ZhouYi::DaLiuRen::Controller

