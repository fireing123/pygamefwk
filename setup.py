from setuptools import setup, find_packages

setup(
    name='pygamefwk',
    version='1.0.2',
    description='pygame framework',
    author= 'fireing123',
    author_email= 'gimd82368@gmail.com',
    url='https://github.com/fireing123/pygamefwk',
    install_requires=["pygame"],
    packages=find_packages(),
    keywords=['pygame framework', 'fireing123', 'pygame'],
    long_description=open('README.md', 'r', encoding="UTF8").read(),
    long_description_content_type='text/markdown'
)
