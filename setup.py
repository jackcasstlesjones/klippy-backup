from setuptools import setup, find_packages

setup(
    name="klippy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "klippy=klippy:main",
        ],
    },
    python_requires=">=3.6",
    description="Kindle clippings to Markdown converter for Obsidian",
    author="Your Name",
    author_email="your.email@example.com",
)
