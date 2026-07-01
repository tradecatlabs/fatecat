// Tyme 主模块定义
export module ZhouYi.tyme;

// 取消可能存在的IN和OUT宏定义
#ifdef IN
#undef IN
#endif
#ifdef OUT
#undef OUT
#endif

// 导入工具模块
import ZhouYi.tyme.util;

// 导入标准库（最后）
import std;

export namespace tyme {
    using namespace std;
    using namespace tyme::util;
    /**
     * @brief 节日类型
     */
    enum class FestivalType {
        DAY = 0,
        TERM = 1,
        EVE = 2
    };

    /**
     * @brief 性别
     */
    enum class Gender {
        WOMAN = 0,
        MAN = 1
    };

    /**
     * @brief 藏干类型
     */
    enum class HideHeavenStemType {
        RESIDUAL = 0,
        MIDDLE = 1,
        MAIN = 2
    };

    /**
     * @brief 内外
     */
    enum class Side {
        IN = 0,
        OUT = 1
    };

    /**
     * @brief 阴阳
     */
    enum class YinYang {
        YIN = 0,
        YANG = 1
    };

    /**
     * @brief 传统文化(民俗)
     */
    class Culture {
    public:
        virtual ~Culture() = default;

        /**
         * @brief 名称
         * @return 名称
         */
        virtual string get_name() const = 0;

        /**
         * @brief 描述
         * @return 描述
         */
        virtual string to_string() const = 0;
    };

    /**
     * @brief 传统文化抽象
     */
    class AbstractCulture : public Culture {
    public:
        ~AbstractCulture() override = default;

        bool equals(const Culture *o) const;

        /**
         * @brief 名称
         * @return 名称
         */
        string get_name() const override;

        /**
         * @brief 描述
         * @return 描述
         */
        string to_string() const override;

        /**
         * @brief 转换为不超范围的索引
         * @param index 索引
         * @param size 数量
         * @return 索引，从0开始
         */
        static int index_of(int index, int size);
    };

    /**
     * @brief 可轮回的Tyme
     */
    class LoopTyme : public AbstractCulture {
    public:
        ~LoopTyme() override = default;

        /**
         * @brief 通过索引初始化
         * @param names 名称列表
         * @param index 索引，支持负数，自动轮转
         */
        LoopTyme(const vector<string> &names, const int index) : names(names), index(index_of(index)) {
        }

        /**
         * @brief 通过名称初始化
         * @param names 名称列表
         * @param name 名称
         */
        LoopTyme(const vector<string> &names, const string &name) : names(names), index(index_of(name)) {
        }

        LoopTyme(const LoopTyme &other) {
            names = other.names;
            index = other.get_index();
        }

        LoopTyme& operator=(const LoopTyme &other) {
            if (this != &other) {
                names = other.names;
                index = other.get_index();
            }
            return *this;
        }

        /**
         * @brief 索引
         * @return 索引，从0开始
         */
        int get_index() const;

        /**
         * @brief 数量
         * @return 数量
         */
        int get_size() const;

        /**
         * @brief 名称
         * @return 名称
         */
        string get_name() const override;

        /**
         * @brief 名称对应的索引
         * @param name 名称
         * @return 索引，从0开始
         */
        int index_of(const string &name) const;

        /**
         * @brief 转换为不超范围的索引
         * @param index 索引
         * @return 索引，从0开始
         */
        int index_of(int index) const;

        /**
         * @brief 推移后的索引
         * @param n 推移步数
         * @return 索引，从0开始
         */
        int next_index(int n) const;

        /**
         * @brief 到目标索引的步数
         * @param target_index 目标索引
         * @return 步数
         */
        int steps_to(int target_index) const;

    protected:
        /**
         * @brief 名称列表
         */
        vector<string> names;

        /**
         * @brief 索引，从0开始
         */
        int index;
    };

    /**
     * @brief 二十八宿
     */
    class TwentyEightStar;
    /**
     * @brief 动物
     */
    class Animal : public LoopTyme {
    public:
        ~Animal() override = default;

        static const vector<string> NAMES;

        explicit Animal(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Animal(const string &name) : LoopTyme(NAMES, name) {
        }

        static Animal from_index(int index);

        static Animal from_name(const string &name);

        Animal next(int n) const;

        /**
         * @brief 二十八宿
         * @return 二十八宿
         */
        TwentyEightStar get_twenty_eight_star() const;
    };

    /**
     * @brief 星座
     */
    class Constellation : public LoopTyme {
    public:
        ~Constellation() override = default;

        static const vector<string> NAMES;

        explicit Constellation(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Constellation(const string &name) : LoopTyme(NAMES, name) {
        }

        static Constellation from_index(int index);

        static Constellation from_name(const string &name);

        Constellation next(int n) const;
    };

    /**
     * @brief 方位
     */
    class Direction;

    /**
     * @brief 五行
     */
    class Element : public LoopTyme {
    public:
        ~Element() override = default;

        static const vector<string> NAMES;

        explicit Element(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Element(const string &name) : LoopTyme(NAMES, name) {
        }

        static Element from_index(int index);

        static Element from_name(const string &name);

        Element next(int n) const;

        bool equals(const Element &other) const;

        /**
         * @brief 我生者
         * @return 五行
         */
        Element get_reinforce() const;

        /**
         * @brief 我克者
         * @return 五行
         */
        Element get_restrain() const;

        /**
         * @brief 生我者
         * @return 五行
         */
        Element get_reinforced() const;

        /**
         * @brief 克我者
         * @return 五行
         */
        Element get_restrained() const;

        /**
         * @brief 方位
         * @return 方位
         */
        Direction get_direction() const;
    };

    /**
     * @brief 九野
     */
    class Land : public LoopTyme {
    public:
        ~Land() override = default;

        static const vector<string> NAMES;

        explicit Land(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Land(const string &name) : LoopTyme(NAMES, name) {
        }

        static Land from_index(int index);

        static Land from_name(const string &name);

        Land next(int n) const;

        /**
         * 方位
         * @return 方位
         */
        Direction get_direction() const;
    };

    /**
     * @brief 方位
     */
    class Direction : public LoopTyme {
    public:
        ~Direction() override = default;

        static const vector<string> NAMES;

        explicit Direction(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Direction(const string &name) : LoopTyme(NAMES, name) {
        }

        static Direction from_index(int index);

        static Direction from_name(const string &name);

        Direction next(int n) const;

        /**
         * @brief 九野
         * @return 九野
         */
        Land get_land() const;

        /**
         * @brief 五行
         * @return 五行
         */
        Element get_element() const;
    };

    /**
     * @brief 建除十二值神
     */
    class Duty : public LoopTyme {
    public:
        ~Duty() override = default;

        static const vector<string> NAMES;

        explicit Duty(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Duty(const string &name) : LoopTyme(NAMES, name) {
        }

        static Duty from_index(int index);

        static Duty from_name(const string &name);

        Duty next(int n) const;
    };

    /**
     * @brief 吉凶
     */
    class Luck : public LoopTyme {
    public:
        ~Luck() override = default;

        static const vector<string> NAMES;

        explicit Luck(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Luck(const string &name) : LoopTyme(NAMES, name) {
        }

        static Luck from_index(int index);

        static Luck from_name(const string &name);

        Luck next(int n) const;
    };

    /**
     * @brief 元（60年=1元）
     */
    class Sixty : public LoopTyme {
    public:
        ~Sixty() override = default;

        static const vector<string> NAMES;

        explicit Sixty(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Sixty(const string &name) : LoopTyme(NAMES, name) {
        }

        static Sixty from_index(int index);

        static Sixty from_name(const string &name);

        Sixty next(int n) const;
    };

    /**
     * @brief 纳音
     */
    class Sound : public LoopTyme {
    public:
        ~Sound() override = default;

        static const vector<string> NAMES;

        explicit Sound(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Sound(const string &name) : LoopTyme(NAMES, name) {
        }

        static Sound from_index(int index);

        static Sound from_name(const string &name);

        Sound next(int n) const;
    };

    /**
     * @brief 旬
     */
    class Ten : public LoopTyme {
    public:
        ~Ten() override = default;

        static const vector<string> NAMES;

        explicit Ten(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Ten(const string &name) : LoopTyme(NAMES, name) {
        }

        static Ten from_index(int index);

        static Ten from_name(const string &name);

        Ten next(int n) const;
    };

    /**
     * @brief 地势(长生十二神)
     */
    class Terrain : public LoopTyme {
    public:
        ~Terrain() override = default;

        static const vector<string> NAMES;

        explicit Terrain(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Terrain(const string &name) : LoopTyme(NAMES, name) {
        }

        static Terrain from_index(int index);

        static Terrain from_name(const string &name);

        Terrain next(int n) const;
    };

    /**
     * @brief 运（20年=1运，3运=1元）
     */
    class Twenty : public LoopTyme {
    public:
        ~Twenty() override = default;

        static const vector<string> NAMES;

        explicit Twenty(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Twenty(const string &name) : LoopTyme(NAMES, name) {
        }

        static Twenty from_index(int index);

        static Twenty from_name(const string &name);

        Twenty next(int n) const;

        /**
         * @brief 元
         */
        Sixty get_sixty() const;
    };

    /**
     * @brief 七曜（七政、七纬、七耀）
     */
    class SevenStar;
    /**
     * @brief 星期
     */
    class Week : public LoopTyme {
    public:
        ~Week() override = default;

        static const vector<string> NAMES;

        explicit Week(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Week(const string &name) : LoopTyme(NAMES, name) {
        }

        static Week from_index(int index);

        static Week from_name(const string &name);

        Week next(int n) const;

        /**
         * @brief 七曜
         * @return 七曜
         */
        SevenStar get_seven_star() const;
    };

    /**
     * @brief 七曜（七政、七纬、七耀）
     */
    class SevenStar : public LoopTyme {
    public:
        ~SevenStar() override = default;

        static const vector<string> NAMES;

        explicit SevenStar(const int index) : LoopTyme(NAMES, index) {
        }

        explicit SevenStar(const string &name) : LoopTyme(NAMES, name) {
        }

        static SevenStar from_index(int index);

        static SevenStar from_name(const string &name);

        SevenStar next(int n) const;

        /**
         * @brief 星期
         * @return 星期
         */
        Week get_week() const;
    };

    /**
     * @brief 地支
     */
    class EarthBranch;
    /**
     * @brief 生肖
     */
    class Zodiac : public LoopTyme {
    public:
        ~Zodiac() override = default;

        static const vector<string> NAMES;

        explicit Zodiac(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Zodiac(const string &name) : LoopTyme(NAMES, name) {
        }

        static Zodiac from_index(int index);

        static Zodiac from_name(const string &name);

        Zodiac next(int n) const;

        bool equals(const Zodiac &other) const;

        /**
         * @brief 地支
         * @return 地支
         */
        EarthBranch get_earth_branch() const;
    };

    /**
     * @brief 神兽
     */
    class Beast;
    /**
     * @brief 宫
     */
    class Zone : public LoopTyme {
    public:
        ~Zone() override = default;

        static const vector<string> NAMES;

        explicit Zone(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Zone(const string &name) : LoopTyme(NAMES, name) {
        }

        static Zone from_index(int index);

        static Zone from_name(const string &name);

        Zone next(int n) const;

        /**
         * @brief 方位
         * @return 方位
         */
        Direction get_direction() const;

        /**
         * @brief 神兽
         * @return 神兽
         */
        Beast get_best() const;
    };

    /**
     * @brief 神兽
     */
    class Beast : public LoopTyme {
    public:
        ~Beast() override = default;

        static const vector<string> NAMES;

        explicit Beast(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Beast(const string &name) : LoopTyme(NAMES, name) {
        }

        static Beast from_index(int index);

        static Beast from_name(const string &name);

        Beast next(int n) const;

        /**
         * @brief 宫
         * @return 宫
         */
        Zone get_zone() const;
    };

    /**
     * @brief 二十八宿
     */
    class TwentyEightStar : public LoopTyme {
    public:
        ~TwentyEightStar() override = default;

        static const vector<string> NAMES;

        explicit TwentyEightStar(const int index) : LoopTyme(NAMES, index) {
        }

        explicit TwentyEightStar(const string &name) : LoopTyme(NAMES, name) {
        }

        static TwentyEightStar from_index(int index);

        static TwentyEightStar from_name(const string &name);

        TwentyEightStar next(int n) const;

        /**
         * @brief 七曜
         * @return 七曜
         */
        SevenStar get_seven_star() const;

        /**
         * @brief 九野
         * @return 九野
         */
        Land get_land() const;

        /**
         * @brief 宫
         * @return 宫
         */
        Zone get_zone() const;

        /**
         * @brief 动物
         * @return 动物
         */
        Animal get_animal() const;

        /**
         * @brief 吉凶
         * @return 吉凶
         */
        Luck get_luck() const;
    };

    /**
     * @brief 北斗九星
     */
    class Dipper : public LoopTyme {
    public:
        ~Dipper() override = default;

        static const vector<string> NAMES;

        explicit Dipper(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Dipper(const string &name) : LoopTyme(NAMES, name) {
        }

        static Dipper from_index(int index);

        static Dipper from_name(const string &name);

        Dipper next(int n) const;
    };

    /**
     * @brief 九星
     */
    class NineStar : public LoopTyme {
    public:
        ~NineStar() override = default;

        static const vector<string> NAMES;

        explicit NineStar(const int index) : LoopTyme(NAMES, index) {
        }

        explicit NineStar(const string &name) : LoopTyme(NAMES, name) {
        }

        static NineStar from_index(int index);

        static NineStar from_name(const string &name);

        NineStar next(int n) const;

        /**
         * @brief 颜色
         * @return 颜色
         */
        string get_color() const;

        /**
         * @brief 五行
         * @return 五行
         */
        Element get_element() const;

        /**
         * @brief 北斗九星
         * @return 北斗九星
         */
        Dipper get_dipper() const;

        /**
         * @brief 方位
         * @return 方位
         */
        Direction get_direction() const;

        string to_string() const override;
    };

    /**
     * @brief 六曜（孔明六曜星）
     */
    class SixStar : public LoopTyme {
    public:
        ~SixStar() override = default;

        static const vector<string> NAMES;

        explicit SixStar(const int index) : LoopTyme(NAMES, index) {
        }

        explicit SixStar(const string &name) : LoopTyme(NAMES, name) {
        }

        static SixStar from_index(int index);

        static SixStar from_name(const string &name);

        SixStar next(int n) const;
    };

    /**
     * @brief 十神
     */
    class TenStar : public LoopTyme {
    public:
        ~TenStar() override = default;

        static const vector<string> NAMES;

        explicit TenStar(const int index) : LoopTyme(NAMES, index) {
        }

        explicit TenStar(const string &name) : LoopTyme(NAMES, name) {
        }

        static TenStar from_index(int index);

        static TenStar from_name(const string &name);

        TenStar next(int n) const;
    };

    /**
     * @brief 黄道黑道
     */
    class Ecliptic : public LoopTyme {
    public:
        ~Ecliptic() override = default;

        static const vector<string> NAMES;

        explicit Ecliptic(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Ecliptic(const string &name) : LoopTyme(NAMES, name) {
        }

        static Ecliptic from_index(int index);

        static Ecliptic from_name(const string &name);

        Ecliptic next(int n) const;

        /**
         * @brief 吉凶
         * @return 吉凶
         */
        Luck get_luck() const;
    };

    /**
    * @brief 黄道黑道十二神
    */
    class TwelveStar : public LoopTyme {
    public:
        ~TwelveStar() override = default;

        static const vector<string> NAMES;

        explicit TwelveStar(const int index) : LoopTyme(NAMES, index) {
        }

        explicit TwelveStar(const string &name) : LoopTyme(NAMES, name) {
        }

        static TwelveStar from_index(int index);

        static TwelveStar from_name(const string &name);

        TwelveStar next(int n) const;

        /**
         * @brief 黄道黑道
         * @return 黄道黑道
         */
        Ecliptic get_ecliptic() const;
    };

    /**
     * @brief 三伏
     */
    class Dog : public LoopTyme {
    public:
        ~Dog() override = default;

        static const vector<string> NAMES;

        explicit Dog(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Dog(const string &name) : LoopTyme(NAMES, name) {
        }

        static Dog from_index(int index);

        static Dog from_name(const string &name);

        Dog next(int n) const;
    };

    /**
     * @brief 三伏天
     */
    class DogDay : public AbstractCulture {
    public:
        ~DogDay() override = default;

        explicit DogDay(const Dog& dog, const int day_index) : dog(dog), day_index(day_index) {
        }

        Dog get_dog() const;

        int get_day_index() const;

        string to_string() const override;

        string get_name() const override;
    protected:
        /**
         * @brief 三伏
         */
        Dog dog;

        /**
         * @brief 天索引
         */
        int day_index;
    };

