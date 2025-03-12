from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """
    This function will return the list of requirements
    """
    requirements_lst: List[str] = []
    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                requirements=line.strip()
                requirements_lst.append(requirements)
    except Exception as e:
        print(f"Error in reading requirements.txt: {e}")
    
    return requirements_lst

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="cmatiass",
    packages=find_packages(),
    install_requires=get_requirements()
)

