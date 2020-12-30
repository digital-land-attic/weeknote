#!/usr/bin/env python3

from bin.summary import create_summary
import os
import sys

from pathlib import Path
from collections import OrderedDict

from frontmatter import Frontmatter

from bin.render import render
from bin.summary import create_summary

from digital_land_frontend.jinja import setup_jinja
from digital_land_frontend.filters import make_link
from digital_land_frontend.markdown.filter import compile_markdown, markdown_filter

output_dir = "docs"
content_dir = "content"
url_root = "weeknote"

# setup jinja
env = setup_jinja()
env.globals["urlRoot"] = url_root
env.filters["make_link"] = make_link
env.filters["markdown"] = markdown_filter

index_template = env.get_template("index.html")
weeknote_template = env.get_template("weeknote.html")


def get_content_pages(directory):
    return os.listdir(directory)


def markdown_files_only(files, file_ext=".md"):
    return [f for f in files if f.endswith(file_ext)]


def read_content_file(filename, expanded=False):
    content = {}
    # fn = Path(filename)
    file_content = Frontmatter.read_file(filename)

    content["content"] = compile_markdown(file_content["body"])
    content["frontmatter"] = file_content["attributes"]
    content["title"] = (
        file_content["attributes"].get("title")
        if file_content["attributes"].get("title") is not None
        else filename.with_suffix("")
    )
    content["date"] = file_content["attributes"].get("date")
    content["displayDate"] = True
    content["section"] = "Weeknote"

    if expanded:
        content["body"] = file_content["body"]

    return content


def render_pages(directory, parent_dir=""):
    path_to_directory = os.path.join(parent_dir, directory)
    pages = get_content_pages(path_to_directory)

    for page in pages:
        p = os.path.join(path_to_directory, page)
        if os.path.isdir(p):
            # handle directories
            print(p, "is a directory")
            render_pages(page, path_to_directory)
        elif page.endswith(".md"):
            # compile and render markdown file
            fn = Path(p)
            contents = read_content_file(fn)
            output_path = os.path.join(output_dir, fn.stem, "index.html")
            render(output_path, weeknote_template, content=contents)
        else:
            # TO DO: copy other pages to /docs
            pass


def render_index():
    summaries = []
    all = get_content_pages(content_dir)
    weeknotes = markdown_files_only(all)
    for weeknote in sorted(weeknotes, reverse=True):
        path_to_file = os.path.join(content_dir, weeknote)
        fn = Path(path_to_file)
        contents = read_content_file(fn, expanded=True)
        summaries.append(
            create_summary(
                contents,
                fn,
                section=contents["section"],
                displayDate=True,
                date=contents["date"],
            )
        )

    output_path = os.path.join(output_dir, "index.html")
    render(output_path, index_template, summaries=summaries)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--local":
        env.globals["staticPath"] = "/static"
        url_root = ""
        env.globals["urlRoot"] = url_root

    render_pages(content_dir)
    render_index()
