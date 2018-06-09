# -*- coding: utf-8 -*-
'''
Created on Jun 8, 2018

@author: Patrik Dufresne
'''
from lektor.pluginsystem import Plugin
from lektor.types import Type
import markdown

EXTENTIONS = [
    "markdown.extensions.extra",
    "markdown.extensions.admonition",
    "markdown.extensions.codehilite",
    "markdown.extensions.headerid",
    "markdown.extensions.meta",
    "markdown.extensions.nl2br",
    "markdown.extensions.sane_lists",
    "markdown.extensions.smarty",
    "markdown.extensions.toc",
    "markdown.extensions.wikilinks",
]


def pythonmarkdown_to_html(text):
    return markdown.markdown(text, EXTENTIONS)


# Wrapper with an __html__ method prevents Lektor from escaping HTML tags.
class HTML(object):

    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


# The name of the class is used a key for the fields type.
class PythonMarkdownType(Type):
    widget = 'multiline-text'

    def value_from_raw(self, raw):
        return HTML(pythonmarkdown_to_html(raw.value or u''))


class PythonMarkdownPlugin(Plugin):
    name = u'pythonmarkdown'
    description = u'Adds AsciiDoc field type to Lektor.'

    def on_setup_env(self, **extra):
        self.env.add_type(PythonMarkdownType)
