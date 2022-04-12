from setuptools import setup,find_packages

setup(
    name='create_time_series_ex03',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'numpy',
        'pandas',
        'matplotlib',
        'xarray',
        'netcdf4',
        'datetime'
        
    ],
    scripts=['scripts/io_TSA.py',
             'scripts/preprocessing.py',
             'scripts/calculation.py',
             'scripts/postprocessing.py',
             'scripts/plotting.py'],
    entry_points={
        'console_scripts': [
            'time_series_analysis = scripts.cli:cli',
        ],
    },
)