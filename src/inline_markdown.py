from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    list_of_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            list_of_nodes.append(node)
            continue
        splited_node = node.text.split(delimiter)
        if len(splited_node) % 2 == 0:
            raise Exception("That's invalid Markdown syntax") 
        counter = len(splited_node)
        for num in range(0, counter):
            if splited_node[num] == "":
                continue 
            if num % 2 == 0:
                list_of_nodes.append(TextNode(splited_node[num], TextType.TEXT))
            else:
                list_of_nodes.append(TextNode(splited_node[num], text_type))
    return list_of_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches
