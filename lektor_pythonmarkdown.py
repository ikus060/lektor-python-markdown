# -*- coding: utf-8 -*-
'''
Created on Jun 8, 2018

@author: Patrik Dufresne
'''
from lektor.pluginsystem import Plugin
from lektor.types import Type
import markdown

SECTION_EXTENSIONS = "extensions"
SECTION_MARKDOWN = "markdown"

DEFAULT_EXTENTIONS = [
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


def pythonmarkdown_to_html(text, cfg):
    # TODO Call events.
    return markdown.markdown(text, **cfg.options)


# Wrapper with an __html__ method prevents Lektor from escaping HTML tags.
class HTML(object):

    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html

    
def _value(v):
    "This function tries to convert the configuration value to a sane type."
    if v.lower() in ['true', 'false']:
        return v.lower() == 'true'
    try:
        return int(v)
    except:
        return v

    
class PythonMarkdownConfig(object):
    """
    Define configuration of python-markdown.
    """

    def _section_as_dict(self, name):
        return {k: _value(v) for k, v in self.plugin_config.section_as_dict(name).items()}

    def _extensions(self):
        return [
            e
            for e, v in (self._section_as_dict(SECTION_EXTENSIONS) or DEFAULT_EXTENTIONS).items()
            if v]
    
    def __init__(self, plugin_config):
        self.plugin_config = plugin_config
        self.options = self._section_as_dict(SECTION_MARKDOWN)
        self.options.update({
            "extensions": self._extensions(),
            "extension_configs": {e: self._section_as_dict(e) for e in self._extensions()},
        })


class PythonMarkdownPlugin(Plugin):
    name = u'pythonmarkdown'
    description = u'Adds AsciiDoc field type to Lektor.'

    def on_setup_env(self, **extra):
        plugin_config = self.get_config()
        
        # We declare this type as an internal class inside the plugin to get
        # access to the get_config() function from the Type.
        #
        # The name of the class is used a key for the fields type.
        class PythonMarkdownType(Type):
            widget = 'multiline-text'
            
            def value_from_raw(self, raw):
                """
                Called to convert the raw value (markdown) into html.
                """
                cfg = PythonMarkdownConfig(plugin_config)
                return HTML(pythonmarkdown_to_html(raw.value or u'', cfg))

        self.env.add_type(PythonMarkdownType)
