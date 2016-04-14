"""
MapARgumentParser extends the standard ArgumentParser for map.py.
It defines all arguments for map.py.

Information about map is available at https://github.com/THLO/map.
"""

import argparse,os
from argparse import ArgumentParser
import MapConstants

class MapArgumentParser(ArgumentParser):

    def __init__(self):
        super(MapArgumentParser,self).__init__(description="The given command is applied to all \
files/directories under the provided path.\n\
The command must be set in quotation marks.\n\n\
placeholders:\n  \
"+MapConstants.placeholder+" is used as the placeholder for the current matching file including the full path.\n  \
"+MapConstants.placeholderFileName+" is used as the placeholder for the current file's name without its path or extension.\n  \
"+MapConstants.placeholderPath+" is used as the placeholder for the current file's path.\n  \
"+MapConstants.placeholderExtension+" is used as the placeholder for the current file's extension including the dot.\n  \
"+MapConstants.placeholderCounterHelpVersion+" is used to refer to an internal counter,\
incremented after each command.\n\n\
examples:\n  map \"mv _ &-%#\" /path/to/folder: A counter is added to all file names.\n" \
"  map -r \"mv _ &/..\" /path/to/folder: Each file is moved to its respective parent directory.",formatter_class=argparse.RawDescriptionHelpFormatter)
        # Get the version information:
        info = loadVersionInfo()
	version = info['__version__']
        versionText = info['__version_text__']
        # Add all arguments:
        self.add_argument("-c", "--count-from", type=checkNegative,default=0,help="set the internal counter to the provided start value.")
        self.add_argument("-d", "--directories", action="store_true",help="apply the command to directories instead of files.")
        self.add_argument("-i", "--ignore-errors", action="store_true", help="continue to execute commands even when a command has failed.")
        self.add_argument("-l", "--list", action="store_true", help="list all commands without executing them.")
        self.add_argument("-n", "--number-length", type=checkNegative,default=0,help="format the counter that is used with \
"+MapConstants.placeholderCounterHelpVersion+". The argument is the length in terms of number of digits of the counter (with leading zeros).")
        self.add_argument("-r", "--recursive", action="store_true",help="search for files recursively under the provided path.")
        self.add_argument("-v", "--verbose", action="store_true", help="display detailed information about the process.")
        self.add_argument("-V",'--version', action='version', version='map '+version+'\n'+versionText,help="display information about the installed version.")
        self.add_argument("-x", "--extensions", help="apply the command to all files with any of the listed extensions. The extensions must be provided in a comma-separated list. By default, the command is \
applied to all files under the provided path.")
        self.add_argument("command", help="The command that is applied to all matching files/directories.")
        self.add_argument("path",nargs='*', help="The (top-level) path where matching files are sought.")

    def format_help(self):
        """ The help statement is slightly changed in that the '.py' extension is dropped. """
	return super(MapArgumentParser,self).format_help().replace('.py','').replace('%%','%').replace('COUNT_FROM','VALUE').replace('NUMBER_LENGTH','LENGTH').replace('EXTENSIONS','EXT')

def checkNegative(value):
    ivalue = int(value)
    if ivalue < 0:
         raise argparse.ArgumentTypeError("%s is invalid because negative integers are not allowed." % value)
    return ivalue

def loadVersionInfo():
    directory = os.path.dirname(__file__) +"/"
    ns = {}
    with open(directory+'version.py') as f: exec(f.read(),ns)
    #print ns__version__
    #print __version_text__
    return ns    

def loadVersion():
    directory = os.path.dirname(__file__) +"/"
    with open(directory+'version.py') as f: exec(f.read())
    print __version__

def getVersionText():
    directory = os.path.dirname(__file__) +"/"
    with open(directory+'version.py') as f: exec(f.read())
    return __version__
