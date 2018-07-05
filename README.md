# ScreamingMantis
## Instructions
To use the program on a linux operating system, the following dependencies must be installed:
* `python3` an interpreter/compiler for python code, use package manager (`apt` for ubuntu) to install
* `pip` a package manager for python library modules, required for API interfacing. Use distro package manager to install (`apt` for ubuntu)
* `python-binance`, `python-kucoin`, `bitfinex`, `btcmarkets` use `pip install --user <name>`

Note: to verify the installation of the modules and find their implementation, use `pip show -f <name>`

## Content
Interacts with cryptocurrency exchange APIs and fetches dynamic price information for various comparisons to be made and judgements on whether profitable arbitrage is possible.

## Agenda 
- [x] add difference between closing prices for binance/kucoin
- [x] add bitfinex & btcmarkets
- [x] implement dynamic information fetching for btcmarkets & bitfinex
- [x] implement file writing and log file management
- [ ] add price comparison with fees
- [ ] add inter-exchange trading
- [ ] add buy and sell order handling

## Files
### screamingMantis.py
The interface for accessing modules of `clientProbe.py`. This program is the one to be run with `python3`
### clientProbe.py
Contains the functions for fetching and comparing dynamic prices between various exchanges.
### logs/2000-07-07.txt
Tracks the output of repeated price comparison between BTCMarkets and Bitfinex over time, with escape sequences for visual price comoparison
### readLog
Bash script for viewing escape sequenced log files, used with `./readLog logs/2000-07-07.txt`
### keys.py
Contains various API keys as attributes and is provided as a skeleton since API keys should never be shared

## Screenshots
![1](/images/1.jpg)

