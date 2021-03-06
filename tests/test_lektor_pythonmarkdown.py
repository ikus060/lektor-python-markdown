
'''
Created on Jun 8, 2018

@author: Patrik Dufresne
'''

from lektor.builder import Builder
from lektor.db import Database
from lektor.environment import Environment
from lektor.project import Project
import os
import shutil
import tempfile
import unittest


class TestLektorAsciidoc(unittest.TestCase):

    def setUp(self):
        self.project = Project.from_path(os.path.join(os.path.dirname(__file__), 'demo-project'))
        self.env = Environment(self.project)
        self.pad = Database(self.env).new_pad()
        self.out = tempfile.mkdtemp()
        self.builder = Builder(self.pad, self.out)

    def tearDown(self):
        try:
            shutil.rmtree(self.out)
        except (OSError, IOError):
            pass

    def test_basic(self):
        failures = self.builder.build_all()
        assert not failures
        page_path = os.path.join(self.builder.destination_path, 'index.html')
        html = open(page_path).read()
        print(html)
        assert '<h1 id="header-1">Header 1</h1>' in html
        assert '<h2 class="customclass" id="header-2">Header 2</h2>' in html
        # The output changes depending on the version of python-markdown uses.
        assert '<pre class="codehilite"><code class="linenums">code here</code></pre>' in html


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
