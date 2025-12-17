from setuptools import setup, find_packages

setup(
    name = "MapleTree",
    version = "2.0.0",
    author = "Ryuji Hazama",
    description="""MapleTree: A Python library for read and write operations on MapleTree data structures.
    Logger: A logging utility""",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages = find_packages(),
    install_requires = [
        "cryptography>=46.0.3",
        "pydantic>=2.12.5"
        ],
    license = "MIT",
    python_requires='>=3.8',
)