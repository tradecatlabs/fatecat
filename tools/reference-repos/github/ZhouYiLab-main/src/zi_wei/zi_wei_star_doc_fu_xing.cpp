// 紫微斗数星曜文档 - 十四辅星（实现）
module ZhouYi.ZiWei.StarDoc.FuXing;

import ZhouYi.ZiWei.StarDoc.Common;
// XingYaoWuXing, XingYaoYinYang 已移至 StarDoc.Common
import ZhouYi.ZhMapper;
import std;

namespace ZhouYi::ZiWei::StarDoc {
    using namespace std;

    // ============= 辅星分类说明 =============
    
    static const map<FuXingCategory, string> FU_XING_CATEGORY_DESCRIPTIONS = {
        {FuXingCategory::LiuJi, 
            "六吉星由左辅、右弼、天魁、天钺、文昌、文曲组成。"
            "吉星之所以叫吉星，是因为它们的特性对盘主本人会比较容易产生正面影响。"
            "但需要打破对星曜吉凶善恶分类的偏见，任何一颗星都有好有坏。"},
        {FuXingCategory::LiuSha,
            "六煞星由地空、地劫、火星、铃星、擎羊、陀罗组成。"
            "煞星的特性相对吉星来说对盘主本人比较容易产生负面影响。"
            "但这就像名门正派也不都是好人，日月神教中也不都是坏人一样。"},
        {FuXingCategory::ErZhu,
            "二助星由天马和禄存组成。"
            "天马是紫微斗数里最坐不住的星曜，增加变数和不确定性。"
            "禄存是财星，会增加稳定性和谨慎。"}
    };

    // ============= 辅星分类映射 =============
    
    static const map<FuXingCategory, vector<string>> FU_XING_CATEGORY_STARS = {
        {FuXingCategory::LiuJi, {"左辅", "右弼", "天魁", "天钺", "文昌", "文曲"}},
        {FuXingCategory::LiuSha, {"地空", "地劫", "火星", "铃星", "擎羊", "陀罗"}},
        {FuXingCategory::ErZhu, {"天马", "禄存"}}
    };

    // ============= 辅星详细数据库 =============
    
