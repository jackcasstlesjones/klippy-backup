from setuptools import setup, find_packages

setup(
    name="klippy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich",
    ],
    entry_points={
        'console_scripts': [
            'klippy=klippy.klippy:main',
        ],
    },
    scripts=['klippy'],  # Add the script to be installed
    description="Kindle clippings to Markdown converter for Obsidian",
    author="Jack",
    author_email="",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