    /**
     * @brief 天干六甲胎神（《天干六甲胎神歌》甲己之日占在门，乙庚碓磨休移动。丙辛厨灶莫相干，丁壬仓库忌修弄。戊癸房床若移整，犯之孕妇堕孩童。）
     */
    class FetusHeavenStem : public LoopTyme {
    public:
        ~FetusHeavenStem() override = default;

        static const vector<string> NAMES;

        explicit FetusHeavenStem(const int index) : LoopTyme(NAMES, index) {
        }

        static FetusHeavenStem from_index(int index);

        FetusHeavenStem next(int n) const;
    };

    /**
     * @brief 地支六甲胎神（《地支六甲胎神歌》子午二日碓须忌，丑未厕道莫修移。寅申火炉休要动，卯酉大门修当避。辰戌鸡栖巳亥床，犯着六甲身堕胎。）
     */
    class FetusEarthBranch : public LoopTyme {
    public:
        ~FetusEarthBranch() override = default;

        static const vector<string> NAMES;

        explicit FetusEarthBranch(const int index) : LoopTyme(NAMES, index) {
        }

        static FetusEarthBranch from_index(int index);

        FetusEarthBranch next(int n) const;
    };

    /**
     * @brief 数九
     */
    class Nine : public LoopTyme {
    public:
        ~Nine() override = default;

        static const vector<string> NAMES;

        explicit Nine(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Nine(const string &name) : LoopTyme(NAMES, name) {
        }

        static Nine from_index(int index);

        static Nine from_name(const string &name);

        Nine next(int n) const;
    };

    /**
     * @brief 数九天
     */
    class NineDay : public AbstractCulture {
    public:
        ~NineDay() override = default;

        explicit NineDay(const Nine &nine, const int day_index) : nine(nine), day_index(day_index) {
        }

        Nine get_nine() const;

        int get_day_index() const;

        string to_string() const override;

        string get_name() const override;
    protected:
        /**
         * @brief 数九
         */
        Nine nine;

        /**
         * @brief 天索引
         */
        int day_index;
    };

    /**
     * @brief 天干彭祖百忌
     */
    class PengZuHeavenStem : public LoopTyme {
    public:
        ~PengZuHeavenStem() override = default;

        static const vector<string> NAMES;

        explicit PengZuHeavenStem(const int index) : LoopTyme(NAMES, index) {
        }

        explicit PengZuHeavenStem(const string &name) : LoopTyme(NAMES, name) {
        }

        static PengZuHeavenStem from_index(int index);

        static PengZuHeavenStem from_name(const string &name);

        PengZuHeavenStem next(int n) const;
    };

    /**
     * @brief 地支彭祖百忌
     */
    class PengZuEarthBranch : public LoopTyme {
    public:
        ~PengZuEarthBranch() override = default;

        static const vector<string> NAMES;

        explicit PengZuEarthBranch(const int index) : LoopTyme(NAMES, index) {
        }

        explicit PengZuEarthBranch(const string &name) : LoopTyme(NAMES, name) {
        }

        static PengZuEarthBranch from_index(int index);

        static PengZuEarthBranch from_name(const string &name);

        PengZuEarthBranch next(int n) const;
    };

    /**
     * @brief 三候
     */
    class ThreePhenology : public LoopTyme {
    public:
        ~ThreePhenology() override = default;

        static const vector<string> NAMES;

        explicit ThreePhenology(const int index) : LoopTyme(NAMES, index) {
        }

        explicit ThreePhenology(const string &name) : LoopTyme(NAMES, name) {
        }

        static ThreePhenology from_index(int index);

        static ThreePhenology from_name(const string &name);

        ThreePhenology next(int n) const;
    };

    /**
     * @brief 梅雨
     */
    class PlumRain : public LoopTyme {
    public:
        ~PlumRain() override = default;

        static const vector<string> NAMES;

        explicit PlumRain(const int index) : LoopTyme(NAMES, index) {
        }

        explicit PlumRain(const string &name) : LoopTyme(NAMES, name) {
        }

        static PlumRain from_index(int index);

        static PlumRain from_name(const string &name);

        PlumRain next(int n) const;
    };

    /**
     * @brief 梅雨天
     */
    class PlumRainDay : public AbstractCulture {
    public:
        ~PlumRainDay() override = default;

        explicit PlumRainDay(const PlumRain &plum_rain, const int day_index) : plum_rain(plum_rain), day_index(day_index) {
        }

        PlumRain get_plum_rain() const;

        int get_day_index() const;

        string to_string() const override;

        string get_name() const override;
    protected:
        /**
         * @brief 梅雨
         */
        PlumRain plum_rain;

        /**
         * @brief 天索引
         */
        int day_index;
    };

    /**
     * @brief 小六壬
     */
    class MinorRen : public LoopTyme {
    public:
        ~MinorRen() override = default;

        static const vector<string> NAMES;

        explicit MinorRen(const int index) : LoopTyme(NAMES, index) {
        }

        explicit MinorRen(const string &name) : LoopTyme(NAMES, name) {
        }

        static MinorRen from_index(int index);

        static MinorRen from_name(const string &name);

        MinorRen next(int n) const;

        /**
         * @brief 吉凶
         * @return 吉凶
         */
        Luck get_luck() const;

        /**
         * @brief 五行
         * @return 五行
         */
        Element get_element() const;
    };

    /**
     * @brief 天干（天元）
     */
    class HeavenStem : public LoopTyme {
    public:
        ~HeavenStem() override = default;

        static const vector<string> NAMES;

        explicit HeavenStem(const int index) : LoopTyme(NAMES, index) {
        }

        explicit HeavenStem(const string &name) : LoopTyme(NAMES, name) {
        }

        static HeavenStem from_index(int index);

        static HeavenStem from_name(const string &name);

        HeavenStem next(int n) const;

        /**
         * @brief 五行
         * @return 五行
         */
        Element get_element() const;

        /**
         * @brief 阴阳
         * @return 阴阳
         */
        YinYang get_yin_yang() const;

        /**
         * @brief 十神（生我者，正印偏印。我生者，伤官食神。克我者，正官七杀。我克者，正财偏财。同我者，劫财比肩。）
         * @param target 天干
         * @return 十神
         */
        TenStar get_ten_star(const HeavenStem &target) const;

        /**
         * @brief 方位
         * @return 方位
         */
        Direction get_direction() const;

        /**
         * @brief 喜神方位（《喜神方位歌》甲己在艮乙庚乾，丙辛坤位喜神安。丁壬只在离宫坐，戊癸原在在巽间。）
         * @return 方位
         */
        Direction get_joy_direction() const;

        /**
         * @brief 阳贵神方位（《阳贵神歌》甲戊坤艮位，乙己是坤坎，庚辛居离艮，丙丁兑与乾，震巽属何日，壬癸贵神安。）
         * @return 方位
         */
        Direction get_yang_direction() const;

        /**
         * @brief 阴贵神方位（《阴贵神歌》甲戊见牛羊，乙己鼠猴乡，丙丁猪鸡位，壬癸蛇兔藏，庚辛逢虎马，此是贵神方。）
         * @return 方位
         */
        Direction get_yin_direction() const;

        /**
         * @brief 财神方位（《财神方位歌》甲乙东北是财神，丙丁向在西南寻，戊己正北坐方位，庚辛正东去安身，壬癸原来正南坐，便是财神方位真。）
         * @return 方位
         */
        Direction get_wealth_direction() const;

        /**
         * @brief 福神方位（《福神方位歌》甲乙东南是福神，丙丁正东是堪宜，戊北己南庚辛坤，壬在乾方癸在西。）
         * @return 方位
         */
        Direction get_mascot_direction() const;

        /**
         * @brief 天干彭祖百忌
         * @return 天干彭祖百忌
         */
        PengZuHeavenStem get_peng_zu_heaven_stem() const;

        /**
         * @brief 地势(长生十二神)
         * @param earth_branch 地支
         * @return 地势(长生十二神)
         */
        Terrain get_terrain(const EarthBranch &earth_branch) const;

        /**
         * @brief 五合（甲己合，乙庚合，丙辛合，丁壬合，戊癸合）
         * @return 天干
         */
        HeavenStem get_combine() const;

        /**
         * @brief 合化（甲己合化土，乙庚合化金，丙辛合化水，丁壬合化木，戊癸合化火）
         * @param target 天干
         * @return 五行，如果无法合化，返回nullopt
         */
        optional<Element> combine(const HeavenStem &target) const;

        bool equals(const HeavenStem &other) const;
    };

    /**
     * @brief 藏干（即人元，司令取天干，分野取天干的五行）
     */
    class HideHeavenStem : public AbstractCulture {
    public:
        ~HideHeavenStem() override = default;

        string get_name() const override;

        explicit HideHeavenStem(const HeavenStem &heaven_stem, const HideHeavenStemType type) : heaven_stem(heaven_stem), type(type) {
        }

        explicit HideHeavenStem(const string &heaven_stem_name, const HideHeavenStemType type) : heaven_stem(HeavenStem::from_name(heaven_stem_name)), type(type) {
        }

        explicit HideHeavenStem(const int heaven_stem_index, const HideHeavenStemType type) : heaven_stem(HeavenStem::from_index(heaven_stem_index)), type(type) {
        }

        /**
         * @brief 天干
         * @return 天干
         */
        HeavenStem get_heaven_stem() const;

        /**
         * @brief 藏干类型
         * @return 藏干类型
         */
        HideHeavenStemType get_type() const;

    protected:
        /**
         * @brief 天干
         */
        HeavenStem heaven_stem;

        /**
         * @brief 藏干类型
         */
        HideHeavenStemType type;
    };

    /**
     * @brief 人元司令分野（地支藏干+天索引）
     */
    class HideHeavenStemDay : public AbstractCulture {
    public:
        ~HideHeavenStemDay() override = default;

        explicit HideHeavenStemDay(const HideHeavenStem &hide_heaven_stem, const int day_index) : hide_heaven_stem(hide_heaven_stem), day_index(day_index) {
        }

        HideHeavenStem get_hide_heaven_stem() const;

        int get_day_index() const;

        string to_string() const override;

        string get_name() const override;
    protected:
        /**
         * @brief 藏干
         */
        HideHeavenStem hide_heaven_stem;

        /**
         * @brief 天索引
         */
        int day_index;
    };

    /**
     * @brief 地支（地元）
     */
    class EarthBranch : public LoopTyme {
    public:
        ~EarthBranch() override = default;

        static const vector<string> NAMES;

        explicit EarthBranch(const int index) : LoopTyme(NAMES, index) {
        }

        explicit EarthBranch(const string &name) : LoopTyme(NAMES, name) {
        }

        static EarthBranch from_index(int index);

        static EarthBranch from_name(const string &name);

        EarthBranch next(int n) const;

        /**
         * @brief 五行
         * @return 五行
         */
        Element get_element() const;

        /**
         * @brief 阴阳
         * @return 阴阳
         */
        YinYang get_yin_yang() const;

        /**
         * @brief 藏干之本气
         * @return 天干
         */
        HeavenStem get_hide_heaven_stem_main() const;

        /**
         * @brief 藏干之中气，无中气返回nullopt
         * @return 天干
         */
        optional<HeavenStem> get_hide_heaven_stem_middle() const;

        /**
         * @brief 藏干之余气，无余气返回nullopt
         * @return 天干
         */
        optional<HeavenStem> get_hide_heaven_stem_residual() const;

        /**
         * @brief 藏干列表
         * @return 藏干列表
         */
        vector<HideHeavenStem> get_hide_heaven_stems() const;

        /**
         * @brief 生肖
         * @return 生肖
         */
        Zodiac get_zodiac() const;

        /**
         * @brief 方位
         * @return 方位
         */
        Direction get_direction() const;

        /**
         * @brief 煞（逢巳日、酉日、丑日必煞东；亥日、卯日、未日必煞西；申日、子日、辰日必煞南；寅日、午日、戌日必煞北。）
         * @return 方位
         */
        Direction get_ominous() const;

        /**
         * @brief 地支彭祖百忌
         * @return 地支彭祖百忌
         */
        PengZuEarthBranch get_peng_zu_earth_branch() const;

        /**
         * @brief 六冲（子午冲，丑未冲，寅申冲，辰戌冲，卯酉冲，巳亥冲）
         * @return 地支
         */
        EarthBranch get_opposite() const;

        /**
         * @brief 六合（子丑合，寅亥合，卯戌合，辰酉合，巳申合，午未合）
         * @return 地支
         */
        EarthBranch get_combine() const;

        /**
         * @brief 六害（子未害、丑午害、寅巳害、卯辰害、申亥害、酉戌害）
         * @return 地支
         */
        EarthBranch get_harm() const;

        /**
         * @brief 合化（子丑合化土，寅亥合化木，卯戌合化火，辰酉合化金，巳申合化水，午未合化土）
         * @param target 地支
         * @return 五行，如果无法合化，返回nullopt
         */
        optional<Element> combine(const EarthBranch &target) const;
    };

    /**
     * @brief 彭祖百忌
     */
    class PengZu;

    /**
     * @brief 六十甲子(六十干支周)
     */
    class SixtyCycle : public LoopTyme {
    public:
        ~SixtyCycle() override = default;

        static const vector<string> NAMES;

        explicit SixtyCycle(const int index) : LoopTyme(NAMES, index) {
        }

        explicit SixtyCycle(const string &name) : LoopTyme(NAMES, name) {
        }

        static SixtyCycle from_index(int index);

        static SixtyCycle from_name(const string &name);

        SixtyCycle next(int n) const;

        /**
         * @brief 天干
         * @return 天干
         */
        HeavenStem get_heaven_stem() const;

        /**
         * @brief 地支
         * @return 地支
         */
        EarthBranch get_earth_branch() const;

        /**
         * @brief 纳音
         * @return 纳音
         */
        Sound get_sound() const;

        /**
         * @brief 彭祖百忌
         * @return 彭祖百忌
         */
        PengZu get_peng_zu() const;

        /**
         * @brief 旬
         * @return 旬
         */
        Ten get_ten() const;

        /**
         * @brief 旬空(空亡)，因地支比天干多2个，旬空则为每一轮干支一一配对后多出来的2个地支
         * @return 旬空(空亡)
         */
        vector<EarthBranch> get_extra_earth_branches() const;
    };

    /**
     * @brief 神煞
     */
    class God : public LoopTyme {
    public:
        ~God() override = default;

        static const vector<string> NAMES;

        explicit God(const int index) : LoopTyme(NAMES, index) {
        }

        explicit God(const string &name) : LoopTyme(NAMES, name) {
        }

        static God from_index(int index);

        static God from_name(const string &name);

        static vector<God> get_day_gods(const SixtyCycle &month, const SixtyCycle &day);

        God next(int n) const;

        /**
         * @brief 吉凶
         * @return 吉凶
         */
        Luck get_luck() const;

    protected:
        static const vector<string> DAY_GODS;
    };

    /**
     * @brief 宜忌
     */
    class Taboo : public LoopTyme {
    public:
        ~Taboo() override = default;

        static const vector<string> NAMES;

        explicit Taboo(const int index) : LoopTyme(NAMES, index) {
        }

        explicit Taboo(const string &name) : LoopTyme(NAMES, name) {
        }

        static Taboo from_index(int index);

        static Taboo from_name(const string &name);

        Taboo next(int n) const;

        /**
         * @brief 日宜
         * @param month 月干支
         * @param day 日干支
         * @return 宜忌列表
         */
        static vector<Taboo> get_day_recommends(const SixtyCycle &month, const SixtyCycle &day);

        /**
         * @brief 日忌
         * @param month 月干支
         * @param day 日干支
         * @return 宜忌列表
         */
        static vector<Taboo> get_day_avoids(const SixtyCycle &month, const SixtyCycle &day);

        /**
         * @brief 时辰宜
         * @param day 日干支
         * @param hour 时辰干支
         * @return 宜忌列表
         */
        static vector<Taboo> get_hour_recommends(const SixtyCycle &day, const SixtyCycle &hour);

        /**
         * @brief 时辰忌
         * @param day 日干支
         * @param hour 时辰干支
         * @return 宜忌列表
         */
        static vector<Taboo> get_hour_avoids(const SixtyCycle &day, const SixtyCycle &hour);

    protected:
        static const vector<string> DAY_TABOO;
        static const vector<string> HOUR_TABOO;

    private:
        static vector<Taboo> get_taboos(vector<string> data, int sup_index, int sub_index, int index);
    };

    /**
     * @brief 月相第几天
     */
    class PhaseDay;

    /**
     * @brief 月相
     */
    class Phase;

    /**
     * @brief 干支月
     */
    class SixtyCycleMonth;

    /**
     * @brief 干支年
     */
    class SixtyCycleYear : public AbstractCulture {
    public:
        ~SixtyCycleYear() override = default;

