from textnode import TextType, TextNode
import os, shutil, sys
from copystatic import copy_files_recursive
from generate_page import generate_page, generate_pages_recursive
 

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")
    copy_files_recursive("./static", "./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()