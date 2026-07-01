#!/usr/bin/env python3
import argparse
import hashlib


def normalize(text):
    return " ".join((text or "").strip().split())


def build_seed(parts):
    base = "|".join(normalize(p) for p in parts if p is not None)
    digest = hashlib.sha256(base.encode('utf-8')).hexdigest()
    return digest[:16]


def main():
    parser = argparse.ArgumentParser(description='Generate a stable seed for divination readings.')
    parser.add_argument('--mode', required=True)
    parser.add_argument('--question', required=True)
    parser.add_argument('--context', default='')
    parser.add_argument('--date', default='')
    args = parser.parse_args()
    print(build_seed([args.mode, args.question, args.context, args.date]))


if __name__ == '__main__':
    main()
