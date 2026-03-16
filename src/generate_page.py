from markdown_blocks import markdown_to_html_node, extract_title
import os
from pathlib import Path

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as f:
        markdown = f.read()
    with open(template_path,"r") as f:
        template = f.read()
    node = markdown_to_html_node(markdown)
    html_string = node.to_html()
    title = extract_title(markdown)
    template_with_title = template.replace( "{{ Title }}", title)
    content_template = template_with_title.replace( "{{ Content }}", html_string)
    href_template = content_template.replace( 'href="/', f'href="{basepath}')
    final_template = href_template.replace( 'src="/', f'src="{basepath}')
    print("BASEPATH DEBUG:", basepath)
    dir = os.path.dirname(dest_path)
    if dir:
        os.makedirs(dir, exist_ok= True)
    with open(dest_path, "w") as page:
        page.write(final_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        entry_path = (os.path.join(dir_path_content, entry))
        if os.path.isfile(entry_path):
            dest_path = Path(os.path.join(dest_dir_path, entry))
            generate_page(entry_path,template_path, dest_path.with_suffix(".html"), basepath)
        else:
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry), basepath)