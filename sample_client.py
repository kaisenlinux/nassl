from pathlib import Path

from nassl.ocsp_response import verify_ocsp_response
from nassl.ssl_client import OpenSslVersionEnum, SslClient, OpenSslVerifyEnum
import socket

mozilla_store = Path("tests") / "mozilla.pem"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)

hostname = "www.cloudflare.com"
sock.connect((hostname, 443))

ssl_client = SslClient(
    ssl_version=OpenSslVersionEnum.TLSV1_2,
    underlying_socket=sock,
    ssl_verify=OpenSslVerifyEnum.PEER,
    ssl_verify_locations=mozilla_store,
)
ssl_client.set_tlsext_status_ocsp()
ssl_client.do_handshake()

print("Received certificate chain")
for pem_cert in ssl_client.get_received_chain():
    print(pem_cert)

print("Verified certificate chain")
for pem_cert in ssl_client.get_verified_chain():
    print(pem_cert)

ocsp_resp = ssl_client.get_tlsext_status_ocsp_resp()
if ocsp_resp:
    print("OCSP Stapling")
    verify_ocsp_response(ocsp_resp, Path(mozilla_store))

print("\nCipher suite")
print(ssl_client.get_current_cipher_name())

print("\nEphemeral Key")
print(ssl_client.get_ephemeral_key())

print("\nHTTP response")
ssl_client.write(f"GET / HTTP/1.0\r\nUser-Agent: Test\r\nHost: {hostname}\r\n\r\n".encode("ascii"))
print(ssl_client.read(2048))
