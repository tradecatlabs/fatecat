#!/usr/bin/env python3
import argparse
import json
import os
import hashlib

from generate_reading_seed import build_seed
from cast_symbols import cast

GEN = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
CTRL = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}

ELEMENT_META = {
    '木': {
        'name': '生发之气',
        'core': '主开路、起意、生长、扩展',
        'risk': '也容易心急、飘、根基未稳'
    },
    '火': {
        'name': '明动之气',
        'core': '主点亮、加速、外显、推动',
        'risk': '也容易过热、躁进、烧得太快'
    },
    '土': {
        'name': '承载之气',
        'core': '主承接、现实、稳定、盘面',
        'risk': '也容易迟滞、负重、推进偏慢'
    },
    '金': {
        'name': '裁断之气',
        'core': '主规则、边界、判断、取舍',
        'risk': '也容易偏硬、偏冷、压感较重'
    },
    '水': {
        'name': '蓄藏之气',
        'core': '主隐伏、观察、回收、等待时机',
        'risk': '也容易多想、迟疑、回流不前'
    }
}

MODE_TO_CHINESE = {
    'general': '综合断事',
    'career': '事业 / 项目 / 决策',
    'relationship': '关系解读',
    'fortune': '当前运势 / 阶段气运',
    'personality': '人设 / 性格 / 天赋倾向'
}

SCENARIO_LABELS = {
    'quit_solo': '辞职 / 转身 / 单干',
    'partnership': '合作 / 合伙 / 接项目',
    'stuck_project': '项目卡住 / 推进受阻',
    'contact': '该不该主动联系',
    'ambiguity': '暧昧 / 推进关系',
    'reconcile': '复合 / 旧人回头',
    'unlucky': '最近总是不顺',
    'big_move': '这个阶段适不适合做大动作',
    'path': '我适合什么路子',
    'self_drain': '自耗 / 节奏失衡'
}

SCENARIO_RULES = {
    'career': [
        {'id': 'quit_solo', 'priority': 1, 'keywords': ['辞职', '单干', '自己的项目', '换赛道', '离开现在的工作']},
        {'id': 'partnership', 'priority': 1, 'keywords': ['合作', '合伙', '接项目', '一起做', '这个项目要不要接']},
        {'id': 'stuck_project', 'priority': 1, 'keywords': ['推不动', '没起色', '卡住', '方向是不是不对', '一直没有结果', '进展慢']}
    ],
    'relationship': [
        {'id': 'contact', 'priority': 1, 'keywords': ['主动联系', '联系他', '联系她', '联系对方', '找他', '找她', '打扰']},
        {'id': 'ambiguity', 'priority': 1, 'keywords': ['暧昧', '在一起', '推进关系', '进一步', '确定关系']},
        {'id': 'reconcile', 'priority': 3, 'keywords': ['前任', '复合', '旧人', '回来', '续头']}
    ],
    'fortune': [
        {'id': 'unlucky', 'priority': 1, 'keywords': ['不顺', '运气很差', '总卡住', '总是不顺', '很背']},
        {'id': 'big_move', 'priority': 1, 'keywords': ['大动作', '换工作', '谈合作', '推进大计划', '适不适合做大动作']}
    ],
    'personality': [
        {'id': 'path', 'priority': 1, 'keywords': ['适合什么路子', '适合创业', '适合做内容', '适合做产品', '适合什么路线']},
        {'id': 'self_drain', 'priority': 1, 'keywords': ['自我消耗', '自耗', '想很多', '推进很慢', '一开始很猛', '后面就散']}
    ]
}


def load_library():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, '..', 'assets', 'phrase-library.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def token(seed, slot):
    h = hashlib.sha256((seed + '|' + slot).encode('utf-8')).hexdigest()
    return int(h[:12], 16)


def choose(seed, slot, items):
    if not items:
        return ''
    return items[token(seed, slot) % len(items)]


def effect_on_subject(subject, other):
    if subject == other:
        return '比和'
    if GEN[other] == subject:
        return '生我'
    if CTRL[other] == subject:
        return '克我'
    if GEN[subject] == other:
        return '泄我'
    if CTRL[subject] == other:
        return '我克'
    return '未知'


