import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_next_to_each_other(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_just_text(self):
        node = TextNode("Just plain text with nothing special", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("Just plain text with nothing special", TextType.TEXT)], new_nodes)

    def test_split_images_processed(self):
        node = TextNode("already image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("already image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")], new_nodes)

    def test_split_same_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to boot dev", TextType.LINK, "https://www.boot.dev"
                ),
            ],
            new_nodes,
        )
    