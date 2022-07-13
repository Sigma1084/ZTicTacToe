from setuptools import setup, find_packages

with open("../README.md", "r") as rm_file:
    long_description = rm_file.read()

setup(
    name='ZTTT',
    version='0.0.4',
    license='MIT',

    description='A Tic Tac Toe Library with a near perfect engine',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url="https://github.com/Sigma1084/ZTicTacToe",
    author="Sumanth NR",
    author_email="sumanthnr62@gmail.com",

    packages=find_packages(exclude=["tests", "examples"]),

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
