from setuptools import setup, find_packages

setup(
    name="pysmith",
    version="0.1.0",
    packages=find_packages(),
    extras_require={
        "frontmatter": ["python-frontmatter>=0.5.0"],
        "markdown": ["markdown2>=2.3.9"],
        "minify": ["rjsmin>=1.1.0"],
        "sass": ["libsass>=0.20.0"],
        "template": ["Jinja2>=2.11.2"],
    }
)
