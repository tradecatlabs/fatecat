#!/usr/bin/env python3
"""
Batch 2: Generate 20 real hexagrams (取象法) + 20 controls + blinding
"""
import json
import random
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts'))
from meihua_calc import (
    BAGUA, HEXAGRAMS, _analyze_hexagram,
    get_hexagram_strategy, get_position_risk, STRATEGY_NEXT_STEPS
)

# ============================================================
# 20 Events (E13-E32) with 取象法 hexagram casting
# ============================================================
EVENTS = [
    {
        "event_id": "E13",
        "event_title_zh": "2026年F1澳洲大獎賽",
        "event_title_en": "2026 F1 Australian Grand Prix",
        "event_domain": "Sports",
        "expected_date": "2026-03-08",
        "event_description": "F1 2026 season opener at Albert Park, Melbourne. First race with revolutionary new regulation cars featuring active aero and smaller engines. New teams and driver lineups debut.",
        "quxiang": {
            "analysis": "F1賽車=震（車、速度、競爭、運動員）；大獎賽=乾（金、冠軍、最高榮譽）",
            "upper_trigram": 4,  # 震 (cars, speed, competition)
            "lower_trigram": 1,  # 乾 (grand prize, gold, champion)
            "upper_reason": "震：賽車、速度、競爭、運動——F1的核心意象",
            "lower_reason": "乾：大獎、金牌、冠軍、最高級別——Grand Prix的本質",
        },
    },
    {
        "event_id": "E14",
        "event_title_zh": "哥倫比亞國會大選",
        "event_title_en": "Colombia Parliamentary Election",
        "event_domain": "Politics",
        "expected_date": "2026-03-08",
        "event_description": "Colombia's parliamentary elections for Senate and House of Representatives. Test of Petro government's political support midway through his term.",
        "quxiang": {
            "analysis": "國會=乾（官方、政權、國家機構）；大選=兌（口舌、辯論、民意表達、投票）",
            "upper_trigram": 1,  # 乾 (government, authority, parliament)
            "lower_trigram": 2,  # 兌 (election, speech, public opinion)
            "upper_reason": "乾：國會、政權、官方機構——政府權力的象徵",
            "lower_reason": "兌：選舉、投票、辯論、口舌——民意表達的過程",
        },
    },
    {
        "event_id": "E15",
        "event_title_zh": "美國編劇工會獎頒獎典禮",
        "event_title_en": "Writers Guild of America Awards Ceremony",
        "event_domain": "Culture/Entertainment",
        "expected_date": "2026-03-08",
        "event_description": "WGA Awards night, a key Oscar precursor for screenwriting. Honors best original and adapted screenplays of the year.",
        "quxiang": {
            "analysis": "編劇=離（文人、文書、書籍）；獎=兌（喜悅、金屬、讚美）；頒獎典禮=離+兌（光明舞台+喜悅表彰）",
            "upper_trigram": 3,  # 離 (writing, literature, arts, stage lights)
            "lower_trigram": 2,  # 兌 (awards, joy, praise, applause)
            "upper_reason": "離：文人、文書、書籍——編劇的核心屬性",
            "lower_reason": "兌：喜悅、獎項、讚美、口碑——頒獎的本質",
        },
    },
    {
        "event_id": "E16",
        "event_title_zh": "喬治亞州聯邦眾議院特別選舉",
        "event_title_en": "Georgia Special U.S. House Election",
        "event_domain": "Politics",
        "expected_date": "2026-03-10",
        "event_description": "Special general election to fill a vacant U.S. House seat in Georgia. A single-day vote with a clear winner determining partisan balance.",
        "quxiang": {
            "analysis": "聯邦=乾（國家、官方、最高權力）；眾議院=坤（眾人、民眾基礎）；特別選舉=震（突發、特別、異常之動）",
            "upper_trigram": 1,  # 乾 (federal, national authority)
            "lower_trigram": 8,  # 坤 (众人, the masses, the House)
            "upper_reason": "乾：聯邦、國家、最高權力——聯邦政府的象徵",
            "lower_reason": "坤：眾人、民眾、基礎——眾議院代表人民",
        },
    },
    {
        "event_id": "E17",
        "event_title_zh": "Pixar動畫《跳跳蟲》首週票房",
        "event_title_en": "Pixar Hoppers Opening Weekend Box Office",
        "event_domain": "Culture/Entertainment",
        "expected_date": "2026-03-08",
        "event_description": "Pixar's Hoppers opening weekend. Animated sci-fi about human mind transferred to robotic beaver to interact with animals. Jon Hamm, Piper Curda voice cast.",
        "quxiang": {
            "analysis": "動畫=離（色彩、光影、螢幕）；跳跳蟲=震（跳躍、活力、運動）；票房=兌（金錢、收穫）",
            "upper_trigram": 3,  # 離 (animation, screen, colorful, light)
            "lower_trigram": 4,  # 震 (hopping, jumping, movement, vitality)
            "upper_reason": "離：動畫、色彩、光影、螢幕——Pixar動畫的視覺本質",
            "lower_reason": "震：跳躍、活力、運動——「跳跳蟲」的核心意象",
        },
    },
    {
        "event_id": "E18",
        "event_title_zh": "NVIDIA GTC大會黃仁勳主題演講",
        "event_title_en": "NVIDIA GTC 2026 Jensen Huang Keynote",
        "event_domain": "Technology",
        "expected_date": "2026-03-17",
        "event_description": "Jensen Huang's keynote at NVIDIA GTC 2026 in San Jose. Expected to announce next-gen AI chips, software platforms, and robotics developments.",
        "quxiang": {
            "analysis": "NVIDIA/GPU/AI=離（電子、科技、光明、網路）；黃仁勳=乾（CEO、領袖、最高）；大會=坤（聚集）",
            "upper_trigram": 3,  # 離 (electronics, tech, light, AI, GPU)
            "lower_trigram": 1,  # 乾 (CEO, leader, premium, high-end)
            "upper_reason": "離：電子科技、GPU、AI、網路——NVIDIA的產業屬性",
            "lower_reason": "乾：CEO、領袖、最高端——黃仁勳的角色與NVIDIA的頂級地位",
        },
    },
    {
        "event_id": "E19",
        "event_title_zh": "聯準會三月利率決議",
        "event_title_en": "FOMC March Interest Rate Decision",
        "event_domain": "Economy",
        "expected_date": "2026-03-18",
        "event_description": "Federal Reserve announces March rate decision after two-day FOMC meeting. Markets expect rates held at 3.5-3.75%. Any surprise cut or hawkish language would move markets.",
        "quxiang": {
            "analysis": "聯準會=乾（官方權威、最高金融機構）；利率=坎（水、流動性、金融之水）；決議=艮（止、定、決斷）",
            "upper_trigram": 1,  # 乾 (Federal Reserve, authority, official)
            "lower_trigram": 6,  # 坎 (interest rates, liquidity, financial flow)
            "upper_reason": "乾：聯準會、官方權威、最高金融機構——央行的地位",
            "lower_reason": "坎：水、流動性、利率——金融之水的流向",
        },
    },
    {
        "event_id": "E20",
        "event_title_zh": "歐盟理事會春季高峰會議",
        "event_title_en": "European Council Spring Summit",
        "event_domain": "International/Diplomacy",
        "expected_date": "2026-03-19",
        "event_description": "EU heads of state meet in Brussels to discuss defense spending, Ukraine policy, economic strategy, and trade relations. Summit conclusions published at close.",
        "quxiang": {
            "analysis": "高峰=艮（山、高處、頂層）；歐盟理事會=乾（國家領袖、官方、最高層級）；會議=兌（討論、口舌）",
            "upper_trigram": 7,  # 艮 (summit, mountain top, highest gathering)
            "lower_trigram": 1,  # 乾 (heads of state, officials, leaders)
            "upper_reason": "艮：高峰、山頂、頂層——高峰會議的核心意象",
            "lower_reason": "乾：國家元首、官方領袖——歐盟各國首腦",
        },
    },
    {
        "event_id": "E21",
        "event_title_zh": "電影《乘客計畫》全球首映",
        "event_title_en": "Project Hail Mary Global Premiere",
        "event_domain": "Culture/Entertainment",
        "expected_date": "2026-03-20",
        "event_description": "Ryan Gosling stars in Amazon MGM's sci-fi adaptation of Andy Weir's novel. An astronaut wakes alone in space on a mission to save Earth from extinction. IMAX release.",
        "quxiang": {
            "analysis": "太空=乾（天、宇宙、最高處）；電影首映=離（光影、螢幕、火）；孤獨太空人=坎（隱伏、孤獨、險）",
            "upper_trigram": 1,  # 乾 (space, cosmos, heaven, the highest)
            "lower_trigram": 3,  # 離 (film, light, screen, fire/rocket)
            "upper_reason": "乾：太空、宇宙、天——故事的核心場景",
            "lower_reason": "離：電影、光影、螢幕——首映的媒介本質",
        },
    },
    {
        "event_id": "E22",
        "event_title_zh": "世界室內田徑錦標賽",
        "event_title_en": "World Athletics Indoor Championships",
        "event_domain": "Sports",
        "expected_date": "2026-03-21",
        "event_description": "Biennial World Athletics Indoor Championships in Nanjing, China. Top track and field athletes compete for gold in sprints, jumps, throws, and distance events.",
        "quxiang": {
            "analysis": "田徑=震（運動、足、跑步、競技）；室內=艮（門、室、封閉空間、止）；錦標=乾（金、冠）",
            "upper_trigram": 4,  # 震 (athletics, running, movement, competition)
            "lower_trigram": 7,  # 艮 (indoor, enclosed space, building)
            "upper_reason": "震：運動、跑步、足、競技——田徑的本質",
            "lower_reason": "艮：室內、建築、門、封閉空間——室內場館",
        },
    },
    {
        "event_id": "E23",
        "event_title_zh": "南澳大利亞州議會選舉",
        "event_title_en": "South Australia State Election",
        "event_domain": "Politics",
        "expected_date": "2026-03-21",
        "event_description": "South Australia state election for House of Assembly and Legislative Council. Determines state government leadership.",
        "quxiang": {
            "analysis": "州=坤（地方、大地、區域）；議會選舉=兌（投票、辯論、口舌、民意）；南澳=離（南方）+坤（地）",
            "upper_trigram": 8,  # 坤 (state/local, land, territory, the masses)
            "lower_trigram": 2,  # 兌 (election, voting, public debate)
            "upper_reason": "坤：州、地方、大地、區域——州級行政的屬性",
            "lower_reason": "兌：選舉、投票、辯論——議會選舉的過程",
        },
    },
    {
        "event_id": "E24",
        "event_title_zh": "聯合國全球反詐欺高峰會",
        "event_title_en": "UN/INTERPOL Global Fraud Summit",
        "event_domain": "International/Diplomacy",
        "expected_date": "2026-03-16",
        "event_description": "UNODC/INTERPOL ministerial-level meeting at Vienna International Centre on combating transnational cybercrime and online fraud globally.",
        "quxiang": {
            "analysis": "高峰會=艮（山頂、聚合、止）；反詐欺=離（揭露、照明、明察）+坎（險、盜賊）；聯合國=乾（國際權威）",
            "upper_trigram": 7,  # 艮 (summit, gathering, stopping crime)
            "lower_trigram": 3,  # 離 (exposure, illumination, investigation)
            "upper_reason": "艮：高峰會、止（制止犯罪）、聚合——打擊犯罪的意象",
            "lower_reason": "離：揭露、照明、明察秋毫——反詐欺=照亮黑暗",
        },
    },
    {
        "event_id": "E25",
        "event_title_zh": "邁阿密公開賽網球男單決賽",
        "event_title_en": "Miami Open Men's Singles Final",
        "event_domain": "Sports",
        "expected_date": "2026-03-29",
        "event_description": "ATP Masters 1000 men's singles final in Miami. One of tennis' most prestigious hard-court tournaments. Winner receives 1000 ranking points.",
        "quxiang": {
            "analysis": "網球=兌（圓球、金屬球拍、喜悅）；決賽=乾（冠軍、最高）；邁阿密=離（南方、熱帶、火熱）",
            "upper_trigram": 2,  # 兌 (ball, round object, joy of competition)
            "lower_trigram": 3,  # 離 (Miami heat, south, fierce competition)
            "upper_reason": "兌：球（圓物）、金屬球拍、勝利的喜悅——網球的意象",
            "lower_reason": "離：南方、熱帶、火熱的競爭——邁阿密的地理與賽事的激烈",
        },
    },
    {
        "event_id": "E26",
        "event_title_zh": "F1日本大獎賽鈴鹿站",
        "event_title_en": "F1 Japanese Grand Prix at Suzuka",
        "event_domain": "Sports",
        "expected_date": "2026-03-29",
        "event_description": "F1 Japanese Grand Prix at Suzuka Circuit. Third race of the 2026 season. Suzuka's figure-8 layout is one of the most demanding circuits in motorsport.",
        "quxiang": {
            "analysis": "F1賽車=震（車、速度、運動）；日本=離（日、太陽、東方）；鈴鹿=兌（鈴聲、金屬聲）",
            "upper_trigram": 4,  # 震 (racing cars, speed, movement)
            "lower_trigram": 3,  # 離 (Japan=日=sun, eastern, fire)
            "upper_reason": "震：賽車、速度、運動、震動——F1的核心屬性",
            "lower_reason": "離：日本（日=太陽）、東方、光明——日本的類象",
        },
    },
    {
        "event_id": "E27",
        "event_title_zh": "NCAA男籃全國冠軍賽",
        "event_title_en": "NCAA Men's Basketball Championship Game",
        "event_domain": "Sports",
        "expected_date": "2026-04-06",
        "event_description": "National championship game in Indianapolis, concluding March Madness. Single decisive game between the Final Four survivors. Clear winner and national champion.",
        "quxiang": {
            "analysis": "NCAA=坤（大學、眾多隊伍、大地基礎）；男籃=震（跳躍、運動、彈跳）；冠軍賽=乾（最高）",
            "upper_trigram": 8,  # 坤 (universities, many teams, mass participation)
            "lower_trigram": 4,  # 震 (basketball, jumping, bouncing, movement)
            "upper_reason": "坤：大學、眾多隊伍、廣闊的參與基礎——NCAA的特性",
            "lower_reason": "震：籃球、跳躍、彈跳、身體衝撞——籃球運動的意象",
        },
    },
    {
        "event_id": "E28",
        "event_title_zh": "名人賽高爾夫大滿貫",
        "event_title_en": "The Masters Golf Tournament",
        "event_domain": "Sports",
        "expected_date": "2026-04-12",
        "event_description": "The Masters at Augusta National Golf Club. Golf's first major of 2026. The champion receives the iconic green jacket on Sunday, April 12.",
        "quxiang": {
            "analysis": "名人=乾（貴人、名人、高貴）；高爾夫=巽（草地、花園、風、柔和）；大滿貫=乾（大、金、最高榮譽）",
            "upper_trigram": 1,  # 乾 (celebrities, nobles, premium, grand)
            "lower_trigram": 5,  # 巽 (golf course=grass/garden, wind, gentle)
            "upper_reason": "乾：名人、貴人、最高榮譽——名人賽的尊貴地位",
            "lower_reason": "巽：草地、花園、風——高爾夫球場的自然意象",
        },
    },
    {
        "event_id": "E29",
        "event_title_zh": "秘魯總統大選",
        "event_title_en": "Peru Presidential Election",
        "event_domain": "Politics",
        "expected_date": "2026-04-12",
        "event_description": "Peru's general election for president and congress. Major Latin American democracy chooses new leadership amid economic and political challenges.",
        "quxiang": {
            "analysis": "秘魯=艮（安第斯山脈國家、山地）；總統大選=乾（最高領導人）+兌（投票、選舉）",
            "upper_trigram": 7,  # 艮 (Peru=Andes mountains, mountainous country)
            "lower_trigram": 2,  # 兌 (election, voting, public expression)
            "upper_reason": "艮：山、安第斯——秘魯的地理象徵",
            "lower_reason": "兌：選舉、投票、辯論——大選的過程",
        },
    },
    {
        "event_id": "E30",
        "event_title_zh": "匈牙利國會大選",
        "event_title_en": "Hungary Parliamentary Election",
        "event_domain": "Politics",
        "expected_date": "2026-04-12",
        "event_description": "Hungary parliamentary elections. Viktor Orbán's Fidesz seeks re-election. Opposition united under Peter Magyar's TISZA party. High stakes for EU relations.",
        "quxiang": {
            "analysis": "匈牙利=坤（中歐平原、大地）；國會=乾（官方、政權、國家機構）；大選=兌（投票）",
            "upper_trigram": 8,  # 坤 (Hungarian plain, continental Europe, land)
            "lower_trigram": 1,  # 乾 (parliament, government, authority)
            "upper_reason": "坤：匈牙利大平原、中歐大地——匈牙利的地理象徵",
            "lower_reason": "乾：國會、政權、官方——國家政治權力的核心",
        },
    },
    {
        "event_id": "E31",
        "event_title_zh": "NASA阿提米絲二號載人繞月任務",
        "event_title_en": "NASA Artemis II Crewed Lunar Flyby Mission",
        "event_domain": "Science/Space",
        "expected_date": "2026-04-01",
        "event_description": "First crewed mission beyond low Earth orbit since Apollo 17 in 1972. Four astronauts on a 10-day lunar flyby. Critical test before Artemis III lunar landing.",
        "quxiang": {
            "analysis": "阿提米絲=月神→坎（月亮）；繞月=巽（環繞、往返、飛行）；載人任務=坤（人、承載）",
            "upper_trigram": 6,  # 坎 (moon, Artemis=moon goddess)
            "lower_trigram": 5,  # 巽 (flight, orbiting, wind, going/returning)
            "upper_reason": "坎：月亮、月球——阿提米絲（月神）的直接象徵",
            "lower_reason": "巽：飛行、環繞、往返——繞月飛行的軌道意象",
        },
    },
    {
        "event_id": "E32",
        "event_title_zh": "印度加甘揚無人太空試飛",
        "event_title_en": "ISRO Gaganyaan Uncrewed Orbital Test Flight",
        "event_domain": "Science/Space",
        "expected_date": "2026-03-30",
        "event_description": "India's first uncrewed orbital test flight of the Gaganyaan spacecraft. Critical step toward India's human spaceflight program. Tests life support and re-entry systems.",
        "quxiang": {
            "analysis": "太空試飛=震（發射、起飛、動力）；印度=離（南方、熱帶）；無人飛船=坤（空虛、大地出發）+乾（天）",
            "upper_trigram": 4,  # 震 (launch, liftoff, explosive force, movement)
            "lower_trigram": 8,  # 坤 (earth/ground, unmanned=empty vessel, India as land)
            "upper_reason": "震：發射、起飛、爆發力——火箭升空的意象",
            "lower_reason": "坤：大地（從地面發射）、無人（空虛的飛船）——出發點",
        },
    },
]

