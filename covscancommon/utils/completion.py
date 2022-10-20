#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import datetime
import os

from six.moves import cPickle as pickle
from six.moves import xmlrpc_client

from covscancommon.utils.conf import get_conf


def get_can_path():
    """
    Return path to can with pickles
    """
    return os.path.join(get_conf().get_conf_dir(), 'bash_compl.pickle')


def get_configs_from_hub():
    """
    Return enabled mockconfigs from hub
    """
    # FIXME: load this URL from /etc/covscan.conf instead
    rpc_url = "https://cov01.lab.eng.brq2.redhat.com/covscanhub/xmlrpc/client/"
    client = xmlrpc_client.ServerProxy(rpc_url, allow_none=True)
    return [x for x in client.mock_config.all() if x['enabled']]


def write_configs():
    """
    write configs which were retieved from hub to pickle can
    """
    can_path = get_can_path()
    with open(can_path, 'w') as fd:
        configs = get_configs_from_hub()
        pickle.dump(configs, fd)
    return configs


def list_enabled_mock_configs():
    """
    this function should be called from outside world
    """
    try:
        with open(get_can_path(), 'r') as can:
            can_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(get_can_path()))

            if can_time + datetime.timedelta(minutes=5) > datetime.datetime.now():
                enabled_configs = pickle.load(can)
            else:
                enabled_configs = write_configs()
    except IOError:
        enabled_configs = write_configs()
    for emc in enabled_configs:
        print(emc['name'])


def main():
    list_enabled_mock_configs()


if __name__ == "__main__":
    main()