        explicit SixtyCycleYear(const int year) : AbstractCulture() {
            if (year < -1 || year > 9999) {
                throw invalid_argument("illegal sixty cycle year: " + std::to_string(year));
            }
            this->year = year;
        }

        static SixtyCycleYear from_year(int year);

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        string get_name() const override;

        SixtyCycleYear next(int n) const;

        /**
         * @brief 运
         * @return 运
         */
        Twenty get_twenty() const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 太岁方位
         * @return 太岁方位
         */
        Direction get_jupiter_direction() const;

        /**
         * @brief 首月（五虎遁：甲己之年丙作首，乙庚之岁戊为头，丙辛必定寻庚起，丁壬壬位顺行流，若问戊癸何方发，甲寅之上好追求。）
         * @return 干支月
         */
        SixtyCycleMonth get_first_month() const;

        /**
         * @brief 干支月列表
         * @return 干支月列表
         */
        vector<SixtyCycleMonth> get_months() const;

    protected:
        /**
         * @brief 年
         */
        int year;
    };

    /**
     * @brief 干支日
     */
    class SixtyCycleDay;

    /**
     * @brief 干支月
     */
    class SixtyCycleMonth : public AbstractCulture {
    public:
        ~SixtyCycleMonth() override = default;

        explicit SixtyCycleMonth(const SixtyCycleYear &year, const SixtyCycle &month) : AbstractCulture(), year(year), month(month) {
        }

        static SixtyCycleMonth from_index(int year, int index);

        /**
         * @brief 干支年
         * @return 干支年
         */
        SixtyCycleYear get_sixty_cycle_year() const;

        /**
         * @brief 年柱
         * @return 年柱
         */
        SixtyCycle get_year() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        string get_name() const override;

        string to_string() const override;

        SixtyCycleMonth next(int n) const;

        /**
         * @brief 位于当年的索引(0-11)，寅月为0，依次类推
         * @return 索引
         */
        int get_index_in_year() const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 太岁方位
         * @return 方位
         */
        Direction get_jupiter_direction() const;

        /**
         * @brief 首日（节令当天）
         * @return 干支日
         */
        SixtyCycleDay get_first_day() const;

        /**
         * @brief 本月的干支日列表
         * @return 干支日列表
         */
        vector<SixtyCycleDay> get_days() const;

    protected:
        /**
         * @brief 干支年
         */
        SixtyCycleYear year;

        /**
         * @brief 月柱
         */
        SixtyCycle month;
    };

    /**
     * @brief 公历日
     */
    class SolarDay;

    /**
     * @brief 公历时刻
     */
    class SolarTime;

    /**
     * @brief 儒略日
     */
    class JulianDay : public AbstractCulture {
    public:
        ~JulianDay() override = default;

        /**
         * @brief 2000年儒略日数(2000-1-1 12:00:00 UTC)
         */
        static const double J2000;

        explicit JulianDay(const double day) : AbstractCulture() {
            this->day = day;
        }

        static JulianDay from_julian_day(double day);

        static JulianDay from_ymd_hms(int year, int month, int day, int hour, int minute, int second);

        /**
         * @brief 儒略日
         * @return 儒略日
         */
        double get_day() const;

        string get_name() const override;

        JulianDay next(int n) const;

        /**
         * @brief 星期
         * @return 星期
         */
        Week get_week() const;

        /**
         * @brief 儒略日相减
         * @param target 儒略日
         * @return 差
         */
        double subtract(const JulianDay &target) const;

        /**
         * @brief 公历时刻
         * @return 公历时刻
         */
        SolarTime get_solar_time() const;

        /**
         * @brief 公历日
         * @return 公历日
         */
        SolarDay get_solar_day() const;

    protected:
        /**
         * @brief 儒略日
         */
        double day;
    };

    /**
     * @brief 灶马头
     */
    class KitchenGodSteed;

    /**
     * @brief 农历月
     */
    class LunarMonth;

    /**
     * @brief 农历年
     */
    class LunarYear : public AbstractCulture {
    public:
        ~LunarYear() override = default;

        static vector<vector<int> > LEAP;

        explicit LunarYear(const int year) : AbstractCulture() {
            static once_flag flag;
            call_once(flag, [] {
                string chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_@";
                string months[] = {
                    "080b0r0j0j0j0C0j0j0C0j0j0j0C0j0C0j0C0F0j0V0V0V0u0j0j0C0j0j0j0j0V0C0j1v0u0C0V1v0C0b080u110u0C0j0C1v9K1v2z0j1vmZbl1veN3s1v0V0C2S1v0V0C2S2o0C0j1Z1c2S1v0j1c0j2z1v0j1c0j392H0b2_2S0C0V0j1c0j2z0C0C0j0j1c0j0N250j0C0j0b081n080b0C0C0C1c0j0N",
                    "0r1v1c1v0V0V0F0V0j0C0j0C0j0V0j0u1O0j0C0V0j0j0j0V0b080u0r0u080b0j0j0C0V0C0V0j0b080V0u080b0j0j0u0j1v0u080b1c0j080b0j0V0j0j0V0C0N1v0j1c0j0j1v2g1v420j1c0j2z1v0j1v5Q9z1v4l0j1vfn1v420j9z4l1v1v2S1c0j1v2S3s1v0V0C2S1v1v2S1c0j1v2S2_0b0j2_2z0j1c0j",
                    "0z0j0j0j0C0j0j0C0j0j0j0C0j0C0j0j0j0j0m0j0C0j0j0C0j0j0j0j0b0V0j0j0C0j0j0j0j0V0j0j0j0V0b0V0V0C0V0C0j0j0b080u110u0V0C0j0N0j0b080b080b0j0r0b0r0b0j0j0j0j0C0j0b0r0C0j0b0j0C0C0j0j0j0j0j0j0j0j0j0b110j0b0j0j0j0C0j0C0j0j0j0j0b080b080b0V080b080b0j0j0j0j0j0j0V0j0j0u1v0j0j0j0C0j0j0j0V0C0N1c0j0C0C0j0j0j1n080b0j0V0C0j0C0C2g0j1c0j0j1v2g1v0j0j1v7N0j1c0j3L0j0j1v5Q1Z5Q1v4lfn1v420j1v5Q1Z5Q1v4l1v2z1v",
                    "0H140r0N0r140r0u0r0V171c11140C0j0u110j0u0j1v0j0C0j0j0j0b080V0u080b0C1v0j0j0j0C0j0b080V0j0j0b080b0j0j0j0j0b080b0C080j0b080b0j0j0j0j0j0j0b080j0b080C0b080b080b080b0j0j0j0j080b0j0C0j0j0j0b0j0j080C0b0j0j0j0j0j0j0b08080b0j0C0j0j0j0b0j0j0K0b0j0C0j0j0j0b080b080j0C0b0j080b080b0j0j0j0j080b0j0b0r0j0j0j0b0j0C0r0b0j0j0j0j0j0j0j0b080j0b0r0C0j0b0j0j0j0r0b0j0C0j0j0j0u0r0b0C0j080b0j0j0j0j0j0j0j1c0j0b0j0j0j0C0j0j0j0j0j0j0j0b080j1c0u0j0j0j0C0j1c0j0u0j1c0j0j0j0j0j0j0j0j1c0j0u1v0j0j0V0j0j2g0j0j0j0C1v0C1G0j0j0V0C1Z1O0j0V0j0j2g1v0j0j0V0C2g5x1v4l1v421O7N0V0C4l1v2S1c0j1v2S2_",
                    "050b080C0j0j0j0C0j0j0C0j0j0j0C0j0C0j0C030j0j0j0j0j0j0j0j0j0C0j0b080u0V080b0j0j0V0j0j0j0j0j0j0j0j0j0V0N0j0C0C0j0j0j0j0j0j0j0j1c0j0u0j1v0j0j0j0j0j0b080b080j0j0j0b080b080b080b080b0j0j0j080b0j0b080j0j0j0j0b080b0j0j0r0b080b0b080j0j0j0j0b080b080j0b080j0b080b080b080b080b0j0j0r0b0j0b080j0j0j0j0b080b0j0j0C080b0b080j0j0j0j0j0j0j0b080u080j0j0b0j0j0j0C0j0b080j0j0j0j0b080b080b080b0C080b080b080b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0b080j0j0C0b080b080j0b0j0j0C080b0j0j0j0j0j0j0b0j0j080C0b0j080b0j0j0j0j0j0j0j0C0j0j0j0b0j0j0C080b0j0j0j0j0j0j0b080b080b0K0b080b080b0j0j0j0j0j0j0j0C0j0j0u0j0j0V0j080b0j0C0j0j0j0b0j0r0C0b0j0j0j0j0j0j0j0j0j0C0j0b080b080b0j0C0C0j0C0j0j0j0u110u0j0j0j0j0j0j0j0j0C0j0j0u0j1c0j0j0j0j0j0j0j0j0V0C0u0j0C0C0V0C1Z0j0j0j0C0j0j0j1v0u0j1c0j0j0j0C0j0j2g0j1c1v0C1Z0V0j4l0j0V0j0j2g0j1v0j1v2S1c7N1v",
                    "0w0j1c0j0V0j0j0V0V0V0j0m0V0j0C1c140j0j0j0C0V0C0j1v0j0N0j0C0j0j0j0V0j0j1v0N0j0j0V0j0j0j0j0j0j080b0j0j0j0j0j0j0j080b0j0C0j0j0j0b0j0j080u080b0j0j0j0j0j0j0b080b080b080C0b0j080b080b0j0j0j0j080b0j0C0j0j0j0b0j0j080u080b0j0j0j0j0j0j0b080b080b080b0r0b0j080b080b0j0j0j0j080b0j0b0r0j0j0b080b0j0j080b0j080b0j080b080b0j0j0j0j0j0b080b0r0C0b080b0j0j0j0j080b0b080b080j0j0j0b080b080b080b0j0j0j0j080b0j0b080j0j0j0j0b080b0j0j0r0b080b0j0j0j0j0j0b080b080j0b0r0b080j0b080b0j0j0j0j080b0j0b080j0j0j0j0b080b0j080b0r0b0j080b080b0j0j0j0j0j0b080b0r0C0b080b0j0j0j0j0j0j0b080j0j0j0b080b080b080b0j0j0j0r0b0j0b080j0j0j0j0b080b0r0b0r0b0j080b080b0j0j0j0j0j0j0b0r0j0j0j0b0j0j0j0j080b0j0b080j0j0j0j0b080b080b0j0r0b0j080b0j0j0j0j0j0j0j0b0r0C0b0j0j0j0j0j0j0j080b0j0C0j0j0j0b0j0C0r0b0j0j0j0j0j0j0b080b080u0r0b0j080b0j0j0j0j0j0j0j0b0r0C0u0j0j0j0C0j080b0j0C0j0j0j0u110b0j0j0j0j0j0j0j0j0j0C0j0b080b0j0j0C0C0j0C0j0j0j0b0j1c0j080b0j0j0j0j0j0j0V0j0j0u0j1c0j0j0j0C0j0j2g0j0j0j0C0j0j0V0j0b080b1c0C0V0j0j2g0j0j0V0j0j1c0j1Z0j0j0C0C0j1v",
                    "160j0j0V0j1c0j0C0j0C0j1f0j0V0C0j0j0C0j0j0j1G080b080u0V080b0j0j0V0j1v0j0u0j1c0j0j0j0C0j0j0j0C0C0j1D0b0j080b0j0j0j0j0C0j0b0r0C0j0b0j0C0C0j0j0j0j0j0j0j0j0j0b0r0b0r0j0b0j0j0j0C0j0b0r0j0j0j0b080b080j0b0C0j080b080b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0b080j0j0j0j0b080b080j0b0C0r0j0b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0j0j0j0C0j0j0b080b0j0j0C080b0j0j0j0j0j0j0b080b080b080C0b080b080b080b0j0j0j0j0j0b080C0j0j0b080b0j0j0C080b0j0j0j0j0j0j0b080j0b0C080j0j0b0j0j0j0j0j0j0b080j0b080C0b080b080b080b0j0j0j0j080b0j0C0j0j0b080b0j0j0C080b0j0j0j0j0j0j0b080j0b080u080j0j0b0j0j0j0j0j0j0b080C0j0j0b080b0j0j0C0j0j080b0j0j0j0j0j0b080b0C0r0b080b0j0j0j0j0j0j0b080j0b080u080b080b080b0j0j0j0C0j0b080j0j0j0j0b0j0j0j0C0j0j080b0j0j0j0j0j0b080b0C0r0b080b0j0j0j0j0j0j0b080j0b0r0b080b080b080b0j0j0j0r0b0j0b0r0j0j0j0b0j0j0j0r0b0j080b0j0j0j0j0j0j0j0b0r0C0b0j0j0j0j0j0j0j0b080j0C0u080b080b0j0j0j0r0b0j0C0C0j0b0j110b0j080b0j0j0j0j0j0j0u0r0C0b0j0j0j0j0j0j0j0j0j0C0j0j0j0b0j1c0j0C0j0j0j0b0j0814080b080b0j0j0j0j0j0j1c0j0u0j0j0V0j0j0j0j0j0j0j0u110u0j0j0j",
                    "020b0r0C0j0j0j0C0j0j0V0j0j0j0j0j0C0j1f0j0C0j0V1G0j0j0j0j0V0C0j0C1v0u0j0j0j0V0j0j0C0j0j0j1v0N0C0V0j0j0j0K0C250b0C0V0j0j0V0j0j2g0C0V0j0j0C0j0j0b081v0N0j0j0V0V0j0j0u0j1c0j080b0j0j0j0j0j0j0V0j0j0u0j0j0V0j0j0j0C0j0b080b080V0b0j080b0j0j0j0j0j0j0j0b0r0C0j0b0j0j0j0C0j080b0j0j0j0j0j0j0u0r0C0u0j0j0j0j0j0j0b080j0C0j0b080b080b0j0C0j080b0j0j0j0j0j0j0b080b110b0j0j0j0j0j0j0j0j0j0b0r0j0j0j0b0j0j0j0r0b0j0b080j0j0j0j0b080b080b080b0r0b0j080b080b0j0j0j0j0j0j0b0r0C0b080b0j0j0j0j080b0j0b080j0j0j0j0b080b080b0j0j0j0r0b0j0j0j0j0j0j0b080b0j080C0b0j080b080b0j0j0j0j080b0j0b0r0C0b080b0j0j0j0j080b0j0j0j0j0j0b080b080b080b0j0j080b0r0b0j0j0j0j0j0j0b0j0j080C0b0j080b080b0j0j0j0j0j0b080C0j0j0b080b0j0j0C0j0b080j0j0j0j0b080b080b080b0C0C080b0j0j0j0j0j0j0b0C0C080b080b080b0j0j0j0j0j0j0b0C080j0j0b0j0j0j0C0j0b080j0b080j0j0b080b080b080b0C0r0b0j0j0j0j0j0j0b080b0r0b0r0b0j080b080b0j0j0j0j0j0j0b0r0C0j0b0j0j0j0j0j0j0b080j0C0j0b080j0b0j0j0K0b0j0C0j0j0j0b080b0j0K0b0j080b0j0j0j0j0j0j0V0j0j0b0j0j0j0C0j0j0j0j",
                    "0l0C0K0N0r0N0j0r1G0V0m0j0V1c0C0j0j0j0j1O0N110u0j0j0j0C0j0j0V0C0j0u110u0j0j0j0C0j0j0j0C0C0j250j1c2S1v1v0j5x2g0j1c0j0j1c2z0j1c0j0j1c0j0N1v0V0C1v0C0b0C0V0j0j0C0j0C1v0u0j0C0C0j0j0j0C0j0j0j0u110u0j0j0j0C0j0C0C0C0b080b0j0C0j080b0j0C0j0j0j0u110u0j0j0j0C0j0j0j0C0j0j0j0u0C0r0u0j0j0j0j0j0j0b0r0b0V080b080b0j0C0j0j0j0V0j0j0b0j0j0j0C0j0j0j0j0j0j0j0b080j0b0C0r0j0b0j0j0j0C0j0b0r0b0r0j0b080b080b0j0C0j0j0j0j0j0j0j0j0b0j0C0r0b0j0j0j0j0j0j0b080b080j0b0r0b0r0j0b0j0j0j0j080b0j0b0r0j0j0j0b080b080b0j0j0j0j080b0j0j0j0j0j0j0b0j0j0j0r0b0j0j0j0j0j0j0b080b080b080b0r0C0b080b0j0j0j0j0j0b080b0r0C0b080b080b080b0j0j0j0j080b0j0C0j0j0j0b0j0j0C080b0j0j0j0j0j0j0b080j0b0C080j0j0b0j0j0j0j0j0j0b0r0b080j0j0b080b080b0j0j0j0j0j0j0b080j0j0j0j0b0j0j0j0r0b0j0b080j0j0j0j0j0b080b080b0C0r0b0j0j0j0j0j0j0b080b080j0C0b0j080b080b0j0j0j0j0j0j",
                    "0a0j0j0j0j0C0j0j0C0j0C0C0j0j0j0j0j0j0j0m0C0j0j0j0j0u080j0j0j1n0j0j0j0j0C0j0j0j0V0j0j0j1c0u0j0C0V0j0j0V0j0j1v0N0C0V2o1v1O2S2o141v0j1v4l0j1c0j1v2S2o0C0u1v0j0C0C2S1v0j1c0j0j1v0N251c0j1v0b1c1v1n1v0j0j0V0j0j1v0N1v0C0V0j0j1v0b0C0j0j0V1c0j0u0j1c0j0j0j0j0j0j0j0j1c0j0u0j0j0V0j0j0j0j0j0j0b080u110u0j0j0j0j0j0j1c0j0b0j080b0j0C0j0j0j0V0j0j0u0C0V0j0j0j0C0j0b080j1c0j0b0j0j0j0C0j0C0j0j0j0b080b080b0j0C0j080b0j0j0j0j0j0j0j0b0C0r0u0j0j0j0j0j0j0b080j0b0r0C0j0b0j0j0j0r0b0j0b0r0j0j0j0b080b080b0j0r0b0j080b0j0j0j0j0j0j0b0j0r0C0b0j0j0j0j0j0j0b080j0j0C0j0j0b080b0j0j0j0j0j0j0j0j0j0j0b080b080b080b0C0j0j080b0j0j0j0j0j0j0b0j0j0C080b0j0j0j0j0j0j0j0j0b0C080j0j0b0j0j0j0j0j",
                    "0n0Q0j1c14010q0V1c171k0u0r140V0j0j1c0C0N1O0j0V0j0j0j1c0j0u110u0C0j0C0V0C0j0j0b671v0j1v5Q1O2S2o2S1v4l1v0j1v2S2o0C1Z0j0C0C1O141v0j1c0j2z1O0j0V0j0j1v0b2H390j1c0j0V0C2z0j1c0j1v2g0C0V0j1O0b0j0j0V0C1c0j0u0j1c0j0j0j0j0j0j0j0j1c0N0j0j0V0j0j0C0j0j0b081v0u0j0j0j0C0j1c0N0j0j0C0j0j0j0C0j0j0j0u0C0r0u0j0j0j0C0j0b080j1c0j0b0j0C0C0j0C0C0j0b080b080u0C0j080b0j0C0j0j0j0u110u0j0j0j0j0j0j0j0j0C0C0j0b0j0j0j0C0j0C0C0j0b080b080b0j0C0j080b0j0C0j0j0j0b0j110b0j0j0j0j0j",
                    "0B0j0V0j0j0C0j0j0j0C0j0C0j0j0C0j0m0j0j0j0j0C0j0C0j0j0u0j1c0j0j0C0C0j0j0j0j0j0j0j0j0u110N0j0j0V0C0V0j0b081n080b0CrU1O5e2SbX2_1Z0V2o141v0j0C0C0j2z1v0j1c0j7N1O420j1c0j1v2S1c0j1v2S2_0b0j0V0j0j1v0N1v0j0j1c0j1v140j0V0j0j0C0C0b080u1v0C0V0u110u0j0j0j0C0j0j0j0C0C0N0C0V0j0j0C0j0j0b080u110u0C0j0C0u0r0C0u080b0j0j0C0j0j0j"
                };
                for (const string &m: months) {
                    int n = 0;
                    const int size = static_cast<int>(m.length()) / 2;
                    vector<int> l;
                    for (int y = 0; y < size; y++) {
                        const int z = y * 2;
                        int t = 0;
                        int c = 1;
                        for (int x = 1; x > -1; x--) {
                            t += c * static_cast<int>(chars.find(m.substr(z + x, 1)));
                            c *= 64;
                        }
                        n += t;
                        l.push_back(n);
                    }
                    LEAP.push_back(l);
                }
            });
            if (year < -1 || year > 9999) {
                throw invalid_argument("illegal lunar year: " + std::to_string(year));
            }
            this->year = year;
        }

