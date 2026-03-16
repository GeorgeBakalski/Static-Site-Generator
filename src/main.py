from textnode import TextType, TextNode
import os, shutil
from copystatic import copy_files_recursive
from generate_page import generate_page

def main():
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_files_recursive("./static", "./public")
    generate_page("content/index.md", "./template.html", "public/index.html")

main()