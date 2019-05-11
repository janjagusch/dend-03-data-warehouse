from setuptools import find_packages


setup(
    name='dend_03_data_warehouse',
    version='0.1.0',
    description='My solution for the data warehousing project for the \
        Data Engineering Nanodegree at Udacity.',
    url='https://github.com/jbj2505/dend_03_data_warehouse.git',
    author='Jan-Benedikt Jagusch',
    author_email='jan.jagusch@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    python_requires='>3.6, <3.7',
    install_requires=[
        "psycopg2-binary>=2.8",
        "pandas>=0.24",
        "boto3>=1.9",
        "python-dotenv>=0.10",
        "botocore>=1.12",
        "matplotlib>=3.0"
    ],
    zip_safe=False
)
