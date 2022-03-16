# ------------------------------------------------------------------------------
# Project: DueDesk
# Module: setup
# Abstract: 
#   Sets up application as a python package for distributing and easy use
#   through `pip install`.
# Inspired by:
#   https://packaging.python.org/tutorials/packaging-projects/
# ------------------------------------------------------------------------------

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    entire_description = fh.read()

exec(open('src/duedesk/__version__.py').read())
setuptools.setup(
    name="DueDesk",
    version=__version__,
    author="Michael Hayworth, Chase Ruskin, Terry Nelson, Josh Prentice",
    author_email="",
    description="The virtual space to help get assignments done in a fun and rewarding way.",
    long_description=entire_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CEN3031-G33/due-desk",
    classifiers=[
        "",
    ],
    install_requires=[],
    entry_points='''
            [console_scripts]
            duedesk=duedesk.duedesk:main
        ''',
    package_dir={"": "src"},
    package_data={"": []},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",
    license_files=('LICENSE',),
)