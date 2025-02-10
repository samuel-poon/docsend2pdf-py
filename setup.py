from setuptools import setup

setup(
    name='docsend2pdf',
    description='Python wrapper for DocSend2PDF',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/samuel-poon/docsend2pdf-py',
    version='0.0.2',
    python_requires='>=3.8',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    packages=['docsend2pdf']
)