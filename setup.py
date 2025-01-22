from setuptools import setup

setup(
    name='docsend2pdf',
    version='0.0.1',
    python_requires='>=3.8',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    packages=['docsend2pdf']
)