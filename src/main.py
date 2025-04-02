from textnode import *
from htmlnode import *
from markdown_blocks import *
import os
import shutil
import sys

if len(sys.argv) > 1:
    BASEPATH = sys.argv[1]
else:
    BASEPATH = ""

docs_PATH = "docs"


def copy_static(path):
    # print(f"path: {path}")
    for dir in os.listdir(path):
        current_path = os.path.join(path, dir)
        # print(f"current path: {current_path}")
        if not os.path.isfile(current_path):
            dir_path = current_path.replace("static", "docs")
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            # print(f"not a file: {current_path}")
            copy_static(current_path)
        else:
            file_path = os.path.join(path, dir)
            # print(f"file path: {file_path}")
            docs = file_path.replace("static", "docs")
            # print(f"file: {docs}")
            shutil.copy(file_path, docs)
            continue


def clear_docs():
    # check if docs folder exists, if it does, delete and recreate it
    if os.path.exists(docs_PATH):
        shutil.rmtree(docs_PATH)
        os.mkdir(docs_PATH)
    else:
        os.mkdir(docs_PATH)


def extract_title(markdown):
    lines = markdown.split("\n")
    head = []
    for line in lines:
        if line.startswith("# "):
            head.append(line[2:].strip())
    return head[0]


# def generate_page(from_path, template_path, dest_path):
#     print(f"Generating page from {from_path} to {dest_path} using {template_path}")
#     with open(from_path, "r") as f:
#         markdown_file = f.read()
#     with open(template_path, "r") as f:
#         template_file = f.read()

#     htmlnode = markdown_to_html_node(markdown_file)
#     content = htmlnode.to_html()
#     title = extract_title(markdown_file)
#     template_file = template_file.replace(r"{{ Content }}", content)
#     template_file = template_file.replace(r"{{ Title }}", title)

#     os.makedirs(os.path.dirname(dest_path), exist_ok=True)
#     with open(dest_path, "w") as f:
#         f.write(template_file)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(
        f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}"
    )
    for dir in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, dir)
        if not os.path.isfile(current_path):
            dir_path = current_path.replace("content", "docs")
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            generate_pages_recursive(current_path, template_path, dest_dir_path)
        else:

            with open(current_path, "r") as f:
                markdown_file = f.read()

            with open(template_path, "r") as f:
                template_file = f.read()

            href = f'href="{BASEPATH}'
            src = f'src="{BASEPATH}'

            htmlnode = markdown_to_html_node(markdown_file)
            content = htmlnode.to_html()
            content = content.replace('src="/', src)
            title = extract_title(markdown_file)
            
            template_file = template_file.replace(r"{{ Content }}", content)
            template_file = template_file.replace(r"{{ Title }}", title)

            
            
            template_file = template_file.replace('href="/', href)
            
            file_path = current_path.replace("content", "docs")
            file_path = file_path.replace(".md", ".html")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write(template_file)


def main():
    clear_docs()
    copy_static("static/")
    generate_pages_recursive("content", "template.html", "docs")


if __name__ == "__main__":
    main()
