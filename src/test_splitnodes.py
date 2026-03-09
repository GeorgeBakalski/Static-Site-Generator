import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode,TextType

class TestTextNode(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_node = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bold block", TextType.BOLD),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), new_node)

    def test_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_node = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("italic block", TextType.ITALIC),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), new_node)

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_node = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), new_node)

    def test_plain(self):
        node = TextNode("This is text with a block word", TextType.TEXT)
        new_node = [
    TextNode("This is text with a block word", TextType.TEXT),
]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), new_node)

    def test_exception(self):
        node = TextNode("This is text with no `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text(self):
        node = TextNode("`This is text with a code block word`", TextType.CODE)
        new_node = [
    TextNode("`This is text with a code block word`", TextType.CODE),
]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), new_node)

    def test_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        correct = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), correct)

    def test_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        correct = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), correct)
