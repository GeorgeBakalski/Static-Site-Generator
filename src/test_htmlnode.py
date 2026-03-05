import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_empty(self):
        node = HTMLNode("a", "link")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        prop1 = {
    "href": "https://www.google.com",
    "target": "_blank",
}
        node = HTMLNode("a", "link", None, prop1)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_different_children(self):
        node = ParentNode(
    "div",
    [
        LeafNode("b", "Bold"),
        LeafNode(None, "Plain text"),
        ParentNode("span", [LeafNode("i", "italic")]),
    ],
)
        self.assertEqual(node.to_html(), "<div><b>Bold</b>Plain text<span><i>italic</i></span></div>")

    def test_to_html_with_parent_props(self):
        node = ParentNode("div", [LeafNode("b", "child")], {"class": "main-container"})
        self.assertEqual(node.to_html(), '<div class="main-container"><b>child</b></div>')

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("b", "child")])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()