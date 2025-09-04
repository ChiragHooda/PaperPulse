from setuptools import find_packages, setup
from typing import List

__HYPHEN = '-e .'

def get_requirements(file_path:str) -> List[str]:
    """
    This function will read the requirements.txt file and return the list of requirements.

    Args:
        file_path (str): Input file path

    Returns:
        List[str]: List of requirements
    """

    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace('\n', '') for req in requirements]

        if __HYPHEN in requirements:
            requirements.remove(__HYPHEN)

    return requirements

setup(
    name='SkimLit',
    version='0.0.1',
    author='Aditya Paul',
    author_email='adityapaul.official@outlook.com',
    packages = find_packages(),
    install_requires=get_requirements('requirements.txt'),
)