def detect_scenario(mode, question, context=''):
    text = ('%s\n%s' % (question or '', context or '')).lower()
    rules = SCENARIO_RULES.get(mode, [])
    best = None
    best_score = 0

    for rule in rules:
        match_score = 0
        for kw in rule['keywords']:
            if kw.lower() in text:
                match_score += len(kw)
        if match_score <= 0:
            continue
        score = match_score + rule.get('priority', 0) * 100
        if score > best_score:
            best = rule['id']
            best_score = score

    return best if best_score > 0 else None


def build_scenario_overlay(mode, scenario_id, roles, metrics):
    if not scenario_id:
        return None

    env = metrics['env_effect']
    obstacle = metrics['obstacle_effect']
    trend = metrics['trend_effect']
    response = metrics['response_on_main']
    speed = metrics.get('manifestation_speed', '中')

    overlays = {
        'quit_solo': {
            'reason': {
                '克我': '这更像旧盘压力仍在，新机会并没有强到足以托你立刻转身。',
                '泄我': '眼下更像你在为这个念头持续耗心力，但承接盘还没完全长出来。',
                '生我': '外机并非没有，只是要先看它能不能接成真实承重，而不是一时兴奋。',
                '比和': '你心里想走的劲头和外部机会在互相放大，所以更要防判断失真。',
                '我克': '局面不是不能推，但主要靠你自己硬整合，成本不会低。'
            },
            'advice': {
                'hold': '这类局面更适合先做副线验证，而不是把退路一次压没。',
                'cautious': '先验需求、再算现金流、再看是否切换主线，这样比一口气辞掉更稳。',
                'move': '若要动，最好也是小规模试跑先行，让现实反馈替你做第二轮筛选。',
                'outer_block': '关键不在敢不敢走，而在你离开旧盘后有没有东西能接住你。',
                'break_build': '该减的旧耗要减，但别把还能供血的部分一起砍掉。'
            },
            'trend': {
                '快': '这类念头起得快，动作也容易一上来就大，所以更要靠验证压住冲动。',
                '中': '转身之意已起，但真正分晓还要看中程承接能不能跟上。',
                '慢': '这不是立刻翻桌的局，更像边搭新盘边等时机成熟。'
            }
        },
        'partnership': {
            'reason': {
                '生我': '合作表面上能借力，但是否真能扶主，还要看规则和边界有没有先立。',
                '克我': '对方或项目本身带着压感，若权责不清，后面很容易越做越拧。',
                '泄我': '这类合作最怕你单方面持续出力，最后变成你在托整个局。',
                '比和': '双方气口相近，容易一拍即合，但也容易一起放大同一种盲点。',
                '我克': '不是接不住，而是接下来要靠你自己不断盯规则、盯交付、盯节奏。'
            },
            'advice': {
                'hold': '先别急着一口答应，先把边界、交付、付款和退出条件谈清。',
                'cautious': '最好的应法是先小单试配合，再谈放大。',
                'move': '能接，但要带着规则接，不要带着关系接。',
                'outer_block': '眼下不是没机会，而是先立规则才能让机会不变坑。',
                'break_build': '该硬的条款要硬，不然前面图省事，后面多半要补更大的窟窿。'
            },
            'trend': {
                '快': '短期容易很快谈热，但热不等于稳，真正分水岭在后续配合。',
                '中': '先有接触与磨合，中程才知道是不是能长期一起做。',
                '慢': '这类局更适合慢慢验人验事，不适合光看眼前兴奋度。'
            }
        },
        'stuck_project': {
            'reason': {
                '克我': '项目不是单点失灵，而是当前结构在反向压你。',
                '泄我': '真正的问题更像目标过散、并行过多，导致气一直漏。',
                '生我': '方向未必全错，说明盘里仍有可借之处，只是还没接顺。',
                '比和': '你和项目当前的问题是同类相引，越着急推进，越容易把原来的毛病放大。',
                '我克': '这不是死局，但要靠你主动收线、重排优先级，才会重新动起来。'
            },
            'advice': {
                'hold': '先别急着判死刑，先看是不是节奏、承接、取舍出了问题。',
                'cautious': '建议先砍并行、缩目标、补闭环，而不是继续加功能或加动作。',
                'move': '若要推，就推最短闭环，不要同时救所有问题。',
                'outer_block': '表面像方向问题，深处常常其实是承接盘没坐稳。',
                'break_build': '先拆旧结构，再让项目回到能呼吸的状态。'
            },
            'trend': {
                '快': '卡点已经显性化，调法若对，反馈也会来得比想象快。',
                '中': '短期先看收线是否有效，中程才看项目会不会重新回暖。',
                '慢': '这类局通常不是一刀就顺，更多是靠几轮整理后才慢慢回气。'
            }
        },
        'contact': {
            'reason': {
                '生我': '对方那边未必全无回音，问题更多在怎么开口，而不只是要不要开口。',
                '克我': '你这边一动就容易更受制，所以主动方式若太重，反而会把关系压得更紧。',
                '泄我': '眼下最明显的是你心力外泄，越想越想联系，越联系越想要结果。',
                '比和': '你和这段关系当前气口互相放大，所以一点动静都容易被你读得很重。',
                '我克': '不是不能联系，只是每一步都要你自己拿捏分寸，稍重就容易失衡。'
            },
            'advice': {
                'hold': '现在更适合先守住分寸，不要拿追问去换安全感。',
                'cautious': '若要联系，宜轻、短、留白，只做一次试探，不做连击。',
                'move': '可以开口，但像敲门，不要像逼对方给答案。',
                'outer_block': '你看到的冷，不一定全是无意，也可能是对方那边还有没松开的结。',
                'break_build': '若真想重新靠近，先别急着表白情绪，先把旧误会或旧节奏理一理。'
            },
            'trend': {
                '快': '这类联系题一旦动，回应通常不会太慢，但回应快不等于结果就稳。',
                '中': '短期可见一点回音，中程还得看双方节奏能不能重新对齐。',
                '慢': '更像先观气口、后等时机，不是现在一碰就立见分晓。'
            }
        },
        'ambiguity': {
            'reason': {
                '生我': '关系里不是没有意，但意和意之间还没完全对齐。',
                '克我': '推进的阻力是真实存在的，往前并不是单靠热度就能推过去。',
                '泄我': '你这边容易先把情绪和期待压进去，结果关系还没稳，自己先累了。',
                '比和': '两边的情绪会彼此放大，所以很容易一下热、一下又冷。',
                '我克': '若要推进，只能靠你拿捏节奏，越急越容易让好感变压感。'
            },
            'advice': {
                'hold': '现在最忌催熟，关系一催就容易变形。',
                'cautious': '先松结、先留白、先让对方也有主动空间，关系才走得下去。',
                'move': '能轻推，但不要一步推到“定关系”这种重结论。',
                'outer_block': '表面有来回，不代表内里已经准备好承接更近的关系。',
                'break_build': '若真有旧结或旧顾虑，要先处理，不然热度上去后还是会掉下来。'
            },
            'trend': {
                '快': '短期会有波动和回响，但也最怕因节奏过快而回落。',
                '中': '关系能否继续往前，关键不在一时热度，而在中程能否稳定。',
                '慢': '更像慢热局，不宜抢答案。'
            }
        },
        'reconcile': {
            'reason': {
                '生我': '旧情未必全断，但未断不等于新局已成。',
                '克我': '旧关系里的压感还在，若旧结没解，回头也容易重演老问题。',
                '泄我': '这类题最怕你一直拿现在的力，去补过去留下的洞。',
                '比和': '旧情和旧习会一起翻上来，所以更要分清是怀念，还是可重建。',
                '我克': '就算有续头，也需要你们主动处理旧结，不会自己好。'
            },
            'advice': {
                'hold': '不要把“还放不下”直接等同于“适合复合”。',
                'cautious': '先辨旧结是否真解，再决定要不要重启联系。',
                'move': '若要回头，也应先从轻联系和复盘开始，不宜直接谈回到从前。',
                'outer_block': '真正难的不是有没有情，而是旧结构有没有被看见并处理。',
                'break_build': '不先拆旧刺，就很难长出新关系。'
            },
            'trend': {
                '快': '旧情翻动会比较快，但快上来的多半也是旧情绪。',
                '中': '短期像回潮，中程才知道能不能真的重建。',
                '慢': '这类题宁可慢一点，也别被一时波动误判成天意回转。'
            }
        },
        'unlucky': {
            'reason': {
                '生我': '并不是全盘都坏，说明局里仍有能回气的口，只是被杂耗压住了。',
                '克我': '你现在的受阻感是真的，不是矫情，是多股压力在一起压盘。',
                '泄我': '这更像多处漏气，不是单点倒霉。',
                '比和': '内外都在放大同一种滞感，所以你会觉得做什么都不顺。',
                '我克': '不是没有解法，而是必须主动收口、断耗、重排节奏。'
            },
            'advice': {
                'hold': '先别急着证明自己还能全线推进，先把最耗的两三处停下来。',
                'cautious': '先减耗、先补睡、先收并行，体感会比你想的回升得快。',
                'move': '可先从最容易恢复的一条线起手，让气先回流。',
                'outer_block': '你现在不一定缺机会，更像缺一口能稳稳回来的气。',
                'break_build': '要转运，先断旧耗，不要一边修一边继续漏。'
            },
            'trend': {
                '快': '如果真能收线减耗，体感改善会比你想的快。',
                '中': '短期先止漏，中程再看回升。',
                '慢': '这是回气局，不是立刻翻盘局。'
            }
        },
        'big_move': {
            'reason': {
                '生我': '局里不是没有可动之机，但能不能做大，还要看承接够不够。',
                '克我': '这个阶段的大动作阻力偏真，若硬推，多半是先消耗你。',
                '泄我': '看似想动，实则当前更像心气外泄，不适合一下开太多新口。',
                '比和': '你的冲劲和外部节奏在一起放大，所以更要防误把躁动当时机。',
                '我克': '不是完全不能动，但要靠你自己控节奏、控规模、控代价。'
            },
            'advice': {
                'hold': '宜小动，不宜大开；先试一角，不要满盘推进。',
                'cautious': '最好把动作拆成试跑、观察、再放量，而不是直接一步到位。',
                'move': '能动，但也更适合先从最关键的一处动起。',
                'outer_block': '外机有，但内盘未必已足够稳，先补盘比先放大更重要。',
                'break_build': '若非要有大变，也宜先切旧耗，再起新局。'
            },
            'trend': {
                '快': '短期会有想动的冲劲，但越快越要防动作大过承接。',
                '中': '先试，再看，再放大，这个节奏更合盘。',
                '慢': '更适合蓄势，不适合重锤。'
            }
        },
        'path': {
            'reason': {
                '生我': '你的路数里本来就有可借之势，关键在把它放进对的场景。',
                '克我': '你不是没有能力，而是一些外部要求并不天然适配你的工作法。',
                '泄我': '你容易把力用在不该长期用力的地方，所以越努力越累。',
                '比和': '你会把自己原本的倾向放得更大，所以环境对不对，影响非常明显。',
                '我克': '你有塑形能力，但如果总靠硬顶，也会把天赋用成消耗。'
            },
            'advice': {
                'hold': '先别急着追求“最厉害的路”，先找“最不反人性的路”。',
                'cautious': '真正适合你的路，多半是能让你稳定输出，而不是只靠一阵猛劲。',
                'move': '可以多试，但要边试边看什么场景最能让你既有产出又不自耗。',
                'outer_block': '你最大的误判，常常不是选错方向，而是把自己放进了不合身的节奏。',
                'break_build': '若总在旧环境里失衡，可能就该换结构，而不是继续怪自己。'
            },
            'trend': {
                '快': '这类题的答案往往不是一下顿悟，而是试几个场景后很快有体感。',
                '中': '短期先辨适配，中程才看定型。',
                '慢': '真正合适的路，常常是越走越顺，而不是一开始就最燃。'
            }
        },
        'self_drain': {
            'reason': {
                '生我': '你不是没有恢复力，只是恢复力总被不必要的消耗抢走。',
                '克我': '你的自耗不是想太多这么简单，而是结构上真的在反向拖你。',
                '泄我': '这是典型心力外泄格：想得多、开得多、收得少。',
                '比和': '你的优点和你的耗损方式常常是同源的，所以才会一体两面。',
                '我克': '你并不是完全控不住自己，只是每次都靠硬压，代价太高。'
            },
            'advice': {
                'hold': '先别想着一口气改性格，先把最明显的耗损入口堵住。',
                'cautious': '少并行、少自证、少给自己加临时战线，你的力就会回来。',
                'move': '若要改，先改节奏，不要先改理想。',
                'outer_block': '你最大的敌人往往不是外部难度，而是自己起势后没把节奏守住。',
                'break_build': '想真正轻一点，得先拆掉那些你明知拖你却一直留着的旧结构。'
            },
            'trend': {
                '快': '只要真减并行，体感会很快告诉你什么叫不那么耗。',
                '中': '先止漏，再稳节奏，中程变化会比较明显。',
                '慢': '这类改变不靠热血，靠持续减耗。'
            }
        }
    }

    scene = overlays.get(scenario_id)
    if not scene:
        return None

    return {
        'label': SCENARIO_LABELS.get(scenario_id, scenario_id),
        'reason': scene.get('reason', {}).get(env),
        'advice': scene.get('advice', {}).get(decide_key(mode, roles, metrics)),
        'trend': scene.get('trend', {}).get(speed)
    }


