// Tyme Util 模块定义
export module ZhouYi.tyme.util;

// 导入标准库（最后）
import std;

export namespace tyme::util {
    class ShouXingUtil {
    public:
        static const double PI_2;
        static const double ONE_THIRD;
        static const int SECOND_PER_DAY;
        static const double SECOND_PER_RAD;

        static double nutation_lon2(double t);

        static double e_lon(double t, int n);

        static double m_lon(double t, int n);

        static double gxc_sun_lon(double t);

        static double ev(double t);

        static double sa_lon(double t, int n);

        static double dt_ext(double y, double jsd);

        static double dt_calc(double y);

        static double dt_t(double t);

        static double mv(double t);

        static double sa_lon_t(double w);

        static double msa_lon(double t, int mn, int sn);

        static double msa_lon_t(double w);

        static double sa_lon_t2(double w);

        static double msa_lon_t2(double w);

        static double qi_high(double w);

        static double shuo_high(double w);

        static double qi_low(double w);

        static double shuo_low(double w);

        static double calc_shuo(double jd);

        static double calc_qi(double jd);

        static double qi_accurate(double w);

        static double qi_accurate2(double jd);

    private:
        static std::string decode(const std::string &s);

        static const double NUT_B[];
        static const double DT_AT[];
        static const double XL0[];
        static const std::vector<std::vector<double>> XL1;
        static const double QI_KB[];
        static const double SHUO_KB[];
        static const std::string QB;
        static const std::string SB;
    };
}