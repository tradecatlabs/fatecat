// 紫微斗数星曜文档 - 四十八神煞（实现）
module ZhouYi.ZiWei.StarDoc.ShenSha;

import ZhouYi.ZiWei.StarDoc.Common;
import ZhouYi.ZhMapper;
import std;

namespace ZhouYi::ZiWei::StarDoc {
    using namespace std;

    // ============= 神煞分类说明 =============
    
    static const map<ShenShaCategory, string> SHEN_SHA_CATEGORY_DESCRIPTIONS = {
        {ShenShaCategory::ChangSheng,
            "长生十二神是出生后就固定的神煞，产生的力量是固定的、长期的。"
            "长生十二神源自八字学中的十二长生，代表生命从出生到死亡再到轮回的不同阶段。"
            "每个阶段都有其独特的气质和能量特征。"},
        {ShenShaCategory::BoShi,
            "博士十二神也是出生后就固定的神煞，产生的力量是固定的、长期的。"
            "博士十二神每颗星都有五行属性，代表不同的气质和能量。"
            "这些神煞影响的是一种长期的气质修饰。"},
        {ShenShaCategory::JiangQian,
            "将前十二神是跟随流年而变化的动态神煞，产生的力量是流动的、有时效性的。"
            "将前十二神主要在流月和流日中起作用，并不影响原局。"
            "代表的是一种动态的心态或情绪变化。"},
        {ShenShaCategory::SuiQian,
            "岁前十二神也是跟随流年而变化的动态神煞，产生的力量是流动的、有时效性的。"
            "岁前十二神同样主要影响流月和流日，其特性也是短暂的。"
            "岁建固定出现在流年命宫，代表一年的开始。"}
    };

    // ============= 神煞分类映射 =============
    
    static const map<ShenShaCategory, vector<string>> SHEN_SHA_CATEGORY_STARS = {
        {ShenShaCategory::ChangSheng, {"长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"}},
        {ShenShaCategory::BoShi, {"博士", "力士", "青龙", "小耗", "将军", "奏书", "飞廉", "喜神", "病符", "大耗", "伏兵", "官府"}},
        {ShenShaCategory::JiangQian, {"将星", "攀鞍", "岁驿", "息神", "华盖", "劫煞", "灾煞", "天煞", "指背", "咸池", "月煞", "亡神"}},
        {ShenShaCategory::SuiQian, {"岁建", "晦气", "丧门", "贯索", "官符", "小耗", "大耗", "龙德", "白虎", "天德", "吊客", "病符"}}
    };

    // ============= 神煞详细数据库 =============
    
