from setuptools import setup, find_packages

# Read the contents of your requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='HealthGPT_Package',
    version='1.0.0',
    packages=find_packages(),
    install_requires=requirements,  # Pass the list of requirements
    entry_points={
        'console_scripts': [
            'StartHealthGPT = HealthGPT.main:main',
        ],
    },
)
