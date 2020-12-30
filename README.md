# Weeknote

This repo renders the [weeknote pages on the digital land site](https://digital-land.github.io/weeknote/).

## Working with repo

Install dependencies (we recommend working in a virtualenv)

    make init

Render pages

    make render

### Writing weeknotes

Things to note

* the first sentence will be extracted as the summary shown on the list page. If you wish to override this then add a `summary` attribute to the frontmatter in the markdown file.
* when adding images from flickr remember to add the `dl-image` class to the `<img>` tag.
