import random
import subprocess
import json

from .navigation import navigation, reproduction
from ..model import get_random_video, get_random_page

VERSION_FILE = '/app/version'
VERSION = None
EXPERIMENT_TYPES = ['navigation', 'reproduction']

def call_program(program):
    result = subprocess.run(program, capture_output=True)
    return result.stdout, result.stderr

def call_ndt7(server = None):
    command = ['ndt7-client', '-no-verify', '-scheme', 'wss', '-format', 'json']
    if server:
        command += ['-server', server]
    result, _ = call_program(command)
    return parser_ndt_output(result)

def parser_ndt_output(output):
    result = str(output)
    blocks = result[2:-3].split('\\n')
    result = '[{}]'.format(','.join(blocks))
    return json.loads(result)

def call_traceroute(server, ip_v6 = False):
    command = ['traceroute', '-6' if ip_v6 else '-4', server]
    result, _ = call_program(command)
    return result

def get_runtime_version():
    global VERSION
    if VERSION:
        return VERSION
    with open(VERSION_FILE, 'r', encoding='utf-8') as f:
        VERSION = f.read()
    return VERSION

def get_experiment_type_at_random():
    return random.choices(EXPERIMENT_TYPES)[0]

def get_navigation_url():
    return get_random_page(engine)

def get_reproduction_url():
    return get_random_video(engine)

def get_url_for_experiment_type(experiment_type):
    return dict.fromkeys(EXPERIMENT_TYPES, [
        get_navigation_url,
        get_reproduction_url,
    ])[experiment_type]()

def navigation_experiment(url, use_adblock, resolution_type):
    return navigation(url, use_adblock, resolution_type)

def reproduction_experiment(url, use_adblock, resolution_type):
    return reproduction(url, use_adblock, resolution_type)

def get_browser_experiment_func(experiment_type):
    return dict.fromkeys(EXPERIMENT_TYPES, [
        navigation_experiment,
        reproduction_experiment,
    ])[experiment_type]
