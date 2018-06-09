# Lektor Python-Markdown Plugin

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