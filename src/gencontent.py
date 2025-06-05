import os
from markdown_blocks import markdown_to_html_node

def generate_pages_recursively(from_path, template_path, dest_path, basepath):
    print(f"Generating pages from {from_path} using template {template_path} to {dest_path}")
    
    if os.path.isdir(from_path):
        for item in os.listdir(from_path):
            item_from_path = os.path.join(from_path, item)
            item_dest_path = os.path.join(dest_path, item)
            if os.path.isdir(item_from_path):
                generate_pages_recursively(item_from_path, template_path, item_dest_path, basepath)
            elif item_from_path.endswith(".md"):
                generate_page(item_from_path, template_path, os.path.join(dest_path, "index.html"), basepath)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")

