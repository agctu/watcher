import sys
import argparse
from . import lib

parser = argparse.ArgumentParser(
    'watcher', 'python -m watcher',
    'watch for files and execute commands'
)

parser.add_argument('dir',type=str,nargs='?',help='under which directory files are watched for changes, default is \'.\'')
parser.add_argument('--regex','-r',action='append',help='patterns specifying which files to include. Defaults to [\'.*\']')
parser.add_argument('--REGEX','-R',action='append',help='patterns specifying which files to exclude. Defaults to []')

parser.add_argument('--after-action','-a', type=str,help='command executed after all other commands being executed')
parser.add_argument('--daction','-d',type=str,help='command executed on file deleted')
parser.add_argument('--maction','-m',type=str,help='command executed on file modified')
parser.add_argument('--caction','-c',type=str,help='command executed on file created')
parser.add_argument('--before-action','-b',type=str,help='command executed before all other commands being executed')
parser.add_argument('--period','-p',type=float,help='the time between two adjacent scanning')

parser.add_argument('--from-empty','-e',action='store_true',help='start the watcher loop as if no file exists before')

parser.add_argument('--use_hash','-H',action='store_true',help='use hash to detect changes instead of ctime')

parser.add_argument('--verbose','-v',action='store_true',help='show debug messages')

real_args=sys.argv[1:]
parsed = parser.parse_args(real_args)

watcher=lib.Watcher(lib.WatcherOption(parsed.__dict__))
watcher.startLoop()
