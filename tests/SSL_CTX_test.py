import tempfile

import pytest

from nassl import _nassl, _nassl_legacy
from nassl.ssl_client import OpenSslVersionEnum, OpenSslVerifyEnum, OpenSslFileTypeEnum


@pytest.mark.parametrize("nassl_module", [_nassl, _nassl_legacy])
class TestCommonSSL_CTX:
    def test_new(self, nassl_module):
        assert nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)

    def test_new_bad(self, nassl_module):
        # Invalid protocol constant
        with pytest.raises(ValueError):
            nassl_module.SSL_CTX(1234)

    def test_set_verify(self, nassl_module):
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        test_ssl_ctx.set_verify(OpenSslVerifyEnum.PEER.value)

    def test_set_verify_bad(self, nassl_module):
        # Invalid verify constant
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        with pytest.raises(ValueError):
            test_ssl_ctx.set_verify(1235)

    def test_load_verify_locations(self, nassl_module):
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        test_file = tempfile.NamedTemporaryFile(delete=False, mode="wt")
        test_file.write(
            """-----BEGIN CERTIFICATE-----
MIIDIDCCAomgAwIBAgIENd70zzANBgkqhkiG9w0BAQUFADBOMQswCQYDVQQGEwJV
UzEQMA4GA1UEChMHRXF1aWZheDEtMCsGA1UECxMkRXF1aWZheCBTZWN1cmUgQ2Vy
dGlmaWNhdGUgQXV0aG9yaXR5MB4XDTk4MDgyMjE2NDE1MVoXDTE4MDgyMjE2NDE1
MVowTjELMAkGA1UEBhMCVVMxEDAOBgNVBAoTB0VxdWlmYXgxLTArBgNVBAsTJEVx
dWlmYXggU2VjdXJlIENlcnRpZmljYXRlIEF1dGhvcml0eTCBnzANBgkqhkiG9w0B
AQEFAAOBjQAwgYkCgYEAwV2xWGcIYu6gmi0fCG2RFGiYCh7+2gRvE4RiIcPRfM6f
BeC4AfBONOziipUEZKzxa1NfBbPLZ4C/QgKO/t0BCezhABRP/PvwDN1Dulsr4R+A
cJkVV5MW8Q+XarfCaCMczE1ZMKxRHjuvK9buY0V7xdlfUNLjUA86iOe/FP3gx7kC
AwEAAaOCAQkwggEFMHAGA1UdHwRpMGcwZaBjoGGkXzBdMQswCQYDVQQGEwJVUzEQ
MA4GA1UEChMHRXF1aWZheDEtMCsGA1UECxMkRXF1aWZheCBTZWN1cmUgQ2VydGlm
aWNhdGUgQXV0aG9yaXR5MQ0wCwYDVQQDEwRDUkwxMBoGA1UdEAQTMBGBDzIwMTgw
ODIyMTY0MTUxWjALBgNVHQ8EBAMCAQYwHwYDVR0jBBgwFoAUSOZo+SvSspXXR9gj
IBBPM5iQn9QwHQYDVR0OBBYEFEjmaPkr0rKV10fYIyAQTzOYkJ/UMAwGA1UdEwQF
MAMBAf8wGgYJKoZIhvZ9B0EABA0wCxsFVjMuMGMDAgbAMA0GCSqGSIb3DQEBBQUA
A4GBAFjOKer89961zgK5F7WF0bnj4JXMJTENAKaSbn+2kmOeUJXRmm/kEd5jhW6Y
7qj/WsjTVbJmcVfewCHrPSqnI0kBBIZCe/zuf6IWUrVnZ9NA2zsmWLIodz2uFHdh
1voqZiegDfqnc1zqcPGUIWVEX/r87yloqaKHee9570+sB3c4
-----END CERTIFICATE-----"""
        )
        test_file.close()
        test_ssl_ctx.load_verify_locations(test_file.name)

    def test_load_verify_locations_bad(self, nassl_module):
        # Certificate file doesn't exist
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        with pytest.raises(_nassl.OpenSSLError):
            test_ssl_ctx.load_verify_locations("tests")

    def test_set_private_key_password_null_byte(self, nassl_module):
        # NULL byte embedded in the password
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        # It raises a TypeError on Python 2.7 and 3.4, and a ValueError on 3.5
        with pytest.raises(Exception, match=" null"):
            test_ssl_ctx.set_private_key_password("AAA\x00AAAA")

    def test_use_certificate_file(self, nassl_module):
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        test_file = tempfile.NamedTemporaryFile(delete=False, mode="wt")
        test_file.write(
            """-----BEGIN CERTIFICATE-----
MIIDCjCCAnOgAwIBAgIBAjANBgkqhkiG9w0BAQUFADCBgDELMAkGA1UEBhMCRlIx
DjAMBgNVBAgMBVBhcmlzMQ4wDAYDVQQHDAVQYXJpczEWMBQGA1UECgwNRGFzdGFy
ZGx5IEluYzEMMAoGA1UECwwDMTIzMQ8wDQYDVQQDDAZBbCBCYW4xGjAYBgkqhkiG
9w0BCQEWC2xvbEBsb2wuY29tMB4XDTEzMDEyNzAwMDM1OFoXDTE0MDEyNzAwMDM1
OFowgZcxCzAJBgNVBAYTAkZSMQwwCgYDVQQIDAMxMjMxDTALBgNVBAcMBFRlc3Qx
IjAgBgNVBAoMGUludHJvc3B5IFRlc3QgQ2xpZW50IENlcnQxCzAJBgNVBAsMAjEy
MRUwEwYDVQQDDAxBbGJhbiBEaXF1ZXQxIzAhBgkqhkiG9w0BCQEWFG5hYmxhLWMw
ZDNAZ21haWwuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlnvP1ltVO
8JDNT3AA99QqtiqCi/7BeEcFDm2al46mv7looz6CmB84osrusNVFsS5ICLbrCmeo
w5sxW7VVveGueBQyWynngl2PmmufA5Mhwq0ZY8CvwV+O7m0hEXxzwbyGa23ai16O
zIiaNlBAb0mC2vwJbsc3MTMovE6dHUgmzQIDAQABo3sweTAJBgNVHRMEAjAAMCwG
CWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAdBgNV
HQ4EFgQUYR45okpFsqTYB1wlQQblLH9cRdgwHwYDVR0jBBgwFoAUP0X2HQlaca7D
NBzVbsjsdhzOqUQwDQYJKoZIhvcNAQEFBQADgYEAWEOxpRjvKvTurDXK/sEUw2KY
gmbbGP3tF+fQ/6JS1VdCdtLxxJAHHTW62ugVTlmJZtpsEGlg49BXAEMblLY/K7nm
dWN8oZL+754GaBlJ+wK6/Nz4YcuByJAnN8OeTY4Acxjhks8PrAbZgcf0FdpJaAlk
Pd2eQ9+DkopOz3UGU7c=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDCjCCAnOgAwIBAgIBAjANBgkqhkiG9w0BAQUFADCBgDELMAkGA1UEBhMCRlIx
DjAMBgNVBAgMBVBhcmlzMQ4wDAYDVQQHDAVQYXJpczEWMBQGA1UECgwNRGFzdGFy
ZGx5IEluYzEMMAoGA1UECwwDMTIzMQ8wDQYDVQQDDAZBbCBCYW4xGjAYBgkqhkiG
9w0BCQEWC2xvbEBsb2wuY29tMB4XDTEzMDEyNzAwMDM1OFoXDTE0MDEyNzAwMDM1
OFowgZcxCzAJBgNVBAYTAkZSMQwwCgYDVQQIDAMxMjMxDTALBgNVBAcMBFRlc3Qx
IjAgBgNVBAoMGUludHJvc3B5IFRlc3QgQ2xpZW50IENlcnQxCzAJBgNVBAsMAjEy
MRUwEwYDVQQDDAxBbGJhbiBEaXF1ZXQxIzAhBgkqhkiG9w0BCQEWFG5hYmxhLWMw
ZDNAZ21haWwuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlnvP1ltVO
8JDNT3AA99QqtiqCi/7BeEcFDm2al46mv7looz6CmB84osrusNVFsS5ICLbrCmeo
w5sxW7VVveGueBQyWynngl2PmmufA5Mhwq0ZY8CvwV+O7m0hEXxzwbyGa23ai16O
zIiaNlBAb0mC2vwJbsc3MTMovE6dHUgmzQIDAQABo3sweTAJBgNVHRMEAjAAMCwG
CWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAdBgNV
HQ4EFgQUYR45okpFsqTYB1wlQQblLH9cRdgwHwYDVR0jBBgwFoAUP0X2HQlaca7D
NBzVbsjsdhzOqUQwDQYJKoZIhvcNAQEFBQADgYEAWEOxpRjvKvTurDXK/sEUw2KY
gmbbGP3tF+fQ/6JS1VdCdtLxxJAHHTW62ugVTlmJZtpsEGlg49BXAEMblLY/K7nm
dWN8oZL+754GaBlJ+wK6/Nz4YcuByJAnN8OeTY4Acxjhks8PrAbZgcf0FdpJaAlk
Pd2eQ9+DkopOz3UGU7c=
-----END CERTIFICATE-----"""
        )
        test_file.close()
        test_ssl_ctx.use_certificate_chain_file(test_file.name)

    def test_use_certificate_file_bad(self, nassl_module):
        # Bad filename
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        with pytest.raises(_nassl.OpenSSLError, match="system lib"):
            test_ssl_ctx.use_certificate_chain_file("invalidPath")

    def test_use_PrivateKey_file(self, nassl_module):
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        test_file = tempfile.NamedTemporaryFile(delete=False, mode="wt")
        test_file.write(
            """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAOWe8/WW1U7wkM1P
cAD31Cq2KoKL/sF4RwUObZqXjqa/uWijPoKYHziiyu6w1UWxLkgItusKZ6jDmzFb
tVW94a54FDJbKeeCXY+aa58DkyHCrRljwK/BX47ubSERfHPBvIZrbdqLXo7MiJo2
UEBvSYLa/AluxzcxMyi8Tp0dSCbNAgMBAAECgYAl0ZpItsEHMWQIDK9b2XWeW0aB
HeGlp9O6p3ex4IhkOmulKk3fYIKz50wZKBLYWahPwO+vopUUHLNw27PwHUgQDmOY
QKAZowO3X5RT5URNzeiI2KTE431uNFqeMR9+XrnjQIZPDDaltACTTZpFp1rFqM+C
/WbZ2VHS/52Vrrj7wQJBAPW64ts+UHNQn1Y+CyYQGVERICdPwC4nSu/+MYpvo0r+
XX1bali8kTdBs2ByoWQOaFr3B4qffd4vb8lIMxt6f3kCQQDvN7ZUsyM/HcSw/4go
pGakZx1OJKBCet6uNA6ymglhDzmFoiAR3QAIxYTVQlc87m0v4ExjVC/nlbdNa4MX
m2j1AkAHgagAbozimOnlJowMo51CXrWOvd7vCgA+CJPW2MYyOkb811gOUeRVvcoO
/jFz7wS9EqLGV0zvBp/xlCULh9hxAkEA2x+tZOiy4J3kDj4D+zaczvulXG8wXbUv
RWNqEzAGZ2IKzt4zgiluXpqPksmyH55HZhOP5Wy4dOovfjt9WaKCAQJAEzgPLx+6
iuiRanrS8dy8Q5UXavmPgBeHXZ4gxWbXD3vC5Qzorgp+P04GhofSCFklXokTPrKN
jsXbhxAIkrdmpg==
-----END PRIVATE KEY-----"""
        )
        test_file.close()
        test_ssl_ctx.use_PrivateKey_file(test_file.name, OpenSslFileTypeEnum.PEM.value)

    def test_use_PrivateKey_file_bad(self, nassl_module):
        # Bad filename
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        with pytest.raises(_nassl.OpenSSLError, match="No such file"):
            test_ssl_ctx.use_PrivateKey_file("invalidPath", OpenSslFileTypeEnum.PEM.value)

    def test_check_private_key(self, nassl_module):
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        test_file = tempfile.NamedTemporaryFile(delete=False, mode="wt")
        test_file.write(
            """-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAOWe8/WW1U7wkM1P
cAD31Cq2KoKL/sF4RwUObZqXjqa/uWijPoKYHziiyu6w1UWxLkgItusKZ6jDmzFb
tVW94a54FDJbKeeCXY+aa58DkyHCrRljwK/BX47ubSERfHPBvIZrbdqLXo7MiJo2
UEBvSYLa/AluxzcxMyi8Tp0dSCbNAgMBAAECgYAl0ZpItsEHMWQIDK9b2XWeW0aB
HeGlp9O6p3ex4IhkOmulKk3fYIKz50wZKBLYWahPwO+vopUUHLNw27PwHUgQDmOY
QKAZowO3X5RT5URNzeiI2KTE431uNFqeMR9+XrnjQIZPDDaltACTTZpFp1rFqM+C
/WbZ2VHS/52Vrrj7wQJBAPW64ts+UHNQn1Y+CyYQGVERICdPwC4nSu/+MYpvo0r+
XX1bali8kTdBs2ByoWQOaFr3B4qffd4vb8lIMxt6f3kCQQDvN7ZUsyM/HcSw/4go
pGakZx1OJKBCet6uNA6ymglhDzmFoiAR3QAIxYTVQlc87m0v4ExjVC/nlbdNa4MX
m2j1AkAHgagAbozimOnlJowMo51CXrWOvd7vCgA+CJPW2MYyOkb811gOUeRVvcoO
/jFz7wS9EqLGV0zvBp/xlCULh9hxAkEA2x+tZOiy4J3kDj4D+zaczvulXG8wXbUv
RWNqEzAGZ2IKzt4zgiluXpqPksmyH55HZhOP5Wy4dOovfjt9WaKCAQJAEzgPLx+6
iuiRanrS8dy8Q5UXavmPgBeHXZ4gxWbXD3vC5Qzorgp+P04GhofSCFklXokTPrKN
jsXbhxAIkrdmpg==
-----END PRIVATE KEY-----"""
        )
        test_file.close()
        test_file2 = tempfile.NamedTemporaryFile(delete=False, mode="wt")
        test_file2.write(
            """-----BEGIN CERTIFICATE-----
MIIDCjCCAnOgAwIBAgIBAjANBgkqhkiG9w0BAQUFADCBgDELMAkGA1UEBhMCRlIx
DjAMBgNVBAgMBVBhcmlzMQ4wDAYDVQQHDAVQYXJpczEWMBQGA1UECgwNRGFzdGFy
ZGx5IEluYzEMMAoGA1UECwwDMTIzMQ8wDQYDVQQDDAZBbCBCYW4xGjAYBgkqhkiG
9w0BCQEWC2xvbEBsb2wuY29tMB4XDTEzMDEyNzAwMDM1OFoXDTE0MDEyNzAwMDM1
OFowgZcxCzAJBgNVBAYTAkZSMQwwCgYDVQQIDAMxMjMxDTALBgNVBAcMBFRlc3Qx
IjAgBgNVBAoMGUludHJvc3B5IFRlc3QgQ2xpZW50IENlcnQxCzAJBgNVBAsMAjEy
MRUwEwYDVQQDDAxBbGJhbiBEaXF1ZXQxIzAhBgkqhkiG9w0BCQEWFG5hYmxhLWMw
ZDNAZ21haWwuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlnvP1ltVO
8JDNT3AA99QqtiqCi/7BeEcFDm2al46mv7looz6CmB84osrusNVFsS5ICLbrCmeo
w5sxW7VVveGueBQyWynngl2PmmufA5Mhwq0ZY8CvwV+O7m0hEXxzwbyGa23ai16O
zIiaNlBAb0mC2vwJbsc3MTMovE6dHUgmzQIDAQABo3sweTAJBgNVHRMEAjAAMCwG
CWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAdBgNV
HQ4EFgQUYR45okpFsqTYB1wlQQblLH9cRdgwHwYDVR0jBBgwFoAUP0X2HQlaca7D
NBzVbsjsdhzOqUQwDQYJKoZIhvcNAQEFBQADgYEAWEOxpRjvKvTurDXK/sEUw2KY
gmbbGP3tF+fQ/6JS1VdCdtLxxJAHHTW62ugVTlmJZtpsEGlg49BXAEMblLY/K7nm
dWN8oZL+754GaBlJ+wK6/Nz4YcuByJAnN8OeTY4Acxjhks8PrAbZgcf0FdpJaAlk
Pd2eQ9+DkopOz3UGU7c=
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIDCjCCAnOgAwIBAgIBAjANBgkqhkiG9w0BAQUFADCBgDELMAkGA1UEBhMCRlIx
DjAMBgNVBAgMBVBhcmlzMQ4wDAYDVQQHDAVQYXJpczEWMBQGA1UECgwNRGFzdGFy
ZGx5IEluYzEMMAoGA1UECwwDMTIzMQ8wDQYDVQQDDAZBbCBCYW4xGjAYBgkqhkiG
9w0BCQEWC2xvbEBsb2wuY29tMB4XDTEzMDEyNzAwMDM1OFoXDTE0MDEyNzAwMDM1
OFowgZcxCzAJBgNVBAYTAkZSMQwwCgYDVQQIDAMxMjMxDTALBgNVBAcMBFRlc3Qx
IjAgBgNVBAoMGUludHJvc3B5IFRlc3QgQ2xpZW50IENlcnQxCzAJBgNVBAsMAjEy
MRUwEwYDVQQDDAxBbGJhbiBEaXF1ZXQxIzAhBgkqhkiG9w0BCQEWFG5hYmxhLWMw
ZDNAZ21haWwuY29tMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDlnvP1ltVO
8JDNT3AA99QqtiqCi/7BeEcFDm2al46mv7looz6CmB84osrusNVFsS5ICLbrCmeo
w5sxW7VVveGueBQyWynngl2PmmufA5Mhwq0ZY8CvwV+O7m0hEXxzwbyGa23ai16O
zIiaNlBAb0mC2vwJbsc3MTMovE6dHUgmzQIDAQABo3sweTAJBgNVHRMEAjAAMCwG
CWCGSAGG+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAdBgNV
HQ4EFgQUYR45okpFsqTYB1wlQQblLH9cRdgwHwYDVR0jBBgwFoAUP0X2HQlaca7D
NBzVbsjsdhzOqUQwDQYJKoZIhvcNAQEFBQADgYEAWEOxpRjvKvTurDXK/sEUw2KY
gmbbGP3tF+fQ/6JS1VdCdtLxxJAHHTW62ugVTlmJZtpsEGlg49BXAEMblLY/K7nm
dWN8oZL+754GaBlJ+wK6/Nz4YcuByJAnN8OeTY4Acxjhks8PrAbZgcf0FdpJaAlk
Pd2eQ9+DkopOz3UGU7c=
-----END CERTIFICATE-----"""
        )
        test_file2.close()
        test_ssl_ctx.use_certificate_chain_file(test_file2.name)
        test_ssl_ctx.use_PrivateKey_file(test_file.name, OpenSslFileTypeEnum.PEM.value)
        test_ssl_ctx.check_private_key()

    def test_check_private_key_bad(self, nassl_module):
        test_ssl_ctx = nassl_module.SSL_CTX(OpenSslVersionEnum.SSLV23.value)
        with pytest.raises(_nassl.OpenSSLError, match="no certificate assigned"):
            test_ssl_ctx.check_private_key()

    # TODO: add get_ca_list tests


class TestModernSSL_CTX:
    def test_tlsv1_3(self):
        ssl_ctx = _nassl.SSL_CTX(OpenSslVersionEnum.TLSV1_3)
        assert ssl_ctx