def role_line(role, item):
    meta = ELEMENT_META[item['element']]
    motion = '动' if item['dynamic'] == '动' else '静'
    strength = '偏强' if item['strength'] == '强' else '偏弱'
    flow = '顺势' if item['flow'] == '顺' else '逆势'
    return '%s见%s，为%s；其性%s，且%s' % (
        role, item['element'], meta['name'], motion + '、' + strength, flow
    )


def score_reading(roles):
    main = roles['主象']
    guest = roles['客象']
    block = roles['阻象']
    change = roles['变象']
    response = roles['应象']

    env = effect_on_subject(main['element'], guest['element'])
    obstacle = effect_on_subject(main['element'], block['element'])
    trend = effect_on_subject(main['element'], change['element'])
    response_to_main = effect_on_subject(main['element'], response['element'])
    response_to_block = effect_on_subject(block['element'], response['element'])

    score = 0
    risk = 0

    if main['element'] in ('木', '火'):
        score += 1
    if main['element'] in ('土', '水'):
        score -= 1
    if main['dynamic'] == '动':
        score += 1
    else:
        score -= 1

    if env == '生我':
        score += 2
    elif env == '比和':
        score += 1
    elif env == '我克':
        score += 0
        risk += 1
    elif env == '泄我':
        score -= 1
        risk += 1
    elif env == '克我':
        score -= 2
        risk += 2

    if obstacle == '克我':
        risk += 2
        score -= 1
    elif obstacle == '泄我':
        risk += 2
        score -= 1
    elif obstacle == '比和':
        risk += 1
    elif obstacle == '我克':
        risk += 1

    if change == '生我':
        score += 1
    elif change == '克我':
        risk += 1
        score -= 1
    elif change == '泄我':
        score -= 1
        risk += 1

    if response_to_main == '生我':
        score += 1
    elif response_to_main == '泄我':
        risk += 1

    if response_to_block == '克我':
        score += 1
        risk = max(0, risk - 1)
    elif response_to_block == '生我':
        risk += 1
    elif response_to_block == '我克':
        risk += 1

    if guest['dynamic'] == '动':
        score += 1
    if block['strength'] == '强':
        risk += 1
    if change['flow'] == '逆':
        risk += 1

    return {
        'env_effect': env,
        'obstacle_effect': obstacle,
        'trend_effect': trend,
        'response_on_main': response_to_main,
        'response_on_obstacle': response_to_block,
        'score': score,
        'risk': risk
    }


