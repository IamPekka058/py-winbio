import ctypes
from ctypes import wintypes

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