    static const map<string, StarDocument> FU_XING_DATABASE = {
        // ==================== 六吉星 ====================
        {"左辅", {
            .name = "左辅",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "助力",
            .zhi_wu = "行善令",
            .bie_hao = "贵人星",
            .description = "左辅的特质是助力，喜欢帮助、提拔别人。这种帮助是有点\"长辈视角\"的从上而下的帮助。"
                          "因此左辅星有\"提高身份地位\"的作用。左辅比较容易有\"架子\"，"
                          "在工作或社交场合中展现出自信和权威，喜欢扮演引领者的角色。"
                          "他们直接和强势可能会让人觉得有些\"高冷\"，不易接近。"
                          "左辅星特别会通过周围的关系提升自己的地位和影响力，善于处理人际关系。",
            .key_trait = "助力、提拔他人、长辈视角",
            .fu_xing_category = FuXingCategory::LiuJi,
            .za_yao_category = nullopt
        }},
        {"右弼", {
            .name = "右弼",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "助力",
            .zhi_wu = "司制令",
            .bie_hao = "贵人星",
            .description = "相比左辅星的直接，右弼星就显得比较柔和了。右弼的帮助是在背后默默的付出，所以常常感受不深。"
                          "温柔、善良、体贴和善解人意都是用来修饰右弼星的。"
                          "他们善于倾听他人的需求，愿意给予帮助和支持，能够给予他人安慰和鼓励。"
                          "右弼星\"耳根子软\"，容易被别人的意见所左右，立场和想法不太坚定。"
                          "很多强势的星曜适合和右弼星搭档，会柔化那些强势星曜的棱角，变得比较\"听劝告\"。"
                          "右弼星会增加一些艺术修养和才气。",
            .key_trait = "柔和助力、善解人意、艺术才气",
            .fu_xing_category = FuXingCategory::LiuJi,
            .za_yao_category = nullopt
        }},
        {"天魁", {
            .name = "天魁",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "贵人",
            .zhi_wu = "助力，成就",
            .bie_hao = "天乙贵人、文星、才星、科甲星",
            .description = "天魁星是天乙贵人，散发出领导的气质。有比较强的领导欲望，喜欢\"管人\"，决策上比较果断。"
                          "魁钺都比较容易打官腔，深谙咬文嚼字之道。"
                          "在贵人星里面，天魁星的助力是需要自己去争取的，并且只会帮你解决眼下的事情，"
                          "就是脚痛医脚头痛医头的概念。天魁星的帮助只能解燃眉之急。"
                          "打铁还须自身硬，天魁星的助力直接和你自身的能力还有认知挂钩。"
                          "这颗星也是科甲之星，主要增加文气，对理工科的帮助并不大。",
            .key_trait = "天乙贵人、领导气质、需主动争取",
            .fu_xing_category = FuXingCategory::LiuJi,
            .za_yao_category = nullopt
        }},
        {"天钺", {
            .name = "天钺",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "贵人",
            .zhi_wu = "助力，成就",
            .bie_hao = "玉堂贵人、细姨星、手术星",
            .description = "天钺星叫玉堂贵人，帮助和右弼星一样比较间接。"
                          "天魁星善于领导，而天钺星善于策划，善于思考、分析和制定方案。"
                          "如果天魁星喜欢\"管人\"，那天钺星就是喜欢\"管事\"，不喜欢别人对他们负责的事情指手画脚。"
                          "和天魁星的脚痛医脚不一样，天钺星更容易直接解决问题的源头，把\"麻烦\"化解于无形。"
                          "天钺星的助力也是需要通过自己的努力去争取的。这颗星能增加聪慧和洞察力。"
                          "辅弼的助力是只要知道了就会帮助，而魁钺还需要你主动去寻求帮助。",
            .key_trait = "玉堂贵人、善于策划、化解问题源头",
            .fu_xing_category = FuXingCategory::LiuJi,
            .za_yao_category = nullopt
        }},
        {"文昌", {
            .name = "文昌",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Jin,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "文贵",
            .zhi_wu = "正途功名，科甲",
            .bie_hao = "科甲星、文书星、风流星、桃花星",
            .description = "文昌星是紫微斗数第一科甲之星，代表文书类的事务，可以看作是\"小天梁\"，有天梁的清高和倔强。"
                          "在古籍中叫做\"正途功名\"，就是那些被家长认可支持的学业方向。"
                          "这颗星比较喜欢文学，会给人文质彬彬的感觉。"
                          "单独来讲不属于桃花星，因为会给人一种比较呆板、缺乏变通的感觉。"
                          "但一旦和其他桃花星组合，就变成桃花星，从呆板变为风流倜傥。"
                          "文昌星的记忆力比较好，对于听过的话、看过的书都比较容易记住。",
            .key_trait = "第一科甲星、正途功名、记忆力强",
            .fu_xing_category = FuXingCategory::LiuJi,
            .za_yao_category = nullopt
        }},
        {"文曲", {
            .name = "文曲",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "文华",
            .zhi_wu = "异途功名，优雅，口才，才华",
            .bie_hao = "八卦星、才艺星、偏房星、才华星、艺术星、桃花星、浪漫星、细姨星",
            .description = "文曲星是紫微斗数里第一文艺之星，代表艺术修养与浪漫，被称作\"异途功名\"（艺途功名）。"
                          "异途是和正途相对的，当家长听到你的志向时想拿刀追你，那多半就是异途功名。"
                          "文曲星通常比较善于变通，内心多愁善感。"
                          "因为会增加一些表达能力，所以引申出了口舌是非的意象。"
                          "文曲星需要增加自己的文化底蕴，让艺术气息有根基，否则容易让人感觉在无病呻吟、故作深沉。"
                          "文昌文曲在一起会形成文贵文华格，表示才华出众。",
            .key_trait = "第一文艺星、异途功名、艺术修养",
            .fu_xing_category = FuXingCategory::LiuJi,
            .za_yao_category = nullopt
        }},

        // ==================== 六煞星 ====================
        {"地空", {
            .name = "地空",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "空亡之气",
            .zhi_wu = "",
            .bie_hao = "破财星、中断星、归零星、宗教星、幻想星、创意星",
            .description = "古籍中对地空的描述是\"半空折翅\"。地空星其实算是比较\"中性\"的一颗星，"
                          "之所以让人有半空折翅的感觉，是因为这颗星重点在想而不是做。"
                          "地空星比较怕麻烦，一旦做事情步骤多、顾虑多，就容易选择逃避，这是被称为\"中断星\"的由来。"
                          "这颗星善于思考，脑子里想法特别多。如果加上天马星，就形成\"天马行空\"，思维不仅活跃，跳跃性还很强。"
                          "这些奇思妙想让地空星在艺术创作、文案策划方面有着比较高的天赋。"
                          "然而在实际中，想法需要落地，地空星的脑洞常常因为无法落地而产生\"别人笑我太疯癫，我笑他人看不穿\"的感觉。",
            .key_trait = "半空折翅、重思考轻行动、创意丰富",
            .fu_xing_category = FuXingCategory::LiuSha,
            .za_yao_category = nullopt
        }},
        {"地劫", {
            .name = "地劫",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "劫煞之气",
            .zhi_wu = "",
            .bie_hao = "破财星、谣言星",
            .description = "对应地空星的\"半空折翅\"，地劫星叫\"浪里行舟\"。区别是地空主要作用在思想上，地劫作用在物质上。"
                          "地劫星对机会比较挑剔，就算面对诱人的机会也会思虑再三。"
                          "因为对机会的挑剔，会错过一些不错的时机，给人一种泼天富贵拍在脸上视而不见的感觉。"
                          "君子爱财取之有道，这种不是什么钱都赚的心态让地劫星成了个\"劳碌命\"。"
                          "地劫星是风险厌恶型的星曜，对于需要看长期效果的事情是个不小的挑战。"
                          "初期投入了，在有风险告警时没能坚持下去，就有了\"给他人做嫁衣\"的感觉。短平快才是他们最擅长的节奏。",
            .key_trait = "浪里行舟、风险厌恶、短平快节奏",
            .fu_xing_category = FuXingCategory::LiuSha,
            .za_yao_category = nullopt
        }},
        {"火星", {
            .name = "火星",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "暴烈之气",
            .zhi_wu = "暴躁破坏",
            .bie_hao = "冲动星",
            .description = "火星会让人变得冲动，但这种冲动是思想上的。火星在做决定时容易欠缺考虑，比较容易随心而行。"
                          "这种冲动的思想方式使得他们常常充满活力和决心，乐于追求自己的目标，不轻易妥协。"
                          "然而这也可能导致他们在做出决定时缺乏充分的考虑，更容易受到情绪的影响而做出冲动的选择。"
                          "比起追求长期的成就和坚实的基础，他们更倾向于追求即时的满足和快速的结果。"
                          "火星对于情绪的影响巨大，开心时热情似火，愤怒时犹如狂风暴雨，情绪起伏较大，喜怒哀乐都会毫不掩饰地表现出来。",
            .key_trait = "思想冲动、情绪起伏大、追求即时满足",
            .fu_xing_category = FuXingCategory::LiuSha,
            .za_yao_category = nullopt
        }},
        {"铃星", {
            .name = "铃星",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "刚烈之气",
            .zhi_wu = "刚强惊吓",
            .bie_hao = "闷骚星、顽石星",
            .description = "和火星的直接表达不同，铃星不会直接将情绪一股脑的释放出来，而是积压在内心慢慢释放。"
                          "铃星通常给人一种内敛、深沉的印象，更倾向于在内心深处思考和消化情绪，不轻易将情感展现在外表。"
                          "这种内敛的特点使得他们在处理情绪时更加冷静和克制，不易被外界情绪所左右。"
                          "然而有时候过度的内敛也可能导致情绪积压，需要学会适当地表达和释放情感。"
                          "铃星比较喜欢精打细算，善于考虑周全，不轻易冲动行事，喜欢有条不紊地规划和安排生活。"
                          "虽然这种谨慎使得他们更稳健可靠，但有时也可能因为过于谨慎而错失一些机会。",
            .key_trait = "内敛深沉、情绪积压、精打细算",
            .fu_xing_category = FuXingCategory::LiuSha,
            .za_yao_category = nullopt
        }},
        {"擎羊", {
            .name = "擎羊",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Jin,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "刑",
            .zhi_wu = "粗暴，残忍",
            .bie_hao = "加工星、叛逆星",
            .description = "如果说火星是思想上的冲动，擎羊就是行为上的冲动。这颗星是个典型的行动派。"
                          "擎羊星更倾向于通过实际行动来表达自己，而不是空谈或思考。"
                          "他们喜欢迅速地采取行动，勇于面对挑战，不畏艰难，善于迅速做出决策并付诸行动。"
                          "三思而后行在擎羊星这里是不存在的，所以需要注意在行动之前多加思考，避免因冲动而犯下错误。"
                          "擎羊星更注重自己的行动和目标，相对不太在意他人的看法或期待。"
                          "他们按照自己的方式和节奏生活，不太受外界影响，在一般人眼中显得有些与众不同，甚至被认为是\"异类\"。",
            .key_trait = "行为冲动、行动派、独立自主",
            .fu_xing_category = FuXingCategory::LiuSha,
            .za_yao_category = nullopt
        }},
        {"陀罗", {
            .name = "陀罗",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Jin,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "忌",
            .zhi_wu = "是非，残忍",
            .bie_hao = "是非星、纠缠星",
            .description = "陀罗星通陀螺，就是小时候抽的那个陀螺，是一颗不停旋转的星曜。"
                          "这颗星会带给人一种容易纠结的情绪，纠结就会容易拖延。"
                          "陀罗星比较容易在做决定时陷入纠结和犹豫之中，难以迅速做出抉择，在行动上显得犹豫不决。"
                          "诚然，三思而后行可以避免很多风险，也能增加事情的成功率。"
                          "但陀罗星还是需要学会克服纠结，勇敢面对抉择，以免错失机会或陷入无休止的循环之中。"
                          "陀罗星善于研究，做事循序渐进不骄不躁，适合接触长线任务，比起眼前利益更在意长足的进步和沉淀。"
                          "他们喜欢研究\"原理\"，喜欢深入了解事物的本质和规律。",
            .key_trait = "纠结拖延、善于研究、循序渐进",
            .fu_xing_category = FuXingCategory::LiuSha,
            .za_yao_category = nullopt
        }},

        // ==================== 二助星 ====================
        {"天马", {
            .name = "天马",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "驿马",
            .zhi_wu = "变动，变迁",
            .bie_hao = "驿马星、动星、财星、司禄之星",
            .description = "要说紫微斗数里最坐不住的星曜，那一定非天马莫属，他会增加很多变数和不确定性。"
                          "天马星精力旺盛，充满活力，喜欢追求刺激和变化，难以坐定，喜欢不断地寻找新的挑战和机遇。"
                          "天马星往往充满了冒险精神，喜欢尝试新鲜事物，对于枯燥乏味的生活缺乏耐心，渴望自由和多样性，不愿受到束缚和限制。"
                          "天马星会积极主动去追求自己内心的目标，喜欢自由自在的氛围。"
                          "比起在一个目标上死磕下去，天马星更喜欢寻找不同的机遇和可能性，更容易发现成功的机会。"
                          "但是坚持和沉淀是天马星的弱项，他们很容易犯捡了芝麻丢西瓜的错误。",
            .key_trait = "坐不住、追求变化、冒险精神",
            .fu_xing_category = FuXingCategory::ErZhu,
            .za_yao_category = nullopt
        }},
        {"禄存", {
            .name = "禄存",
            .star_type = StarType::FuXing,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "财富",
            .zhi_wu = "人寿，贵爵",
            .bie_hao = "财星",
            .description = "如果哪颗星在紫微斗数里最受人欢迎，那可能就是禄存星了。因为这是颗财星，有谁会对他有抵抗力呢？"
                          "但是禄存的这个财其实是一种类似于\"本钱\"的感觉。禄存星会增加稳定性，因为人对于自己的本钱都是比较谨慎的。"
                          "对于财务的支出，禄存星是非常谨慎的，这种谨慎的态度确实可以避免很多经济上的损失，但同时也容易错失很多机会。"
                          "禄存星也是风险厌恶型的星曜，他能够稳定一些浮躁的主星。"
                          "所以古籍上常常会把禄存星作为一种解煞的星曜来看待。",
            .key_trait = "财星、本钱、谨慎稳定",
            .fu_xing_category = FuXingCategory::ErZhu,
            .za_yao_category = nullopt
        }}
    };

