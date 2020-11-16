import setuptools

setuptools.setup(
    name='rdfgs-mapper',
    version='0.0.1',
    description='Mapping utilities for rdfgs',
    author='Adin Drabkin',
    packages=setuptools.find_packages(),
    install_requires=[
        "shapely",
        "xlrd",
        "geopandas", # required for visualize
        "matplotlib", # required for visualize
        "beautifultable",
        "descartes",  # required for visualize
    ],
    include_package_data=True,
#    package_data={
#        'rdfgs_map_data': ['*', '*/*', '*/*/*'],
#    },
    entry_points={
        'console_scripts': [
            'rdfgs-mapper=rdfgs_mapper.rdfgs_mapper.rdfgs_mapper:run'
        ]
    }
)
