#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import re
import sys
from optparse import OptionParser
from pathlib import Path

from django.core.exceptions import ObjectDoesNotExist

from covscanhub.scan.models import MockConfig

PROJECT_DIR = Path(__file__).parents[2]

if PROJECT_DIR not in sys.path:
    print('%s is not on sys.path' % PROJECT_DIR)
    sys.path.append(PROJECT_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'covscanhub.settings'


def sync(enabled_state):
    profile_files = os.listdir('/etc/mock')

    all_configs = MockConfig.objects.all()

    for f in profile_files:
        if re.match(r'[\w\-\.]+-[\w\-\.]+-[\w\-\.]+\.cfg', f):
            try:
                m = MockConfig.objects.get(name=f[:-4])
                all_configs.remove(m)
            except ObjectDoesNotExist:
                m = MockConfig()
                m.name = f[:-4]
                m.enabled = enabled_state
                m.save()
    for m in all_configs:
        m.enabled = False
        m.save()


def set_options():
    parser = OptionParser()
    parser.add_option("-e", "--enabled",
                      help="set configs to enabled? default: false",
                      action="store_true", dest="enabled", default=False)

    (options, args) = parser.parse_args()

    return parser, options, args


def main():
    parser, options, args = set_options()
    sync(options.enabled)


if __name__ == '__main__':
    main()
