import ctypes, Enum, Types
from ctypes import wintypes
from Helper import FAILED

class WinBioAuthenticator():
    
    def __init__(self, lib_path = r"C:\Windows\System32\winbio.dll", openSession = True):
        # Setting lib
        self.lib = ctypes.WinDLL(lib_path)
        
        # Init variables
        self.identity = Types.WINBIO_IDENTITY()
        self.session_handle = wintypes.HANDLE()
        #self.session_handle_ptr = ctypes.pointer(session_handle)
        if(openSession == False):
            return None
        
        #Open session
        self.openSession()
    
    def openSession(self, WINBIO_TYPE = Enum.WINBIO_TYPE.FINGERPRINT, WINBIO_POOL = Enum.WINBIO_POOL.SYSTEM, WINBIO_FLAG = Enum.WINBIO_FLAG.DEFAULT):
        #print("OpenSession (Session Handle) -> {}".format(self.session_handle_ptr.contents))
        ret = self.lib.WinBioOpenSession(WINBIO_TYPE, WINBIO_POOL, WINBIO_FLAG, ctypes.c_void_p(None), 0, Enum.WINBIO_DB.DEFAULT, ctypes.byref(self.session_handle))
        print("OpenSession (Return) -> {}".format(ret))
        print("OpenSession (Session Handle) -> {}".format(self.session_handle))
        #Check if operation failed
        failed = FAILED(ret)
        print("OpenSession -> {}".format(failed))
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, "Success.")
    
    def locateSensor(self):
        self.unit_id = wintypes.ULONG()
        print("Wird aufgerufen...")
        ret = self.lib.WinBioLocateSensor(self.session_handle, ctypes.byref(self.unit_id))
        print("Aufgerufen...")
        failed = FAILED(ret)
        if(failed):
            print("locateSensor (Error) -> {}".format(failed))
            return
        print(self.unit_id)

    def identify(self, subtype = Enum.WINBIO_FINGER_UNSPECIFIED.POS_01):
        unitid_ptr = ctypes.pointer(ctypes.c_ulong())
        identity_ptr = ctypes.pointer(Types.WINBIO_IDENTITY())
        subtype_ptr = ctypes.pointer(ctypes.c_ubyte())
        reject_detail_ptr = ctypes.pointer(ctypes.c_ulong())
        print("IDENTIFY (Session Handle) -> {}".format(self.session_handle_ptr.contents))
        print("DEBUG Library wird aufgerufen.")
        ret = self.lib.WinBioIdentify(self.session_handle_ptr.contents,unitid_ptr, identity_ptr, subtype_ptr, reject_detail_ptr)
        print(reject_detail_ptr)
        print("IDENTIFY -> {}".format(ret))
        print("DEBUG Library wurde aufgerufen.")
        failed = FAILED(ret)
        print("IDENTIFY -> {}".format(failed))
        if(failed[0]):
            return Types.Result(False, failed[1])
        self.identity = identity_ptr[0]
        self.free(ctypes.addressof(identity_ptr))
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
        schema_ptr_ptr = ctypes.pointer(schema_ptr)
        ret = self.lib.WinBioEnumBiometricUnits(WINBIO_TYPE, schema_ptr_ptr, size_ptr)
        print(size_ptr.contents)
        self.unit_id = schema_ptr.contents.UnitId
        #Check if operation failed
        self.free(schema_ptr_ptr.contents)
        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        self.availableBiometricUnits = schema_ptr[0]
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
    
    def acquireFocus(self):
        ret = self.lib.WinBioAcquireFocus()
        
        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, failed[1])
    
    def releaseFocus(self):
        ret = self.lib.WinBioRealeaseFocus()
        
        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, failed[1])
    
    def enrollBegin(self, subfactor = Enum.SUBFACTOR.WINBIO_ANSI_381_POS_LH_INDEX_FINGER):
        ret = self.lib.WinBioEnrollBegin(self.session_handle, self.unit_id)

        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, failed[1])

    def enrollCapture(self):
        rejectDetail = ctypes.c_ulong()
        ret = self.lib.WinBioEnrollCapture(self.session_handle, ctypes.byref(rejectDetail))
        print(ret)
        print(rejectDetail)
        failed = FAILED(ret)
        if(failed[0]):
            return Types.Result(False, failed[1])
        return Types.Result(True, failed[1])







    