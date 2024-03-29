import pathlib
import os
from setuptools import setup
from subrake.parser import __VERSION__

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="subrake",
    version=__VERSION__,
    zip_safe=False,
    description="A Subdomain Enumeration and Validation tool for Bug Bounty and Pentesters.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hash3liZer/Subrake",
    author="hash3liZer",
    author_email="sheikhshameerkashif@protonmail.com",
    license="GPLv3",
    download_url = 'https://github.com/hash3liZer/Subrake/archive/v3.3.tar.gz',
    keywords=['bugbounty', 'bugbountytips', 'tool', 'subdomain', 'pentesting'],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: POSIX",
    ],
    packages=["subrake", "subrake.handlers", "subrake.modules"],
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        "console_scripts": [
            "subrake=subrake.__main__:main",
        ]
    },
)
