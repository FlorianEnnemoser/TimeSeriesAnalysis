from setuptools import setup,find_packages

setup(
    name='PlotTimeSeries',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license = "MIT",
    install_requires=[
        'click',
        'numpy',
        'pandas',
        'matplotlib',
        'xarray',
        'netcdf4',
        
    ],
    scripts=['scripts/io_TSA.py',
             'scripts/preprocessing.py',
             'scripts/calculation.py',
             'scripts/postprocessing.py',
             'scripts/plotting.py'],
    entry_points={
        'console_scripts': [
            'plt_tsa = scripts.cli:tsa',
        ],
    },
)