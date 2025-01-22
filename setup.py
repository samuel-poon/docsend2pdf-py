from setuptools import setup

setup(
    name='docsend2pdf',
    description='Python wrapper for DocSend2PDF',
    version='0.0.1',
    python_requires='>=3.8',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    packages=['docsend2pdf']
)