    static const map<string, ShenShaDocument> SHEN_SHA_DATABASE = {
        // ==================== 长生十二神 ====================
        {"长生", {
            .name = "长生",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "长生代表生命的开始阶段，充满活力和好奇心。"
                          "有长生星的人通常思维活跃，喜欢探索新事物。"
                          "这颗星增加好奇心和创新思维，让人对未知充满期待。",
            .key_effect = "增加好奇心和创新思维",
            .is_fixed = true
        }},
        {"沐浴", {
            .name = "沐浴",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "沐浴代表新生事物的初始阶段，如同婴儿沐浴。"
                          "有沐浴星的人喜欢干净整洁的环境，对周围的秩序有要求。"
                          "但同时容易心浮气躁，情绪波动较大。",
            .key_effect = "喜欢干净环境，容易心浮气躁",
            .is_fixed = true
        }},
        {"冠带", {
            .name = "冠带",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "冠带代表成长阶段，如同青年开始穿戴冠带。"
                          "有冠带星的人血气方刚，充满斗志和竞争意识。"
                          "会增加占有欲和好胜心，不甘落于人后。",
            .key_effect = "血气方刚，增加占有欲，好胜心强",
            .is_fixed = true
        }},
        {"临官", {
            .name = "临官",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "临官代表步入社会、开始任职的阶段。"
                          "有临官星的人独立性强，能够独当一面。"
                          "可以理解为冠带的加强版，更加成熟和独立。",
            .key_effect = "增加独立性，冠带的加强版",
            .is_fixed = true
        }},
        {"帝旺", {
            .name = "帝旺",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "帝旺代表人生的巅峰阶段，如日中天。"
                          "有帝旺星的人自信心强，充满干劲和魄力。"
                          "但也有点志得意满的意味，需要注意谦虚。",
            .key_effect = "增加自信心，志得意满",
            .is_fixed = true
        }},
        {"衰", {
            .name = "衰",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "衰代表从巅峰开始下降的阶段。"
                          "有衰星的人欲望和积极性会降低，但也显得比较老成和理智。"
                          "遇事更加沉稳，不会冲动行事。",
            .key_effect = "降低欲望和积极性，显得老成理智",
            .is_fixed = true
        }},
        {"病", {
            .name = "病",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "病代表身体或精神状态较弱的阶段。"
                          "有病星的人类似于天月星的感觉，喜欢思考但执行力不强。"
                          "适合从事需要深度思考的工作。",
            .key_effect = "类似天月星，爱思考，降低执行力",
            .is_fixed = true
        }},
        {"死", {
            .name = "死",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "死代表生命周期中静止的阶段。"
                          "有死星的人斗志不强，比较容易有畏难情绪。"
                          "遇到困难时可能选择退缩而非迎难而上。",
            .key_effect = "斗志不强，容易畏难",
            .is_fixed = true
        }},
        {"墓", {
            .name = "墓",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "墓代表收藏和积累的阶段。"
                          "有墓星的人比较低调内敛，冲劲不足但善于积累。"
                          "在财务上比较节俭，量入为出。",
            .key_effect = "低调，冲劲不足，节俭，量入为出",
            .is_fixed = true
        }},
        {"绝", {
            .name = "绝",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "绝代表生命周期中的最低点。"
                          "有绝星的人比较消极，缺乏热情。"
                          "社交欲望较低，喜欢独处。",
            .key_effect = "消极，缺乏热情，降低社交欲望",
            .is_fixed = true
        }},
        {"胎", {
            .name = "胎",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "胎代表新生命孕育的阶段。"
                          "有胎星的人表达欲强，喜欢寻求变化。"
                          "内心渴望新的开始和突破。",
            .key_effect = "增加表达，寻求变化的欲望",
            .is_fixed = true
        }},
        {"养", {
            .name = "养",
            .category = ShenShaCategory::ChangSheng,
            .wu_xing = nullopt,
            .description = "养代表生命孕育成长的阶段。"
                          "有养星的人好奇心强，对未来充满希望。"
                          "代表着希望和新生的力量。",
            .key_effect = "增加好奇心，代表希望",
            .is_fixed = true
        }},

        // ==================== 博士十二神 ====================
        {"博士", {
            .name = "博士",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Shui,
            .description = "博士星五行属水，代表智慧和学识。"
                          "有博士星的人聪慧过人，思考能力强。"
                          "适合从事需要深度思考和学习的领域。",
            .key_effect = "增加聪慧、学识和思考能力",
            .is_fixed = true
        }},
        {"力士", {
            .name = "力士",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Huo,
            .description = "力士星五行属火，代表勇猛和力量。"
                          "有力士星的人执著、勇猛、坚韧、果敢。"
                          "带有个人英雄主义色彩，敢于挑战。",
            .key_effect = "增加执著、勇猛、坚韧、果敢的气质",
            .is_fixed = true
        }},
        {"青龙", {
            .name = "青龙",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Shui,
            .description = "青龙星五行属水，代表行动力和反应力。"
                          "有青龙星的人执行力强，反应敏捷。"
                          "企图心强，善于把握机会。",
            .key_effect = "增加执行力和反应力，企图心强",
            .is_fixed = true
        }},
        {"小耗", {
            .name = "小耗",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Huo,
            .description = "小耗星五行属火，代表消耗和散失。"
                          "有小耗星的人不拘小节，为人豪迈。"
                          "但可能缺乏恒心，做事容易半途而废。",
            .key_effect = "不拘小节，豪迈，缺乏恒心",
            .is_fixed = true
        }},
        {"将军", {
            .name = "将军",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Mu,
            .description = "将军星五行属木，代表权力和掌控。"
                          "有将军星的人占有欲强，对权力的掌控欲强。"
                          "适合担任领导角色。",
            .key_effect = "增加占有欲，对权力的掌控欲强",
            .is_fixed = true
        }},
        {"奏书", {
            .name = "奏书",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Jin,
            .description = "奏书星五行属金，代表文书和表达。"
                          "有奏书星的人文案能力和理解能力强。"
                          "善于书面表达和文字工作。",
            .key_effect = "增加文案和理解能力",
            .is_fixed = true
        }},
        {"飞廉", {
            .name = "飞廉",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Huo,
            .description = "飞廉星五行属火，代表好奇和表达。"
                          "有飞廉星的人好奇心强，表达欲旺盛。"
                          "但表达方式可能比较不讨喜，容易引起是非。",
            .key_effect = "增加好奇心和表达欲，表达方式不讨喜",
            .is_fixed = true
        }},
        {"喜神", {
            .name = "喜神",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Huo,
            .description = "喜神星五行属火，代表喜庆和欢乐。"
                          "有喜神星的人给人喜庆的感觉，人缘较好。"
                          "但也有拖延的意味，做事可能不够果断。",
            .key_effect = "增加喜庆感觉，有拖延意味",
            .is_fixed = true
        }},
        {"病符", {
            .name = "病符",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Shui,
            .description = "病符星五行属水，性质类似天月星。"
                          "有病符星的人可能在健康方面需要注意。"
                          "代表一种病态的气质。",
            .key_effect = "性质类似天月星",
            .is_fixed = true
        }},
        {"大耗", {
            .name = "大耗",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Huo,
            .description = "大耗星五行属火，代表消耗和投机。"
                          "有大耗星的人投机性强，有赌性。"
                          "在财务上可能有较大的起伏。",
            .key_effect = "增加投机性，赌性",
            .is_fixed = true
        }},
        {"伏兵", {
            .name = "伏兵",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Huo,
            .description = "伏兵星五行属火，代表隐藏和警惕。"
                          "有伏兵星的人比较多疑，缺乏安全感。"
                          "做事谨慎，但也可能过于担忧。",
            .key_effect = "增加多疑，不安全感",
            .is_fixed = true
        }},
        {"官府", {
            .name = "官府",
            .category = ShenShaCategory::BoShi,
            .wu_xing = XingYaoWuXing::Huo,
            .description = "官府星五行属火，代表官非和是非。"
                          "有官府星的人可能容易遇到是非或官司。"
                          "需要注意言行，避免不必要的纠纷。",
            .key_effect = "增加是非、官非的概率",
            .is_fixed = true
        }},

        // ==================== 将前十二神 ====================
        {"将星", {
            .name = "将星",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "将星可以理解为一种能量增益器。"
                          "在流月流日遇到将星时，会让人看起来精神比较饱满。"
                          "整体状态会有所提升。",
            .key_effect = "能量增益器，精神饱满",
            .is_fixed = false
        }},
        {"攀鞍", {
            .name = "攀鞍",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "攀鞍可以理解为移动的三台八座。"
                          "在流月流日遇到攀鞍时，会短暂地增加知名度。"
                          "可能会有一些抛头露面的机会。",
            .key_effect = "移动的三台八座，短暂增加知名度",
            .is_fixed = false
        }},
        {"岁驿", {
            .name = "岁驿",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "岁驿效果和天马星类似，代表改变、变迁、奔忙。"
                          "在流月流日遇到岁驿时，会有想改变或者寻求变化的心态。"
                          "可能会有出行或搬迁的情况。",
            .key_effect = "类似天马星，代表改变、变迁、奔忙",
            .is_fixed = false
        }},
        {"息神", {
            .name = "息神",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "息神会让意志比较消沉。"
                          "在流月流日遇到息神时，容易破罐子破摔。"
                          "遇到困难比较容易产生放弃的心思。",
            .key_effect = "意志消沉，容易放弃",
            .is_fixed = false
        }},
        {"华盖", {
            .name = "华盖",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "可以理解为临时的华盖星。"
                          "在流月流日遇到华盖时，会增加艺术气息和孤高感。"
                          "由于只影响流月和流日，效果是短暂的。",
            .key_effect = "临时的华盖星",
            .is_fixed = false
        }},
        {"劫煞", {
            .name = "劫煞",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "劫煞容易产生一种突然的精神压力。"
                          "在流月流日遇到劫煞时，可能会有意想不到的压力。"
                          "需要注意调节情绪。",
            .key_effect = "突然的精神压力",
            .is_fixed = false
        }},
        {"灾煞", {
            .name = "灾煞",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "灾煞代表一种意外的困扰。"
                          "在流月流日遇到灾煞时，可能会有一些小意外或困难。"
                          "需要多加小心。",
            .key_effect = "意外的困扰",
            .is_fixed = false
        }},
        {"天煞", {
            .name = "天煞",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "天煞代表一种来自长辈或上司的压力。"
                          "在流月流日遇到天煞时，可能会受到来自上位者的压力。"
                          "需要注意与长辈或上司的关系。",
            .key_effect = "来自长辈或上司的压力",
            .is_fixed = false
        }},
        {"指背", {
            .name = "指背",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "指背代表一种被人背后议论的情况。"
                          "在流月流日遇到指背时，可能会有流言蜚语。"
                          "需要注意言行，避免被人抓住把柄。",
            .key_effect = "被人背后议论",
            .is_fixed = false
        }},
        {"咸池", {
            .name = "咸池",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "可以理解为临时的咸池星。"
                          "在流月流日遇到咸池时，桃花运会有所增加。"
                          "但需要注意把握分寸。",
            .key_effect = "临时的咸池星",
            .is_fixed = false
        }},
        {"月煞", {
            .name = "月煞",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "月煞代表一种来自女性的压力。"
                          "在流月流日遇到月煞时，可能会有来自女性的困扰。"
                          "需要注意与女性的关系。",
            .key_effect = "来自女性的压力",
            .is_fixed = false
        }},
        {"亡神", {
            .name = "亡神",
            .category = ShenShaCategory::JiangQian,
            .wu_xing = nullopt,
            .description = "亡神让人比较马大哈，代表着一种意外。"
                          "在流月流日遇到亡神时，可能会丢三落四导致物品丢失。"
                          "或者买了没用的东西导致钱财浪费。",
            .key_effect = "马大哈，容易丢三落四",
            .is_fixed = false
        }},

        // ==================== 岁前十二神 ====================
        {"岁建", {
            .name = "岁建",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "岁建固定出现在流年命宫，代表一年的开始。"
                          "岁建所在的宫位是流年的核心，代表这一年的主基调。"
                          "是流年分析的重要参考点。",
            .key_effect = "固定在流年命宫，代表一年开始",
            .is_fixed = false
        }},
        {"晦气", {
            .name = "晦气",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "晦气增加情绪的不稳定性。"
                          "在流月流日遇到晦气时，就是传说中的水逆。"
                          "情绪容易波动，需要注意调节。",
            .key_effect = "增加情绪不稳定，水逆",
            .is_fixed = false
        }},
        {"丧门", {
            .name = "丧门",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "丧门增加悲观情绪。"
                          "在流月流日遇到丧门时，可能会比较低落。"
                          "需要注意保持积极心态。",
            .key_effect = "增加悲观情绪",
            .is_fixed = false
        }},
        {"贯索", {
            .name = "贯索",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "贯索增加束缚感。"
                          "在流月流日遇到贯索时，可能会感到被限制。"
                          "做事可能会有诸多阻碍。",
            .key_effect = "增加束缚感",
            .is_fixed = false
        }},
        {"官符", {
            .name = "官符",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "官符代表官非，或者与公家打交道。"
                          "在流月流日遇到官符时，可能需要处理一些官方事务。"
                          "需要注意遵守法律法规。",
            .key_effect = "代表官非或与公家打交道",
            .is_fixed = false
        }},
        // 注意：岁前十二神中的小耗、大耗与博士十二神中重名，使用不同的key区分
        {"岁前小耗", {
            .name = "小耗",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "岁前小耗增加消费欲望。"
                          "在流月流日遇到小耗时，可能会有一些额外的支出。"
                          "需要注意控制消费。",
            .key_effect = "增加消费欲望",
            .is_fixed = false
        }},
        {"岁前大耗", {
            .name = "大耗",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "岁前大耗增加消费欲望，特别是与异性之间的共同消费。"
                          "在流月流日遇到大耗时，可能会有较大的支出。"
                          "尤其注意在异性交往中的花费。",
            .key_effect = "增加消费欲望，特别是与异性共同消费",
            .is_fixed = false
        }},
        {"龙德", {
            .name = "龙德",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "龙德增加物质方面的幸运值，能够降低煞星的力量。"
                          "在流月流日遇到龙德时，会比较顺利。"
                          "是一颗吉星，能化解一些不好的影响。",
            .key_effect = "增加物质幸运值，降低煞星力量",
            .is_fixed = false
        }},
        {"白虎", {
            .name = "白虎",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "白虎增加冲动性，会增强煞星的力量。"
                          "在流月流日遇到白虎时，需要特别注意控制情绪。"
                          "避免冲动行事带来不良后果。",
            .key_effect = "增加冲动性，增强煞星力量",
            .is_fixed = false
        }},
        {"天德", {
            .name = "天德",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "天德增加名声，能够降低煞星的力量。"
                          "在流月流日遇到天德时，有利于提升声誉。"
                          "是一颗吉星，能带来正面的影响。",
            .key_effect = "增加名声，降低煞星力量",
            .is_fixed = false
        }},
        {"吊客", {
            .name = "吊客",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "吊客增加悲观情绪，会增强煞星的力量。"
                          "在流月流日遇到吊客时，情绪可能比较低落。"
                          "需要注意调节心态。",
            .key_effect = "增加悲观情绪，增强煞星力量",
            .is_fixed = false
        }},
        {"岁前病符", {
            .name = "病符",
            .category = ShenShaCategory::SuiQian,
            .wu_xing = nullopt,
            .description = "岁前病符增加病态感，会增强煞星的力量。"
                          "在流月流日遇到病符时，需要注意健康。"
                          "可能会有一些小病小痛。",
            .key_effect = "增加病态感，增强煞星力量",
            .is_fixed = false
        }}
    };

