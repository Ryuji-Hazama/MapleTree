from setuptools import setup, find_packages

setup(
    name = "MapleX",
    version = "2.1.0",
    author = "Ryuji Hazama",
    description="""MapleX: A Python library for Maple file format operations, with logging and console color utilities""",
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