        LunarYear(const LunarYear &other) {
            year = other.year;
        }

        LunarYear &operator=(const LunarYear &other);

        static LunarYear from_year(int year);

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        /**
         * @brief 天数
         * @return 天数
         */
        int get_day_count() const;

        /**
         * @brief 月数
         * @return 月数
         */
        int get_month_count() const;

        string get_name() const override;

        LunarYear next(int n) const;

        /**
         * @brief 运
         * @return 运
         */
        Twenty get_twenty() const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 太岁方位
         * @return 方位
         */
        Direction get_jupiter_direction() const;

        /**
         * @brief 闰月
         * @return 闰月数字，1代表闰1月，0代表无闰月
         */
        int get_leap_month() const;

        /**
         * @brief 灶马头
         * @return 灶马头
         */
        KitchenGodSteed get_kitchen_god_steed() const;

        /**
         * @brief 首月（农历月，即一月，俗称正月）
         * @return 农历月
         */
        LunarMonth get_first_month() const;

        /**
         * @brief 农历月列表
         * @return 农历月列表
         */
        vector<LunarMonth> get_months() const;

    protected:
        /**
         * @brief 年
         */
        int year;
    };

    /**
     * @brief 农历季节
     */
    class LunarSeason : public LoopTyme {
    public:
        ~LunarSeason() override = default;

        static const vector<string> NAMES;

        explicit LunarSeason(const int index) : LoopTyme(NAMES, index) {
        }

        explicit LunarSeason(const string &name) : LoopTyme(NAMES, name) {
        }

        LunarSeason(const LunarSeason &other) = default;

        static LunarSeason from_index(int index);

        static LunarSeason from_name(const string &name);

        LunarSeason next(int n) const;
    };

    /**
     * @brief 逐月胎神
     */
    class FetusMonth;

    /**
     * @brief 节气
     */
    class SolarTerm : public LoopTyme {
    public:
        ~SolarTerm() override = default;

        static const vector<string> NAMES;

        explicit SolarTerm(const int year, const int index) : LoopTyme(NAMES, index) {
            const int size = get_size();
            init_by_year((year * size + index) / size, get_index());
        }

        explicit SolarTerm(const int year, const string &name) : LoopTyme(NAMES, name) {
            init_by_year(year, index);
        }

        static SolarTerm from_index(int year, int index);

        static SolarTerm from_name(int year, const string &name);

        SolarTerm next(int n) const;

        /**
         * @brief 是否节令
         * @return true/false
         */
        bool is_jie() const;

        /**
         * @brief 是否气令
         * @return true/false
         */
        bool is_qi() const;

        /**
         * @brief 儒略日
         * @return 儒略日
         */
        JulianDay get_julian_day() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 粗略的儒略日
         * @return 儒略日数
         */
        double get_cursory_julian_day() const;

    protected:
        /**
         * @brief 年
         */
        int year = 0;

        /**
         * @brief 粗略的儒略日
         */
        double cursory_julian_day = 0;

        void init_by_year(int year, int offset);
    };

    /**
     * @brief 农历月
     */
    class LunarMonth : public AbstractCulture {
    public:
        ~LunarMonth() override = default;

        static const vector<string> NAMES;

        LunarMonth(const LunarMonth &other): year(other.year), month(other.month), leap(other.leap), day_count(other.day_count), index_in_year(other.index_in_year), first_julian_day(other.first_julian_day) {
        }

        LunarMonth &operator=(const LunarMonth &other);

        explicit LunarMonth(const int year, const int month) : AbstractCulture(), year(LunarYear::from_year(year)), first_julian_day(0) {
            if (month == 0 || month > 12 || month < -12) {
                throw invalid_argument(&"illegal lunar month: "[month]);
            }
            const int m = abs(month);
            const bool leap = month < 0;
            const int current_leap_month = this->year.get_leap_month();
            if (leap && m != current_leap_month) {
                throw invalid_argument("illegal leap month " + std::to_string(m) + " in lunar year" + std::to_string(year));
            }

            // 冬至
            const double dong_zhi_jd = SolarTerm::from_index(year, 0).get_cursory_julian_day();

            // 冬至前的初一，今年首朔的日月黄经差
            double w = ShouXingUtil::calc_shuo(dong_zhi_jd);
            if (w > dong_zhi_jd) {
                w -= 29.53;
            }

            // 正常情况正月初一为第3个朔日，但有些特殊的
            int offset = 2;
            if (year > 8 && year < 24) {
                offset = 1;
            } else if (LunarYear::from_year(year - 1).get_leap_month() > 10 && year != 239 && year != 240) {
                offset = 3;
            }

            // 位于当年的索引
            int index = m - 1;
            if (leap || (current_leap_month > 0 && m > current_leap_month)) {
                index += 1;
            }
            this->index_in_year = index;

            // 本月初一
            w += 29.5306 * (offset + index);
            const double first_day = ShouXingUtil::calc_shuo(w);
            this->first_julian_day = JulianDay::from_julian_day(JulianDay::J2000 + first_day);
            // 本月天数 = 下月初一 - 本月初一
            this->day_count = static_cast<int>(ShouXingUtil::calc_shuo(w + 29.5306) - first_day);
            this->month = m;
            this->leap = leap;
        }

        static LunarMonth from_ym(int year, int month);

        /**
         * @brief 农历年
         * @return 农历年
         */
        LunarYear get_lunar_year() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 月
         * @return 月，当月为闰月时，返回负数
         */
        int get_month_with_leap() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        /**
         * @brief 天数
         * @return 天数
         */
        int get_day_count() const;

        /**
         * @brief 位于当年的索引(0-12)
         * @return 索引
         */
        int get_index_in_year() const;

        string get_name() const override;

        string to_string() const override;

        LunarMonth next(int n) const;

        /**
         * @brief 农历季节
         * @return 农历季节
         */
        LunarSeason get_season() const;

        /**
         * @brief 初一的儒略日
         * @return 儒略日
         */
        JulianDay get_first_julian_day() const;

        /**
         * @brief 是否闰月
         * @return true/false
         */
        bool is_leap() const;

        /**
         * @brief 周数
         * @param start 起始星期，1234560分别代表星期一至星期天
         * @return 周数
         */
        int get_week_count(int start) const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 太岁方位
         * @return 方位
         */
        Direction get_jupiter_direction() const;

        /**
         * @brief 逐月胎神
         * @return 逐月胎神
         */
        optional<FetusMonth> get_fetus() const;

        /**
         * @brief 小六壬
         * @return 小六壬
         */
        MinorRen get_minor_ren() const;

    protected:
        /**
         * @brief 农历年
         */
        LunarYear year;

        /**
         * @brief 月
         */
        int month;

        /**
         * @brief 是否闰月
         */
        bool leap;

        /**
         * @brief 天数
         */
        int day_count;

        /**
         * @brief 位于当年的索引，0-12
         */
        int index_in_year;

        /**
         * @brief 初一的儒略日
         */
        JulianDay first_julian_day;
    };

    /**
     * @brief 农历日
     */
    class LunarDay;

    /**
     * @brief 农历周
     */
    class LunarWeek : public AbstractCulture {
    public:
        ~LunarWeek() override = default;

        static const vector<string> NAMES;

        explicit LunarWeek(const int year, const int month, const int index, const int start) : AbstractCulture(), month(LunarMonth::from_ym(year, month)), start(Week::from_index(start)) {
            if (index < 0 || index > 5) {
                throw invalid_argument("illegal lunar week index: " + std::to_string(index));
            }
            if (start < 0 || start > 6) {
                throw invalid_argument("illegal lunar week start: " + std::to_string(start));
            }
            if (index >= this->month.get_week_count(start)) {
                throw invalid_argument("illegal lunar week index: " + std::to_string(index) + " in month: " + this->month.to_string());
            }
            this->index = index;
        }

        static LunarWeek from_ym(int year, int month, int index, int start);

        /**
         * @brief 农历月
         * @return 农历月
         */
        LunarMonth get_lunar_month() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 索引，0-5
         * @return 索引
         */
        int get_index() const;

        /**
         * @brief 起始星期
         * @return 星期
         */
        Week get_start() const;

        string get_name() const override;

        string to_string() const override;

        LunarWeek next(int n) const;

        bool equals(const LunarWeek &other) const;

        /**
         * @brief 本周第1天
         * @return 农历日
         */
        LunarDay get_first_day() const;

        /**
         * @brief 本周农历日列表
         * @return 农历日列表
         */
        vector<LunarDay> get_days() const;

    protected:
        /**
         * @brief 公历月
         */
        LunarMonth month;

        /**
         * @brief 索引，0-5
         */
        int index;

        /**
         * @brief 起始星期
         */
        Week start;
    };

    /**
     * @brief 逐日胎神
     */
    class FetusDay;

    /**
     * @brief 公历传统节日
     */
    class SolarFestival;
    /**
     * @brief 农历传统节日
     */
    class LunarFestival;

    /**
     * @brief 农历日
     */
    class LunarDay : public AbstractCulture {
    public:
        ~LunarDay() override = default;

        static const vector<string> NAMES;

        explicit LunarDay(const int year, const int month, const int day) : AbstractCulture(), month(LunarMonth::from_ym(year, month)), day(day) {
            if (day < 1 || day > this->month.get_day_count()) {
                throw invalid_argument("illegal day " + std::to_string(day) + " in " + this->month.to_string());
            }
        }

        static LunarDay from_ymd(int year, int month, int day);

        /**
         * @brief 农历月
         * @return 农历月
         */
        LunarMonth get_lunar_month() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 日
         * @return 日
         */
        int get_day() const;

        string get_name() const override;

        string to_string() const override;

        LunarDay next(int n) const;

        bool equals(const LunarDay &other) const;

        /**
         * @brief 是否在指定农历日之前
         * @param other 农历日
         * @return true/false
         */
        bool is_before(const LunarDay &other) const;

        /**
         * @brief 是否在指定农历日之后
         * @param other 农历日
         * @return true/false
         */
        bool is_after(const LunarDay &other) const;

        /**
         * @brief 星期
         * @return 星期
         */
        Week get_week() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        /**
         * @brief 建除十二值神
         * @return 建除十二值神
         */
        Duty get_duty() const;

        /**
         * @brief 黄道黑道十二神
         * @return 黄道黑道十二神
         */
        TwelveStar get_twelve_star() const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 太岁方位
         * @return 方位
         */
        Direction get_jupiter_direction() const;

        /**
         * @brief 逐日胎神
         * @return 逐日胎神
         */
        FetusDay get_fetus_day() const;

        /**
         * @brief 月相第几天
         * @return 月相第几天
         */
        PhaseDay get_phase_day() const;

        /**
         * @brief 月相
         * @return 月相
         */
        Phase get_phase() const;

        /**
         * @brief 六曜
         * @return 六曜
         */
        SixStar get_six_star() const;

        /**
         * @brief 公历日
         * @return 公历日
         */
        SolarDay get_solar_day() const;

        /**
         * @brief 干支日
         * @return 干支日
         */
        SixtyCycleDay get_sixty_cycle_day() const;

        /**
         * @brief 二十八宿
         * @return 二十八宿
         */
        TwentyEightStar get_twenty_eight_star() const;

        /**
         * @brief 神煞列表(吉神宜趋，凶神宜忌)
         * @return 神煞列表
         */
        vector<God> get_gods() const;

        /**
         * @brief 宜
         * @return 宜忌列表
         */
        vector<Taboo> get_recommends() const;

        /**
         * @brief 忌
         * @return 宜忌列表
         */
        vector<Taboo> get_avoids() const;

        /**
         * @brief 小六壬
         * @return 小六壬
         */
        MinorRen get_minor_ren() const;

        /**
         * @brief 农历传统节日
         * @return 农历传统节日，如果没有则返回空
         */
        optional<LunarFestival> get_festival() const;

    protected:
        /**
         * @brief 农历月
         */
        LunarMonth month;

        /**
         * @brief 日
         */
        int day;
    };

    /**
     * @brief 公历时刻
     */
    class SolarTime;

    /**
     * @brief 干支时辰
     */
    class SixtyCycleHour;

    /**
     * @brief 八字
     */
    class EightChar;

    /**
     * @brief 农历时辰
     */
    class LunarHour;

    /**
     * @brief 八字计算接口
     */
    class EightCharProvider {
    public:
        virtual ~EightCharProvider() = default;

        /**
         * @brief 八字
         * @param hour 农历时辰
         * @return 八字
         */
        virtual EightChar get_eight_char(LunarHour hour) const = 0;
    };

    /**
     * @brief 默认的八字计算（晚子时日柱算第二天）
     */
    class DefaultEightCharProvider : public EightCharProvider {
    public:
        EightChar get_eight_char(LunarHour hour) const override;
    };

