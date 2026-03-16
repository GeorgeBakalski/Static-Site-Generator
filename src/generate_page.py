from markdown_blocks import markdown_to_html_node, extract_title
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path,"r") as f:
        markdown = f.read()
    with open(template_path,"r") as f:
        template = f.read()
    node = markdown_to_html_node(markdown)
    html_string = node.to_html()
    title = extract_title(markdown)
    template_with_title = template.replace( "{{ Title }}", title)
    final_template = template_with_title.replace( "{{ Content }}", html_string)
    
    dir = os.path.dirname(dest_path)
    if dir:
        os.makedirs(dir, exist_ok= True)
    with open(dest_path, "w") as page:
        page.write(final_template)

