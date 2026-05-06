# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import Popen, PIPE
from lunarcalendar import zh_festivals, zh_solarterms

'''
`with Popen() can only run on Python 3.4+`, so excluded from pytest.
'''


def _assert_output_line_count(args, count):
    with Popen(['python', 'lunarcalendar/command.py'] + args, stdout=PIPE) as p:
        assert len([li for li in p.stdout.readlines() if li.strip()]) == count


def test_command():
    _assert_output_line_count(['重阳节'], 1)
    _assert_output_line_count(['重阳节', '2010'], 1)
    _assert_output_line_count(['重阳'], 1)
    _assert_output_line_count(['重阳', '2011'], 1)

    _assert_output_line_count(['登高节'], 1)
    _assert_output_line_count(['登高节', '2012'], 1)
    _assert_output_line_count(['登高節'], 1)
    _assert_output_line_count(['登高節', '2013'], 1)

    _assert_output_line_count(['没有节'], 0)
    _assert_output_line_count(['没有节', '2014'], 0)

    _assert_output_line_count(['all'], len(zh_festivals) + len(zh_solarterms))
    _assert_output_line_count(['all', '2015'], len(zh_festivals) + len(zh_solarterms))

    _assert_output_line_count(['festival'], len(zh_festivals))
    _assert_output_line_count(['festivals', '2016'], len(zh_festivals))

    _assert_output_line_count(['solarterm'], len(zh_solarterms))
    _assert_output_line_count(['solarterms', '2017'], len(zh_solarterms))

test_command()
