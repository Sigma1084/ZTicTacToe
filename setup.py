from setuptools import setup

with open("README.md", "r") as rm_file:
    long_description = rm_file.read()

setup(
    name='ZTTT',
    version='0.0.1',
    license='MIT',
    description='A Tic Tac Toe Library with a near perfect engine',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['ZTTT'],
    package_dir={'': 'src'},

    url="https://github.com/Sigma1084/ZTicTacToe",
    author="Sumanth NR",
    author_email="sumanthnr62@gmail.com",
)