    /**
     * @brief Lunar流派2的八字计算（晚子时日柱算当天）
     */
    class LunarSect2EightCharProvider : public EightCharProvider {
    public:
        EightChar get_eight_char(LunarHour hour) const override;
    };

    /**
     * @brief 农历时辰
     */
    class LunarHour : public AbstractCulture {
    public:
        ~LunarHour() override = default;

        /**
         * @brief 八字计算接口
         */
        static EightCharProvider *provider;

        explicit LunarHour(const int year, const int month, const int day, const int hour, const int minute, const int second) : AbstractCulture(), day(LunarDay::from_ymd(year, month, day)) {
            if (hour < 0 || hour > 23) {
                throw invalid_argument("illegal hour: " + std::to_string(hour));
            }
            if (minute < 0 || minute > 59) {
                throw invalid_argument("illegal minute: " + std::to_string(minute));
            }
            if (second < 0 || second > 59) {
                throw invalid_argument("illegal second: " + std::to_string(second));
            }
            this->hour = hour;
            this->minute = minute;
            this->second = second;
        }

        static LunarHour from_ymd_hms(int year, int month, int day, int hour, int minute, int second);

        /**
         * @brief 农历日
         * @return 农历日
         */
        LunarDay get_lunar_day() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 日
         * @return 日
         */
        int get_day() const;

        /**
         * @brief 时
         * @return 时
         */
        int get_hour() const;

        /**
         * @brief 分
         * @return 分
         */
        int get_minute() const;

        /**
         * @brief 秒
         * @return 秒
         */
        int get_second() const;

        string get_name() const override;

        string to_string() const override;

        LunarHour next(int n) const;

        /**
         * @brief 位于当天的索引
         * @return 索引
         */
        int get_index_in_day() const;

        /**
         * @brief 是否在指定农历时辰之前
         * @param other 农历时辰
         * @return true/false
         */
        bool is_before(const LunarHour &other) const;

        /**
         * @brief 是否在指定农历时辰之后
         * @param other 农历时辰
         * @return true/false
         */
        bool is_after(const LunarHour &other) const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        /**
         * @brief 黄道黑道十二神
         * @return 黄道黑道十二神
         */
        TwelveStar get_twelve_star() const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 公历时刻
         * @return 公历时刻
         */
        SolarTime get_solar_time() const;

        /**
         * @brief 干支时辰
         * @return 干支时辰
         */
        SixtyCycleHour get_sixty_cycle_hour() const;

        /**
         * @brief 宜
         * @return 宜忌列表
         */
        vector<Taboo> get_recommends() const;

        /**
         * @brief 忌
         * @return 宜忌列表
         */
        vector<Taboo> get_avoids() const;

        /**
         * @brief 小六壬
         * @return 小六壬
         */
        MinorRen get_minor_ren() const;

        /**
         * @brief 八字
         * @return 八字
         */
        EightChar get_eight_char() const;

    protected:
        /**
         * @brief 农历日
         */
        LunarDay day;

        /**
         * @brief 时
         */
        int hour;

        /**
         * @brief 分
         */
        int minute;

        /**
         * @brief 秒
         */
        int second;
    };

    /**
     * @brief 节气第几天
     */
    class SolarTermDay : public AbstractCulture {
    public:
        ~SolarTermDay() override = default;

        explicit SolarTermDay(const SolarTerm &solar_term, const int day_index) : solar_term(solar_term), day_index(day_index) {
        }

        SolarTerm get_solar_term() const;

        int get_day_index() const;

        string to_string() const override;

        string get_name() const override;
    protected:
        /**
         * @brief 节气
         */
        SolarTerm solar_term;

        /**
         * @brief 天索引
         */
        int day_index;
    };

    /**
     * @brief 公历周
     */
    class SolarWeek;

    /**
     * @brief 公历月
     */
    class SolarMonth;

    /**
     * @brief 公历季度
     */
    class SolarSeason;

    /**
     * @brief 公历半年
     */
    class SolarHalfYear;

    /**
     * @brief 公历年
     */
    class SolarYear : public AbstractCulture {
    public:
        ~SolarYear() override = default;

        explicit SolarYear(const int year) : AbstractCulture() {
            if (year < 1 || year > 9999) {
                throw invalid_argument("illegal solar year: " + std::to_string(year));
            }
            this->year = year;
        }

        static SolarYear from_year(int year);

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 天数（1582年355天，平年365天，闰年366天）
         * @return 天数
         */
        int get_day_count() const;

        /**
         * @brief 是否闰年(1582年以前，使用儒略历，能被4整除即为闰年。以后采用格里历，四年一闰，百年不闰，四百年再闰。)
         * @return true/false
         */
        bool is_leap() const;

        string get_name() const override;

        SolarYear next(int n) const;

        /**
         * @brief 月份列表，1年有12个月。
         * @return 月份列表
         */
        vector<SolarMonth> get_months() const;

        /**
         * @brief 季度列表，1年有4个季度。
         * @return 季度列表
         */
        vector<SolarSeason> get_seasons() const;

        /**
         * @brief 半年列表，1年有2个半年。
         * @return 半年列表
         */
        vector<SolarHalfYear> get_half_years() const;

    protected:
        /**
         * @brief 年
         */
        int year;
    };

    /**
     * @brief 公历半年
     */
    class SolarHalfYear : public AbstractCulture {
    public:
        ~SolarHalfYear() override = default;

        static const vector<string> NAMES;

        explicit SolarHalfYear(const int year, const int index) : AbstractCulture(), year(SolarYear::from_year(year)) {
            if (index < 0 || index > 1) {
                throw invalid_argument("illegal solar half year index: " + std::to_string(index));
            }
            this->index = index;
        }

        static SolarHalfYear from_index(int year, int index);

        /**
         * @brief 公历年
         * @return 公历年
         */
        SolarYear get_solar_year() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 索引
         * @return 索引，0-1
         */
        int get_index() const;

        string get_name() const override;

        string to_string() const override;

        SolarHalfYear next(int n) const;

        /**
         * @brief 季度列表，半年有2个季度。
         * @return 季度列表
         */
        vector<SolarSeason> get_seasons() const;

        /**
         * @brief 月份列表，半年有6个月。
         * @return 月份列表
         */
        vector<SolarMonth> get_months() const;

    protected:
        /**
         * @brief 年
         */
        SolarYear year;

        /**
         * @brief 索引，0-1
         */
        int index;
    };

    /**
     * @brief 公历季度
     */
    class SolarSeason : public AbstractCulture {
    public:
        ~SolarSeason() override = default;

        static const vector<string> NAMES;

        explicit SolarSeason(const int year, const int index) : AbstractCulture(), year(SolarYear::from_year(year)) {
            if (index < 0 || index > 3) {
                throw invalid_argument("illegal solar season index: " + std::to_string(index));
            }
            this->index = index;
        }

        static SolarSeason from_index(int year, int index);

        /**
         * @brief 公历年
         * @return 公历年
         */
        SolarYear get_solar_year() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 索引
         * @return 索引，0-3
         */
        int get_index() const;

        string get_name() const override;

        string to_string() const override;

        SolarSeason next(int n) const;

        /**
         * @brief 月份列表，1季度有3个月。
         * @return 月份列表
         */
        vector<SolarMonth> get_months() const;

    protected:
        /**
         * @brief 年
         */
        SolarYear year;

        /**
         * @brief 索引，0-3
         */
        int index;
    };

    /**
     * @brief 公历日
     */
    class SolarDay;

    /**
     * @brief 公历月
     */
    class SolarMonth : public AbstractCulture {
    public:
        ~SolarMonth() override = default;

        static const vector<string> NAMES;
        static const int DAYS[];

        explicit SolarMonth(const int year, const int month) : AbstractCulture(), year(SolarYear::from_year(year)) {
            if (month < 1 || month > 12) {
                throw invalid_argument("illegal solar month: " + std::to_string(month));
            }
            this->month = month;
        }

        static SolarMonth from_ym(int year, int month);

        /**
         * @brief 公历年
         * @return 公历年
         */
        SolarYear get_solar_year() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 天数（1582年10月只有21天)
         * @return 天数
         */
        int get_day_count() const;

        /**
         * @brief 位于当年的索引(0-11)
         * @return 索引
         */
        int get_index_in_year() const;

        /**
         * @brief 公历季度
         * @return 公历季度
         */
        SolarSeason get_season() const;

        /**
         * @brief 周数
         * @param start 起始星期，1234560分别代表星期一至星期天
         * @return 周数
         */
        int get_week_count(int start) const;

        string get_name() const override;

        string to_string() const override;

        SolarMonth next(int n) const;

        /**
         * @brief 本月的公历周列表
         * @param start 星期几作为一周的开始，1234560分别代表星期一至星期天
         * @return 公历周列表
         */
        vector<SolarWeek> get_weeks(int start) const;

        /**
         * @brief 本月的公历日列表
         * @return 公历日列表
         */
        vector<SolarDay> get_days() const;

    protected:
        /**
         * @brief 年
         */
        SolarYear year;

        /**
         * @brief 月
         */
        int month;
    };

    /**
     * @brief 候
     */
    class Phenology;

    /**
     * @brief 七十二候
     */
    class PhenologyDay;

    /**
     * @brief 藏历日，仅支持藏历1950年十二月初一（公历1951年1月8日）至藏历2050年十二月三十（公历2051年2月11日）
     */
    class RabByungDay;

    /**
     * @brief 公历日
     */
    class SolarDay : public AbstractCulture {
    public:
        ~SolarDay() override = default;

        static const vector<string> NAMES;

        explicit SolarDay(const int year, const int month, const int day) : AbstractCulture(), month(SolarMonth::from_ym(year, month)) {
            if (day < 1) {
                throw invalid_argument("illegal solar day: " + std::to_string(year) + "-" + std::to_string(month) + "-" + std::to_string(day));
            }
            if (1582 == year && 10 == month) {
                if ((day > 4 && day < 15) || day > 31) {
                    throw invalid_argument("illegal solar day: " + std::to_string(year) + "-" + std::to_string(month) + "-" + std::to_string(day));
                }
            } else if (day > this->month.get_day_count()) {
                throw invalid_argument("illegal solar day: " + std::to_string(year) + "-" + std::to_string(month) + "-" + std::to_string(day));
            }
            this->day = day;
        }

        static SolarDay from_ymd(int year, int month, int day);

        /**
         * @brief 公历月
         * @return 公历月
         */
        SolarMonth get_solar_month() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 日
         * @return 日
         */
        int get_day() const;

        /**
         * @brief 星期
         * @return 星期
         */
        Week get_week() const;

        /**
         * @brief 星座
         * @return 星座
         */
        Constellation get_constellation() const;

        string get_name() const override;

        string to_string() const override;

        SolarDay next(int n) const;

        /**
         * @brief 是否在指定公历日之前
         * @param other 公历日
         * @return true/false
         */
        bool is_before(const SolarDay &other) const;

        /**
         * @brief 是否在指定公历日之后
         * @param other 公历日
         * @return true/false
         */
        bool is_after(const SolarDay &other) const;

        bool equals(const SolarDay &other) const;

        /**
         * @brief 节气
         * @return 节气
         */
        SolarTerm get_term() const;

        /**
         * @brief 节气第几天
         * @return 节气第几天
         */
        SolarTermDay get_term_day() const;

        /**
         * @brief 公历周
         * @param start 起始星期，1234560分别代表星期一至星期天
         * @return 公历周
         */
        SolarWeek get_solar_week(int start) const;

        /**
         * @brief 候
         * @return 候
         */
        Phenology get_phenology() const;

        /**
         * @brief 七十二候
         * @return 七十二候
         */
        PhenologyDay get_phenology_day() const;

        /**
         * @brief 三伏天
         * @return 三伏天
         */
        optional<DogDay> get_dog_day() const;

        /**
         * @brief 数九天
         * @return 数九天
         */
        optional<NineDay> get_nine_day() const;

        /**
         * @brief 梅雨天（芒种后的第1个丙日入梅，小暑后的第1个未日出梅）
         * @return 梅雨天
         */
        optional<PlumRainDay> get_plum_rain_day() const;

        /**
         * @brief 人元司令分野
         * @return 人元司令分野
         */
        HideHeavenStemDay get_hide_heaven_stem_day() const;

        /**
         * @brief 位于当年的索引
         * @return 索引
         */
        int get_index_in_year() const;

        /**
         * @brief 公历日期相减，获得相差天数
         * @param other 公历日
         * @return 天数
         */
        int subtract(const SolarDay &other) const;

        /**
         * @brief 儒略日
         * @return 儒略日
         */
        JulianDay get_julian_day() const;

        /**
         * @brief 农历日
         * @return 农历日
         */
        LunarDay get_lunar_day() const;

        /**
         * @brief 干支日
         * @return 干支日
         */
        SixtyCycleDay get_sixty_cycle_day() const;

        /**
         * @brief 藏历日
         * @return 藏历日
         */
        RabByungDay get_rab_byung_day() const;

        /**
         * @brief 公历节日
         * @return 公历节日
         */
        optional<SolarFestival> get_festival() const;

        /**
         * @brief 月相第几天
         * @return 月相第几天
         */
        PhaseDay get_phase_day() const;

        /**
         * @brief 月相
         * @return 月相
         */
        Phase get_phase() const;

    protected:
        /**
         * @brief 公历月
         */
        SolarMonth month;

        /**
         * @brief 日
         */
        int day;
    };

    /**
     * @brief 公历周
     */
    class SolarWeek : public AbstractCulture {
    public:
        ~SolarWeek() override = default;

        static const vector<string> NAMES;

        explicit SolarWeek(const int year, const int month, const int index, const int start) : AbstractCulture(), month(SolarMonth::from_ym(year, month)), start(Week::from_index(start)) {
            if (index < 0 || index > 5) {
                throw invalid_argument("illegal solar week index: " + std::to_string(index));
            }
            if (start < 0 || start > 6) {
                throw invalid_argument("illegal solar week start: " + std::to_string(start));
            }
            if (index >= this->month.get_week_count(start)) {
                throw invalid_argument("illegal solar week index: " + std::to_string(index) + " in month: " + this->month.to_string());
            }
            this->index = index;
        }

        static SolarWeek from_ym(int year, int month, int index, int start);

        /**
         * @brief 公历月
         * @return 公历月
         */
        SolarMonth get_solar_month() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 索引，0-5
         * @return 索引
         */
        int get_index() const;

        /**
         * @brief 位于当年的索引
         * @return 索引
         */
        int get_index_in_year() const;

        /**
         * @brief 起始星期
         * @return 星期
         */
        Week get_start() const;

        string get_name() const override;

        string to_string() const override;

        SolarWeek next(int n) const;

        bool equals(const SolarWeek &other) const;

        /**
         * @brief 本周第1天
         * @return 公历日
         */
        SolarDay get_first_day() const;

        /**
         * @brief 本周公历日列表
         * @return 公历日列表
         */
        vector<SolarDay> get_days() const;

    protected:
        /**
         * @brief 公历月
         */
        SolarMonth month;

        /**
         * @brief 索引，0-5
         */
        int index;

        /**
         * @brief 起始星期
         */
        Week start;
    };

    /**
     * @brief 干支时辰
     */
    class SixtyCycleHour;

    /**
     * @brief 公历时刻
     */
    class SolarTime : public AbstractCulture {
    public:
        ~SolarTime() override = default;

        SolarTime(const SolarTime &other): day(other.day), hour(other.hour), minute(other.minute), second(other.second) {
        }

        SolarTime &operator=(const SolarTime &other);

        explicit SolarTime(const int year, const int month, const int day, const int hour, const int minute, const int second) : AbstractCulture(), day(SolarDay::from_ymd(year, month, day)) {
            if (hour < 0 || hour > 23) {
                throw invalid_argument("illegal hour: " + std::to_string(hour));
            }
            if (minute < 0 || minute > 59) {
                throw invalid_argument("illegal minute: " + std::to_string(minute));
            }
            if (second < 0 || second > 59) {
                throw invalid_argument("illegal second: " + std::to_string(second));
            }
            this->hour = hour;
            this->minute = minute;
            this->second = second;
        }

        static SolarTime from_ymd_hms(int year, int month, int day, int hour, int minute, int second);

        /**
         * @brief 公历日
         * @return 公历日
         */
        SolarDay get_solar_day() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 日
         * @return 日
         */
        int get_day() const;

        /**
         * @brief 时
         * @return 时
         */
        int get_hour() const;

        /**
         * @brief 分
         * @return 分
         */
        int get_minute() const;

        /**
         * @brief 秒
         * @return 秒
         */
        int get_second() const;

        string get_name() const override;

        string to_string() const override;

        SolarTime next(int n) const;

        /**
         * @brief 是否在指定公历日之前
         * @param other 公历日
         * @return true/false
         */
        bool is_before(const SolarTime &other) const;

