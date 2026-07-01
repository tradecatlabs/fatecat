// 紫微斗数星曜文档 - 三十七杂耀（实现）
module ZhouYi.ZiWei.StarDoc.ZaYao;

import ZhouYi.ZiWei.StarDoc.Common;
import ZhouYi.ZhMapper;
import std;

namespace ZhouYi::ZiWei::StarDoc {
    using namespace std;

    // ============= 杂耀分类说明 =============
    
    static const map<ZaYaoCategory, string> ZA_YAO_CATEGORY_DESCRIPTIONS = {
        {ZaYaoCategory::JiaoJi, 
            "交际类杂耀包括天姚、红鸾、天喜、咸池、沐浴、大耗。"
            "这类星曜主要影响人的社交能力、人际关系和桃花运。"},
        {ZaYaoCategory::GuAo,
            "孤傲类杂耀包括孤辰、寡宿、华盖、天哭、天虚。"
            "这类星曜往往带来孤独、清高或悲伤的特质。"},
        {ZaYaoCategory::CaiYi,
            "才艺类杂耀包括龙池、凤阁、天才、天官、天福。"
            "这类星曜增强艺术天赋、才能和官运福气。"},
        {ZaYaoCategory::JinGui,
            "矜贵类杂耀包括三台、八座、恩光、天贵。"
            "这类星曜带来尊贵、地位和贵人运。"},
        {ZaYaoCategory::JingShen,
            "精神类杂耀包括天厨、天寿、天巫、天月。"
            "这类星曜影响精神层面、健康长寿和玄学能力。"},
        {ZaYaoCategory::XingYun,
            "幸运类杂耀包括天德、月德、龙德、解神、天解。"
            "这类星曜带来贵人相助、化解灾难的力量。"},
        {ZaYaoCategory::JianKang,
            "健康类杂耀包括天伤、天使、阴煞、破碎。"
            "这类星曜与身体健康、伤病意外相关。"},
        {ZaYaoCategory::FengShang,
            "封赏类杂耀包括封诰、天刑、蜚廉。"
            "这类星曜关系到荣誉、法律和是非。"},
        {ZaYaoCategory::SiXiang,
            "思想类杂耀包括台辅、截空、旬空、天空、劫煞。"
            "这类星曜影响思维方式、空亡和意外变数。"}
    };

    // ============= 杂耀分类映射 =============
    
    static const map<ZaYaoCategory, vector<string>> ZA_YAO_CATEGORY_STARS = {
        {ZaYaoCategory::JiaoJi, {"天姚", "红鸾", "天喜", "咸池", "沐浴", "大耗"}},
        {ZaYaoCategory::GuAo, {"孤辰", "寡宿", "华盖", "天哭", "天虚"}},
        {ZaYaoCategory::CaiYi, {"龙池", "凤阁", "天才", "天官", "天福"}},
        {ZaYaoCategory::JinGui, {"三台", "八座", "恩光", "天贵"}},
        {ZaYaoCategory::JingShen, {"天厨", "天寿", "天巫", "天月"}},
        {ZaYaoCategory::XingYun, {"天德", "月德", "龙德", "解神", "天解"}},
        {ZaYaoCategory::JianKang, {"天伤", "天使", "阴煞", "破碎"}},
        {ZaYaoCategory::FengShang, {"封诰", "天刑", "蜚廉"}},
        {ZaYaoCategory::SiXiang, {"台辅", "截空", "旬空", "天空", "劫煞"}}
    };

    // ============= 杂耀详细数据库 =============
    
