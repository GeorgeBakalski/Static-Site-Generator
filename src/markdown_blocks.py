from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if block[:2] == "# " or block[:3] == "## " or block[:4] == "### " or block[:5] == "#### " or block[:6] == "##### " or block[:7] == "###### " : 
        return BlockType.HEADING
    
    if block[:4] == "```\n" and block[-4:] == "\n```":
        return BlockType.CODE

    split_block = block.split("\n")
    counter = 0
    for line in split_block:
        if line[0] == ">":
            counter += 1
    if counter == len(split_block):
        return BlockType.QUOTE
    
    counter = 0 
    for line in split_block:
        if line[:2] == "- ":
            counter += 1
    if counter == len(split_block):
        return BlockType.UNORDERED_LIST
        
    counter = 0 
    for i in range(0, len(split_block)):
        if split_block[i].startswith(f"{i + 1}. "):
            counter += 1
    if counter == len(split_block):
        return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH
        
    
    

def markdown_to_blocks(markdown):
    list_of_blocks = markdown.split("\n\n")
    return_list = []
    for i in range(0,len(list_of_blocks)):
        list_of_blocks[i] = list_of_blocks[i].strip()
        if list_of_blocks[i] != "":
            return_list.append(list_of_blocks[i])
    return return_list
            
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.CODE:  
            all_nodes.append(ParentNode("pre", strip_code(block)))

        elif block_type == BlockType.UNORDERED_LIST:
            all_nodes.append(ParentNode(block_type_to_tag(block_type, block), strip_unordered_list(block)))

        elif block_type == BlockType.ORDERED_LIST:
            all_nodes.append(ParentNode(block_type_to_tag(block_type, block), strip_ordered_list(block)))

        elif block_type == BlockType.QUOTE:
            all_nodes.append(ParentNode(block_type_to_tag(block_type, block), text_to_children(strip_quote(block))))

        elif block_type == BlockType.HEADING:
            all_nodes.append(ParentNode(block_type_to_tag(block_type, block), text_to_children(strip_heading(block))))

        else:
            all_nodes.append(ParentNode(block_type_to_tag(block_type, block), text_to_children(block.replace("\n", " "))))
    return ParentNode("div", all_nodes)
        
def strip_heading(block):
    if block.startswith("# "):
        return block[2:]
    if block.startswith("## "):
        return block[3:]
    if block.startswith("### "):
        return block[4:]
    if block.startswith("#### "):
        return block[5:]
    if block.startswith("##### "):
        return block[6:]
    if block.startswith("###### "):
        return block[7:]
    return block

def strip_quote(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        clean = line[2:].rstrip()
        children.append(clean)
    return "\n".join(children)

def strip_unordered_list(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        clean = line[2:].rstrip()
        children.append(ParentNode("li", text_to_children(clean)))
    return children

def strip_ordered_list(block):
    lines = block.split(f"\n")
    children = []
    for line in lines:
        content = line.split(". ", 1)[1]
        children.append(ParentNode("li", text_to_children(content)))
    return children

def strip_code(block):
    textnode = TextNode(block[4:-3], TextType.TEXT)
    return  [ParentNode("code", [text_node_to_html_node(textnode)])]

def text_to_children(block):
    nodes = text_to_textnodes(block)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children
        
def block_type_to_tag(block_type, block):
    if block_type == BlockType.PARAGRAPH:
        return "p"
    if block_type == BlockType.CODE:
        return "code"
    if block_type == BlockType.HEADING:
        return heading_1_to_6(block)
    if block_type == BlockType.QUOTE:
        return "blockquote"
    if block_type == BlockType.UNORDERED_LIST:
        return "ul"
    if block_type == BlockType.ORDERED_LIST:
        return "ol"

def heading_1_to_6(block):
    if block.startswith("# "):
        return "h1"
    if block.startswith("## "):
        return "h2"
    if block.startswith("### "):
        return "h3"
    if block.startswith("#### "):
        return "h4"
    if block.startswith("##### "):
        return "h5"
    if block.startswith("###### "):
        return "h6"
    
def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception("There should be a title")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].rstrip()