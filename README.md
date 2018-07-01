# ScreamingMantis
## Instructions
To use the program, the following dependencies exist:
* `python3` an interpreter/compiler for python code, use package manager to install
* `pip` a package manager for python library modules, required for API interfacing
* `python-binance`, `python-kucoin`, `bitfinex`, `btcmarkets` use `pip install <name>`

Note: to verify the installation of the modules and find their implementation,
use `pip show -f <name>`

## Content
Interacts with cryptocurrency exchange APIs and fetches dynamic price information for various comparisons

## Files
### screamingMantis.py
The interface for accessing modules of `clientProbe.py`. This program is the one to be run with `python3`
### clientProbe.py
Contains the functions for fetching and comparing dynamic prices between various exchanges.
### logs/2000-07-07.txt
Tracks the output of repeated price comparison between BTCMarkets and Bitfinex over time, with escape sequences for visual price comoparison
### readLog
Bash script for viewing escaped log files, used with `./readLog logs/2000-07-07.txt`
### keys.py
Contains various API keys as attributes and is provided as a skeleton since API keys should never be shared

## Screenshots
![1](/images/1.jpg)