    static const map<string, StarDocument> ZA_YAO_DATABASE = {
        // ==================== 交际类 ====================
        {"天姚", {
            .name = "天姚",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "风流",
            .zhi_wu = "",
            .bie_hao = "桃花星、风流星、魅力星",
            .description = "天姚星是紫微斗数里最具魅力的星曜。他会让人散发出一种独特的魅力，"
                          "这种魅力类似于那种\"撩人于不经意之间\"的能力，相当具有异性吸引力。"
                          "天姚在和他人互动时能够让人感到被重视和关注，所以桃花也很旺。"
                          "这颗星比较喜欢浪漫，情感上比较细腻敏感，比较会照顾其他人的情绪，是很出色的\"社交高手\"。"
                          "天姚星比较\"阳光\"，能让人感到轻松自在。"
                          "天姚星\"会撩\"但不代表他们\"是渣\"。这颗星比较不走心，只是纯粹在享受交际带来的成就感。",
            .key_trait = "魅力四射、社交高手、不经意间撩人",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JiaoJi
        }},
        {"红鸾", {
            .name = "红鸾",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "婚姻",
            .zhi_wu = "",
            .bie_hao = "桃花星",
            .description = "红鸾星是一颗婚姻类型的桃花星。和天姚星、咸池星单纯的桃花不一样，"
                          "红鸾星主\"结果\"，所以星盘中红鸾星亮的人往往会有不错的婚姻运势。"
                          "他们往往会在感情中找到合适的伴侣，迈向婚姻的殿堂。"
                          "这种桃花属于那种\"有意义\"的桃花，不是为了交际而交际，而是为了结婚而交际。"
                          "在感情中红鸾星比较专注且认真，更容易维护一段稳定和长久的感情。"
                          "红鸾会增加自己的颜值和气质，更加注重外表和形象，打扮得体，从而散发出吸引力。",
            .key_trait = "婚姻桃花、注重结果、专注认真",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JiaoJi
        }},
        {"天喜", {
            .name = "天喜",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "姻缘",
            .zhi_wu = "",
            .bie_hao = "桃花星",
            .description = "天喜星和红鸾星是一对，红鸾是付出，天喜是收获。"
                          "有天喜星的人往往桃花运较旺，而且这种桃花偏向于\"被追求\"的类型。"
                          "比较容易吸引他人的关注和喜爱。"
                          "但天喜星对于感情的态度比较像一场游戏，喜欢享受追求的刺激和快感，对感情可能不会特别认真。"
                          "由于桃花的属性，天喜也可以算是一颗人缘星曜，它会给人带来更多的社交机会和人际关系。"
                          "在工作、学习或生活中，天喜星会给你带来一些新的朋友和合作伙伴。"
                          "当红鸾与天喜在一起时叫\"鸾喜相会\"，主喜庆之事。",
            .key_trait = "被追求型桃花、人缘佳、享受过程",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JiaoJi
        }},
        {"咸池", {
            .name = "咸池",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "桃花",
            .zhi_wu = "",
            .bie_hao = "桃花星、风流星、败神",
            .description = "咸池星也叫\"败神\"，这可不是什么好词汇。咸池的桃花比较偏向于\"败家\"的桃花。"
                          "和天姚星相比，咸池星更像是酒池肉林中的桃花。"
                          "咸池星善于引发一些肤浅的、短暂的关系，不如红鸾那样注重长久和稳定。"
                          "咸池星比较容易陷入不良的感情关系中，或者过于放纵自己的情感生活，导致感情上的波折和困扰。"
                          "需要学会控制自己的情感，避免过于轻率地陷入感情纠葛中。"
                          "咸池星也代表着某种艺术天赋，尤其是与音乐、舞蹈和表演相关的领域。",
            .key_trait = "败神桃花、容易放纵、艺术天赋",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JiaoJi
        }},
        {"沐浴", {
            .name = "沐浴",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "桃花",
            .zhi_wu = "",
            .bie_hao = "桃花星、咸池星",
            .description = "沐浴星也是一颗桃花星，但它的桃花带有一些\"清洗\"和\"净化\"的意味。"
                          "沐浴星的人往往外表比较吸引人，有一种清新脱俗的气质。"
                          "但在感情方面，沐浴星可能会带来一些不稳定的因素，"
                          "感情上容易有一些波动和变化，可能会经历一些感情的\"洗礼\"。"
                          "沐浴星也代表着一种蜕变和成长，通过经历一些感情上的挫折，"
                          "最终能够获得更加成熟和稳定的感情观。"
                          "这颗星在八字学中也是十二长生之一，代表新生事物的初始阶段。",
            .key_trait = "清新脱俗、感情波动、蜕变成长",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JiaoJi
        }},
        {"大耗", {
            .name = "大耗",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "耗散",
            .zhi_wu = "",
            .bie_hao = "耗财星、破败星",
            .description = "大耗星是一颗耗散之星，主要影响财务和精力方面。"
                          "有大耗星的人在财务上比较容易出现支出大于收入的情况，钱财容易散失。"
                          "在社交场合中，大耗星的人往往比较大方，喜欢请客、送礼，"
                          "这种慷慨有时候会超出自己的承受能力。"
                          "大耗星也可能表示精力的消耗，容易在一些不必要的事情上浪费时间和精力。"
                          "需要学会节制和计划，避免因为过于慷慨或者浪费而导致财务上的困境。"
                          "在流年遇到大耗时，要特别注意理财和开支的控制。",
            .key_trait = "耗散钱财、慷慨大方、精力消耗",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JiaoJi
        }},

        // ==================== 孤傲类 ====================
        {"孤辰", {
            .name = "孤辰",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "孤独",
            .zhi_wu = "",
            .bie_hao = "孤星、孤克星",
            .description = "孤辰星代表一种孤独和独立的特质。有孤辰星的人往往比较喜欢独处，"
                          "不太喜欢热闹的社交场合，更享受一个人的时光。"
                          "这种孤独并不一定是负面的，有时候反而能带来更深层次的思考和自我成长。"
                          "孤辰星的人在亲密关系中可能会显得比较疏离，"
                          "需要学会在保持独立的同时，也要照顾到身边人的情感需求。"
                          "孤辰与寡宿是一对，孤辰主男，寡宿主女。"
                          "当孤辰星比较突出时，可能会影响婚姻和感情的顺利度。",
            .key_trait = "喜欢独处、独立思考、亲密关系疏离",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::GuAo
        }},
        {"寡宿", {
            .name = "寡宿",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "孤独",
            .zhi_wu = "",
            .bie_hao = "孤星、寡星",
            .description = "寡宿星和孤辰星类似，都代表孤独的特质。"
                          "但寡宿星的孤独更偏向于内心的孤寂和情感上的疏离。"
                          "有寡宿星的人在感情方面可能会经历一些波折，不太容易找到合适的伴侣。"
                          "即使在人群中，也可能会有一种\"众人皆醉我独醒\"的感觉。"
                          "寡宿星的人需要学会打开心扉，主动去建立和维护人际关系。"
                          "孤辰主男，寡宿主女，但这不是绝对的，需要结合整体星盘来分析。"
                          "寡宿星也代表一种超脱世俗的清高，适合从事需要独立思考的工作。",
            .key_trait = "内心孤寂、感情波折、清高超脱",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::GuAo
        }},
        {"华盖", {
            .name = "华盖",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Mu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "孤高",
            .zhi_wu = "",
            .bie_hao = "艺术星、孤高星、宗教星",
            .description = "华盖星是一颗充满艺术气息和灵性的星曜。"
                          "有华盖星的人往往对艺术、宗教、哲学等领域有着浓厚的兴趣。"
                          "他们通常具有独特的审美观和创造力，在艺术创作方面有不错的天赋。"
                          "华盖星也代表一种孤高的气质，有时候会让人觉得不太好接近。"
                          "在古代，华盖是皇帝车驾上的伞盖，象征着尊贵和保护。"
                          "所以华盖星也有一定的贵人运，能够得到贵人的庇护。"
                          "但华盖星的人如果太过清高，可能会影响到人际关系的和谐。",
            .key_trait = "艺术天赋、孤高气质、对玄学感兴趣",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::GuAo
        }},
        {"天哭", {
            .name = "天哭",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Jin,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "悲伤",
            .zhi_wu = "",
            .bie_hao = "哭星、悲伤星",
            .description = "天哭星顾名思义，代表悲伤和哭泣。有天哭星的人情感比较丰富细腻，"
                          "容易被感动，也容易感到悲伤。他们对周围人的情绪比较敏感，"
                          "有时候会因为他人的不幸而感到难过。"
                          "天哭星也可能表示人生中会经历一些让人伤心的事情，比如离别、失去等。"
                          "但这种悲伤也是成长的一部分，能够让人更加成熟和坚强。"
                          "在艺术方面，天哭星能够增加创作的深度和感染力，"
                          "适合从事需要表达情感的工作，如写作、音乐、表演等。",
            .key_trait = "情感细腻、容易伤感、艺术感染力",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::GuAo
        }},
        {"天虚", {
            .name = "天虚",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "虚耗",
            .zhi_wu = "",
            .bie_hao = "虚星、耗星",
            .description = "天虚星代表虚空和耗散。有天虚星的人可能会在某些方面感到空虚或不满足，"
                          "即使物质上比较充裕，内心也可能会有一种缺失感。"
                          "天虚星也可能表示在某些事情上付出了很多，但收获却不如预期。"
                          "这颗星提醒人们要学会知足常乐，不要过分追求那些虚无的东西。"
                          "天虚星与天哭星有时候会一起出现，表示精神上的一些困扰。"
                          "但如果能够正确对待，天虚星也能带来对人生更深层次的思考和领悟。",
            .key_trait = "内心空虚、付出多收获少、需学会知足",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::GuAo
        }},

        // ==================== 才艺类 ====================
        {"龙池", {
            .name = "龙池",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "才艺",
            .zhi_wu = "",
            .bie_hao = "才艺星、文艺星",
            .description = "龙池星是一颗才艺之星，代表着艺术天赋和文化修养。"
                          "有龙池星的人往往在文学、艺术、音乐等方面有着不错的天赋。"
                          "龙池星的人通常比较文雅，有着良好的审美能力和艺术鉴赏力。"
                          "龙池与凤阁是一对，龙池代表阳性的才艺，比如书法、绘画、乐器演奏等。"
                          "当龙池凤阁同宫或会照时，表示才华出众，在艺术领域能够有所成就。"
                          "这颗星也代表着一种高雅的生活态度，喜欢追求精神层面的满足。",
            .key_trait = "艺术天赋、文雅高雅、审美能力强",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::CaiYi
        }},
        {"凤阁", {
            .name = "凤阁",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "才艺",
            .zhi_wu = "",
            .bie_hao = "才艺星、艺术星",
            .description = "凤阁星也是一颗才艺之星，与龙池星相对应。"
                          "凤阁代表阴性的才艺，比如舞蹈、歌唱、刺绣等。"
                          "有凤阁星的人通常比较有气质，举止优雅，在艺术表现方面有着独特的魅力。"
                          "凤阁星的人注重外表和形象，打扮得体，气质出众。"
                          "龙池凤阁同宫或会照，是一个很好的才艺组合，表示才华横溢。"
                          "凤阁星也代表着贵气，有一定的贵人运和社会地位。",
            .key_trait = "气质优雅、艺术魅力、注重形象",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::CaiYi
        }},
        {"天才", {
            .name = "天才",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Mu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "聪明",
            .zhi_wu = "",
            .bie_hao = "才星、智慧星",
            .description = "天才星顾名思义，代表着聪明才智。有天才星的人通常学习能力比较强，"
                          "对新事物的接受能力和理解能力都比较出色。"
                          "天才星能够增强一个人的思维能力和创造力，在学业和事业上都能有所帮助。"
                          "这颗星也代表着一种灵活变通的能力，能够举一反三，融会贯通。"
                          "但天才星如果没有其他星曜的配合，可能会出现\"小聪明\"的情况，"
                          "即聪明反被聪明误，所以还需要踏实努力才能发挥最大的效果。"
                          "天才星在命宫或事业宫时，对学业和事业都有加分的作用。",
            .key_trait = "聪明才智、学习能力强、灵活变通",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::CaiYi
        }},
        {"天官", {
            .name = "天官",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "官运",
            .zhi_wu = "",
            .bie_hao = "官星、贵星",
            .description = "天官星代表官运和仕途。有天官星的人在事业上比较容易获得晋升和发展的机会。"
                          "这颗星能够增加一个人的领导能力和管理才能，适合从事管理类的工作。"
                          "天官星也代表着一定的社会地位和声望，能够得到他人的尊重。"
                          "在古代，天官星旺的人适合进入仕途，在现代则表示适合在体制内发展。"
                          "天官星与天福星相配合时，表示既有官运又有福气，是很好的组合。"
                          "但天官星如果被煞星冲破，则可能表示事业上会遇到一些波折。",
            .key_trait = "官运亨通、领导能力、社会地位",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::CaiYi
        }},
        {"天福", {
            .name = "天福",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "福气",
            .zhi_wu = "",
            .bie_hao = "福星、吉星",
            .description = "天福星是一颗福星，代表福气和好运。有天福星的人生活中往往比较顺利，"
                          "能够逢凶化吉，遇到困难也比较容易得到解决。"
                          "天福星能够带来物质上和精神上的满足，让人生活得比较舒适愉快。"
                          "这颗星也代表着贵人运，在需要帮助的时候总是能够遇到贵人相助。"
                          "天福星的人通常比较乐观开朗，对生活充满希望和热情。"
                          "但福气太好有时候也会让人变得懈怠，所以还是需要保持努力和上进的心态。",
            .key_trait = "福气满满、逢凶化吉、乐观开朗",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::CaiYi
        }},

        // ==================== 矜贵类 ====================
        {"三台", {
            .name = "三台",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "尊贵",
            .zhi_wu = "",
            .bie_hao = "贵星、权贵星",
            .description = "三台星代表尊贵和地位。有三台星的人往往能够获得较高的社会地位和声望。"
                          "三台在古代天文中是北斗七星附近的星座，象征着高位和权力。"
                          "三台星的人通常比较有威严，在人群中容易成为被尊敬的对象。"
                          "三台与八座是一对，三台主贵，八座主名。当两者同宫或会照时，表示名利双收。"
                          "这颗星也代表着一种稳重的气质，做事踏实可靠，值得信赖。"
                          "三台星在事业宫或命宫时，对事业发展有很大的帮助。",
            .key_trait = "尊贵地位、威严稳重、名利双收",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JinGui
        }},
        {"八座", {
            .name = "八座",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "名望",
            .zhi_wu = "",
            .bie_hao = "名星、声望星",
            .description = "八座星代表名望和声誉。有八座星的人往往能够在社会上获得较好的名声和知名度。"
                          "八座在古代天文中也是北斗附近的星座，象征着荣誉和赞誉。"
                          "八座星的人通常比较注重自己的形象和名誉，在各种场合都能够表现得体。"
                          "八座与三台相配合时，是一个很好的组合，表示既有地位又有名望。"
                          "这颗星也代表着一种优雅的气质，在社交场合中能够得到他人的好评。"
                          "八座星有时也表示适合从事与公众形象相关的工作。",
            .key_trait = "名望声誉、形象良好、社交得体",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JinGui
        }},
        {"恩光", {
            .name = "恩光",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "贵人",
            .zhi_wu = "",
            .bie_hao = "贵人星、恩星",
            .description = "恩光星代表贵人的恩惠和帮助。有恩光星的人往往能够得到贵人的照顾和提拔。"
                          "恩光星的\"恩\"字代表恩情，\"光\"字代表光芒，合起来就是贵人的光辉照耀。"
                          "这颗星能够在关键时刻带来帮助，让人能够度过难关，获得发展的机会。"
                          "恩光星与天贵星相配合时，贵人运更加旺盛。"
                          "恩光星的人通常也比较懂得感恩，愿意在自己有能力的时候帮助他人。"
                          "这种善意的循环能够让恩光星的贵人运持续不断。",
            .key_trait = "贵人相助、关键时刻有帮助、懂得感恩",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JinGui
        }},
        {"天贵", {
            .name = "天贵",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "贵气",
            .zhi_wu = "",
            .bie_hao = "贵星、尊贵星",
            .description = "天贵星代表天生的贵气和尊贵。有天贵星的人往往气质比较出众，"
                          "给人一种高贵典雅的感觉。这种贵气是与生俱来的，无需刻意培养。"
                          "天贵星的人通常比较容易得到他人的尊重和认可，在社会上有一定的地位。"
                          "天贵星与恩光星相配合时，不仅有贵气，还能得到贵人的帮助。"
                          "这颗星也代表着一种优越的出身或成长环境。"
                          "天贵星在命宫时，能够提升整体格局的层次。",
            .key_trait = "天生贵气、气质出众、受人尊重",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JinGui
        }},

        // ==================== 精神类 ====================
        {"天厨", {
            .name = "天厨",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "食禄",
            .zhi_wu = "",
            .bie_hao = "食禄星、美食星",
            .description = "天厨星代表食禄和口福。有天厨星的人通常比较有口福，"
                          "在美食方面有着比较好的享受。天厨星也代表着厨艺方面的天赋，"
                          "适合从事与饮食相关的行业。"
                          "这颗星也有\"天赐食禄\"的含义，表示不愁吃穿，生活比较富足。"
                          "天厨星的人通常比较懂得享受生活，注重生活的品质。"
                          "在事业方面，天厨星也代表着稳定的收入来源。",
            .key_trait = "有口福、厨艺天赋、生活富足",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JingShen
        }},
        {"天寿", {
            .name = "天寿",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "长寿",
            .zhi_wu = "",
            .bie_hao = "寿星、长寿星",
            .description = "天寿星代表长寿和健康。有天寿星的人通常身体比较健康，寿命比较长。"
                          "天寿星也代表着一种豁达乐观的心态，这种心态本身就有利于健康长寿。"
                          "这颗星能够化解一些疾病方面的不良影响，起到保护健康的作用。"
                          "天寿星的人通常比较注重养生，懂得如何保持身心的平衡。"
                          "在老年时，天寿星能够带来安享晚年的福气。"
                          "天寿星在疾厄宫时，对健康有很好的保护作用。",
            .key_trait = "健康长寿、豁达乐观、注重养生",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JingShen
        }},
        {"天巫", {
            .name = "天巫",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "玄学",
            .zhi_wu = "",
            .bie_hao = "灵感星、玄学星、宗教星",
            .description = "天巫星代表灵感和直觉。有天巫星的人通常第六感比较强，"
                          "对很多事情有着敏锐的直觉。天巫星也代表着对玄学、宗教等神秘事物的兴趣。"
                          "这颗星能够增强一个人的灵性和悟性，适合从事与玄学相关的研究或工作。"
                          "天巫星的人通常比较有信仰，相信冥冥之中有某种力量的指引。"
                          "在创意和艺术方面，天巫星也能带来独特的灵感和创造力。"
                          "天巫星有时也表示与宗教或慈善事业有缘。",
            .key_trait = "直觉敏锐、对玄学感兴趣、灵性高",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JingShen
        }},
        {"天月", {
            .name = "天月",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "疾病",
            .zhi_wu = "",
            .bie_hao = "病星、疾病星",
            .description = "天月星代表疾病和健康方面的问题。有天月星的人在健康方面需要多加注意，"
                          "可能会比较容易生病或有一些慢性疾病。"
                          "天月星提醒人们要注重预防，保持良好的生活习惯。"
                          "这颗星不一定代表严重的疾病，有时只是表示身体比较虚弱或抵抗力较低。"
                          "天月星的人需要定期检查身体，及时发现和治疗潜在的健康问题。"
                          "在疾厄宫遇到天月星时，需要特别关注健康。",
            .key_trait = "健康需注意、身体较虚弱、需重视预防",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JingShen
        }},

        // ==================== 幸运类 ====================
        {"天德", {
            .name = "天德",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "解厄",
            .zhi_wu = "",
            .bie_hao = "贵人星、解神星",
            .description = "天德星是一颗贵人星，代表着上天的恩德和庇护。"
                          "有天德星的人往往能够逢凶化吉，在危难时刻得到贵人的帮助。"
                          "天德星也代表着个人的品德和修养，品德高尚的人更容易得到天德星的庇护。"
                          "这颗星能够化解一些灾难和不顺，起到保护的作用。"
                          "天德星与月德星相配合时，解厄的力量更加强大。"
                          "天德星的人通常也比较有爱心，愿意帮助他人。",
            .key_trait = "逢凶化吉、贵人庇护、品德高尚",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::XingYun
        }},
        {"月德", {
            .name = "月德",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "解厄",
            .zhi_wu = "",
            .bie_hao = "贵人星、解神星",
            .description = "月德星与天德星类似，都是解厄的贵人星。"
                          "月德星代表阴性的贵人力量，通常与女性贵人或母性关怀有关。"
                          "有月德星的人在生活中往往能够得到女性长辈或贵人的帮助。"
                          "月德星也代表着温和善良的品性，有着包容和宽恕的美德。"
                          "天德月德同宫或会照时，解厄化煞的力量最强。"
                          "月德星的人通常比较有同情心，对他人的苦难能够感同身受。",
            .key_trait = "女性贵人、温和善良、解厄化煞",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::XingYun
        }},
        {"龙德", {
            .name = "龙德",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "吉祥",
            .zhi_wu = "",
            .bie_hao = "吉星、贵人星",
            .description = "龙德星是一颗吉星，代表着龙的恩德和庇护。"
                          "有龙德星的人往往运气比较好，能够在各方面得到顺利的发展。"
                          "龙德星也代表着权威和力量，能够增强一个人的影响力和号召力。"
                          "这颗星在流年出现时，往往预示着一年的运势比较好。"
                          "龙德星的人通常比较有领导气质，能够得到他人的拥护和支持。"
                          "在事业方面，龙德星能够带来发展和提升的机会。",
            .key_trait = "运气好、权威力量、领导气质",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::XingYun
        }},
        {"解神", {
            .name = "解神",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Mu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "化解",
            .zhi_wu = "",
            .bie_hao = "解厄星、化解星",
            .description = "解神星顾名思义，代表化解和解决问题的力量。"
                          "有解神星的人在遇到困难时往往能够找到解决的办法，化险为夷。"
                          "解神星也代表着一种乐观积极的心态，相信问题总会有解决的办法。"
                          "这颗星能够化解一些煞星的不良影响，起到保护的作用。"
                          "解神星的人通常比较善于沟通和调解，能够化解矛盾和冲突。"
                          "在流年遇到解神星时，一些积压的问题可能会得到解决。",
            .key_trait = "化解问题、乐观积极、善于调解",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::XingYun
        }},
        {"天解", {
            .name = "天解",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "解厄",
            .zhi_wu = "",
            .bie_hao = "解神星、化解星",
            .description = "天解星与解神星类似，都是代表化解和解决问题的力量。"
                          "天解星更偏向于来自上天的帮助和指引，有一种冥冥之中的庇护感。"
                          "有天解星的人在困境中往往能够得到意想不到的帮助。"
                          "天解星也代表着智慧和领悟力，能够看清问题的本质，找到解决之道。"
                          "这颗星能够化解一些因果和业力方面的问题。"
                          "天解星的人通常比较有信念，相信努力总会有回报。",
            .key_trait = "上天庇护、智慧领悟、化解因果",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::XingYun
        }},

        // ==================== 健康类 ====================
        {"天伤", {
            .name = "天伤",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "损伤",
            .zhi_wu = "",
            .bie_hao = "伤星、损伤星",
            .description = "天伤星代表损伤和伤害。有天伤星的人在生活中可能会比较容易受伤，"
                          "需要特别注意安全。天伤星也可能表示经历一些精神上的创伤。"
                          "这颗星提醒人们要谨慎行事，避免不必要的风险。"
                          "天伤星在疾厄宫或迁移宫时，需要特别注意身体安全和出行安全。"
                          "天伤星的人可能会有一些童年或成长过程中的创伤经历。"
                          "但这些经历也可以成为成长的养分，让人变得更加坚强。",
            .key_trait = "容易受伤、需注意安全、可能有创伤经历",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JianKang
        }},
        {"天使", {
            .name = "天使",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "死亡",
            .zhi_wu = "",
            .bie_hao = "丧门星、死符星",
            .description = "天使星虽然名字听起来很美好，但在紫微斗数中却代表着死亡和丧葬。"
                          "有天使星的人可能会与丧葬、医疗等行业有缘。"
                          "天使星也可能表示会经历一些亲人的离世或生死相关的事情。"
                          "这颗星提醒人们要珍惜身边的人，活在当下。"
                          "天使星的人有时会对生死问题有着比较深刻的思考和认识。"
                          "在流年遇到天使星时，需要注意家人的健康。",
            .key_trait = "与丧葬有缘、思考生死、珍惜当下",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JianKang
        }},
        {"阴煞", {
            .name = "阴煞",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Shui,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "阴邪",
            .zhi_wu = "",
            .bie_hao = "小人星、暗害星",
            .description = "阴煞星代表阴暗和小人。有阴煞星的人可能会在生活中遇到一些小人或暗中作祟的情况。"
                          "阴煞星提醒人们要谨慎交友，提防那些表面友好但暗地里不怀好意的人。"
                          "这颗星也可能表示一些隐藏的疾病或问题，需要注意排查。"
                          "阴煞星的人需要增强自己的判断力，不要轻易相信他人。"
                          "在工作中，阴煞星可能表示会遇到一些同事或下属的阻挠。"
                          "保持正直和光明磊落是化解阴煞星影响的最好方法。",
            .key_trait = "需防小人、谨慎交友、保持正直",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JianKang
        }},
        {"破碎", {
            .name = "破碎",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "破损",
            .zhi_wu = "",
            .bie_hao = "破败星、损失星",
            .description = "破碎星代表破损和不完整。有破碎星的人在某些方面可能会经历一些缺失或不圆满。"
                          "破碎星也可能表示物品容易损坏或丢失。"
                          "这颗星提醒人们要珍惜所拥有的，不要过分追求完美。"
                          "破碎星的人可能在感情或家庭方面会有一些不如意的地方。"
                          "但缺憾也是人生的一部分，接受不完美反而能够让人更加自在。"
                          "破碎星有时也代表着打破常规，有突破和创新的意味。",
            .key_trait = "可能有缺憾、珍惜所有、接受不完美",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::JianKang
        }},

        // ==================== 封赏类 ====================
        {"封诰", {
            .name = "封诰",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "荣誉",
            .zhi_wu = "",
            .bie_hao = "荣誉星、封赏星",
            .description = "封诰星代表荣誉和封赏。在古代，封诰是皇帝给予臣子的封号和赏赐。"
                          "有封诰星的人往往能够得到认可和奖赏，在事业上取得一定的成就。"
                          "封诰星也代表着一种社会地位的提升，能够获得他人的尊重。"
                          "这颗星在事业宫或命宫时，对事业发展有很好的帮助。"
                          "封诰星的人通常比较有上进心，愿意为了荣誉和成就而努力。"
                          "在流年遇到封诰星时，可能会有获奖、晋升等喜事。",
            .key_trait = "获得荣誉、事业成就、地位提升",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::FengShang
        }},
        {"天刑", {
            .name = "天刑",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "刑罚",
            .zhi_wu = "",
            .bie_hao = "刑星、法律星",
            .description = "天刑星代表刑罚和法律。有天刑星的人可能会与法律、军警等行业有缘。"
                          "天刑星也代表着一种严格和正直的性格，对是非有着明确的判断。"
                          "这颗星可能会带来一些是非或官司，需要注意遵守法律法规。"
                          "天刑星的人通常比较有原则，不轻易妥协。"
                          "在吉星的帮助下，天刑星可以表示从事法律、医疗等需要严谨的行业。"
                          "天刑星也代表着一种孤独感，因为过于正直可能会得罪一些人。",
            .key_trait = "与法律有缘、严格正直、有原则",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::FengShang
        }},
        {"蜚廉", {
            .name = "蜚廉",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "是非",
            .zhi_wu = "",
            .bie_hao = "是非星、口舌星",
            .description = "蜚廉星代表是非和口舌。有蜚廉星的人可能会比较容易遇到是非和流言蜚语。"
                          "蜚廉星提醒人们要谨言慎行，不要轻易在背后议论他人。"
                          "这颗星也可能表示容易被人误解或遭到诽谤。"
                          "蜚廉星的人需要学会保护自己，不要让流言影响到自己的情绪和判断。"
                          "在工作中，蜚廉星可能表示会遇到一些同事的闲言碎语。"
                          "保持清者自清的心态，用行动来证明自己是最好的应对方式。",
            .key_trait = "易遇是非、谨言慎行、清者自清",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::FengShang
        }},

        // ==================== 思想类 ====================
        {"台辅", {
            .name = "台辅",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "辅助",
            .zhi_wu = "",
            .bie_hao = "辅星、助力星",
            .description = "台辅星代表辅助和帮助。有台辅星的人往往能够得到他人的协助和支持。"
                          "台辅星也代表着一种愿意帮助他人的品性，是个好助手。"
                          "这颗星在事业宫时，表示能够得到下属或同事的有力配合。"
                          "台辅星的人通常比较有团队意识，善于合作。"
                          "与三台八座配合时，台辅星能够增加整体的贵气。"
                          "台辅星也代表着一种稳重可靠的形象。",
            .key_trait = "得人协助、善于配合、稳重可靠",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::SiXiang
        }},
        {"截空", {
            .name = "截空",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "空亡",
            .zhi_wu = "",
            .bie_hao = "空亡星、截断星",
            .description = "截空星代表截断和空亡。有截空星的人在某些方面可能会遇到中断或落空的情况。"
                          "截空星也代表着一种超脱世俗的想法，不太执着于物质。"
                          "这颗星可能会削弱同宫星曜的力量，让事情变得不那么确定。"
                          "截空星的人需要学会接受变化，不要过分执着于既定的计划。"
                          "在思想上，截空星能够带来一些独特的见解和创意。"
                          "截空星有时也代表着一种放下和释然的智慧。",
            .key_trait = "可能遇中断、超脱世俗、放下执着",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::SiXiang
        }},
        {"旬空", {
            .name = "旬空",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Tu,
            .yin_yang = XingYaoYinYang::Yin,
            .hua_qi = "空亡",
            .zhi_wu = "",
            .bie_hao = "空亡星、落空星",
            .description = "旬空星与截空星类似，都代表空亡和落空。"
                          "有旬空星的人在某些方面可能会有一种\"虚\"的感觉，计划容易落空。"
                          "旬空星也代表着一种不切实际的想法或期望。"
                          "这颗星提醒人们要脚踏实地，不要好高骛远。"
                          "旬空星的人在精神层面可能会比较有追求，对物质不太执着。"
                          "在玄学方面，旬空星能够增加灵性和悟性。"
                          "旬空星有时也代表着一种\"无中生有\"的创造力。",
            .key_trait = "计划易落空、脚踏实地、灵性高",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::SiXiang
        }},
        {"天空", {
            .name = "天空",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "空亡",
            .zhi_wu = "",
            .bie_hao = "空亡星、创意星",
            .description = "天空星代表天上的虚空，是最\"空\"的一颗星曜。"
                          "有天空星的人想象力非常丰富，脑子里充满了各种奇思妙想。"
                          "天空星在物质方面可能会带来一些损失或落空的情况。"
                          "但在精神和创意方面，天空星却是一颗非常有利的星曜。"
                          "天空星的人适合从事需要创意和想象力的工作，如艺术、设计、写作等。"
                          "这颗星也代表着一种不受束缚的自由精神。"
                          "天空星需要找到一个能够让想法落地的途径，否则容易流于空想。",
            .key_trait = "想象力丰富、创意无限、自由精神",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::SiXiang
        }},
        {"劫煞", {
            .name = "劫煞",
            .star_type = StarType::ZaYao,
            .wu_xing = XingYaoWuXing::Huo,
            .yin_yang = XingYaoYinYang::Yang,
            .hua_qi = "劫夺",
            .zhi_wu = "",
            .bie_hao = "劫星、灾星",
            .description = "劫煞星代表劫夺和意外。有劫煞星的人可能会遇到一些突如其来的变故或损失。"
                          "劫煞星提醒人们要未雨绸缪，做好应对突发情况的准备。"
                          "这颗星也可能表示会有一些小人或竞争对手来\"劫\"走你的机会。"
                          "劫煞星的人需要增强自己的竞争力，不要轻易让机会从手中溜走。"
                          "在流年遇到劫煞星时，需要特别注意财务安全和人身安全。"
                          "但劫煞星有时也代表着一种快速的变化和转机。",
            .key_trait = "可能遇意外、未雨绸缪、增强竞争力",
            .fu_xing_category = nullopt,
            .za_yao_category = ZaYaoCategory::SiXiang
        }}
    };

