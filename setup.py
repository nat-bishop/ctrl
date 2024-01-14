from setuptools import setup, find_packages

setup(
    name='FileControl',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Click==8.1.7',
        'Spacy==3.7.2',
        'en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.1/en_core_web_lg-3.7.1-py3-none-any.whl',
        'opencv-python==4.8.1.78',
        'psycopg2==2.9.9'
    ],
    entry_points={
        'console_scripts': [
            'ctrl = ctrl.cli:cli',
        ],
    },
)
