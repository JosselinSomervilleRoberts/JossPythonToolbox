import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='toolbox',
    version='0.4.2',
    author='Josselin Somerville Roberts',
    author_email='josselin.somerville@gmail.com',
    description='Usefull functions for my personnal use',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/JosselinSomervilleRoberts/JossPythonToolbox.git',
    project_urls = {
        "Bug Tracker": "https://github.com/JosselinSomervilleRoberts/JossPythonToolbox/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=['requests',
                      'boto3',
                      'configparser',
                      'dowel',
                      'wandb'],
)