    // ============= ShenShaDocument::to_string 实现 =============

    string ShenShaDocument::to_string() const {
        ostringstream oss;
        
        oss << "【" << name << "】\n";
        oss << "━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
        
        oss << "神煞分类: " << Mapper::to_zh(category) << "\n";
        oss << "类型: " << (is_fixed ? "固定（出生后不变）" : "流动（随流年变化）") << "\n";
        
        if (wu_xing.has_value()) {
            oss << "五行: " << Mapper::to_zh(wu_xing.value()) << "\n";
        }
        
        oss << "━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
        
        if (!key_effect.empty()) {
            oss << "核心效果: " << key_effect << "\n";
        }
        
        if (!description.empty()) {
            oss << "\n" << description << "\n";
        }
        
        return oss.str();
    }

    // ============= 实现函数 =============

    string get_shen_sha_category_description(ShenShaCategory category) {
        auto it = SHEN_SHA_CATEGORY_DESCRIPTIONS.find(category);
        if (it != SHEN_SHA_CATEGORY_DESCRIPTIONS.end()) {
            return it->second;
        }
        return "";
    }

    vector<string> get_shen_sha_by_category(ShenShaCategory category) {
        auto it = SHEN_SHA_CATEGORY_STARS.find(category);
        if (it != SHEN_SHA_CATEGORY_STARS.end()) {
            return it->second;
        }
        return {};
    }

