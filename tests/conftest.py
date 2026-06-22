import ctypes
import ctypes.wintypes

import pytest

from unicommerce import AsyncUnicommerce, Unicommerce


class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ("Flags", ctypes.wintypes.DWORD),
        ("Type", ctypes.wintypes.DWORD),
        ("TargetName", ctypes.c_wchar_p),
        ("Comment", ctypes.c_wchar_p),
        ("LastWritten", ctypes.wintypes.FILETIME),
        ("CredentialBlobSize", ctypes.wintypes.DWORD),
        ("CredentialBlob", ctypes.c_void_p),
        ("Persist", ctypes.wintypes.DWORD),
        ("AttributeCount", ctypes.wintypes.DWORD),
        ("Attributes", ctypes.c_void_p),
        ("TargetAlias", ctypes.c_wchar_p),
        ("UserName", ctypes.c_wchar_p),
    ]


def _read_credential(target: str) -> str | None:
    advapi32 = ctypes.windll.advapi32
    cred_ptr = ctypes.c_void_p()
    if advapi32.CredReadW(target, 1, 0, ctypes.byref(cred_ptr)):
        cred = ctypes.cast(cred_ptr, ctypes.POINTER(CREDENTIAL)).contents
        secret = ctypes.wstring_at(cred.CredentialBlob, cred.CredentialBlobSize // 2)
        advapi32.CredFree(cred_ptr)
        return secret
    return None


TENANT = "YOUR_TENANT"
USERNAME = _read_credential("unicommerce-login-id")
PASSWORD = _read_credential("unicommerce-password")
FACILITY = "YOUR_TENANT"

if not USERNAME or not PASSWORD:
    pytest.exit("Unicommerce credentials not found in Windows Credential Manager", returncode=1)


@pytest.fixture(scope="session")
def client():
    c = Unicommerce(tenant=TENANT, username=USERNAME, password=PASSWORD, facility=FACILITY)
    yield c
    c.close()


@pytest.fixture
def async_client():
    return AsyncUnicommerce(tenant=TENANT, username=USERNAME, password=PASSWORD, facility=FACILITY)
