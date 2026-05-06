# -*- coding: utf-8 -*-
import sys
from lunarcalendar.solarterm import zh_solarterms


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("lack of args: year")
        sys.exit(1)
    year = int(sys.argv[1])
    for fest in zh_solarterms:
        print(fest.get_lang('zh'), fest(year))
