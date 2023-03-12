from setuptools import setup, find_packages

setup(
    name='websites_info_scraper',
    version='1.0.0',
    packages=find_packages(),
    url='',
    license='',
    author='Thiago Silva',
    author_email='someemail@email.com',
    description='Collect information from an inputted website url',
    setup_requires=['wheel'],
    install_requires=[
        "click>=8.1.2",
        "setuptools>=62.1.0",
        "requests>=2.25.1",
        "bs4>=0.0.1",
        "pandas>=1.4.2",
        "fastparquet>=0.8.1",
        "scrapy>=2.8.0",
        "googlesearch-python>=1.1.0",
    ],
    entry_points={
        'console_scripts': [
            "scrape-url=websites_scraper.main:main",
            "create-parameters=websites_scraper.main:parameter_creation",
        ]
    },
    include_package_data=True

)
