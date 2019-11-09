from setuptools import setup

setup(
    name='flaskr',
    packages=['flaskr'],
    include_package_data=True,
    install_requires=[
        'flask', 'yagmail', 'keyring', 'itsdangerous', 'wtforms', 'werkzeug', 'googleapiclient', 'google'
    ],
)