    // ============= 实现函数 =============

    string get_za_yao_category_description(ZaYaoCategory category) {
        auto it = ZA_YAO_CATEGORY_DESCRIPTIONS.find(category);
        if (it != ZA_YAO_CATEGORY_DESCRIPTIONS.end()) {
            return it->second;
        }
        return "";
    }

    vector<string> get_za_yao_by_category(ZaYaoCategory category) {
        auto it = ZA_YAO_CATEGORY_STARS.find(category);
        if (it != ZA_YAO_CATEGORY_STARS.end()) {
            return it->second;
        }
        return {};
    }

    vector<CategoryInfo> get_all_za_yao_categories() {
        vector<CategoryInfo> result;
        
        for (int i = 0; i < static_cast<int>(ZaYaoCategory::COUNT); ++i) {
            auto cat = static_cast<ZaYaoCategory>(i);
            CategoryInfo info;
            info.name = string(Mapper::to_zh(cat));
            
            auto desc_it = ZA_YAO_CATEGORY_DESCRIPTIONS.find(cat);
            if (desc_it != ZA_YAO_CATEGORY_DESCRIPTIONS.end()) {
                info.description = desc_it->second;
            }
            
            auto stars_it = ZA_YAO_CATEGORY_STARS.find(cat);
            if (stars_it != ZA_YAO_CATEGORY_STARS.end()) {
                info.stars = stars_it->second;
            }
            
            result.push_back(info);
        }
        
        return result;
    }

    optional<StarDocument> get_za_yao_document(const string& star_name) {
        auto it = ZA_YAO_DATABASE.find(star_name);
        if (it != ZA_YAO_DATABASE.end()) {
            return it->second;
        }
        return nullopt;
    }

    optional<ZaYaoCategory> get_za_yao_category(const string& star_name) {
        auto it = ZA_YAO_DATABASE.find(star_name);
        if (it != ZA_YAO_DATABASE.end() && it->second.za_yao_category.has_value()) {
            return it->second.za_yao_category;
        }
        return nullopt;
    }

    vector<string> get_all_za_yao_names() {
        vector<string> result;
        for (const auto& [name, _] : ZA_YAO_DATABASE) {
            result.push_back(name);
        }
        return result;
    }

} // namespace ZhouYi::ZiWei::StarDoc