def decide_key(mode, roles, metrics):
    guest = roles['客象']
    block = roles['阻象']
    change = roles['变象']
    main = roles['主象']

    if metrics['env_effect'] in ('生我', '比和') and metrics['obstacle_effect'] in ('克我', '泄我', '比和'):
        if guest['flow'] == '顺' and block['strength'] == '强':
            return 'outer_block'

    if change['element'] in ('金', '火') and metrics['response_on_obstacle'] == '克我' and metrics['risk'] >= 2:
        return 'break_build'

    if metrics['score'] >= 3 and metrics['risk'] <= 2 and main['dynamic'] == '动':
        return 'move'

    if metrics['score'] <= 0 or (main['dynamic'] == '静' and metrics['risk'] >= 2):
        return 'hold'

    return 'cautious'


def build_reason(seed, library, roles, metrics, scenario_overlay=None):
    main = roles['主象']
    guest = roles['客象']
    block = roles['阻象']
    change = roles['变象']

    relation_phrases = library['relation_phrases']
    p_env = choose(seed, 'reason-env', relation_phrases.get(metrics['env_effect'], ['']))
    p_block = choose(seed, 'reason-block', relation_phrases.get(metrics['obstacle_effect'], ['']))

    trend_map = {
        '生我': '得扶而续，后势较易转稳',
        '克我': '受压而改，后势多带修正之意',
        '泄我': '外泄而散，后势易有耗力与分神',
        '我克': '需主动用力，后势成于取舍与控制',
        '比和': '同气相叠，后势会放大当前倾向'
    }
    trend_line = trend_map.get(metrics['trend_effect'], '后势仍有变化，不会原样停留')

    guest_line_map = {
        '生我': '外部条件对你有托举之意',
        '克我': '外部压力对你有压制之势',
        '泄我': '这件事会持续牵扯你的心力与投入',
        '我克': '你对外部局面并非无力，但需要自己多出手整合',
        '比和': '外部情势与你当前心气较为同频，会相互放大'
    }
    guest_line = guest_line_map.get(metrics['env_effect'], '外部情势与内在状态互有牵连')

    block_line_map = {
        '生我': '这道阻力未必全坏，其中也带一点逼你成形的压力',
        '克我': '这里是直接卡住你的地方，不宜硬顶',
        '泄我': '这里最容易耗神耗力，久拖则气会散',
        '我克': '你并非不能处理，只是处理它要花成本',
        '比和': '这更像内外同类之阻，容易在同一个毛病上反复打转'
    }
    block_line = block_line_map.get(metrics['obstacle_effect'], '这里确实是当下绕不开的一处卡点')

    lines = []
    lines.append('主象见%s，属%s，%s。' % (main['element'], ELEMENT_META[main['element']]['name'], ELEMENT_META[main['element']]['core']))
    lines.append('客象见%s，%s；从体用关系看，可概括为“%s”。' % (guest['element'], guest_line, p_env))
    lines.append('阻象见%s，说明真正的卡点不只在外面，更在结构、节奏或心力分配上；从主阻关系看，是“%s”，所以%s。' % (block['element'], p_block, block_line))
    lines.append('变象见%s，表示后势不会原样停着不动，整体更像“%s”。' % (change['element'], trend_line))
    if scenario_overlay and scenario_overlay.get('reason'):
        lines.append(scenario_overlay['reason'])
    return ' '.join(lines)


