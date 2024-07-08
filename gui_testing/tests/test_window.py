"""Unit tests for app
"""

# Import testing packages
import unittest

# Import app modules
import app


class TestMessage(unittest.TestCase):

    def setUp(self):
        self.app = app.App()

    def tearDown(self):
        self.app.update()
        self.app.destroy()

    def test_root_geometry(self):
        geo = self.app.winfo_screenwidth()
        self.assertEqual(geo, 1536)

    def test_on_submit(self):
        self.app._on_submit()
        self.assertEqual(self.app.mytext.get(), 'Testing _on_submit')


if __name__ == '__main__':
    unittest.main()
