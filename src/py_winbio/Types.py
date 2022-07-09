import ctypes
from ctypes import wintypes

#Maximum size of SID according to the docs
SECURITY_MAX_SID_SIZE = 68

class GUID(ctypes.Structure):
    _fields_ = [("Data1", wintypes.DWORD),
                ("Data2", wintypes.DWORD),
                ("Data3", wintypes.DWORD)]

class AccountSid(ctypes.Structure):
    _fields_ = [("Size", ctypes.c_ulong),
                ("Data", ctypes.c_char * SECURITY_MAX_SID_SIZE)]

class Value(ctypes.Structure):
    _fields_ = [("Null", ctypes.c_ulong),
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
                ("DeviceInstanceId", ctypes.c_char_p),
                ("Description", ctypes.c_char_p),
                ("Manufacturer", ctypes.c_char_p),
                ("Model", ctypes.c_char_p),
                ("SerialNumber", ctypes.c_char_p),
                ("FirmwareVersion", WINBIO_VERSION)]

class WINBIO_IDENTITY(ctypes.Structure):
    _fields_ = [("Type", ctypes.c_ulong),
                ("Value", Value)]

class Result():
    def __init__(self, state, response):
        self.state = state
        self.response = response

    def getStatus(self):
        return self.state
    
    def getResponse(self):
        return self.response