    // ============= 实现函数 =============

    string get_fu_xing_category_description(FuXingCategory category) {
        auto it = FU_XING_CATEGORY_DESCRIPTIONS.find(category);
        if (it != FU_XING_CATEGORY_DESCRIPTIONS.end()) {
            return it->second;
        }
        return "";
    }

    vector<string> get_fu_xing_by_category(FuXingCategory category) {
        auto it = FU_XING_CATEGORY_STARS.find(category);
        if (it != FU_XING_CATEGORY_STARS.end()) {
            return it->second;
        }
        return {};
    }

    vector<CategoryInfo> get_all_fu_xing_categories() {
        vector<CategoryInfo> result;
        
        for (int i = 0; i < static_cast<int>(FuXingCategory::COUNT); ++i) {
            auto cat = static_cast<FuXingCategory>(i);
            CategoryInfo info;
            info.name = string(Mapper::to_zh(cat));
            
            auto desc_it = FU_XING_CATEGORY_DESCRIPTIONS.find(cat);
            if (desc_it != FU_XING_CATEGORY_DESCRIPTIONS.end()) {
                info.description = desc_it->second;
            }
            
            auto stars_it = FU_XING_CATEGORY_STARS.find(cat);
            if (stars_it != FU_XING_CATEGORY_STARS.end()) {
                info.stars = stars_it->second;
            }
            
            result.push_back(info);
        }
        
        return result;
    }

    optional<StarDocument> get_fu_xing_document(const string& star_name) {
        auto it = FU_XING_DATABASE.find(star_name);
        if (it != FU_XING_DATABASE.end()) {
            return it->second;
        }
        return nullopt;
    }

    optional<FuXingCategory> get_fu_xing_category(const string& star_name) {
        auto it = FU_XING_DATABASE.find(star_name);
        if (it != FU_XING_DATABASE.end() && it->second.fu_xing_category.has_value()) {
            return it->second.fu_xing_category;
        }
        return nullopt;
    }

    vector<string> get_all_fu_xing_names() {
        vector<string> result;
        for (const auto& [name, _] : FU_XING_DATABASE) {
            result.push_back(name);
        }
        return result;
    }

} // namespace ZhouYi::ZiWei::StarDoc
