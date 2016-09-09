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
Created on Dec 13, 2009
@author: Aidin Gharibnavaz

This module contains fuctions for handling the output of
the console. (Printing, formatting, highlighting ...)
'''

import utils
from utils import ANSICOLORS

def print_horizonal_line():
    """Prints an horizonal line on the terminal.
    """
    terminal_width, terminal_height = utils.terminal_size()
    print ANSICOLORS.FGREY % ('-' * (terminal_width - 3))


def output_printer(object_to_print):
    """Format the given object as a string, and print it
    page by page to the output.
    
    @param object_to_print: Can be of any built-in types.
    """
    formatted_text = output_formatter(object_to_print)
    print formatted_text
    #Following code use pydoc.pager for paging the result, but it have problems
    #with ANSI color sequenses.
#    if not settings_dict['paging']:
#        print formatted_text
#        return
#    
#    out_put = StringIO()
#    print >> out_put, formatted_text    
#    out_put.seek(0)
#    pager(out_put.read())

    #Following code prints the output page by page, but the result is not very
    #nice.
#    text_lines = formated_text.splitlines()
#    
#    terminal_width, terminal_height = terminal_size()
#    
#    line_counter = 0
#    for line in text_lines:
#        if line_counter < terminal_height - 2:
#            print line
#        else:
#            print
#            #FIXME: Wait for any key press, instead of enter.
#            choise = raw_input(ANSICOLORS.BNORMAL % 
#                               "<-- press enter to continue, 'q' to quit -->")
#            print
#            if choise == 'q':
#                return
#            line_counter = 0
#        
#        line_counter += 1
    
            
def output_formatter(object_to_format):
    """Format the given object to a clean and nice string. 
    
    @param object_to_format: Can be a list, dictionary, or string.
    
    @return: A nice string, suitable to show to the user.
    """
    if isinstance(object_to_format, tuple):
        object_to_format = list(object_to_format)
    
    if object_to_format == None:
        return 'Empty Result'
    if isinstance(object_to_format, basestring):
        #Don't format strings.
        return ANSICOLORS.BNORMAL % object_to_format
    if isinstance(object_to_format, list):
        return _format_list(object_to_format)
    if isinstance(object_to_format, dict):
        return _format_dictionary(object_to_format)
    
    try:
        result = str(object_to_format)
    except Exception:
        result = 'Unknown result type'
    
    return result

def _format_dictionary(dict_to_format):
    """Gets a dictionary, and returns a formatted table."""
    if len(dict_to_format) == 0:
        return 'Empty result'

    for item in dict_to_format.values():
        if isinstance(item, (list, dict, tuple)):
            #Some of the values of the dictionary are list or dict,
            #So we can't show this as a simple table.
            return _format_object_as_tree(dict_to_format)
    
    result = ''
    
    terminal_width, terminal_height = utils.terminal_size()
    columns_width = (terminal_width - 9) / 2
    keys_column_width = columns_width
    values_column_width = columns_width
    
    if columns_width > 26: #Max width for keys column
        keys_column_width = 26
        values_column_width = terminal_width - 9 - keys_column_width
    
    table_border = ANSICOLORS.FBLUE % ('   +' + \
                                      '='*(keys_column_width) + '+' + \
                                      '='*(values_column_width) + '+' + '\n')
    if not keys_column_width%2 == 0:
        #Ensure that the widths are even.
        keys_column_width = keys_column_width -1
        values_column_width = values_column_width + 1
    
    table_header = table_border
    table_header += ANSICOLORS.FBLUE % ('   |' + (' '*(keys_column_width/2-2)) + \
                                        'KEYS' + \
                                        (' '*(keys_column_width/2-2)) +\
                                        '|' +  (' '*(values_column_width/2-3)) + \
                                        'VALUES' + \
                                        (' '*(values_column_width/2-3)) +\
                                        '|' + '\n' )
    table_header += table_border    
    result += table_header
    
    line = ANSICOLORS.FBLUE % '   | '
    for key in dict_to_format:
        value = dict_to_format[key]
        #Ensure that our keys and values are strings.
        key = str(key)
        if not isinstance(value, basestring):
            value = str(value)
        
        #Printing in KEYS column.
        #-2 is for those extra spaces between and after text in the column.
        if len(key) > keys_column_width - 2:
            key = key[:keys_column_width - 5] + '...'
        line += ('%-{0}s'.format(keys_column_width-2) % key) + \
                ANSICOLORS.FBLUE % ' | '
        
        #Printing in VALUES column.
        if len(value) > values_column_width - 2:
            value = value[:values_column_width - 5] + '...'
        line += ('%-{0}s'.format(values_column_width-2) % value) + \
                ANSICOLORS.FBLUE % ' |'
        
        result += line + '\n'
        line = ANSICOLORS.FBLUE % '   | '

    result += table_border
    return result


def _format_list(list_to_format):
    """Formats a list, regardless of how complex it is.
    
    @param list_to_format: List to format
    
    @return: Formated list as a string.
    """
    if len(list_to_format) == 0:
        return 'Empty result'
    
    if isinstance(list_to_format[0], list):
        #If first item is list, all of the others should be list too.
        for item in list_to_format:
            if isinstance(item, list):
                #Its a cmplex list.
                return _format_object_as_tree(list_to_format)
        #Its a list of lists
        return _format_list_of_lists(list_to_format)
    
    if isinstance(list_to_format[0], dict):
        #Check if all of the items are dictionary, and all have the same keys.
        try:
            first_element_keys = list_to_format[0].keys()
            for index in range(len(list_to_format)):
                if list_to_format[index].keys() != first_element_keys:
                    #Keys are different. Return a tree.
                    return _format_object_as_tree(list_to_format)
                for dict_value in list_to_format[index].values():
                    if isinstance(dict_value, (dict, list, tuple)):
                        #Values of the dictionaries are complex, format it
                        #as a tree.
                        return _format_object_as_tree(list_to_format)
                    
        except AttributeError:
            #Not all of the items are dictionary.
            return _format_object_as_tree(list_to_format)
        #All tests are passed.
        return _format_list_of_dictionaries(list_to_format)

    #If some of the elements of the list are list, dict, or tuple, it can't
    #be formatted as a simple list.
    for list_item in list_to_format:
        if isinstance(list_item, (list, dict, tuple)):
            return _format_object_as_tree(list_to_format)
    
    #Its a simple list.
    return _format_simple_list(list_to_format)


def _format_simple_list(list_to_format):
    """Gets a list, and returns a formated string."""
    if len(list_to_format) == 0:
        return 'Empty result'
    
    max_item_length = 1
    for item in list_to_format:
        if not isinstance(item, basestring):
            item = str(item)
        max_item_length = max(max_item_length, len(item))
    
    max_item_length += len(ANSICOLORS.FBLUE)    
    terminal_width, terminal_height = utils.terminal_size()
    
    number_of_columns_to_draw = min(terminal_width / (max_item_length + 2),
                                    len(list_to_format)) or 1
    
    columns_width = ((terminal_width - 4) / number_of_columns_to_draw) - 2
    
    table_border = ANSICOLORS.FBLUE % ('  ' + \
                                      ('+'  + \
                                      ('-'*(columns_width))) * \
                                      number_of_columns_to_draw + '+\n')
    
    result = table_border
    line = '  %s ' % ANSICOLORS.FBLUE%'|'
    
    current_column = 1
    for item in list_to_format:
        #Ensure that our item is string, and we can apply formatting on it.
        if not isinstance(item, basestring):
            item = str(item)
        
        #If the length of the item is greater that the column's width, cut it.
        if len(item) >= columns_width - 2:
            item = item[:columns_width - 5] + '...'
        
        line += '%-{0}s %s '.format(columns_width - 2) %\
                             (item, ANSICOLORS.FBLUE%'|')
        if current_column >= number_of_columns_to_draw:
            result += line + '\n'
            line = '  %s ' % ANSICOLORS.FBLUE%'|'
            current_column = 0
            
        current_column += 1
    
    if len(line) > (4 + len(ANSICOLORS.FBLUE)):
        #There's some another items in the current line,
        #don't forget to add them to the result, too!
        result += line + '\n'
    
    result += table_border
    result += ANSICOLORS.BGREEN % \
              ('   count: %s' % len(list_to_format)) + '\n'
    
    return result


def _format_list_of_dictionaries(list_to_format):
    """Format the given list of dictionaries, to a human readable
    table. If keys of the dictionaries were different, it will
    return a Tree instead of table.
    """
    if len(list_to_format) == 0:
        return 'Empty result'

    first_element_keys = list_to_format[0].keys()
    #Estimate how many columns should be draw on screen
    terminal_width, terminal_height = utils.terminal_size()
    number_of_keys_to_draw = len(first_element_keys)
    if (number_of_keys_to_draw * 11) > (terminal_width - 5):
        #Terminal width is too small for showing all of the columns.
        print "Some of the columns can't be draw on the screen because of the",\
              "small width of the terminal."
        user_answer = raw_input("Do you want to see a detailed view? [Y/n]")
        if not user_answer.upper() in ('N', 'NO'):
            return _format_list_of_dict_as_detailed_view(list_to_format)
         
        number_of_keys_to_draw = (terminal_width - 5) / 11
    
    #Finding the max len of data in each column.
    max_length = {}
    #First, column headers.
    dict_keys = list_to_format[0].keys()
    for column_index in range(number_of_keys_to_draw):
        max_length[column_index] = len(dict_keys[column_index])
    
    for dict in list_to_format:
        for column_index in range(number_of_keys_to_draw):
            dict_value = dict[dict_keys[column_index]]
            if not isinstance(dict_value, basestring):
                dict_value = str(dict_value)
            
            max_length[column_index] = max(max_length[column_index],
                                               len(dict_value))
    
    #Calculating column size's factors
    sum_of_lengths = 0
    for column_index in max_length:
        sum_of_lengths += max_length[column_index]
    size_factors = {}
    for column_index in max_length:
        size_factors[column_index] = float(max_length[column_index]) / \
                                     sum_of_lengths

    columns_width = {}
    for column_index in range(number_of_keys_to_draw):
        columns_width[column_index] = \
            int((terminal_width - 9) * size_factors[column_index])
    
    #Normalizing columns width
    for column_index in columns_width:
        if columns_width[column_index] < 8:
            #Set it to min size
            leakage = 11 - columns_width[column_index]
            columns_width[column_index] = 8
            #Normalize other columns
            for i in range(leakage):
                max_width_index = 0
                for index in columns_width:
                    if columns_width[index] > columns_width[max_width_index]:
                        max_width_index = index
                columns_width[max_width_index] -= 1
                
    
    #Creating table's border
    table_border = ANSICOLORS.FBLUE % '   +'
    for column_index in columns_width:
        table_border += ANSICOLORS.FBLUE % \
                        ('-' * columns_width[column_index] + '+')
    
    result = table_border + '\n'

    line = ANSICOLORS.FBLUE % '   | '
    
    #Table header
    column_index = 0
    for key_index in range(number_of_keys_to_draw):
        column_header = first_element_keys[key_index]
        if len(column_header) > columns_width[column_index] - 2:
            column_header = column_header[:columns_width[column_index]-5] \
                            + '...'
        
        line += '%-{0}s'.format(columns_width[column_index]-2) \
                % column_header
        line += ANSICOLORS.FBLUE % ' | '
        column_index += 1
    
    result += line + '\n'
    result += table_border + '\n'
    
    #Table content
    line = ANSICOLORS.FBLUE % '   | '

    for item in list_to_format:
        #Make sure that our item is a string.
        column_index = 0
        for key_index in range(number_of_keys_to_draw):
            strItem = item[first_element_keys[key_index]]
            if not isinstance(strItem, basestring):
                strItem = str(strItem)
            
            if len(strItem) > columns_width[column_index] - 4:
                strItem = strItem[:columns_width[column_index]-7] + '...'
            
            line += '%-{0}s'.format(columns_width[column_index] - 2) % strItem
            line += ANSICOLORS.FBLUE % ' | '
            
            column_index += 1
        
        result += line + '\n'
        line = ANSICOLORS.FBLUE % '   | '
    
    result += table_border + '\n'
    result += ANSICOLORS.BGREEN % '      count: %s\n' % len(list_to_format)
    if number_of_keys_to_draw != len(first_element_keys):
        #Warn the user that some columns didn't draw
        result += ANSICOLORS.FYELLOW % ("   Some of the columns are not "+\
                                      "appears because of "+\
                                      "the small width of the screen.\n")
    return result


def _format_list_of_dict_as_detailed_view(list_to_format):
    """It formats each element in the list (dictionary) as a table,
    and shows them one by one.
    """
    if list_to_format == None:
        return 'Empty result'
    
    total_records = len(list_to_format)
    current_record = 0
    
    for dict in list_to_format:
        current_record += 1
        single_table = _format_dictionary(dict)
        print single_table
        print ANSICOLORS.FGREEN % "   Page %s of %s" % (current_record,
                                                           total_records)
        print ANSICOLORS.BNORMAL % "< Press any key to continue, 'q' to exit >"
        input_character = utils.getch()
        print input_character
        if input_character == 'q':
            break
    
    #We already print out the result ourselves.
    return ''


def _format_list_of_lists(list_to_format):
    return _format_object_as_tree(list_to_format)


def _format_object_as_tree(object_to_format):
    """Format the given object as a tree.
    
    @return: A string represents a tree.
    """
    raw_tree = _format_single_tree_node(object_to_format, 1)
    
    terminal_width, terminal_height = utils.terminal_size()
    #Cut the lines greater that terminal width
    formated_tree = ''
    tree_lines = raw_tree.splitlines()
    for line in tree_lines:
        if len(line) > terminal_width - 1:
            line = line[:len(line)-4] + '...'
        formated_tree += line + '\n'
    
    return formated_tree 


def _format_single_tree_node(node, indent):
    """Returns a string which represents the node.
    
    @param node: Can be any object
    @param indent: An integer, represents the empty space
                   before item.
    
    @return: Formated node as a string.
    """
    result = ''
    
    if isinstance(node, list):
        for list_item in node:
            if isinstance(list_item, (list, dict)):
                result += ANSICOLORS.FBLUE % (' ' * indent + '|- ')
                result += ANSICOLORS.BBLUE % '+' + '\n'
                result += _format_single_tree_node(list_item, indent + 3)
            else:
                result += ANSICOLORS.FBLUE % (' ' * indent + '|-')
                result += '{0}\n'.format(list_item)
    
    elif isinstance(node, dict):
        for dict_key in node:
            if isinstance(node[dict_key], (list, dict)):
                result += ANSICOLORS.FBLUE % (' ' * indent + '|-')
                result += ANSICOLORS.BNORMAL % str(dict_key)
                result += '%s %s' % (' = ',
                                     ANSICOLORS.BBLUE % '+')
                result += '\n'
                result += _format_single_tree_node(node[dict_key], indent + 3)
            else:
                result += ANSICOLORS.FBLUE % (' ' * indent + '|-')
                result += '%s = ' % dict_key
                result += ANSICOLORS.BNORMAL % node[dict_key]
                result += '\n'
                
    else:
        result += ANSICOLORS.FBLUE % (' ' * indent + '-')
        result += node + '\n'

    return result

