from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='kri_libs',
    version='0.0.1',
    author='Rimba Prayoga',
    author_email='rimba47prayoga@gmail.com',
    description='Utility for KRI',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/doyanrebahan/kri_libs',
    project_urls={
        "Bug Tracker": "https://github.com/doyanrebahan/kri_libs/issues"
    },
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'Django >= 2.2',
        "djangorestframework",
        "simplejson"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
