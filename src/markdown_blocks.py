from enum import Enum

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
            