def compute_changing_line(upper, lower):
    """動爻 = (先天八卦數 of 上卦 + 先天八卦數 of 下卦) mod 6, 餘0為6"""
    total = upper + lower
    remainder = total % 6
    return 6 if remainder == 0 else remainder

def compute_full_hexagram(upper, lower, dong_yao):
    """Compute full hexagram analysis using meihua_calc functions"""
    result = _analyze_hexagram(upper, lower, dong_yao)
    hex_num = result["本卦"]["序號"]

    # Get strategy
    strategy = get_hexagram_strategy(hex_num)

    # Get position risk
    binary = result["本卦"]["二進位"]
    is_yang = binary[6 - dong_yao] == '1'
    risk = get_position_risk(dong_yao, is_yang)

    return result, strategy, risk, is_yang

def main():
    # ============================================================
    # Step 1: Compute real hexagrams using 取象法
    # ============================================================
    real_hexagrams = []
    for event in EVENTS:
        q = event["quxiang"]
        upper = q["upper_trigram"]
        lower = q["lower_trigram"]
        dong_yao = compute_changing_line(upper, lower)

        result, strategy, risk, is_yang = compute_full_hexagram(upper, lower, dong_yao)

        real_hex = {
            "method": "取象法",
            "quxiang_analysis": q["analysis"],
            "upper_trigram": f"{upper} → {BAGUA[upper]['name']}({BAGUA[upper]['symbol']})",
            "upper_reason": q["upper_reason"],
            "lower_trigram": f"{lower} → {BAGUA[lower]['name']}({BAGUA[lower]['symbol']})",
            "lower_reason": q["lower_reason"],
            "changing_line": dong_yao,
            "changing_line_calc": f"({upper}+{lower}) mod 6 = {dong_yao}",
            "primary_hexagram": {
                "number": result["本卦"]["序號"],
                "name": result["本卦"]["名稱"],
            },
            "changed_hexagram": {
                "number": result["變卦"]["序號"],
                "name": result["變卦"]["名稱"],
            },
            "mutual_hexagram": {
                "name": result["互卦"]["名稱"],
            },
            "ti_yong": result["體用"],
            "strategy": strategy,
            "position_risk": risk,
            "next_step": STRATEGY_NEXT_STEPS.get(strategy["advice"], "") if strategy else "",
        }

        real_hexagrams.append(real_hex)

    # ============================================================
    # Step 2: Generate 20 control hexagrams with seed 20260305
    # ============================================================
    rng = random.Random(20260305)
    control_hexagrams = []

    for i in range(20):
        # Get corresponding real hexagram to avoid collision
        real_hex_num = real_hexagrams[i]["primary_hexagram"]["number"]
        real_chang_line = real_hexagrams[i]["changing_line"]

        # Generate control, re-roll if it matches the real hexagram
        while True:
            hex_num = rng.randint(1, 64)
            chang_line = rng.randint(1, 6)
            if hex_num != real_hex_num or chang_line != real_chang_line:
                break

        # Find the upper/lower trigrams for this hexagram number
        upper_ctrl = lower_ctrl = None
        for (u, l), (num, name) in HEXAGRAMS.items():
            if num == hex_num:
                upper_ctrl, lower_ctrl = u, l
                break

        result, strategy, risk, is_yang = compute_full_hexagram(upper_ctrl, lower_ctrl, chang_line)

        control_hex = {
            "method": "random",
            "primary_hexagram": {
                "number": result["本卦"]["序號"],
                "name": result["本卦"]["名稱"],
            },
            "changing_line": chang_line,
            "changed_hexagram": {
                "number": result["變卦"]["序號"],
                "name": result["變卦"]["名稱"],
            },
            "mutual_hexagram": {
                "name": result["互卦"]["名稱"],
            },
            "ti_yong": result["體用"],
        }
        control_hexagrams.append(control_hex)

    # ============================================================
    # Step 3: Random A/B blinding assignment
    # ============================================================
    rng_blind = random.Random(20260305 + 1)  # Different seed for blinding
    blinding = []

    for i in range(20):
        real_is_A = rng_blind.choice([True, False])
        blinding.append({"real_is_A": real_is_A})

    # ============================================================
    # Step 4: Build full casting records
    # ============================================================
    casting_records = {
        "generated": "2026-03-05",
        "batch": 2,
        "method": "取象法 (Imagery-based hexagram casting)",
        "random_seed": 20260305,
        "blinding_seed": 20260306,
        "events": [],
    }

    blinding_key = {
        "generated": "2026-03-05",
        "batch": 2,
        "warning": "SEALED until evaluation phase. Do not open during interpretation.",
        "events": [],
    }

    for i, event in enumerate(EVENTS):
        entry = {
            "event_id": event["event_id"],
            "event_title_zh": event["event_title_zh"],
            "event_title_en": event["event_title_en"],
            "event_domain": event["event_domain"],
            "expected_date": event["expected_date"],
            "event_description": event["event_description"],
            "real_hexagram": real_hexagrams[i],
            "control_hexagram": control_hexagrams[i],
            "blinding": blinding[i],
        }
        casting_records["events"].append(entry)

        blinding_key["events"].append({
            "event_id": event["event_id"],
            "real_is_A": blinding[i]["real_is_A"],
            "label_A": "real" if blinding[i]["real_is_A"] else "control",
            "label_B": "control" if blinding[i]["real_is_A"] else "real",
        })

    # ============================================================
    # Step 5: Write output files
    # ============================================================
    base_dir = os.path.dirname(__file__)

    # Casting records
    casting_path = os.path.join(base_dir, "casting_records_batch2.json")
    with open(casting_path, "w", encoding="utf-8") as f:
        json.dump(casting_records, f, ensure_ascii=False, indent=2)
    print(f"Written: {casting_path}")

    # Random seed file
    seed_path = os.path.join(base_dir, "random_seed_batch2.txt")
    with open(seed_path, "w") as f:
        f.write("Batch 2 Random Seed: 20260305\n")
        f.write("Blinding Seed: 20260306\n")
        f.write("Generated: 2026-03-05\n")
        f.write("Method: Python random.Random(20260305) for control hexagrams\n")
        f.write("        Python random.Random(20260306) for A/B assignment\n")
    print(f"Written: {seed_path}")

    # Blinding key
    interp_dir = os.path.join(base_dir, "..", "interpretations")
    blinding_path = os.path.join(interp_dir, "blinding_key_batch2.json")
    with open(blinding_path, "w", encoding="utf-8") as f:
        json.dump(blinding_key, f, ensure_ascii=False, indent=2)
    print(f"Written: {blinding_path}")

    # ============================================================
    # Step 6: Print summary for verification
    # ============================================================
    print("\n" + "=" * 70)
    print("BATCH 2 SUMMARY — 20 Events (E13-E32)")
    print("=" * 70)

    for i, event in enumerate(EVENTS):
        eid = event["event_id"]
        rh = real_hexagrams[i]
        ch = control_hexagrams[i]
        bl = blinding[i]

        real_label = "A" if bl["real_is_A"] else "B"
        ctrl_label = "B" if bl["real_is_A"] else "A"

        print(f"\n{eid}: {event['event_title_zh']} ({event['expected_date']})")
        print(f"  Real ({real_label}): {rh['primary_hexagram']['number']} {rh['primary_hexagram']['name']} → "
              f"{rh['changed_hexagram']['number']} {rh['changed_hexagram']['name']} (Line {rh['changing_line']})")
        print(f"  Ctrl ({ctrl_label}): {ch['primary_hexagram']['number']} {ch['primary_hexagram']['name']} → "
              f"{ch['changed_hexagram']['number']} {ch['changed_hexagram']['name']} (Line {ch['changing_line']})")
        if rh['strategy']:
            print(f"  Strategy: {rh['strategy']['type']} / {rh['strategy']['advice']} / {rh['strategy']['ji_rate']}%")

if __name__ == "__main__":
    main()
