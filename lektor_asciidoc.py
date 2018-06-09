# -*- coding: utf-8 -*-
from subprocess import PIPE, Popen

from lektor.pluginsystem import Plugin
from lektor.types import Type


def asciidoc_to_html(text):
    p = Popen(['asciidoc', '--no-header-footer', '--backend=html5', '-'],
              stdin=PIPE, stdout=PIPE, stderr=PIPE)

    out, err = p.communicate(text)
    if p.returncode != 0:
        raise RuntimeError('asciidoc: "%s"' % err)

    return out


# Wrapper with an __html__ method prevents Lektor from escaping HTML tags.
class HTML(object):
    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


class AsciiDocType(Type):
    widget = 'multiline-text'

    def value_from_raw(self, raw):
        return HTML(asciidoc_to_html(raw.value or u''))


class AsciiDocPlugin(Plugin):
    name = u'AsciiDoc'
    description = u'Adds AsciiDoc field type to Lektor.'

    def on_setup_env(self, **extra):
        self.env.add_type(AsciiDocType)