        /**
         * @brief 是否在指定公历日之后
         * @param other 公历日
         * @return true/false
         */
        bool is_after(const SolarTime &other) const;

        bool equals(const SolarTime &other) const;

        /**
         * @brief 节气
         * @return 节气
         */
        SolarTerm get_term() const;

        /**
         * @brief 候
         * @return 候
         */
        Phenology get_phenology() const;

        /**
         * @brief 公历时刻相减，获得相差秒数
         * @param other 公历时刻
         * @return 秒数
         */
        int subtract(const SolarTime &other) const;

        /**
         * @brief 儒略日
         * @return 儒略日
         */
        JulianDay get_julian_day() const;

        /**
         * @brief 干支时辰
         * @return 干支时辰
         */
        SixtyCycleHour get_sixty_cycle_hour() const;

        /**
         * @brief 农历时辰
         * @return 农历时辰
         */
        LunarHour get_lunar_hour() const;

        /**
         * @brief 月相
         * @return 月相
         */
        Phase get_phase() const;

    protected:
        /**
         * @brief 公历日
         */
        SolarDay day;

        /**
         * @brief 时
         */
        int hour;

        /**
         * @brief 分
         */
        int minute;

        /**
         * @brief 秒
         */
        int second;
    };

    /**
     * @brief 八字
     */
    class EightChar : public AbstractCulture {
    public:
        ~EightChar() override = default;

        explicit EightChar(const SixtyCycle &year, const SixtyCycle &month, const SixtyCycle &day, const SixtyCycle &hour) : AbstractCulture(), year(year), month(month), day(day), hour(hour) {
        }

        explicit EightChar(const string &year, const string &month, const string &day, const string &hour) : AbstractCulture(), year(SixtyCycle(year)), month(SixtyCycle(month)), day(SixtyCycle(day)), hour(SixtyCycle(hour)) {
        }

        /**
         * @brief 年柱
         * @return 年柱
         */
        SixtyCycle get_year() const;

        /**
         * @brief 月柱
         * @return 月柱
         */
        SixtyCycle get_month() const;

        /**
         * @brief 日柱
         * @return 日柱
         */
        SixtyCycle get_day() const;

        /**
         * @brief 时柱
         * @return 时柱
         */
        SixtyCycle get_hour() const;

        /**
         * @brief 胎元
         * @return 胎元
         */
        SixtyCycle get_fetal_origin() const;

        /**
         * @brief 胎息
         * @return 胎息
         */
        SixtyCycle get_fetal_breath() const;

        /**
         * @brief 命宫
         * @return 命宫
         */
        SixtyCycle get_own_sign() const;

        /**
         * @brief 身宫
         * @return 身宫
         */
        SixtyCycle get_body_sign() const;

        /**
         * @brief 公历时刻列表
         * @param start_year 开始年(含)，支持1-9999年
         * @param end_year 结束年(含)，支持1-9999年
         * @return 公历时刻列表
         */
        vector<SolarTime> get_solar_times(int start_year, int end_year) const;

        string get_name() const override;

    protected:
        /**
         * @brief 年柱
         */
        SixtyCycle year;

        /**
         * @brief 月柱
         */
        SixtyCycle month;

        /**
         * @brief 日柱
         */
        SixtyCycle day;

        /**
         * @brief 时柱
         */
        SixtyCycle hour;
    };

    /**
     * @brief 灶马头(灶神的坐骑)
     */
    class KitchenGodSteed : public AbstractCulture {
    public:
        ~KitchenGodSteed() override = default;

        static const vector<string> NUMBERS;

        explicit KitchenGodSteed(const int lunar_year) : AbstractCulture(), first_day_sixty_cycle(LunarDay::from_ymd(lunar_year, 1, 1).get_sixty_cycle()) {
        }

        static KitchenGodSteed from_lunar_year(int lunar_year);

        /**
         * @brief 几鼠偷粮
         * @return 几鼠偷粮
         */
        string get_mouse() const;

        /**
         * @brief 草子几分
         * @return 草子几分
         */
        string get_grass() const;

        /**
         * @brief 几牛耕田（正月第一个丑日是初几，就是几牛耕田）
         * @return 几牛耕田
         */
        string get_cattle() const;

        /**
         * @brief 花收几分
         * @return 花收几分
         */
        string get_flower() const;

        /**
         * @brief 几龙治水（正月第一个辰日是初几，就是几龙治水）
         * @return 几龙治水
         */
        string get_dragon() const;

        /**
         * @brief 几马驮谷
         * @return 几马驮谷
         */
        string get_horse() const;

        /**
         * @brief 几鸡抢米
         * @return 几鸡抢米
         */
        string get_chicken() const;

        /**
         * @brief 几姑看蚕
         * @return 几姑看蚕
         */
        string get_silkworm() const;

        /**
         * @brief 几屠共猪
         * @return 几屠共猪
         */
        string get_pig() const;

        /**
         * @brief 甲田几分
         * @return 甲田几分
         */
        string get_field() const;

        /**
         * @brief 几人分饼（正月第一个丙日是初几，就是几人分饼）
         * @return 几人分饼
         */
        string get_cake() const;

        /**
         * @brief 几日得金（正月第一个辛日是初几，就是几日得金）
         * @return 几日得金
         */
        string get_gold() const;

        /**
         * @brief 几人几丙
         * @return 几人几丙
         */
        string get_people_cakes() const;

        /**
         * @brief 几人几锄
         * @return 几人几锄
         */
        string get_people_hoes() const;

        string get_name() const override;

    protected:
        /**
         * @brief 正月初一的干支
         */
        SixtyCycle first_day_sixty_cycle;

        string by_heaven_stem(int n) const;

        string by_earth_branch(int n) const;
    };

    /**
     * @brief 逐月胎神（正十二月在床房，二三九十门户中，四六十一灶勿犯，五甲七子八厕凶。）
     */
    class FetusMonth : public LoopTyme {
    public:
        ~FetusMonth() override = default;

        static const vector<string> NAMES;

        explicit FetusMonth(const int index) : LoopTyme(NAMES, index) {
        }

        static optional<FetusMonth> from_lunar_month(const LunarMonth &lunar_month);

        FetusMonth next(int n) const;
    };

    /**
     * @brief 彭祖百忌
     */
    class PengZu : public AbstractCulture {
    public:
        ~PengZu() override = default;

        explicit PengZu(const SixtyCycle &sixty_cycle) : peng_zu_heaven_stem(PengZuHeavenStem::from_index(sixty_cycle.get_heaven_stem().get_index())), peng_zu_earth_branch(PengZuEarthBranch::from_index(sixty_cycle.get_earth_branch().get_index())) {
        }

        static PengZu from_sixty_cycle(const SixtyCycle &sixty_cycle);

        string get_name() const override;

        /**
         * @brief 天干彭祖百忌
         * @return 天干彭祖百忌
         */
        PengZuHeavenStem get_peng_zu_heaven_stem() const;

        /**
         * @brief 地支彭祖百忌
         * @return 地支彭祖百忌
         */
        PengZuEarthBranch get_peng_zu_earth_branch() const;

    protected:
        /**
         * @brief 天干彭祖百忌
         */
        PengZuHeavenStem peng_zu_heaven_stem;

        /**
         * @brief 地支彭祖百忌
         */
        PengZuEarthBranch peng_zu_earth_branch;
    };

    /**
     * @brief 干支时辰
     */
    class SixtyCycleHour;
    /**
     * @brief 干支日（立春换年，节令换月）
     */
    class SixtyCycleDay : public AbstractCulture {
    public:
        ~SixtyCycleDay() override = default;

        SixtyCycleDay(const SixtyCycleDay &other): solar_day(other.solar_day), month(other.month), day(other.day) {
        }

        SixtyCycleDay &operator=(const SixtyCycleDay &other);

        explicit SixtyCycleDay(const SolarDay &solar_day, const SixtyCycleMonth &month, const SixtyCycle &day) : AbstractCulture(), solar_day(solar_day), month(month), day(day) {
        }

        explicit SixtyCycleDay(const SolarDay &solar_day) : AbstractCulture(), solar_day(solar_day) {
            const int solar_year = solar_day.get_year();
            const SolarDay spring_solar_day = SolarTerm::from_index(solar_year, 3).get_julian_day().get_solar_day();
            const LunarDay lunar_day = solar_day.get_lunar_day();
            LunarYear lunar_year = lunar_day.get_lunar_month().get_lunar_year();
            if (lunar_year.get_year() == solar_year) {
                if (solar_day.is_before(spring_solar_day)) {
                    lunar_year = lunar_year.next(-1);
                }
            } else if (lunar_year.get_year() < solar_year) {
                if (!solar_day.is_before(spring_solar_day)) {
                    lunar_year = lunar_year.next(1);
                }
            }
            const SolarTerm term = solar_day.get_term();
            int index = term.get_index() - 3;
            if (index < 0 && term.get_julian_day().get_solar_day().is_after(spring_solar_day)) {
                index += 24;
            }
            this->month = SixtyCycleMonth(SixtyCycleYear::from_year(lunar_year.get_year()), LunarMonth::from_ym(solar_year, 1).get_sixty_cycle().next(static_cast<int>(std::floor(index * 1.0 / 2))));
            this->day = lunar_day.get_sixty_cycle();
        }

        static SixtyCycleDay from_solar_day(const SolarDay &solar_day);

        /**
         * @brief 公历日
         * @return 公历日
         */
        SolarDay get_solar_day() const;

        /**
         * @brief 干支月
         * @return 干支月
         */
        SixtyCycleMonth get_sixty_cycle_month() const;

        /**
         * @brief 年柱
         * @return 年柱
         */
        SixtyCycle get_year() const;

        /**
         * @brief 月柱
         * @return 月柱
         */
        SixtyCycle get_month() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        string get_name() const override;

        string to_string() const override;

        /**
         * @brief 推移
         * @param n 推移天数
         * @return 干支日
         */
        SixtyCycleDay next(int n) const;

        /**
         * @brief 建除十二值神
         * @return 建除十二值神
         */
        Duty get_duty() const;

        /**
         * @brief 黄道黑道十二神
         * @return 黄道黑道十二神
         */
        TwelveStar get_twelve_star() const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 太岁方位
         * @return 方位
         */
        Direction get_jupiter_direction() const;

        /**
         * @brief 逐日胎神
         * @return 逐日胎神
         */
        FetusDay get_fetus_day() const;

        /**
         * @brief 二十八宿
         * @return 二十八宿
         */
        TwentyEightStar get_twenty_eight_star() const;

        /**
         * @brief 神煞列表(吉神宜趋，凶神宜忌)
         * @return 神煞列表
         */
        vector<God> get_gods() const;

        /**
         * @brief 宜
         * @return 宜忌列表
         */
        vector<Taboo> get_recommends() const;

        /**
         * @brief 忌
         * @return 宜忌列表
         */
        vector<Taboo> get_avoids() const;

        /**
         * @brief 干支时辰列表
         * @return 干支时辰列表
         */
        vector<SixtyCycleHour> get_hours() const;

    protected:
        /**
         * @brief 公历日
         */
        SolarDay solar_day;

        /**
         * @brief 干支月
         */
        optional<SixtyCycleMonth> month;

        /**
         * @brief 日柱
         */
        optional<SixtyCycle> day;
    };

    /**
     * @brief 干支时辰（立春换年，节令换月，23点换日）
     */
    class SixtyCycleHour : public AbstractCulture {
    public:
        ~SixtyCycleHour() override = default;

        explicit SixtyCycleHour(const SolarTime &solar_time) : AbstractCulture(), solar_time(solar_time) {
            const int solar_year = solar_time.get_year();
            const SolarTime spring_solar_time = SolarTerm::from_index(solar_year, 3).get_julian_day().get_solar_time();
            const LunarHour lunar_hour = solar_time.get_lunar_hour();
            const LunarDay lunar_day = lunar_hour.get_lunar_day();
            LunarYear lunar_year = lunar_day.get_lunar_month().get_lunar_year();
            if (lunar_year.get_year() == solar_year) {
                if (solar_time.is_before(spring_solar_time)) {
                    lunar_year = lunar_year.next(-1);
                }
            } else if (lunar_year.get_year() < solar_year) {
                if (!solar_time.is_before(spring_solar_time)) {
                    lunar_year = lunar_year.next(1);
                }
            }

            SolarTerm term = solar_time.get_term();
            int index = term.get_index() - 3;
            if (index < 0 && term.get_julian_day().get_solar_time().is_after(SolarTerm::from_index(solar_year, 3).get_julian_day().get_solar_time())) {
                index += 24;
            }
            SixtyCycle d = lunar_day.get_sixty_cycle();
            if (solar_time.get_hour() >= 23) {
                d = d.next(1);
            }
            day = SixtyCycleDay(solar_time.get_solar_day(), SixtyCycleMonth(SixtyCycleYear::from_year(lunar_year.get_year()), LunarMonth::from_ym(solar_year, 1).get_sixty_cycle().next(static_cast<int>(std::floor(index * 0.5)))), d);
            hour = lunar_hour.get_sixty_cycle();
        }

        static SixtyCycleHour from_solar_time(const SolarTime &solar_time);

        /**
         * @brief 年柱
         * @return 年柱
         */
        SixtyCycle get_year() const;

        /**
         * @brief 月柱
         * @return 月柱
         */
        SixtyCycle get_month() const;

        /**
         * @brief 日柱
         * @return 日柱
         */
        SixtyCycle get_day() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        /**
         * @brief 干支日
         * @return 干支日
         */
        SixtyCycleDay get_sixty_cycle_day() const;

        /**
         * @brief 公历时刻
         * @return 公历时刻
         */
        SolarTime get_solar_time() const;

        string get_name() const override;

        string to_string() const override;

        SixtyCycleHour next(int n) const;

        /**
         * @brief 位于当天的索引
         * @return 索引
         */
        int get_index_in_day() const;

        /**
         * @brief 九星
         * @return 九星
         */
        NineStar get_nine_star() const;

        /**
         * @brief 黄道黑道十二神
         * @return 黄道黑道十二神
         */
        TwelveStar get_twelve_star() const;

        /**
         * @brief 宜
         * @return 宜忌列表
         */
        vector<Taboo> get_recommends() const;

        /**
         * @brief 忌
         * @return 宜忌列表
         */
        vector<Taboo> get_avoids() const;

        /**
         * @brief 八字
         * @return 八字
         */
        EightChar get_eight_char() const;

    protected:
        /**
         * @brief 公历时刻
         */
        SolarTime solar_time;

        /**
         * @brief 干支日
         */
        optional<SixtyCycleDay> day;

        /**
         * @brief 时柱
         */
        optional<SixtyCycle> hour;
    };

    /**
     * @brief 逐日胎神
     */
    class FetusDay : public AbstractCulture {
    public:
        ~FetusDay() override = default;

        explicit FetusDay(const SixtyCycle &sixty_cycle) : AbstractCulture(), fetus_heaven_stem(FetusHeavenStem(sixty_cycle.get_heaven_stem().get_index() % 5)), fetus_earth_branch(FetusEarthBranch(sixty_cycle.get_earth_branch().get_index() % 6)) {
            constexpr int indices[] = {3, 3, 8, 8, 8, 8, 8, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, -9, -9, -9, -9, -9, -5, -5, -1, -1, -1, -3, -7, -7, -7, -7, -5, 7, 7, 7, 7, 7, 7, 2, 2, 2, 2, 2, 3, 3, 3, 3};
            const int index = indices[sixty_cycle.get_index()];
            side = index < 0 ? Side::IN : Side::OUT;
            direction = Direction::from_index(index);
        }

        explicit FetusDay(const SixtyCycleDay &sixty_cycle_day) : FetusDay(sixty_cycle_day.get_sixty_cycle()) {
        }

        explicit FetusDay(const LunarDay &lunar_day) : FetusDay(lunar_day.get_sixty_cycle()) {
        }

        static FetusDay from_sixty_cycle_day(const SixtyCycleDay &sixty_cycle_day);

        static FetusDay from_lunar_day(const LunarDay &lunar_day);

        string get_name() const override;

        /**
         * @brief 内外
         * @return 内外
         */
        Side get_side() const;

        /**
         * @brief 方位
         * @return 方位
         */
        Direction get_direction() const;

        /**
         * @brief 天干六甲胎神
         * @return 天干六甲胎神
         */
        FetusHeavenStem get_fetus_heaven_stem() const;

        /**
         * @brief 地支六甲胎神
         * @return 地支六甲胎神
         */
        FetusEarthBranch get_fetus_earth_branch() const;

    protected:
        /**
         * @brief 天干六甲胎神
         */
        FetusHeavenStem fetus_heaven_stem;

        /**
         * @brief 地支六甲胎神
         */
        FetusEarthBranch fetus_earth_branch;

