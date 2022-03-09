from setuptools import (
    find_packages,
    setup
)

INSTALL_REQUIRES = (
    'requests',
    'cached_property',
    'requests-ip-rotator',
    'bs4',
    'pandas'
)

setup(
    name='daft_property_price_register',
    version='0.0.1',
    python_requires='>=3.5',
    author='Robert Lucey',
    url='https://github.com/RobertLucey/daft-property-price-register',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=INSTALL_REQUIRES,
    package_data={
        'daft_property_price_register': [
            'resources/DAFT.csv.tar.gz',
        ]
    },
    entry_points={
        'console_scripts': [
            'scrape_daft = daft_property_price_register.bin.scrape:main',
            'load_daft = daft_property_price_register.bin.load:main',
        ]
    }
)