def manifestation_speed(roles):
    moving = 0
    if roles['主象']['dynamic'] == '动':
        moving += 1
    if roles['客象']['dynamic'] == '动':
        moving += 2
    if roles['阻象']['dynamic'] == '动':
        moving += 1
    if roles['变象']['dynamic'] == '动':
        moving += 2
    if roles['应象']['dynamic'] == '动':
        moving += 1

    if moving >= 5:
        return '快'
    if moving <= 1:
        return '慢'
    return '中'


def build_phased_trend(seed, library, roles, metrics, mode, verdict_key, scenario_overlay=None):
    guest = roles['客象']
    block = roles['阻象']
    change = roles['变象']
    speed = manifestation_speed(roles)

    near_templates = {
        '生我': '近势外缘对你有扶托，眼前不算全闭',
        '克我': '近势外压先到，眼前会先感到受制',
        '泄我': '近势最明显的是耗神耗力，事情会牵着你走',
        '我克': '近势要靠你主动出手整合，不能只等局面自己变好',
        '比和': '近势同气相引，眼前会放大你当前的心气与动作'
    }
    mid_templates = {
        '生我': '中势的卡点未必全坏，反而可能逼你把结构补出来',
        '克我': '中势真正要过的是硬障，不调整结构就容易反复撞墙',
        '泄我': '中势最怕久拖，拖久了气会散，问题会从小耗变成大耗',
        '我克': '中势不是不能过，而是每推进一步都要付出成本',
        '比和': '中势容易在同一类问题上反复打转，若不改方法就会原地消耗'
    }
    late_templates = {
        '生我': '后势有转稳之意，越往后越容易看见成形',
        '克我': '后势带修正压力，不改法则后面仍会觉得紧',
        '泄我': '后势怕继续外泄，若不收口，越到后面越疲',
        '我克': '后势成于取舍与控制，敢收、敢断、敢整合，路会出来',
        '比和': '后势会把现在的倾向继续放大，方向对就越走越顺，方向错也会越走越偏'
    }

    near = near_templates.get(metrics['env_effect'], '近势已有显象，但还要继续看外势怎么落')
    middle = mid_templates.get(metrics['obstacle_effect'], '中势的关键在过程承接，而不只在一时判断')
    later = late_templates.get(metrics['trend_effect'], '后势仍会转化，暂不算定局')

    speed_line = {
        '快': '整体动象不弱，显化偏快，近期较容易见到回音。',
        '中': '动静参半，事情会逐步显化，不是一蹴而就。',
        '慢': '整体偏静，端倪未全显，更像在蓄势待成。'
    }[speed]

    if mode == 'relationship' and speed == '快':
        speed_line = '情势已有波动，回应快慢会比你想的更明显，但也更怕用力过头。'
    elif mode == 'career' and speed == '快':
        speed_line = '局面已有动象，近期容易看到反馈，但反馈未必等于已经稳成。'
    elif mode == 'fortune' and speed == '慢':
        speed_line = '这一段更像回气期，不是立刻翻盘期，先调顺比先提速更重要。'

    mode_trend_bank = library.get('trend_phrases', {}).get(mode, library.get('trend_phrases', {}).get('general', {}))
    mode_line = choose(seed, 'trend-mode', mode_trend_bank.get(verdict_key, []))
    detail_line = ''
    if scenario_overlay and scenario_overlay.get('trend'):
        detail_line = scenario_overlay['trend']
    else:
        detail_line = mode_line

    parts = ['近势：%s；中势：%s；后势：%s。' % (near, middle, later)]
    if detail_line:
        parts.append(detail_line.rstrip('。') + '。')
    parts.append(speed_line)
    return ''.join(parts)


