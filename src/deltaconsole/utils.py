# DeltaConsole, A console for DeltaPy applications.
# Copyright (C) 2009-2011  Aidin Gharibnavaz <aidin@aidinhut.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on Nov 2009
@author: Aidin Gharibnavaz

Useful utilities.
'''

import sys
import os
import optparse
import re
from ConfigParser import SafeConfigParser, NoOptionError

SETTINGS_DICT = {'timing': True,
                 'command_prefix': '',
                 'paging': True,
                 'debugging': True}


#Constant values, for different Operating Systems.
if os.name == 'nt':
    __CONFIG_FILE = os.path.join(
                        os.path.abspath(
                            os.path.dirname(
                                sys.modules[__name__].__file__)),
                        'services.conf')
else:
    __CONFIG_FILE = '/etc/deltaconsole/services.conf'

#If config file dosen't exists, create it.
#XXX: What if user dose not have permission?
if not os.path.exists(__CONFIG_FILE):
    try:
        os.mkdir('/etc/deltaconsole/')
    except OSError:
        #If the directory already exist.
        pass
    try:
        cfg = open(__CONFIG_FILE, 'w')
        cfg.write('[example]\n')
        cfg.write('host: 127.0.0.1\n')
        cfg.write('port: 9083\n')
        cfg.write('protocol: xmlrpc\n')
        cfg.close()
    except IOError:
        pass

if os.name == 'nt':
    #As far as I know, only Windows don't understand ANSI escape sequences.
    class ANSICOLORS:
        FRED        = '%s'
        BRED        = '%s'
        FGREEN      = '%s'
        BGREEN      = '%s'
        FYELLOW     = '%s'
        BYELLOW     = '%s'
        FBLUE       = '%s'
        BBLUE       = '%s'
        FPURPLE     = '%s'
        BPURPLE     = '%s'
        FCYAN       = '%s'
        BCYAN       = '%s'
        FGREY       = '%s'
        BWHITE      = '%s'
        BNORMAL     = '%s'
else:
    class ANSICOLORS:
        """This class holds ANSI escape sequenses.
        Names starts with F are normal colors,
        and the ones starts with B are bright colors.
        
        Usage: ANSICOLORS.FRED % 'this will appears in red'
        """
        FRED        = '[00;31m%s[00m'
        BRED        = '[01;31m%s[00m'
        FGREEN      = '[00;32m%s[00m'
        BGREEN      = '[01;32m%s[00m'
        FYELLOW     = '[00;33m%s[00m'
        BYELLOW     = '[01;33m%s[00m'
        FBLUE       = '[00;34m%s[00m'
        BBLUE       = '[01;34m%s[00m'
        FPURPLE     = '[00;35m%s[00m'
        BPURPLE     = '[01;35m%s[00m'
        FCYAN       = '[00;36m%s[00m'
        BCYAN       = '[01;36m%s[00m'
        FGREY       = '[00;37m%s[00m'
        BWHITE      = '[01;37m%s[00m'
        BNORMAL     = '[01m%s[00m'


def getch():
    """Gets a single character from standard input.
    Does not echo to the screen.
    """
    if os.name == 'nt':
        return _getch_windows()
    else:
        return _getch_unix()


def _getch_unix():
    """Get a single character from standard input,
    on Unix systems.
    """
    import tty, termios
    
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def _getch_windows():
    """Get a single character from standard input,
    on Windows.
    """
    import msvcrt
    return msvcrt.getch()


class CommandParsingError(Exception):
    """Should be raise whenever any errors occure when
    parsing a command string
    """
    pass


def print_welcome(version):
    """Print the welcome message.
    
    @param version: Version of the program.
    """
    print ANSICOLORS.FYELLOW % "    ___     _ _             ___                       _      "
    print ANSICOLORS.FYELLOW % "   /   \\___| | |_  __ _    / __\\ ___  _ __  ___  ___ | | ___"
    print ANSICOLORS.FYELLOW % "  / /\\ / _ \\ | __|/ _` |  / /   / _ \\| '_ \\/ __|/ _ \\| |/ _ \\"
    print ANSICOLORS.FYELLOW % " / /_//  __/ | |_| (_| | / /___| (_) | | | \\__ \\ (_) | |  __/"
    print ANSICOLORS.FYELLOW % "/___,' \\___|_|\\__|\\__,_| \____/ \\___/|_| |_|___/\\___/|_|\\___|"
    print ANSICOLORS.FYELLOW % "    version : %s" % version
    
    print 
    print ANSICOLORS.BNORMAL % " Type 'help' for more information"
    print 


def _ioctl_GWINSZ(fd):
    import fcntl
    import termios
    import struct
    try:
        cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
                           '1234'))
    except:
        return None
    
    return cr


def terminal_size():
    """Returns current terminal size as a tuple, in
    (width, height) format.
    """
    if os.name != 'posix':
        #Only Unix systems support these modules.
        return (80, 25)
    
    # Try open file descriptors.
    cr = _ioctl_GWINSZ(0) or _ioctl_GWINSZ(1) or _ioctl_GWINSZ(2)
    if not cr:
        # ...then ctty
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = _ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        # defaults
        cr = (25, 80)
    
    # reverse rows, cols
    return int(cr[1]), int(cr[0])


def get_configurations(arguments):
    """Parse command line arguments, read the configurations,
    and return an object which represents the configurations.
    If this function find '-l' or '--load' among the arguments,
    it try to read the config file. And if the config, or the
    specified section not found, it terminates the application.
    
    @param arguments: Command line arguments.
    
    @return: An object which have an attribute for each option.
    """
    global __CONFIG_FILE
    
    options = commandline_arguments_parser(arguments)
    
    if options.load is None:
        return options
    
    section_name = options.load
    #Loading options from config file.
    config_parser = SafeConfigParser()
    #Check whether user select another config file.
    if options.services_config is not None:
        __CONFIG_FILE = options.services_config
    
    if len(config_parser.read(__CONFIG_FILE)) == 0:
        print "Couldn't find services.conf file."
        sys.exit(5)
    if not config_parser.has_section(section_name):
        print "Couldn't find section [{0}] in services.conf file".format(section_name)        
        sys.exit(5)
    
    #TODO: Find a better way for doing this.
    #options.__dict__ = {}
    try:
        options.host = config_parser.get(section_name, 'host')
        options.port = config_parser.get(section_name, 'port')
        options.protocol = config_parser.get(section_name, 'protocol')
    except NoOptionError:
        print "The specified config section dosen't have the required options."
        sys.exit(6)
    #It's optional.
    if config_parser.has_option(section_name, 'service_name'):
        options.service_name = config_parser.get(section_name, 'service_name')
    else:
        options.service_name = 'xmlrpc'
    
    return options

def commandline_arguments_parser(arguments):
    """Parse given command line arguments.
    
    @param arguments: Command line arguments, as a list. (Or pass
                      sys.argv directly to this functions)
    @return: An object which have an attribute for each option
             in the arguments.
    """
    parser = optparse.OptionParser()
    
    parser.add_option('-l', '--load', dest='load', metavar='SECTION',
                      help='Specify a section in the services.conf file, to '
                      'load the configurations from.', default=None)
    parser.add_option('-n', '--host', dest='host',
                      help='Specify a host [default: %default]',
                      default='127.0.0.1')
    parser.add_option('-p', '--port', dest='port',
                      help='Specify a port to connect to [default: %default]',
                      default='7669')
    parser.add_option('-t', '--protocol', dest='protocol',
                      help='Protocol to use for connection. [default: %default]',
                      default='xmlrpc')
    parser.add_option('-s', '--service-name', dest='service_name',
                      help='Service name to use [Example: -s xmlrpc]',
                      default='xmlrpc')
    parser.add_option('-u', '--user', dest='user',
                      help='Specify a user name to login with',
                      default=None)
    parser.add_option('-c', '--services-config', dest='services_config',
                      metavar='FILE',
                      help='Specify another file as services.conf',
                      default=None)
    
    config_file_group = optparse.OptionGroup(parser, 'Config files',
                            "Configuration files can be found in the "
                            "/etc/deltaconsole/ directory. On windows, they can"
                            " be found on the installed directory. "
                            "You can set information of services in "
                            "`services.conf' and loads them using `-l' "
                            "parameter. "
                            "`alias.conf' can be use to define aliases for "
                            "server-side commands. Read it to find out how.")
    parser.add_option_group(config_file_group)
    parsed_arguments = parser.parse_args(arguments)
    
    #Returning options, and ignoring args.
    return parsed_arguments[0]

def is_local_command(command_string):
    """Check whether the given command is a local command
    or not.
    
    @return: Boolean
    """
    splited_command = command_string.partition('(')
    
    if (splited_command[0].strip().find(' ') == -1 and
        splited_command[2] != ''):
        return False
    else:
        return True
    
def server_command_parser(command_string):
    """Gets a string, parse it, and return it
    as python variables.
    
    @param command_string: String to parse.
    
    @return: A tuple contains a string as the command, and
             a tuple as its arguments.
    """
    if not command_string.rstrip(): #Empty line (user just hit enter)
        return None, None
    
    user_command, ignore_me, user_arguments = command_string.partition('(')
    
    user_command = SETTINGS_DICT['command_prefix'] + user_command
    
    user_arguments = user_arguments.rstrip()
    #Removing last ')'
    if user_arguments.endswith(')'):
        user_arguments = user_arguments[:len(user_arguments)-1]
    else:
        raise CommandParsingError('Missing close paranthese')

    user_arguments, context_args = __get_context_from_arguments(user_arguments)
    
    return user_command.strip(), user_arguments, context_args

def __get_context_from_arguments(arguments):
    """
    Extracts context from arguments.

    @param arguments: arguments

    @return: context
    @rtype: string
    """

    context = re.search(", ?context ?= ?\{.*\}", arguments)
    if not context:
        return arguments, '{}'

    context = context.group(0)
    arguments = arguments.replace(context, '').strip()

    context_args = re.search('{.*}', context)
    if not context_args:
        return arguments, '{}'

    context_args = context_args.group(0)

    return arguments, context_args.strip()

def local_command_parser(command_string):
    """Get a string, parse it, and return Python variables.
    
    @param command_string: String to parse.
    
    @return: A tuple contains a string as the command, and
             a tuple as its arguments.
    """
    if not command_string.rstrip(): #Empty line (user just hit enter)
        return None, None
    
    user_input_list = command_string.split(' ')
    for i in range(user_input_list.count('')):
        user_input_list.remove('')
    
    user_command = user_input_list[0]
    
    user_arguments = tuple(user_input_list[1:])
    return user_command.strip(), user_arguments


def print_elapsed_time(start_time, end_time):
    """Calculate and print the elapsed time.
    Usage: Call this function before an event with reset=True,
           and call it after the event with reset=False.
    """
    if not SETTINGS_DICT['timing']:
        #Timing is disabled by the user.
        return
    
    elapsed_time = end_time - start_time
    if elapsed_time == 0:
        #Maybe the operating system can't meature this small time.
        elapsed_time = 0.0001
    
    print ANSICOLORS.FCYAN % \
        'Command takes [{0}] seconds to execute.'.format(elapsed_time)


def format_xmlrpc_fault_error(error_message):
    """Get an xmlrpc fault message as a string, and format it as
    a human-readble message.
    
    @param error_message: XMLRPC fault message as a string.
    
    @return: Formated string.
    """
    start_of_message = error_message.index('>:')
    return error_message[start_of_message+2:]

