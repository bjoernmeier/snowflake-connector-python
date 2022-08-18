import logging
import socket
import time
import random

from OpenSSL import SSL

from snowflake.connector.ocsp_asn1crypto import SnowflakeOCSPAsn1Crypto as SFOCSP

hostname = "hinhzm1sfcb1stg.blob.core.windows.net"

ctx = SSL.Context(SSL.SSLv23_METHOD)
s = socket.create_connection((hostname, 443))
s = SSL.Connection(ctx, s)
s.set_connect_state()
s.set_tlsext_host_name(hostname.encode())

s.sendall('HEAD / HTTP/1.0\n\n'.encode())
s.recv(16)

for logger_name in ['snowflake', 'botocore']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    ch = logging.FileHandler(f'/tmp/snowflake_locks.log')
    # ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s'))
    logger.addHandler(ch)


ocsp = SFOCSP(
    ocsp_response_cache_uri="file:///tmp/ocsp_response_cache.json", use_fail_open=True
)
ocsp.validate(hostname, s)

