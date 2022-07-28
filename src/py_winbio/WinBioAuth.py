import ctypes, Enum, Types
from Helper import FAILED

class WinBioAuthenticator():
    def __init__(self, lib_path = r"C:\Windows\System32\winbio.dll", openSession = True):
        # Setting lib
        self.lib = ctypes.CDLL(lib_path)
        
        # Init variables
        session_handle = ctypes.c_uint32()
        self.session_handle_ptr = ctypes.pointer(session_handle)
        if(openSession == False):
            return None
        
        #Open session
        self.openSession()
    
    def openSession(self, WINBIO_TYPE = Enum.WINBIO_TYPE.FINGERPRINT, WINBIO_POOL = Enum.WINBIO_POOL.SYSTEM, WINBIO_FLAG = Enum.WINBIO_FLAG.DEFAULT):
        ret = self.lib.WinBioOpenSession(WINBIO_TYPE, WINBIO_POOL, WINBIO_FLAG, None, 0, None, self.session_handle_ptr)
        
        #Check if operation failed
        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, "Success.")

    def identify(self, subtype = Enum.WINBIO_FINGER_UNSPECIFIED.POS_01):
        unitid_ptr = ctypes.pointer(ctypes.c_ulong())
        identity_ptr = ctypes.pointer(Types.WINBIO_IDENTITY())
        subtype_ptr = ctypes.pointer(ctypes.c_ubyte(subtype))
        reject_detail_ptr = ctypes.pointer(ctypes.c_ulong())
        
        ret = self.lib.WinBioIdentify(self.session_handle_ptr[0],unitid_ptr, identity_ptr, subtype_ptr, reject_detail_ptr)

        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        self.identity = identity_ptr[0]
        return Types.Result(True, self.identity)

    def verify(self, subtype = Enum.WINBIO_FINGER_UNSPECIFIED.POS_01):
        identity_ptr = ctypes.pointer(self.identity)
        #subtype_ptr = ctypes.pointer(ctypes.c_ubyte(subtype))
        unitId_ptr = ctypes.pointer(ctypes.c_int32())
        reject_detail_ptr = ctypes.pointer(ctypes.c_ulong())
        match_ptr = ctypes.pointer(ctypes.c_bool())

        ret = self.lib.WinBioVerify(self.session_handle_ptr[0], subtype, identity_ptr, unitId_ptr, match_ptr, reject_detail_ptr)

        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, self.failed[1])

    def enumerateBiometricUnits(self, WINBIO_TYPE = Enum.WINBIO_TYPE.FINGERPRINT):
        schema_ptr = ctypes.pointer(Types.WINBIO_UNIT_SCHEMA())
        size = ctypes.c_int32()
        size_ptr = ctypes.pointer(size)
        
        ret = self.lib.WinBioEnumBiometricUnits(WINBIO_TYPE, schema_ptr, size_ptr)
        
        #Check if operation failed
        failed = FAILED(ret)
        if(failed[0]):
            self.free(schema_ptr)
            return Types.Result(False, failed[1])
        self.availableBiometricUnits = schema_ptr[0]
        self.free(schema_ptr)
        return Types.Result(True, size_ptr[0])

    def cancel(self):
        ret = self.lib.WinBioCancel(self.session_handle_ptr[0])

        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, failed[1])

    def free(self, address):
        ret = self.lib.WinBioFree(address)

        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, failed[1])






    