    vector<CategoryInfo> get_all_shen_sha_categories() {
        vector<CategoryInfo> result;
        
        for (int i = 0; i < static_cast<int>(ShenShaCategory::COUNT); ++i) {
            auto cat = static_cast<ShenShaCategory>(i);
            CategoryInfo info;
            info.name = string(Mapper::to_zh(cat));
            
            auto desc_it = SHEN_SHA_CATEGORY_DESCRIPTIONS.find(cat);
            if (desc_it != SHEN_SHA_CATEGORY_DESCRIPTIONS.end()) {
                info.description = desc_it->second;
            }
            
            auto stars_it = SHEN_SHA_CATEGORY_STARS.find(cat);
            if (stars_it != SHEN_SHA_CATEGORY_STARS.end()) {
                info.stars = stars_it->second;
            }
            
            result.push_back(info);
        }
        
        return result;
    }

    optional<ShenShaDocument> get_shen_sha_document(const string& star_name) {
        auto it = SHEN_SHA_DATABASE.find(star_name);
        if (it != SHEN_SHA_DATABASE.end()) {
            return it->second;
        }
        
        // 尝试带前缀的查找（岁前小耗、岁前大耗、岁前病符）
        string prefixed_name = "岁前" + star_name;
        it = SHEN_SHA_DATABASE.find(prefixed_name);
        if (it != SHEN_SHA_DATABASE.end()) {
            return it->second;
        }
        
        return nullopt;
    }

    optional<ShenShaCategory> get_shen_sha_category(const string& star_name) {
        auto doc = get_shen_sha_document(star_name);
        if (doc.has_value()) {
            return doc->category;
        }
        return nullopt;
    }

    vector<string> get_all_shen_sha_names() {
        vector<string> result;
        for (const auto& [key, doc] : SHEN_SHA_DATABASE) {
            result.push_back(doc.name);
        }
        return result;
    }

    bool is_fixed_shen_sha(const string& star_name) {
        auto doc = get_shen_sha_document(star_name);
        if (doc.has_value()) {
            return doc->is_fixed;
        }
        return false;
    }

    bool is_dynamic_shen_sha(const string& star_name) {
        auto doc = get_shen_sha_document(star_name);
        if (doc.has_value()) {
            return !doc->is_fixed;
        }
        return false;
    }

} // namespace ZhouYi::ZiWei::StarDoc
