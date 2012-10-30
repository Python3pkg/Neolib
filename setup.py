import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
setup(
    name = "neolib",
    version = "1.0.0",
    packages = find_packages(),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['lxml', 'beautifulsoup4', 'requests', 'PIL'],

    # metadata for upload to PyPI
    author = "Joshua Gilman",
    author_email = "joshuagilman@gmail.com",
    description = "Neolib is an in-depth and robust Python library designed to assist programmers in creating programs which automate mundane tasks on the popular browser based game, Neopets",
    license = "PSF",
    keywords = "neopets",
    url = "https://github.com/jmgilman/Neolib",   # project home page, if any
)
