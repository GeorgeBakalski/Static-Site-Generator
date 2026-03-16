import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title

class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_empty_lines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        md = "#### This is a HEADING"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.HEADING
        )

    def test_block_to_block_type_code(self):
        md = "```\nThis is CODE \n```"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.CODE
        )

    def test_block_to_block_type_quote(self):
        md = "> This \n>is \n>a \n> QUOTE    "
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.QUOTE
        )

    def test_block_to_block_type_unordered_list(self):
        md = "- This \n- is \n- an \n- UNORDERED LIST"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_ordered_list(self):
        md = "1. This \n2. is \n3. an \n4. ORDERED LIST"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_paragraph(self):
        md = "This is a PARAGRAPH"
        block_type = block_to_block_type(md)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is **bolded** paragraph
> text in a p
> tag here
> This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>This is <b>bolded</b> paragraph\ntext in a p\ntag here\nThis is another paragraph with <i>italic</i> text and <code>code</code> here</blockquote></div>",
    )
        
    def test_unordered_list_block(self):
        md = """
- This is **bolded** paragraph
- text in a p
- tag here
- This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>This is <b>bolded</b> paragraph</li><li>text in a p</li><li>tag here</li><li>This is another paragraph with <i>italic</i> text and <code>code</code> here</li></ul></div>",
    )
    
    def test_ordered_list_block(self):
        md = """
1. This is **bolded** paragraph
2. text in a p
3. tag here
4. This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>This is <b>bolded</b> paragraph</li><li>text in a p</li><li>tag here</li><li>This is another paragraph with <i>italic</i> text and <code>code</code> here</li></ol></div>",
    )
        
    def test_headingblock(self):
        md = """
# This is **bolded** paragraph

#### text in a p

##### tag here

###### This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h1>This is <b>bolded</b> paragraph</h1><h4>text in a p</h4><h5>tag here</h5><h6>This is another paragraph with <i>italic</i> text and <code>code</code> here</h6></div>",
    )
        
    def test_all_blocks(self):
        md = """
# This is **bolded** heading

#### text in another heading

This is **bolded** paragraph

> This is a 
> quote with _italic_ text 
> and `code` here

```
this is **just** _code_
```

- this is 
- an unordered **list**

1. this is
2. an _ordered_ list

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h1>This is <b>bolded</b> heading</h1><h4>text in another heading</h4><p>This is <b>bolded</b> paragraph</p><blockquote>This is a\nquote with <i>italic</i> text\nand <code>code</code> here</blockquote><pre><code>this is **just** _code_\n</code></pre><ul><li>this is</li><li>an unordered <b>list</b></li></ul><ol><li>this is</li><li>an <i>ordered</i> list</li></ol></div>",
    )
        
def test_extract_title(self):
    md = """
# This is **bolded** heading

#### text in another heading

This is **bolded** paragraph

> This is a 
> quote with _italic_ text 
> and `code` here

```
this is **just** _code_
```

- this is 
- an unordered **list**

1. this is
2. an _ordered_ list

"""    
    title =  extract_title(md)
    self.assertEqual( title, "This is **bolded** heading")

def test_extract_no_title(self):
    md = """

#### text in another heading

This is **bolded** paragraph

> This is a 
> quote with _italic_ text 
> and `code` here

```
this is **just** _code_
```

- this is 
- an unordered **list**

1. this is
2. an _ordered_ list

"""    
    with self.assertRaises(Exception):
        extract_title(md)