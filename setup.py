from setuptools import setup, find_packages

install_requires = [
    'Fabric==1.6.0',
    'Flask==0.10.1',
    'Flask-Alembic==0.1',
    'Flask-Gravatar==0.3.0',
    'Flask-Login==0.2.6',
    'Flask-SQLAlchemy==0.16',
    'Flask-Script==0.5.3',
    'Flask-WTF==0.8.3',
    'GitPython==0.3.2.RC1',
    'alembic==0.6.0',
    'psycopg2==2.5',
    'Flask-DebugToolbar',
]

setup(
    name='Aurora',
    version='0.0.3',
    author='Eugene Akentyev',
    author_email='ak3ntev@gmail.com',
    url='https://github.com/ak3n/aurora',
    description='A web interface for Fabric',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    license='MIT',
    entry_points={
        'console_scripts': [
            'aurora = aurora_app.runner:main',
        ],
    },
    dependency_links=['https://github.com/ak3n/flask-alembic/' +
                      'tarball/master#egg=flask-alembic-0.1']
)
