import os
import secrets
import subprocess

from pythonjsonlogger.jsonlogger import JsonFormatter as BaseJsonFormatter


COMMIT_HASH = None


class BooleanParseError(Exception):
    pass


def get_or_create_secret_key(base_dir):
    filepath = os.path.join(base_dir, 'secret_key.txt')
    try:
        with open(filepath) as f:
            secret_key = f.read().strip()
    except FileNotFoundError as e:
        secret_key = secrets.token_urlsafe(50)
        with open(filepath, 'w') as f:
            f.write(secret_key)
    return secret_key


def parse_bool(string):
    s = str(string).lower()
    if s in ('true', 't', 'yes', 'y', '1'):
        return True
    elif s in ('false', 'f', 'no', 'n', '0', 'none', ''):
        return False
    else:
        raise BooleanParseError("Cannot parse boolean from: {}".format(string))


def env_var(varname, raise_on_missing=True, default=None):
    try:
        return os.environ[varname]
    except KeyError:
        if raise_on_missing:
            raise EnvironmentError("Missing environ variable: {}".format(varname))
        return default


def git_rev_parse(rev='HEAD', short=False):
    global COMMIT_HASH
    if COMMIT_HASH is None:
        cmd = ['git', 'rev-parse', rev]
        if short:
            cmd.insert(-1, '--short')
        COMMIT_HASH = subprocess.check_output(cmd).strip().decode('utf-8')
    return COMMIT_HASH


class JsonFormatter(BaseJsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(JsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['commit'] = git_rev_parse()
