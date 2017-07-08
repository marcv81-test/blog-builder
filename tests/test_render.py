import unittest

import engine.model
import engine.render

class TestRender(unittest.TestCase):

    def test_site(self):
        s = engine.model.Site('sample-site')
        r = engine.render.Renderer(
            engine.render.HtmlRenderer('templates'),
            engine.render.ImageRenderer())
        r.render_site(s, 'output')
