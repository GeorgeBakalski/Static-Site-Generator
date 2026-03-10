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

def split_nodes_image(old_nodes):
    list_of_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            list_of_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)
        sections = []
        for image_alt, image_link in images:
            sections = original_text.split(f"![{image_alt}]({image_link})", 1)

            if len(sections) != 2 :
                raise Exception("That's invalid Markdown syntax") 
            if sections[0] != "":
                list_of_nodes.append(TextNode(sections[0], TextType.TEXT))

            original_text = sections[1]
            list_of_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

        if original_text != "":
            list_of_nodes.append(TextNode(original_text, TextType.TEXT))
    return list_of_nodes
       
def split_nodes_link(old_nodes):
    list_of_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            list_of_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)
        sections = []
        for link_alt, link in links:
            sections = original_text.split(f"[{link_alt}]({link})", 1)

            if len(sections) != 2 :
                raise Exception("That's invalid Markdown syntax") 
            if sections[0] != "":
                list_of_nodes.append(TextNode(sections[0], TextType.TEXT))

            original_text = sections[1]
            list_of_nodes.append(TextNode(link_alt, TextType.LINK, link))

        if original_text != "":
            list_of_nodes.append(TextNode(original_text, TextType.TEXT))
    return list_of_nodes