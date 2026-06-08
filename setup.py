from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="interior_erp",
    version="0.0.1",
    description="Custom ERP system for an Interior Design company",
    author="Telepathy",
    author_email="test@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
