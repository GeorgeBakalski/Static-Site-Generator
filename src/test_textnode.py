import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        self.assertEqual(node, node2)

        

    def test_text_type(self):
        node3 = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        node4 = TextNode("This is a link node", TextType.ITALIC, "https://www.boot.dev")

        self.assertNotEqual(node3, node4)

    def test_url(self):
        node5 = TextNode("This is another link node", TextType.LINK, "https://www.boot.dev")
        node6 = TextNode("This is another link node", TextType.LINK)

        self.assertNotEqual(node5, node6)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("click me", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "click me")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    

if __name__ == "__main__":
    unittest.main()