def build_advice(seed, library, roles, metrics, mode, verdict_key, scenario_overlay=None):
    response = roles['应象']
    main = roles['主象']
    element_advice = choose(seed, 'advice-el', library['advice_by_element'][response['element']])
    mode_advice_bank = library.get('mode_advice', {}).get(mode, library.get('mode_advice', {}).get('general', {}))
    mode_advice = choose(seed, 'mode-advice', mode_advice_bank.get(verdict_key, ['']))
    extra = []

    primary_advice = ''
    if scenario_overlay and scenario_overlay.get('advice'):
        primary_advice = scenario_overlay['advice']
    else:
        primary_advice = mode_advice

    if primary_advice:
        extra.append(primary_advice)

    risk_bank = library.get('risk_lines', {}).get(mode, library.get('risk_lines', {}).get('general', []))
    if metrics['risk'] >= 3 and risk_bank:
        extra.append(choose(seed, 'risk-line', risk_bank))

    if response['element'] == main['element']:
        extra.append('应象与主象同气，说明最有效的解法往往不是换人格，而是把你本来的长处用对地方。')

    return element_advice + ' ' + ' '.join(extra)


def build_signature(seed, library, verdict_key, mode):
    sig_bank = library['signatures'].get(mode, library['signatures']['general'])
    return choose(seed, 'signature', sig_bank[verdict_key])


