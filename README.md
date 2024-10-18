# azcam-expstatus

*azcam-expstatus* is an *azcam* application which displays exposure status in a GUI window. The GUI is built with Qt using PySide6.

## Installation

```shell
git clone https://github.com/mplesser/azcam-expstatus
pip install -e azcam-expstatus
```

## Usage:

`pythonw -m azcam_expstatus.expstatus -port 2452`

There are two command line options to specify the connection to azcamserver:
- -host *hostname* (default "localhost")
- -port *portnumber* (default 2402)
