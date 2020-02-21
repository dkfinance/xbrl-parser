# xbrl-parser

![Discord](https://img.shields.io/discord/679223715652698135?style=for-the-badge)

Parses XBRL files (DEI, GAAP, IFRS).

## Install
`git clone https://github.com/dkfinance/xbrl-parser.git`

`cd xbrl-parser`

`pip install -e .`

## Usage 
```                       
usage: parse_xbrl [-h] [-s XBRL_STANDARD] files [files ...]

positional arguments:
  files                 One or XLBR files to be parsed.

optional arguments:
  -h, --help            show this help message and exit
  -s XBRL_STANDARD, --xbrl-standard XBRL_STANDARD
                        Which standard do you want to parse? available options: 'IFRS', 'DEI', 'GAAP'.
```

## Examples
```
parse_xbrl -s IFRS examples/vestas_2018.xml > vestas_2018.json
```
