import unittest

import engine.model

class TestModel(unittest.TestCase):

    def test_site(self):
        s = engine.model.Site('sample-site')
        self.assertEqual(s.meta['title'], 'Sample Site')
        self.assertEqual(s.meta['url'], 'http://127.0.0.1')

    def test_post(self):
        s = engine.model.Site('sample-site')
        self.assertEqual(len(s.posts), 2)
        p = s.posts[0]
        self.assertEqual(p.id, 'sample-1')
        self.assertEqual(p.meta['title'], 'Sample Post #1')
        self.assertEqual(p.content, '机器人\n')

    def test_image(self):
        s = engine.model.Site('sample-site')
        p = s.posts[1]
        self.assertEqual(len(p.images), 1)
        i = p.images[0]
        self.assertEqual(i.id, 'grey')
