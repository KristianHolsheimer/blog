#!/usr/bin/env python3
import os
import sys

from argparse import ArgumentParser
from configparser import ConfigParser

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from blog.utils import env_var  # noqa
from blog.settings import BASE_DIR, LOG_DIR  # noqa


"""
This is a bit silly, really. I should really just use the dynamic variables
that wsgi config files already offers.

"""


PROJECT = 'blog'


def create_uwsgi_config_file(output_filename):
    conf = ConfigParser()

    settings = (
        ('uid', 'www-data'),
        ('gid', 'www-data'),
        ('home', os.path.join(env_var('WORKON_HOME'), PROJECT)),
        ('chdir', BASE_DIR),
        ('module', '{}.wsgi'.format(PROJECT)),
        ('master', 'true'),
        ('processes', '2'),
        ('socket', '/run/uwsgi/{}.sock'.format(PROJECT)),
        ('chmod-socket', '664'),
        ('vacuum', 'true'),
        ('enable-threads', 'true'),
        ('logto', os.path.join(LOG_DIR, 'uwsgi.log')),
    )
    conf.add_section('uwsgi')
    for k, v in settings:
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
