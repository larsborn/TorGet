# Tor GET Client
Python-based HTTP downloader that uses the Tor SOCKS proxy. The TorBrowser for example will run such a proxy in the 
background anyway.

## Installation

Requires at least Python 3.7 and the package `requests` to be installed. Fully compatible with being run in a virtual
environment.

## Example Usage
After aliasing the script `tor-get.py` to `tget` a session to retrieve your own IP may look like this:

```Batch
$ tget --debug https://api.ipify.org/
[DEBUG] Using User-Agent string: Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0
[DEBUG] Downloading "https://api.ipify.org/"...
[DEBUG] Writing to "20200411_113512_https_api_ipify_org_"...

$ cat 20200411_113512_https_api_ipify_org_
77.247.181.162
```


[torproject.org]: https://torproject.org/
