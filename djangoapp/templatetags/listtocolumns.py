# -*- coding: utf-8 -*-
"""Copyright (c) 2009 Sergio Gabriel Teves
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
"""Splits query results list into multiple sublists for template display."""
from django.template import Library, Node, TemplateSyntaxError

register = Library()

class SplitListNode(Node):
    def __init__(self, results, cols, new_results):
        self.results, self.cols, self.new_results = results, cols, new_results

    def split_seq(self, results, cols=2):
        start = 0
        for i in xrange(cols):
            stop = start + len(results[i::cols])
            yield results[start:stop]
            start = stop

    def render(self, context):
        context[self.new_results] = self.split_seq(context[self.results], int(self.cols))
        return ''

def list_to_columns(parser, token):
    """Parse template tag: {% list_to_colums results as new_results 2 %}"""
    bits = token.contents.split()
    if len(bits) != 5:
        raise TemplateSyntaxError, "list_to_columns results as new_results 2"
    if bits[2] != 'as':
        raise TemplateSyntaxError, "second argument to the list_to_columns tag must be 'as'"
    return SplitListNode(bits[1], bits[4], bits[3])

list_to_columns = register.tag(list_to_columns)
