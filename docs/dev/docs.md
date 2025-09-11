---
title: Docs
---

# 📝 Docs

To build the documentation, run the following command:

```sh
# Install python documentation dependencies:
pip install -r ./requirements/requirements.docs.txt

# Serve documentation locally (for development):
./scripts/docs.sh
# Or:
mkdocs serve

# Or build documentation:
./scripts/docs.sh -b
# Or:
mkdocs build
```

## MkDocs Material

### Installation

```sh
pip install -U mkdocs-material mkdocs-render-swagger-plugin
```

### Commands

- `mkdocs new [dir-name]` - Create a new project.
- `mkdocs serve` - Start the live-reloading docs server.
- `mkdocs build` - Build the documentation site.
- `mkdocs -h` - Print help message and exit.

### Docs layout

```txt
mkdocs.yml    # The configuration file.
docs/
    index.md  # The documentation homepage.
    ...       # Other markdown pages, images and other files.
```

## References

- [MkDocs Documentation](https://www.mkdocs.org)
- [MkDocs Material Documentation](https://squidfunk.github.io/mkdocs-material)
- [MkDocs Swagger Renderer Plugin](https://github.com/bharel/mkdocs-render-swagger-plugin)
- [mkdocstrings Documentation](https://mkdocstrings.github.io)
