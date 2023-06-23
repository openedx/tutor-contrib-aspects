"""Package metadata for tutor-contrib-aspects."""
import io
import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    """Load README file which populates long_description field."""
    with io.open(os.path.join(HERE, "README.rst"), "rt", encoding="utf8") as file:
        return file.read()


def load_about():
    """Load about file which stores the package version."""
    about = {}
    with io.open(
        os.path.join(HERE, "tutoraspects", "__about__.py"),
        "rt",
        encoding="utf-8",
    ) as file:
        exec(file.read(), about)  # pylint: disable=exec-used
    return about


ABOUT = load_about()


setup(
    name="tutor-contrib-aspects",
    version=ABOUT["__version__"],
    url="https://github.com/open-craft/tutor-contrib-aspects",
    project_urls={
        "Code": "https://github.com/open-craft/tutor-contrib-aspects",
        "Issue tracker": "https://github.com/open-craft/tutor-contrib-aspects/issues",
    },
    license="AGPLv3",
    author="The Open edX Community",
    description="Aspects plugin for Tutor",
    long_description_content_type="text/x-rst",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=["tutor", "bcrypt"],
    entry_points={"tutor.plugin.v1": ["aspects = tutoraspects.plugin"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
