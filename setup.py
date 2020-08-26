import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="subrake",
    version="3.3",
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
    packages=["subrake", "subrake.handlers"],
    include_package_data=True,
    install_requires=["requests", "dnspython", "beautifulsoup4"],
    entry_points={
        "console_scripts": [
            "subrake=subrake.__main__:main",
        ]
    },
)
