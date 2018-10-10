import ast
import io
import re

from setuptools import setup

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_pythonmarkdown.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='Patrik Dufresne Service Logiciel inc.',
    author_email='info@patrikdufresne.com',
    description=description,
    keywords='Lektor plugin static-site blog Python-Markdown',
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-pythonmarkdown',
    py_modules=['lektor_pythonmarkdown'],
    install_requires=['markdown<3.0.0'],
    tests_require=['lektor'],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    url='https://github.com/ikus060/lektor-python-markdown',
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Lektor',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'lektor.plugins': [
            'pythonmarkdown = lektor_pythonmarkdown:PythonMarkdownPlugin',
        ]
    }
)
