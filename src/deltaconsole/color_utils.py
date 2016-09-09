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
Created on Aug, 2011
@author: Aidin Gharibnavaz

This module contains some functions to handle
terminal colors.
'''

import re

UNIX_COLORS = {'default': '\x1b[00m',
               'red': '\x1b[00;31m',
               'bright_red': '\x1b[01;31m',
               'green': '\x1b[00;32m',
               'bright_green': '\x1b[01;32m',
               'yellow': '\x1b[00;33m',
               'bright_yellow': '\x1b[01;33m',
               'blue': '\x1b[00;34m',
               'bright_blue': '\x1b[01;34m',
               'purple': '\x1b[00;35m',
               'bright_purple': '\x1b[01;35m',
               'cyan': '\x1b[00;36m',
               'bright_cyan': '\x1b[01;36m',
               'white': '\x1b[00;37m',
               'bright_white': '\x1b[01;37m',
               'bright_normal': '\x1b[01m'}

WINDOWS_COLORS = {'default': 7,
                  'red': 4,
                  'bright_red': 12,
                  'green': 2,
                  'bright_green': 10,
                  'yellow': 6,
                  'bright_yellow': 14,
                  'blue': 1,
                  'bright_blue': 9,
                  'purple': 5,
                  'bright_purple': 13,
                  'cyan': 3,
                  'bright_cyan': 11,
                  'white': 8,
                  'bright_white': 15,
                  'bright_normal': 15}

COLORS_PATTERN = re.compile('@(?P<name>%s)@' % '|'.join(UNIX_COLORS.keys()))
