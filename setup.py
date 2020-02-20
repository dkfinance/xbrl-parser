import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xbrl_report_parser",
    version="0.0.1",
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
            'parse_ifrs=xbrl_parser.console_scripts.__main__:parse_ifrs',
            'parse_gaap=xbrl_parser.console_scripts.__main__:parse_gaap',
            'parse_dei=xbrl_parser.console_scripts.__main__:parse_dei',
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