def render(mode, question, context='', date='', style='standard', seed=None):
    library = load_library()
    final_seed = seed or build_seed([mode, question, context, date])
    roles = cast(final_seed, mode)
    metrics = score_reading(roles)
    metrics['manifestation_speed'] = manifestation_speed(roles)
    verdict_key = decide_key(mode, roles, metrics)
    scenario_id = detect_scenario(mode, question, context)
    scenario_overlay = build_scenario_overlay(mode, scenario_id, roles, metrics)

    judgments = library['judgments'].get(mode, library['judgments']['general'])
    verdict = choose(final_seed, 'judgment', judgments[verdict_key])
    reason = build_reason(final_seed, library, roles, metrics, scenario_overlay=scenario_overlay)
    trend = build_phased_trend(final_seed, library, roles, metrics, mode, verdict_key, scenario_overlay=scenario_overlay)
    advice = build_advice(final_seed, library, roles, metrics, mode, verdict_key, scenario_overlay=scenario_overlay)
    signature = build_signature(final_seed, library, verdict_key, mode)

    role_lines = [role_line(role, roles[role]) for role in ['主象', '客象', '阻象', '变象', '应象']]
    dynamic_summary = '；'.join(role_lines) + '。'

    data = {
        'mode': mode,
        'mode_label': library['mode_labels'].get(mode, MODE_TO_CHINESE.get(mode, mode)),
        'question': question,
        'seed': final_seed,
        'roles': roles,
        'analysis': metrics,
        'verdict_key': verdict_key,
        'scenario_id': scenario_id,
        'scenario_label': SCENARIO_LABELS.get(scenario_id) if scenario_id else '',
        'reading': {
            '总断': verdict,
            '生克与动静': dynamic_summary,
            '断因': reason,
            '断势': trend,
            '断法': advice,
            '签语': signature
        }
    }

    if style == 'quick':
        text = '\n'.join([
            '总断：' + data['reading']['总断'],
            '断因：' + data['reading']['断因'],
            '断法：' + data['reading']['断法'],
            '签语：' + data['reading']['签语']
        ])
    elif style == 'deep':
        deep_lines = [
            '问题归类：' + data['mode_label'],
            '问题：' + question
        ]
        if data.get('scenario_label'):
            deep_lines.append('命中场景：' + data['scenario_label'])
        deep_lines.extend([
            '主象：' + json.dumps(roles['主象'], ensure_ascii=False),
            '客象：' + json.dumps(roles['客象'], ensure_ascii=False),
            '阻象：' + json.dumps(roles['阻象'], ensure_ascii=False),
            '变象：' + json.dumps(roles['变象'], ensure_ascii=False),
            '应象：' + json.dumps(roles['应象'], ensure_ascii=False),
            '生克与动静：' + data['reading']['生克与动静'],
            '总断：' + data['reading']['总断'],
            '断因：' + data['reading']['断因'],
            '断势：' + data['reading']['断势'],
            '断法：' + data['reading']['断法'],
            '签语：' + data['reading']['签语']
        ])
        text = '\n'.join(deep_lines)
    else:
        text = '\n'.join([
            '总断：' + data['reading']['总断'],
            '断因：' + data['reading']['断因'],
            '断势：' + data['reading']['断势'],
            '断法：' + data['reading']['断法'],
            '签语：' + data['reading']['签语']
        ])

    data['text'] = text
    return data


def main():
    parser = argparse.ArgumentParser(description='Render a structured Chinese-style divination reading.')
    parser.add_argument('--mode', default='general', choices=['general', 'career', 'relationship', 'fortune', 'personality'])
    parser.add_argument('--question', required=True)
    parser.add_argument('--context', default='')
    parser.add_argument('--date', default='')
    parser.add_argument('--style', default='standard', choices=['quick', 'standard', 'deep'])
    parser.add_argument('--seed', default='')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    out = render(
        mode=args.mode,
        question=args.question,
        context=args.context,
        date=args.date,
        style=args.style,
        seed=args.seed or None
    )

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(out['text'])


if __name__ == '__main__':
    main()
