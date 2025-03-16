import sys
import argparse
from . import lib

parser = argparse.ArgumentParser(
    'watcher', 'python -m watcher',
    'watch for files and execute commands'
)

parser.add_argument('dir',type=str,nargs='?')
parser.add_argument('--regex','-r',action='append')
parser.add_argument('--REGEX','-R',action='append')

parser.add_argument('--after-action','-a', type=str)
parser.add_argument('--daction','-d',type=str)
parser.add_argument('--maction','-m',type=str)
parser.add_argument('--caction','-c',type=str)
parser.add_argument('--before-action','-b',type=str)
parser.add_argument('--period','-p',type=float)

parser.add_argument('--use_hash','-H',action='store_true')

parser.add_argument('--verbose','-v',action='store_true')

real_args=sys.argv[1:]
parsed = parser.parse_args(real_args)

watcher=lib.Watcher(lib.WatcherOption(parsed.__dict__))
watcher.startLoop()
