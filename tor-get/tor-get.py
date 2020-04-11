#!/usr/bin/env python3
import argparse
import logging
import unicodedata
import re
import os
import datetime

import requests
import requests.adapters

__version__ = '1.0.0'


class FixedTimeoutAdapter(requests.adapters.HTTPAdapter):
    def send(self, *pargs, **kwargs):
        if kwargs['timeout'] is None:
            kwargs['timeout'] = 5
        return super(FixedTimeoutAdapter, self).send(*pargs, **kwargs)


class TorGetException(Exception):
    pass


class TorGetClient:
    AUTO_CLEAR_COOKIES = True

    def __init__(self, user_agent: str, socks_proxy_address: str = 'socks4a://127.0.0.1:9050'):
        self.session = requests.session()
        self.session.mount('https://', FixedTimeoutAdapter())
        self.session.mount('http://', FixedTimeoutAdapter())
        self.session.headers = {'User-Agent': user_agent}
        self.session.proxies['http'] = socks_proxy_address
        self.session.proxies['https'] = socks_proxy_address

    def get(self, url: str, expect_200: bool = True):
        if self.AUTO_CLEAR_COOKIES:
            self.clear_cookies()
        response = self.session.get(url)
        if expect_200 and response.status_code != 200:
            raise TorGetException(F'Non 200-Status-Code: {response.status_code}')

        return response.content

    def clear_cookies(self):
        self.session.cookies.clear()


class ConsoleHandler(logging.Handler):
    def emit(self, record):
        print('[%s] %s' % (record.levelname, record.msg))


def generate_name_from_url(url: str):
    value = url
    for underscore_needle in ['://', '.', '/']:
        value = value.replace(underscore_needle, '_')
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub(rb'[^\w\s-]', b'', value).strip().lower()
    value = re.sub(rb'[-\s]+', b'-', value)

    return value.decode('utf-8')


if __name__ == '__main__':
    import platform

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--overwrite-files', action='store_true')
    parser.add_argument('--spider', action='store_true', help='Tries to download everything')
    parser.add_argument('--target-directory', default='.')
    parser.add_argument('url', help='URL to download')
    parser.add_argument(
        '--user-agent',
        default=F'TorGet/{__version__} (python-requests {requests.__version__}) '
                F'{platform.system()} ({platform.release()})'
    )
    args = parser.parse_args()

    logger = logging.getLogger('TorGet')
    logger.handlers.append(ConsoleHandler())
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    logger.debug(F'Using User-Agent string: {args.user_agent}')
    client = TorGetClient(args.user_agent)
    try:
        logger.debug(F'Downloading "{args.url}"...')
        try:
            content = client.get(args.url)
            file_name = F'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}_{generate_name_from_url(args.url)}'
            logger.debug(F'Writing to "{file_name}"...')
            if not os.path.exists(file_name) or args.overwrite_files:
                with open(file_name, 'wb') as fp:
                    fp.write(content)
        except requests.exceptions.ConnectionError:
            logger.error(F'Cannot download "{args.url}".')

    except TorGetException as e:
        logger.exception(e)