        /**
         * @brief 内外
         */
        Side side;

        /**
         * @brief 方位
         */
        Direction direction = Direction::from_index(0);
    };

    /**
     * @brief 候
     */
    class Phenology : public LoopTyme {
    public:
        ~Phenology() override = default;

        static const vector<string> NAMES;

        explicit Phenology(const int year, const int index) : LoopTyme(NAMES, index) {
            this->year = year;
        }

        explicit Phenology(const int year, const string &name) : LoopTyme(NAMES, name) {
            const int size = get_size();
            this->year = (year * size + index) / size;
        }

        static Phenology from_index(int year, int index);

        static Phenology from_name(int year, const string &name);

        Phenology next(int n) const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 三候
         * @return 三候
         */
        ThreePhenology get_three_phenology() const;

        /**
         * @brief 儒略日
         * @return 儒略日
         */
        JulianDay get_julian_day() const;

    protected:
        /**
         * @brief 年
         */
        int year;
    };

    /**
     * @brief 七十二候
     */
    class PhenologyDay : public AbstractCulture {
    public:
        ~PhenologyDay() override = default;

        explicit PhenologyDay(const Phenology &phenology, const int day_index) : phenology(phenology), day_index(day_index) {
        }

        Phenology get_phenology() const;

        int get_day_index() const;

        string to_string() const override;

        string get_name() const override;
    protected:
        /**
         * @brief 候
         */
        Phenology phenology;

        /**
         * @brief 天索引
         */
        int day_index;
    };

    /**
     * @brief 童限信息
     */
    class ChildLimitInfo {
    public:
        ~ChildLimitInfo() = default;

        explicit ChildLimitInfo(const SolarTime &start_time, const SolarTime &end_time, const int year_count, const int month_count, const int day_count, const int hour_count, const int minute_count): start_time(start_time), end_time(end_time), year_count(year_count), month_count(month_count), day_count(day_count), hour_count(hour_count), minute_count(minute_count) {
        }

        /**
         * @brief 开始(即出生)的公历时刻
         * @return 开始(即出生)的公历时刻
         */
        SolarTime get_start_time() const;

        /**
         * @brief 结束(即开始起运)的公历时刻
         * @return 结束(即开始起运)的公历时刻
         */
        SolarTime get_end_time() const;

        /**
         * @brief 年数
         * @return 年数
         */
        int get_year_count() const;

        /**
         * @brief 月数
         * @return 月数
         */
        int get_month_count() const;

        /**
         * @brief 日数
         * @return 日数
         */
        int get_day_count() const;

        /**
         * @brief 小时数
         * @return 小时数
         */
        int get_hour_count() const;

        /**
         * @brief 分钟数
         * @return 分钟数
         */
        int get_minute_count() const;

    protected:
        /**
         * @brief 开始(即出生)的公历时刻
         */
        SolarTime start_time;

        /**
         * @brief 结束(即开始起运)的公历时刻
         */
        SolarTime end_time;

        /**
         * @brief 年数
         */
        int year_count;

        /**
         * @brief 月数
         */
        int month_count;

        /**
         * @brief 日数
         */
        int day_count;

        /**
         * @brief 小时数
         */
        int hour_count;

        /**
         * @brief 分钟数
         */
        int minute_count;
    };

    /**
     * @brief 童限计算接口
     */
    class ChildLimitProvider {
    public:
        virtual ~ChildLimitProvider() = default;

        /**
         * @brief 童限信息
         * @param birth_time 出生公历时刻
         * @param term 节令
         * @return 童限信息
         */
        virtual ChildLimitInfo get_info(SolarTime birth_time, SolarTerm term) const = 0;
    };

    /**
     * @brief 童限计算抽象
     */
    class AbstractChildLimitProvider : public ChildLimitProvider {
    public:
        ChildLimitInfo next(const SolarTime &birth_time, int add_year, int add_month, int add_day, int add_hour, int add_minute, int add_second) const;
    };

    /**
     * @brief 默认的童限计算
     */
    class DefaultChildLimitProvider : public AbstractChildLimitProvider {
    public:
        ChildLimitInfo get_info(SolarTime birth_time, SolarTerm term) const override;
    };

    /**
     * @brief 元亨利贞的童限计算
     */
    class China95ChildLimitProvider : protected AbstractChildLimitProvider {
    public:
        ChildLimitInfo get_info(SolarTime birth_time, SolarTerm term) const override;
    };

    /**
     * @brief Lunar的流派1童限计算（按天数和时辰数计算，3天1年，1天4个月，1时辰10天）
     */
    class LunarSect1ChildLimitProvider : protected AbstractChildLimitProvider {
    public:
        ChildLimitInfo get_info(SolarTime birth_time, SolarTerm term) const override;
    };

    /**
     * @brief Lunar的流派2童限计算（按分钟数计算）
     */
    class LunarSect2ChildLimitProvider : protected AbstractChildLimitProvider {
    public:
        ChildLimitInfo get_info(SolarTime birth_time, SolarTerm term) const override;
    };

    /**
     * @brief 大运
     */
    class DecadeFortune;

    /**
     * @brief 小运
     */
    class Fortune;

    /**
     * @brief 童限
     */
    class ChildLimit {
    public:
        /**
         * @brief 童限计算接口
         */
        static ChildLimitProvider *provider;

        ~ChildLimit() = default;

        explicit ChildLimit(const SolarTime &birth_time, const Gender gender): eight_char(birth_time.get_lunar_hour().get_eight_char()), gender(gender), forward(get_forward(eight_char, gender)), info(get_info(birth_time, forward)) {
        }

        static ChildLimit from_solar_time(const SolarTime &birth_time, Gender gender);

        /**
         * @brief 八字
         * @return 八字
         */
        EightChar get_eight_char() const;

        /**
         * @brief 性别
         * @return 性别
         */
        Gender get_gender() const;

        /**
         * @brief 是否顺推
         * @return true/false
         */
        bool is_forward() const;

        /**
         * @brief 年数
         * @return 年数
         */
        int get_year_count() const;

        /**
         * @brief 月数
         * @return 月数
         */
        int get_month_count() const;

        /**
         * @brief 日数
         * @return 日数
         */
        int get_day_count() const;

        /**
         * @brief 小时数
         * @return 小时数
         */
        int get_hour_count() const;

        /**
         * @brief 分钟数
         * @return 分钟数
         */
        int get_minute_count() const;

        /**
         * @brief 开始(即出生)的公历时刻
         * @return 公历时刻
         */
        SolarTime get_start_time() const;

        /**
         * @brief 结束(即开始起运)的公历时刻
         * @return 公历时刻
         */
        SolarTime get_end_time() const;

        /**
         * @brief 起运大运
         * @return 大运
         */
        DecadeFortune get_start_decade_fortune() const;

        /**
         * @brief 所属大运
         * @return 大运
         */
        DecadeFortune get_decade_fortune() const;

        /**
         * @brief 小运
         * @return 小运
         */
        Fortune get_start_fortune() const;

        /**
         * @brief 开始(即出生)干支年
         * @return 干支年
         */
        SixtyCycleYear get_start_sixty_cycle_year() const;

        /**
         * @brief 结束(即起运)干支年
         * @return 干支年
         */
        SixtyCycleYear get_end_sixty_cycle_year() const;

        /**
         * @brief 开始年龄
         * @return 开始年龄
         */
        int get_start_age() const;

        /**
         * @brief 结束年龄
         * @return 结束年龄
         */
        int get_end_age() const;

    protected:
        /**
         * @brief 八字
         */
        EightChar eight_char;

        /**
         * @brief 性别
         */
        Gender gender;

        /**
         * @brief 顺逆
         */
        bool forward;

        /**
         * @brief 童限信息
         */
        ChildLimitInfo info;

    private:
        bool get_forward(const EightChar &eight_char, Gender gender);

        ChildLimitInfo get_info(const SolarTime &birth_time, bool forward);
    };

    /**
     * @brief 小运
     */
    class Fortune : public AbstractCulture {
    public:
        ~Fortune() override = default;

        explicit Fortune(const ChildLimit &child_limit, const int index): child_limit(child_limit), index(index) {
        }

        static Fortune from_child_limit(const ChildLimit &child_limit, int index);

        /**
         * @brief 年龄
         * @return 年龄
         */
        int get_age() const;

        /**
         * @brief 干支年
         * @return 干支年
         */
        SixtyCycleYear get_sixty_cycle_year() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        string get_name() const override;

        Fortune next(int n) const;

    protected:
        /**
         * @brief 童限
         */
        ChildLimit child_limit;

        /**
         * @brief 序号
         */
        int index;
    };

    /**
     * @brief 大运
     */
    class DecadeFortune : public AbstractCulture {
    public:
        ~DecadeFortune() override = default;

        explicit DecadeFortune(const ChildLimit &child_limit, int index): child_limit(child_limit), index(index) {
        }

        static DecadeFortune from_child_limit(const ChildLimit &child_limit, int index);

        /**
         * @brief 开始年龄
         * @return 开始年龄
         */
        int get_start_age() const;

        /**
         * @brief 结束年龄
         * @return 结束年龄
         */
        int get_end_age() const;

        /**
         * @brief 开始干支年
         * @return 干支年
         */
        SixtyCycleYear get_start_sixty_cycle_year() const;

        /**
         * @brief 结束干支年
         * @return 干支年
         */
        SixtyCycleYear get_end_sixty_cycle_year() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        string get_name() const override;

        DecadeFortune next(int n) const;

        /**
         * @brief 开始小运
         * @return 小运
         */
        Fortune get_start_fortune() const;

    protected:
        /**
         * @brief 童限
         */
        ChildLimit child_limit;

        /**
         * @brief 序号
         */
        int index;
    };

    /**
     * @brief 法定假日（自2001-12-29起）
     */
    class LegalHoliday : public AbstractCulture {
    public:
        ~LegalHoliday() override = default;

        static const vector<string> NAMES;
        static string DATA;

        explicit LegalHoliday(const int year, const int month, const int day, const string &data): day(SolarDay::from_ymd(year, month, day)), name(NAMES[data[9] - '0']), work(data[8] == '0'), target(compute_target(data)) {
        }

        static optional<LegalHoliday> from_ymd(int year, int month, int day);

        SolarDay get_day() const;

        SolarDay get_target() const;

        bool is_work() const;

        optional<LegalHoliday> next(int n) const;

        string to_string() const override;

        string get_name() const override;

    protected:
        /**
         * @brief 公历日
         */
        SolarDay day;

        /**
         * @brief 名称
         */
        string name;

        /**
         * @brief 是否上班
         */
        bool work;

        /**
         * @brief 节假日当天的公历日
         */
        SolarDay target;

    private:
        SolarDay compute_target(const string &data) const;
    };

    /**
     * @brief 藏历五行
     */
    class RabByungElement : public Element {
    public:
        ~RabByungElement() override = default;

        explicit RabByungElement(const int index) : Element(index) {
        }

        explicit RabByungElement(const string &name) : Element(regex_replace(name, regex("铁"), "金")) {
        }

        static RabByungElement from_index(int index);

        static RabByungElement from_name(const string &name);

        string get_name() const override;

        RabByungElement next(int n) const;

        bool equals(const RabByungElement &other) const;

        /**
         * @brief 我生者
         * @return 五行
         */
        RabByungElement get_reinforce() const;

        /**
         * @brief 我克者
         * @return 五行
         */
        RabByungElement get_restrain() const;

        /**
         * @brief 生我者
         * @return 五行
         */
        RabByungElement get_reinforced() const;

        /**
         * @brief 克我者
         * @return 五行
         */
        RabByungElement get_restrained() const;

        /**
         * @brief 方位
         * @return 方位
         */
        Direction get_direction() const;
    };

    /**
     * @brief 藏历月，仅支持藏历1950年十二月至藏历2050年十二月
     */
    class RabByungMonth;

    /**
     * @brief 藏历年(公历1027年为藏历元年，第一饶迥火兔年）
     */
    class RabByungYear : public AbstractCulture {
    public:
        ~RabByungYear() override = default;

        explicit RabByungYear(const int rab_byung_index, const SixtyCycle& sixty_cycle): AbstractCulture(), rab_byung_index(rab_byung_index), sixty_cycle(sixty_cycle) {
            if (rab_byung_index < 0 || rab_byung_index > 150) {
                throw invalid_argument("illegal rab-byung index: " + std::to_string(rab_byung_index));
            }
        }

        static RabByungYear from_sixty_cycle(int rab_byung_index, const SixtyCycle& sixty_cycle);

        static RabByungYear from_element_zodiac(int rab_byung_index, const RabByungElement& element, const Zodiac& zodiac);

        static RabByungYear from_year(int year);

        /**
         * @brief 饶迥序号
         * @return 数字，从0开始
         */
        int get_rab_byung_index() const;

        /**
         * @brief 干支
         * @return 干支
         */
        SixtyCycle get_sixty_cycle() const;

        /**
         * @brief 生肖
         * @return 生肖
         */
        Zodiac get_zodiac() const;

        /**
         * @brief 五行
         * @return 藏历五行
         */
        RabByungElement get_element() const;

        string get_name() const override;

        RabByungYear next(int n) const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 闰月
         * @return 闰月数字，1代表闰1月，0代表无闰月
         */
        int get_leap_month() const;

        /**
         * @brief 公历年
         * @return 公历年
         */
        SolarYear get_solar_year() const;

        /**
         * @brief 月份数量
         * @return 数量
         */
        int get_month_count() const;

        /**
         * @brief 首月
         * @return 藏历月
         */
        RabByungMonth get_first_month() const;

        /**
         * @brief 藏历月列表
         * @return 藏历月列表
         */
        vector<RabByungMonth> get_months() const;
    protected:
        /**
         * @brief 饶迥(胜生周)序号，从0开始
         */
        int rab_byung_index;

        /**
         * @brief 干支
         */
        SixtyCycle sixty_cycle;
    };

    /**
     * @brief 藏历月，仅支持藏历1950年十二月至藏历2050年十二月
     */
    class RabByungMonth : public AbstractCulture {
    public:
        ~RabByungMonth() override = default;

        static const vector<string> NAMES;
        static const vector<string> ALIAS;
        static std::map<int, vector<int>> DAYS;

