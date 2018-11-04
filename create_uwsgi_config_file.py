#!/usr/bin/env python3
import os
import sys

from argparse import ArgumentParser
from configparser import ConfigParser

from blog.utils import env_var
from blog.settings import BASE_DIR


PROJECT = 'blog'


def create_uwsgi_config_file(output_filename):
    conf = ConfigParser()

    settings = {
        'home': os.path.join(env_var('WORKON_HOME'), PROJECT),
        'chdir': os.path.join(BASE_DIR, PROJECT),
        'module': '{}.wsgi'.format(PROJECT),
        'master': 'true',
        'processes': '2',
        'socket': '/tmp/{}.sock'.format(PROJECT),
        'chmod-socket': '664',
        'vacuum': 'true',
    }
    conf.add_section('uwsgi')
    for k, v in settings.items():
        conf.set('uwsgi', k, v)

    if output_filename is None:
        conf.write(sys.stdout)
    else:
        with open(output_filename, 'w') as f:
            conf.write(f)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--output_filename', '-o', action='store', help="if unspecified, conf is written to STDOUT")
    args = parser.parse_args()
    create_uwsgi_config_file(args.output_filename)
