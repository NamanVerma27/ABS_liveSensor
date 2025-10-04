from setuptools import find_packages , setup
from typing import List

def get_requirements() -> list[str]:
    requirements_list: list[str] = [] # Correct in-function variable annotation
    return requirements_list

setup(
    name="sensor",
    version="0.1.0",
    author="Naman",
    author_email="namanv417@gmail.com",
    packages = find_packages(),

    install_requires = get_requirements() 
)