        explicit RabByungMonth(const RabByungYear& year, const int month): AbstractCulture(), year(year), month(month), leap(month < 0) {
            static once_flag flag;
            call_once(flag, [] {
                int y = 1950;
                int m = 11;
                istringstream years(R"(2c>,182[>1:2TA4ZI=n1E2Bk1J2Ff3Mk503Oc62g=,172^>1:2XA1>2UE2Bo1I2Fj3Lo62Fb3Mf5,03N^72b=1:2]A1>2ZF1B2VI2Em1K2Fe,2Lh1R3Na603P\:172Y>1;2UB2=m2Dq1J2Eh,2Kl1Q3Me603Pa:172^>1;2YA2=p1C2UI,2Dk2Jp3QEc3Mi603Pf:3L[72b?1:2]A1<2UB2XH,2Cn1I2Ei1L2Ie1Q3Na703Q\:2`@1;2XA,4\H;m1B2TI2Em1L2Ij1Q3Nf603Q`903QW:,2[@1;2TB2XI1E4TMAh2Io3RFe3Mj603Pc803Q[;,2^?1;2WA2>q1E2Bm1I2Fi1M2Hc3Of70,3P^82a>1:2[A1>2WE1B2TI2Fm1L2Hf3Ni6,03Oa703PZ:3`A62V>4]F;q1B4YJ>l2Eq1L2Gi3Ml5,03Nd603Q_9172[>1;2XB2>p1E2VK2Fl,1K2Fc3Mh603Pc9172`>1;2\B1>2UD2=j2En,1J2Fg3Mm62Ib3Pj;3M_703R[:2`B1=2YB2=n,1C2TI2Fk1L2Ig1P3Nd703Q_:152X<2[A,2<q1B2WI2Ep1L2Il1Q3Ni703Qc9152[:2^@,1;2WB2>o1E2Bk1I2Fh1M2Ib3Pf803R^9,2a?1;2ZA1>2UE2Bp1I2Fl1M2If3Oi80,3Pa803QY:2^A1>2ZE1B4WJ>j2Fp1M2Hi1N2H`,3Od703Q]:162Y>1;2VB2?o1E4VM@h2Gl1M,2Hd3Ng603Qa9172^>1;2ZB1?2UE2@l2Fo1L,2Gg3Mk62H`3Pf:172c?3QY;2_B1>2YD2?o1E,2TK2Fj1M2Ie1P3Mb703R^;172X=2\C1>,2TD2WJ2Fn1L2Ij1P3Ng703Rb:162[<2_B1=,2VC2>m1E4TMAh2Io3QFe3Nl82Ja3Qf:152_;0,3RU<2ZB1>2TE2Bn1I2Fj1M2Je3Pk:2K^3Ra:,03RY;2]A1>2XE1B2TI2Fo1M2Ii1P2Ka3Qd8,03R]:3bB62W>4]F:q1B2?n1F4VNAh2Il1O2Jd,3Pg803Q`:162\=1;2XB1?2TF2Bl2Ho1N,2Ig3Nk703Qd9162`>1;2]B1?2XE2Ao1G2TM,2Hj1M2Id1P3M_603R\;172W>2\E1@2TE,2?i2Gm1M2Ih1P3Md603Ra;172[=28q1?2WD,2?m2Fq1M2Il1P3Mi72I^3Re:162_<172W=,2ZC2?q1E2Bk1I2Fh1M2Jd1Q3M^52b;16,2Y<2]B1>2VE2Bp1I2Fm1M2Jh1Q2Lb3Re:15,2\;3aC62U>2[E1B4WJ>k1F4TNBg2Jl1P2Le3Qh9,03R`:172Z=1:2VB2?q1F2Bk2Ip1P2Jg,1P2J_3Qc:162^=1;2[B1?2WF2Bo1H2Bg2Ij,1O2Jc3Qg:3L\62c>3QY;3aC72V?2[F1A2TG2Bj,2Hm1N2Jg1P3Mb603R_;182Z>1:2T@2WF2Am,2Gp1M2Ik1P3Mg603Rc;172^>192W?2ZE,2@p1F2Bj2Io3QEe1M2Jb1Q3M]72b=182Z>,2]D1?2VE2Bn1I2Fk1M2Jg1Q3Ma62e<172]=,172U>2YE1B2UI2Fp1N2Jk1Q3Me503M\6,2`<172Y>3_F:2TB2?n1F2Cj2Jo3QDc2Lh1R,3L_52c;172]=1:2XB1?2UF2Cn1I2Eg2Kk1P,2Lb3Rf;162a=1:2]B1?2ZF1B2TH2Dj2Jm,1O2Kf1Q3M`603Q\;182Y?2;q1A2WH2Cm,2Hq1O2Ji1P3Me603Qa;182]>1:2WA2[G2Ap,1G2Bi2Im1P3Mi72I_3Qf;3N\72Eh1:2Z?29o,1@2UF2Bm1I2Fh1M2Je1Q3N`72f?3PY92]>19,2U?2YF2Bq1I2Fm1M2Jj1Q3Nd603O]72`=,182X?4]F:o1B4WI=k1F4UNCi2Jn3REc3Mh503N`6,2c<182\>1:2VA2?q1F2Cm1J2Fg2Lk1R3Mc5,2f<172`=1:2[A1?2XF2Cq1I2Ek2Kn1R,2Lf1R3N_62d>3PZ:3aC72W?2;p1B2WI2Dn1J,2De2Ki1Q3Mc603Q_:182\?1;2VB2<m2Cq1I,2Dh2Jl1P3Mg603Qd;182`?1;2ZA2<p1B,2UH2Cl1I2Ef3Mm82Jc1Q3N_703QY:2]@1;2UA,2XG2Bp1I2Fk1M2Jh1Q3Nc703Q]92`?1:,2X@4\G:n1B2VI2Fp1M2Jl1R3Ng603P`82d>,192[?1;2UA2>o1F2Ck1J2Gg3Mk603Oc70,3OZ82_>1:2YA1?2VF2Cp1J2Fj1M2Gc3Nf5,03O^72b>1:2^B1?4[G;n1C2VJ2Fn1L2Gf,3Mi503Nb603Q]:172Y?1<2UB2>m2Eq1K2Fi,2Kl1R3Mf603Qa:182^?1;2YB2>q1D2VJ,2Dl1J2Fe3Mj603Qg;3N]72c@3QX;2]A1=2VB,2YI2Co1J2Fi1M2Je1Q3Nb703R]:2aA1<2XA,2<n1C2UI2Fn1M2Jj1Q3Nf703Q`903RX:,2[@1<2TB4YJ>l1E4UNBi1J2Ge3Mk703Pc803Q[9,2^?1;2XB2>q1E2Cn1J2Gj1M2Ic3Of70,3P^82b?1;2\A1>2XF1C2UJ2Fm1M2Hf3Ni6,03Oa703Q[:3aB72W>1<2TC2?m2Fq1L2Gi3Ml5,03Ne703Q_:172\>1<2XB2?q1E2WL2Fl,1L2Gd3Ni603Qd:172a?1;2\B1>2VD2>k,2Eo1K2Gh1M2Ic1Q3N`703R\;3aC62U=2YC2>o,1D2TJ2Fl1M2Jh1Q3Ne703R`:162Y<2\B,1=2TC4XJ=j2Fp1M2Jm3QFc3Ni803Qc:152\;2_A,1<2WB2>o1E2Bl1J2Gh1N2Jc3Qg903R^:,2b@1;2[B1>2VE2Cq1J2Gl1N2Jf3Pj80,3Qa803RZ;2_B1>4[F:o1C4XK?k2Fp1M2Ii1O2Ia,3Pd703R^:172Y>1<2VC2?p1F2Ai2Hl1M,2Hd3Oh703Qb:172^>1<2[C1?2UE2Al2Go,1L2Hg3Nl82Ia3Qg;3M]72e@3RZ;3`C72T>2YD2@o1E,2TK2Gk1M2Jf1Q3Nb703R^;172Y=2\D1>,2TD4XK>i2Fo1M2Jj1Q3Ng703Rb;172\<2`C1=,2WC2?n1F4VNBi1J2Gf1N2Kb3Rf:162_;15,2V<2ZB1?2TE2Bn1J2Gk1N2Kf1Q2L^3Rb:,152Z;2^B1>2YE1B2UJ2Go1N2Ji1P2Kb3Qd9,03R];172X>1;2TC2@n1G2Bi2Im1O2Jd,3Ph803Ra:172\>1;2YC1@2UF2Bl2Hp1N,2Ig3Ol82J`3Qe:172a>1;4^C7q1?2XF2Ao1G2UN,2Hj1N2Jd1Q3N`703R];182X>2]F1@2TF,2@j2Gn1M2Jq1Q3Ne703Ra;172\>192T?,2WE2@m1F4TMAf2Im3QEc3Nj82J`3Rf;172_=182W>,2ZD2?q1F2Bl1I2Gj1N2Ke1R3M_62b<17,2Z=2]C1?2WE2Bq1I2Gn1N2Ki1Q3Mb52e;16,2]<172V>4[F:o1B4XK?l1G4UOCh2Jl1Q2Le3Rh:,152`;172Z>1;2WB2@q1G2Cl2Ip1P2K_)");
                string ys;
                while (getline(years, ys, ',')) {
                    while (!ys.empty()) {
                        const int len = ys[0] - '0';
                        auto data = vector<int>();
                        for (int i = 0; i < len; i++) {
                            data.push_back(ys[i + 1] - '5' - 30);
                        }
                        DAYS[y * 13 + m] = data;
                        m++;
                        ys = ys.substr(len + 1);
                    }
                    y++;
                    m = 0;
                }
            });
            if (month == 0 || month > 12 || month < -12) {
                throw invalid_argument("illegal rab-byung month: " + std::to_string(month));
            }
            const int y = year.get_year();
            if (y < 1950 || y > 2050) {
                throw invalid_argument("rab-byung year " + std::to_string(month) + " must between 1950 and 2050");
            }
            const int m = abs(month);
            if (y == 1950 && m < 12) {
                throw invalid_argument("month " + std::to_string(month) + " must be 12 in rab-byung year " + std::to_string(y));
            }
            const int leap_month = year.get_leap_month();
            if (leap && m != leap_month) {
                throw invalid_argument("illegal leap month " + std::to_string(m) + " in rab-byung year " + std::to_string(y));
            }
            // 位于当年的索引
            int index = m - 1;
            if (leap || (0 < leap_month && leap_month < m)) {
                index += 1;
            }
            index_in_year = index;
        }

        explicit RabByungMonth(const int year, const int month): RabByungMonth(RabByungYear::from_year(year), month) {
        }

        explicit RabByungMonth(const int rab_byung_index, const RabByungElement& element, const Zodiac& zodiac, const int month): RabByungMonth(RabByungYear::from_element_zodiac(rab_byung_index, element, zodiac), month) {
        }

        static RabByungMonth from_ym(int year, int month);

        static RabByungMonth from_element_zodiac(int rab_byung_index, const RabByungElement& element, const Zodiac& zodiac, int month);

        /**
         * @brief 藏历年
         * @return 藏历年
         */
        RabByungYear get_rab_byung_year() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 月
         * @return 月，当月为闰月时，返回负数
         */
        int get_month_with_leap() const;

        /**
         * @brief 位于当年的索引
         * @return 索引(0-12)
         */
        int get_index_in_year() const;

        /**
         * @brief 是否闰月
         * @return true/false
         */
        bool is_leap() const;

        string get_name() const override;

        /**
         * @brief 别名
         * @return 别名
         */
        string get_alias() const;

        string to_string() const override;

        RabByungMonth next(int n) const;

        bool equals(const RabByungMonth &other) const;

        /**
         * @brief
         * @return
         */
        int get_day_count() const;

        /**
         * @brief 特殊日子列表
         * @return 特殊日子列表，闰日为正，缺日为负
         */
        vector<int> get_special_days() const;

        /**
         * @brief 闰日列表
         * @return 闰日列表
         */
        vector<int> get_leap_days() const;

        /**
         * @brief 缺日列表
         * @return 缺日列表
         */
        vector<int> get_miss_days() const;

        /**
         * @brief 首日
         * @return 藏历日
         */
        RabByungDay get_first_day() const;

        /**
         * @brief 本月的藏历日列表
         * @return 藏历日列表
         */
        vector<RabByungDay> get_days() const;
    protected:
        /**
         * @brief 藏历年
         */
        RabByungYear year;

        /**
         * @brief 月
         */
        int month;

        /**
         * @brief 是否闰月
         */
        bool leap;

        /**
         * @brief 位于当年的索引，0-12
         */
        int index_in_year;
    };
    
    /**
     * @brief 公历现代节日
     */
    class SolarFestival : public AbstractCulture {
    public:
        ~SolarFestival() override = default;

        static const vector<string> NAMES;
        static string DATA;

        explicit SolarFestival(const FestivalType type, const SolarDay &day, const int start_year, const string &data): _type(type), index(stoi(data.substr(1, 2))), day(day), name(NAMES[index]), start_year(start_year) {
        }

        static optional<SolarFestival> from_index(int year, int index);

        static optional<SolarFestival> from_ymd(int year, int month, int day);

        FestivalType get_type() const;

        int get_index() const;

        SolarDay get_day() const;

        int get_start_year() const;

        optional<SolarFestival> next(int n) const;

        string to_string() const override;

        string get_name() const override;

    protected:
        /**
         * @brief 类型
         */
        FestivalType _type;

        /**
         * @brief 索引
         */
        int index;

        /**
         * @brief 公历日
         */
        SolarDay day;

        /**
         * @brief 名称
         */
        string name;

        /**
         * @brief 起始年
         */
        int start_year;
    };

    /**
     * @brief 农历传统节日（依据国家标准《农历的编算和颁行》GB/T 33661-2017）
     */
    class LunarFestival : public AbstractCulture {
    public:
        ~LunarFestival() override = default;

        static const vector<string> NAMES;
        static string DATA;

        explicit LunarFestival(const FestivalType type, const LunarDay &day, optional<SolarTerm> solar_term, const string &data): _type(type), index(stoi(data.substr(1, 2))), day(day), name(NAMES[index]), solar_term(std::move(solar_term)) {
        }

        static optional<LunarFestival> from_index(int year, int index);

        static optional<LunarFestival> from_ymd(int year, int month, int day);

        FestivalType get_type() const;

        int get_index() const;

        LunarDay get_day() const;

        optional<SolarTerm> get_solar_term() const;

        optional<LunarFestival> next(int n) const;

        string to_string() const override;

        string get_name() const override;

    protected:
        /**
         * @brief 类型
         */
        FestivalType _type;

        /**
         * @brief 索引
         */
        int index;

        /**
         * @brief 农历日
         */
        LunarDay day;

        /**
         * @brief 名称
         */
        string name;

        /**
         * @brief 节气
         */
        optional<SolarTerm> solar_term;
    };

    /**
     * @brief 藏历日，仅支持藏历1950年十二月初一（公历1951年1月8日）至藏历2050年十二月三十（公历2051年2月11日）
     */
    class RabByungDay : public AbstractCulture {
    public:
        ~RabByungDay() override = default;

        static const vector<string> NAMES;

        explicit RabByungDay(const RabByungMonth& month, const int day): AbstractCulture(), month(month), day(day), leap(day < 0) {
            if (day == 0 || day < -30 || day > 30) {
                throw invalid_argument("illegal day " + std::to_string(day) + " in " + month.to_string());
            }
            const int d = abs(day);
            if (leap) {
                if (vector<int> l = month.get_leap_days(); find(l.begin(), l.end(), d) != l.end()) {
                    throw invalid_argument("illegal leap day " + std::to_string(d) + " in " + month.to_string());
                }
            }
            if (!leap) {
                if (vector<int> l = month.get_miss_days(); find(l.begin(), l.end(), d) != l.end()) {
                    throw invalid_argument("illegal day " + std::to_string(d) + " in " + month.to_string());
                }
            }
        }

        explicit RabByungDay(const int year, const int month, const int day): RabByungDay(RabByungMonth(year, month), day) {
        }

        explicit RabByungDay(const int rab_byung_index, const RabByungElement& element, const Zodiac& zodiac, const int month, const int day): RabByungDay(RabByungMonth(rab_byung_index, element, zodiac, month), day) {
        }

        static RabByungDay from_ymd(int year, int month, int day);

        static RabByungDay from_element_zodiac(int rab_byung_index, const RabByungElement& element, const Zodiac& zodiac, int month, int day);

        static RabByungDay from_solar_day(const SolarDay& solar_day);

        /**
         * @brief 藏历月
         * @return 藏历月
         */
        RabByungMonth get_rab_byung_month() const;

        /**
         * @brief 年
         * @return 年
         */
        int get_year() const;

        /**
         * @brief 月
         * @return 月
         */
        int get_month() const;

        /**
         * @brief 日
         * @return 日
         */
        int get_day() const;

        /**
         * @brief 是否闰日
         * @return true/false
         */
        bool is_leap() const;

        /**
         * @brief 日
         * @return 日，当日为闰日时，返回负数
         */
        int get_day_with_leap() const;

        string get_name() const override;

        string to_string() const override;

        /**
         * @brief 藏历日相减
         * @param target 藏历日
         * @return 相差天数
         */
        int subtract(const RabByungDay& target) const;

        /**
         * @brief 公历日
         * @return 公历日
         */
        SolarDay get_solar_day() const;

        RabByungDay next(int n) const;
    protected:
        /**
         * @brief 藏历月
         */
        RabByungMonth month;

        /**
         * @brief 日
         */
        int day;

        /**
         * @brief 是否闰日
         */
        bool leap;
    };

    /**
     * @brief 月相
     */
    class Phase : public LoopTyme {
    public:
        ~Phase() override = default;

        static const vector<string> NAMES;

        explicit Phase(const int lunar_year, const int lunar_month, const int index) : LoopTyme(NAMES, index) {
            const LunarMonth m = LunarMonth::from_ym(lunar_year, lunar_month).next(index / static_cast<int>(NAMES.size()));
            this->lunar_year = m.get_year();
            this->lunar_month = m.get_month_with_leap();
        }

        explicit Phase(const int lunar_year, const int lunar_month, const string &name) : LoopTyme(NAMES, name), lunar_year(lunar_year), lunar_month(lunar_month) {
        }

        static Phase from_index(int lunar_year, int lunar_month, int index);

        static Phase from_name(int lunar_year, int lunar_month, const string &name);

        Phase next(int n) const;

        /**
         * @brief 公历时刻
         * @return 公历时刻
         */
        SolarTime get_solar_time() const;

        /**
         * @brief 公历日
         * @return 公历日
         */
        SolarDay get_solar_day() const;
    protected:
        /**
         * @brief 农历年
         */
        int lunar_year;

        /**
         * @brief 农历月
         */
        int lunar_month;

        SolarTime get_start_solar_time() const;
    };

    /**
     * @brief 月相第几天
     */
    class PhaseDay : public AbstractCulture {
    public:
        ~PhaseDay() override = default;

        explicit PhaseDay(const Phase& phase, const int day_index) : phase(phase), day_index(day_index) {
        }

        Phase get_phase() const;

        int get_day_index() const;

        string to_string() const override;

        string get_name() const override;
    protected:
        /**
         * @brief 月相
         */
        Phase phase;

        /**
         * @brief 天索引
         */
        int day_index;
    };
}
