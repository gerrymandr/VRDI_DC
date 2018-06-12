from setuptools import setup
import versioneer

requirements = [
    # package requirements go here
]

setup(
    name='DiscreteCompactness',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Discrete compactness measures of districting plans",
    author="MGGG VRDI",
    author_email='gerrymandr@gmail.com',
    url='https://github.com/gerrymandr/DiscreteCompactness',
    packages=['discretecompactness'],
    entry_points={
        'console_scripts': [
            'discretecompactness=discretecompactness.cli:cli'
        ]
    },
    install_requires=requirements,
    keywords='DiscreteCompactness',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
    ]
)
