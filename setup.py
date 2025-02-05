"""Package metadata for tutor-contrib-aspects."""

import io
import os
import re

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


class MultipleConstraintException(BaseException):
    """
    Exception raised when multiple constraints are provided.
    """


def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Requirements will include any constraints from files specified
    with -c in the requirements files.
    Returns a list of requirement strings.
    """
    # Removed the automated comment that was because it fails linting
    # similarly had to update other code below for lint fails.

    # e.g. {"django": "Django", "confluent-kafka": "confluent_kafka[avro]"}
    by_canonical_name = {}

    def check_name_consistent(package):
        """
        Raise exception if package is named different ways.

        This ensures that packages are named consistently so we can match
        constraints to packages. It also ensures that if we require a package
        with extras we don't constrain it without mentioning the extras (since
        that too would interfere with matching constraints.)
        """
        canonical = package.lower().replace("_", "-").split("[")[0]
        seen_spelling = by_canonical_name.get(canonical)
        if seen_spelling is None:
            by_canonical_name[canonical] = package
        elif seen_spelling != package:
            raise Exception(  # pylint: disable=broad-exception-raised
                f'Encountered both "{seen_spelling}" and "{package}" in requirements '
                "and constraints files; please use just one or the other."
            )

    requirements = {}
    constraint_files = set()

    # groups "pkg<=x.y.z,..." into ("pkg", "<=x.y.z,...")
    re_package_name_base_chars = r"a-zA-Z0-9\-_."  # chars allowed in base package name
    # Two groups: name[maybe,extras], and optionally a constraint
    requirement_line_regex = re.compile(
        r"([%s]+(?:\[[%s,\s]+\])?)([<>=][^#\s]+)?"  # pylint: disable=consider-using-f-string
        % (re_package_name_base_chars, re_package_name_base_chars)
    )

    def add_version_constraint_or_raise(
        current_line, current_requirements, add_if_not_present
    ):
        regex_match = requirement_line_regex.match(current_line)
        if regex_match:
            package = regex_match.group(1)
            version_constraints = regex_match.group(2)
            check_name_consistent(package)
            existing_version_constraints = current_requirements.get(package, None)
            # It's fine to add constraints to an unconstrained package,
            # but raise an error if there are already constraints in place.
            if (
                existing_version_constraints
                and existing_version_constraints != version_constraints
            ):
                raise MultipleConstraintException(
                    f"Multiple constraint definitions found for {package}:"
                    f' "{existing_version_constraints}" and "{version_constraints}".'
                    f"Combine constraints into one location with {package}"
                    f"{existing_version_constraints},{version_constraints}."
                )
            if add_if_not_present or package in current_requirements:
                current_requirements[package] = version_constraints

    # Read requirements from .in files and store the path to any
    # constraint files that are pulled in.
    for path in requirements_paths:
        with open(path, encoding="utf8") as reqs:
            for line in reqs:
                if is_requirement(line):
                    add_version_constraint_or_raise(line, requirements, True)
                if line and line.startswith("-c") and not line.startswith("-c http"):
                    constraint_files.add(
                        os.path.dirname(path)
                        + "/"
                        + line.split("#")[0].replace("-c", "").strip()
                    )

    # process constraint files: add constraints to existing requirements
    for constraint_file in constraint_files:
        with open(constraint_file, encoding="utf8") as reader:
            for line in reader:
                if is_requirement(line):
                    add_version_constraint_or_raise(line, requirements, False)

    # process back into list of pkg><=constraints strings
    constrained_requirements = [
        f'{pkg}{version or ""}' for (pkg, version) in sorted(requirements.items())
    ]
    return constrained_requirements


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    Returns:
        bool: True if the line is not blank, a comment,
        a URL, or an included file
    """
    # Removed the automated comment that was because it fails linting
    # similarly had to update other code below for lint fails.

    return (
        line and line.strip() and not line.startswith(("-r", "#", "-e", "git+", "-c"))
    )


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
    url="https://github.com/openedx/tutor-contrib-aspects",
    project_urls={
        "Code": "https://github.com/openedx/tutor-contrib-aspects",
        "Issue tracker": "https://github.com/openedx/tutor-contrib-aspects/issues",
    },
    license="Apache 2.0",
    author="The Open edX Community",
    description="Aspects plugin for Tutor",
    long_description_content_type="text/x-rst",
    long_description=load_readme(),
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=load_requirements("requirements/base.in"),
    entry_points={"tutor.plugin.v1": ["aspects = tutoraspects.plugin"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
