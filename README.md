# Lektor Python-Markdown Plugin

[![pipeline status](http://git.patrikdufresne.com/pdsl/lektor-python-markdown/badges/master/pipeline.svg)](http://git.patrikdufresne.com/pdsl/lektor-python-markdown/commits/master)

A [Lektor](https://www.getlektor.com/) plugin to parse markdown using
[Python-Markdown](https://python-markdown.github.io/). By default, lektor
uses [mistune](http://mistune.readthedocs.io/en/latest/) to parse markdown
field.
With this plugin, you can chose which parser is to be used by setting a
different type on the field. Either: `markdown` or `pythonmarkdown`

## Installation

Add lektor-pythonmarkdown to your project from command line:

```
lektor plugins add lektor-pythonmarkdown
```

## Usage

In your model, you need to define the type of field as follow:
```
[model]
name = Page

[fields.body]
label = Body
type = pythonmarkdown

```

# Warning !

This plugins is is obviously incompatible with all of the mistune-specific events and plugins. Namely, all of `markdown-*` events and the plugins built around them.


# Advance configuration

This lektor plugins provide a nice way to configure python-markdown. For instance, it's possible to explicitly define the extentions to be enabled and to configure each of them seperatly.

For an advance configuration, you need to create a file named `pythonmarkdown.ini` in the `configs` folder.

In that file you may write something similar to the following:
```
[markdown]
# Define the configuration of python-markdown.
# Reference: https://python-markdown.github.io/reference/#markdown

#output_format = xhtml1
#tab_length = 4
#safe_mode = False
#enable_attributes = True
#smart_emphasis = True
#lazy_ol = True

[extensions]
# List extensions to be enabled.
markdown.extensions.extra = 1
markdown.extensions.admonition = 1
markdown.extensions.codehilite = 1
markdown.extensions.meta = 1
markdown.extensions.nl2br = 1
markdown.extensions.sane_lists = 1
markdown.extensions.smarty = 1
markdown.extensions.toc = 1
markdown.extensions.wikilinks = 1

[markdown.extensions.codehilite]
# Specific configuration for an extension.
# Reference: https://python-markdown.github.io/extensions/code_hilite/#usage
linenums = True
#guess_lang = True
#css_class = codehilite
#pygments_style = default
#noclasses = False
#use_pygments = True

```
