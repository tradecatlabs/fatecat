#!/usr/bin/env python3
import argparse
import hashlib
import json

ELEMENTS = ['木', '火', '土', '金', '水']
DYNAMICS = ['动', '静']
STRENGTHS = ['强', '弱']
FLOW = ['顺', '逆']
ROLES = ['主象', '客象', '阻象', '变象', '应象']

MODE_BIASES = {
    'career': {
        '主象': ['木', '土', '金'],
        '阻象': ['土', '金', '水'],
        '应象': ['金', '水', '木']
    },
    'relationship': {
        '主象': ['水', '火', '木'],
        '阻象': ['金', '土', '水'],
        '应象': ['水', '木', '金']
    },
    'fortune': {
        '主象': ['土', '水', '木'],
        '阻象': ['土', '金', '火'],
        '应象': ['水', '土', '木']
    },
    'personality': {
        '主象': ['木', '金', '水'],
        '阻象': ['金', '火', '土'],
        '应象': ['水', '木', '土']
    }
}


def token_to_int(seed, salt):
    h = hashlib.sha256((seed + '|' + salt).encode('utf-8')).hexdigest()
    return int(h[:12], 16)


def pick(seq, n):
    return seq[n % len(seq)]


def biased_element(seed, role, mode):
    n = token_to_int(seed, role + '|element|' + mode)
    mode_bias = MODE_BIASES.get(mode, {}).get(role)
    if mode_bias and (n % 10) < 7:
        return pick(mode_bias, n)
    return pick(ELEMENTS, n)


def cast(seed, mode='general'):
    result = {}
    for role in ROLES:
        n = token_to_int(seed, role)
        element = biased_element(seed, role, mode)
        result[role] = {
            'element': element,
            'dynamic': pick(DYNAMICS, n // 7),
            'strength': pick(STRENGTHS, n // 13),
            'flow': pick(FLOW, n // 17)
        }
    return result


def summarize_relations(data):
    elements = {role: data[role]['element'] for role in ROLES}
    return {
        '主客': elements['主象'] + '-' + elements['客象'],
        '主阻': elements['主象'] + '-' + elements['阻象'],
        '主变': elements['主象'] + '-' + elements['变象'],
        '阻应': elements['阻象'] + '-' + elements['应象']
    }


def main():
    parser = argparse.ArgumentParser(description='Cast symbolic roles for a structured Chinese-style reading.')
    parser.add_argument('--seed', required=True)
    parser.add_argument('--mode', default='general', choices=['general', 'career', 'relationship', 'fortune', 'personality'])
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    data = cast(args.seed, args.mode)
    if args.json:
        out = {
            'mode': args.mode,
            'roles': data,
            'relations': summarize_relations(data)
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print('mode:', args.mode)
        for role in ROLES:
            item = data[role]
            print('%s: %s / %s / %s / %s' % (
                role, item['element'], item['dynamic'], item['strength'], item['flow']
            ))
        rel = summarize_relations(data)
        print('relations:', ', '.join('%s=%s' % (k, v) for k, v in rel.items()))


if __name__ == '__main__':
    main()
