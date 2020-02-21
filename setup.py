import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xbrl_report_parser",
    version="0.0.4",
    author="Kristian Nymann Jakobsen",
    author_email="kristian@nymann.dev",
    description="Extract financial reports data from XBRL files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dkfinance/xbrl-parser",
    packages=setuptools.find_packages(),
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
    ],
    entry_points={
        'console_scripts': [
            'parse_xbrl=xbrl_parser.console_scripts.__main__:main',
        ]
    },
    install_requires=["pprint"],
    extras_require={
        'lint': [
            "pylint",
            "coverage"
        ]
    }
)
