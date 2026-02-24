import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_empty(self):
        node1 = HTMLNode("a", "link")
        self.assertEqual(node1.props_to_html(), "")

    def test_props_to_html_multiple(self):
        prop1 = {
    "href": "https://www.google.com",
    "target": "_blank",
}
        node2 = HTMLNode("a", "link", None, prop1)
        self.assertEqual(node2.props_to_html(), ' href="https://www.google.com" target="_blank"')



if __name__ == "__main__":
    unittest.main()