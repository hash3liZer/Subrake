import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Subrake",
    version="3.1",
    description="A Subdomain Enumeration and Validation tool for Bug Bounty and Pentesters.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hash3liZer/Subrake",
    author="hash3liZer",
    author_email="admin@shellvoide.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GPLv3 License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["subrake"],
    include_package_data=True,
    install_requires=["requests", "dnspython", "beautifulsoup4"],
    entry_points={
        "console_scripts": [
            "subrake=subrake.__main__:main",
        ]
    },
)
