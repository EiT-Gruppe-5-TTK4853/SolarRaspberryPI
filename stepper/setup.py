from setuptools import setup, find_packages


# Function to read the list of requirements from requirements.txt
def load_requirements(filename="requirements.txt"):
    with open(filename, "r") as file:
        return file.read().splitlines()


setup(
    name="stepper",
    version="0.1",
    packages=find_packages(),
    install_requires=load_requirements(),
)
