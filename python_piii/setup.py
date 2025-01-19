import setuptools
import pathlib


HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name='TOPSIS-Simranjit-102216033',
    version='0.0.1',
    author='Simranjit Kaur',
    author_email='skaur6_be22@thapar.edu',
    desription='Factorial Calculating Package For Python',
    long_description=README,  # Use the README content
    long_description_content_type="text/markdown",
    packages= setuptools.find_packages(),
    classifiers=['Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent'],


)


