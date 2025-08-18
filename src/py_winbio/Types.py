import ctypes
from ctypes import wintypes, POINTER

#Maximum size of SID according to the docs
SECURITY_MAX_SID_SIZE = 68

WINBIO_SESSION_HANDLE = wintypes.HANDLE
WINBIO_UNIT_ID = ctypes.c_ulong
WINBIO_REJECT_DETAIL = ctypes.c_ulong
WINBIO_BIOMETRIC_SUBTYPE = ctypes.c_ubyte

class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)]

class AccountSid(ctypes.Structure):
    _fields_ = [("Size", wintypes.ULONG),
                ("Data", (ctypes.c_ubyte * SECURITY_MAX_SID_SIZE))]

class Value(ctypes.Union):
    _fields_ = [("Null", wintypes.ULONG),
                ("Wildcard", ctypes.c_ulong),
                ("TemplateGuid", GUID),
                ("AccountSid", AccountSid)]

class WINBIO_VERSION(ctypes.Structure):
    _fields_ = [("MajorVersion", wintypes.DWORD),
                ("MinorVersion", wintypes.DWORD)]

class WINBIO_UNIT_SCHEMA(ctypes.Structure):
    _fields_ = [("UnitId", ctypes.c_int32),
                ("PoolType", ctypes.c_ulong),
                ("BiometricFactor", ctypes.c_ulong),
                ("SensorSubType", ctypes.c_long),
                ("Capabilities", ctypes.c_long),
                ("DeviceInstanceId", ctypes.c_wchar_p),
                ("Description", ctypes.c_wchar_p),
                ("Manufacturer", ctypes.c_wchar_p),
                ("Model", ctypes.c_wchar_p),
                ("SerialNumber", ctypes.c_wchar_p),
                ("FirmwareVersion", WINBIO_VERSION)]

class WINBIO_IDENTITY(ctypes.Structure):
    _fields_ = [("Type", ctypes.c_uint32),
                ("Value", Value)]

# TODO - Finish the structure https://learn.microsoft.com/en-us/windows/win32/api/winbio/ne-winbio-winbio_async_notification_method
#class WINBIO_ASYNC_NOTIFY_CALLBACK(ctypes.Structure):
#    _fields_ = [("WINBIO_ASYNC_NOTIFY_NONE", 0),
#                ("WINBIO_ASYNC_NOTIFY_CALLBACK", )]

# TODO - Finish the structure https://learn.microsoft.com/en-US/windows/win32/api/winbio/ns-winbio-winbio_async_result
#class ASYNC_RESULT(ctypes.Structure):

class Result():
    def __init__(self, state, response):
        self.state = state
        self.response = response

    def getStatus(self):
        return self.state
    
    def getResponse(self):
        return self.response

PWINBIO_UNIT_SCHEMA = POINTER(WINBIO_UNIT_SCHEMA)
PWINBIO_IDENTITY = POINTER(WINBIO_IDENTITY)
PWINBIO_UNIT_ID = POINTER(WINBIO_UNIT_ID)
PWINBIO_REJECT_DETAIL = POINTER(WINBIO_REJECT_DETAIL)
PWINBIO_BIOMETRIC_SUBTYPE = POINTER(WINBIO_BIOMETRIC_SUBTYPE)
