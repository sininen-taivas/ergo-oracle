import hashlib
import json
import logging
import secrets
import string
from logging.handlers import RotatingFileHandler
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

LOG_FORMAT = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

TARGET_ADDRESS = {
    'mainnet': '4MQyMKvMbnCJG3aJ',
    'testnet': 'Ms7smJmdbakqfwNo',
}

TARGET_SERVER = {
    'mainnet': 'localhost:9053',
    'testnet': 'localhost:9052'
}


def setup_logger(stdout=True, file_name=None, network=False):  # type: () -> logging.Logger
    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG)
    if file_name is not None:
        _handler = RotatingFileHandler(file_name, maxBytes=1024 * 1024, backupCount=3)
        _handler.setFormatter(LOG_FORMAT)
        _logger.addHandler(_handler)
    if stdout:
        _console = logging.StreamHandler()
        _console.setLevel(logging.DEBUG)
        _console.setFormatter(LOG_FORMAT)
        logging.getLogger('').addHandler(_console)
    if not network:
        logging.getLogger('ergo-api').setLevel(logging.CRITICAL)
    return _logger


class ErgoApiException(Exception):

    def __init__(self, error, reason, detail):
        super(ErgoApiException, self).__init__()
        self.detail = detail
        self.reason = reason
        self.error = error

    def __str__(self):
        return 'Ergo API server not responding. Reason: %s' % str(self.reason)


class ErgoClient:
    def __init__(self, server, api_key=None):
        self.server, self.api_key = server, api_key
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        if api_key is not None:
            self.headers['api_key'] = api_key
        self.logger = logging.getLogger('ergo-api')

    def log(self, message, level=logging.DEBUG):
        self.logger.log(level, 'ErgoClient:%s' % message)

    def request(self, path, data=None):  # type: (str) -> (int, dict)
        url = urljoin('http://%s' % self.server, path)
        if data is not None and not isinstance(data, bytes):
            data = bytes(json.dumps(data), encoding='utf-8')
        self.log('request: %s %s' % (url, data))
        req = Request(url=url, headers=self.headers, data=data)
        try:
            res = urlopen(req)  # type: http.client.HTTPResponse
            res_data = json.loads(res.read())
            self.log('response: %s' % str(res_data), level=logging.DEBUG)
            return res_data
        except HTTPError as eres:
            self.log('Ergo API server error: %s' % str(eres), level=logging.DEBUG)
            raise ErgoApiException(**json.loads(eres.read()))
        except URLError as e:
            self.log('Ergo API server not responding. Reason: %s' % str(e.reason), level=logging.ERROR)
            raise


def get_digest(fo):
    sha256 = hashlib.sha256()  # type: _hashlib.HASH
    for buf in iter(lambda: fo.read(4096), b''):
        sha256.update(buf)
    return sha256.hexdigest()


def pwgen(pwlen: int = None) -> string:
    """
    Generate random string with length `pwlen`, default `pwlen = 8`
    """
    if not pwlen:
        pwlen = 8
    alphabet = string.ascii_letters + string.digits
    passwd = []
    while len(passwd) < pwlen:
        passwd.append(secrets.choice(alphabet))
    return ''.join(passwd)
