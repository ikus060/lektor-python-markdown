# -*- coding: utf-8 -*-
'''
Created on Jun 8, 2018

@author: Patrik Dufresne
'''
import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import LinkPattern
import types
from weakref import ref as weakref

from lektor.context import get_ctx, url_to
from lektor.pluginsystem import Plugin
from lektor.types import Type
from lektor.utils import bool_from_string
from markupsafe import Markup
from werkzeug.urls import url_parse


SECTION_EXTENSIONS = "extensions"
SECTION_MARKDOWN = "markdown"
DEFAULT_EXTENTIONS = {
    "markdown.extensions.extra": 1,
}


def sanitize_url(self, link):
    """
    Patched function to resolve the url using Lektor.
    """
    try:
        url = url_parse(link)
        if not url.scheme:
            link = url_to("!" + link)
    except:
        # Do not fail if something went wrong during the url parsing.
        pass
    return LinkPattern.sanitize_url(self, link)


class LektorMarkdownExtension(Extension):
    """
    This class represent an extension into the python-markdown to implement
    some logic in url handling to mimic the current behaviour of default
    markdown rendered (mistune).
    """
    
    def _patch(self, p):
        """
        Monkey patch the sanitize_url method.
        """
        p.sanitize_url = types.MethodType(sanitize_url, p)

    def extendMarkdown(self, md, md_globals):
        self._patch(md.inlinePatterns['link'])
        self._patch(md.inlinePatterns['image_link'])
        self._patch(md.inlinePatterns['image_reference'])
        self._patch(md.inlinePatterns['reference'])


class PythonMarkdownConfig(object):
    """
    Define configuration of python-markdown.
    """

    def _section_as_dict(self, name):

        def _value(v):
            "This function tries to convert the configuration value to a sane type."
            w = bool_from_string(v)
            if w is not None:
                return w
            try:
                return int(v)
            except:
                return v
        
        return {k: _value(v) for k, v in self.plugin_config.section_as_dict(name).items()}

    def _builtin_extensions(self):
        return [LektorMarkdownExtension()]

    def _extensions(self):
        return [
            e
            for e, v in (self._section_as_dict(SECTION_EXTENSIONS) or DEFAULT_EXTENTIONS).items()
            if v]
    
    def __init__(self, plugin_config):
        self.plugin_config = plugin_config
        self.options = self._section_as_dict(SECTION_MARKDOWN)
        self.options.update({
            "extensions": self._extensions() + self._builtin_extensions(),
            "extension_configs": {e: self._section_as_dict(e) for e in self._extensions()},
        })


def pythonmarkdown_to_html(text, record=None):
    """
    Convert python-markdown into html.
    """
    ctx = get_ctx()
    if ctx is None:
        raise RuntimeError('Context is required for python-markdown rendering')
    
    env = get_ctx().env
    plugin = env.plugins.get('pythonmarkdown', None)
    if not plugin:
        raise RuntimeError('PythonMarkdownPLugin is required for python-markdown rendering')    
    cfg = PythonMarkdownConfig(plugin.get_config())
    # TODO May need to emit event to let other plugin hook into this one.
    return markdown.markdown(text, **cfg.options)


class PythonMarkdown(object):

    def __init__(self, source, record=None):
        self.source = source
        self.__record = weakref(record) if record is not None else lambda: None
        self.__html = None
        self.__meta = None

    def __bool__(self):
        return bool(self.source)

    __nonzero__ = __bool__

    def __render(self):
        if self.__html is None:
            self.__html = pythonmarkdown_to_html(self.source, self.__record())
            self.__meta = None

    @property
    def meta(self):
        self.__render()
        return self.__meta

    @property
    def html(self):
        self.__render()
        return Markup(self.__html)

    def __getitem__(self, name):
        return self.meta[name]

    def __unicode__(self):
        self.__render()
        return self.__html

    def __html__(self):
        self.__render()
        return Markup(self.__html)


class PythonMarkdownDescriptor(object):

    def __init__(self, source):
        self.source = source

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return PythonMarkdown(self.source, record=obj)


class PythonMarkdownType(Type):
    widget = 'multiline-text'
    
    def value_from_raw(self, raw):
        """
        Called to convert the raw value (markdown) into html.
        """
        return PythonMarkdownDescriptor(raw.value or u'')


class PythonMarkdownPlugin(Plugin):
    name = u'pythonmarkdown'
    description = u'Add pythonmarkdownn field type to Lektor to make use of python-markdown as a renderer.'

    def on_setup_env(self, **extra):
        self.env.add_type(PythonMarkdownType)
