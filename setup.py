from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", encoding="utf-8") as fh:
    install_requires = fh.read()

setup(
    name="typecutter",
    version="0.1.0",
    description="Cut typesets using Vapoursynth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="subs.in.tokyo@gmail.com",
    url="https://github.com/cN3rd/typecutter",
    install_requires=install_requires,
    python_requires=">=3.9",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": ["typecutter=typecutter.app:main"],
    },
)
