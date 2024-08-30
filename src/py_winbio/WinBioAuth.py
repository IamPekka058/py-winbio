import ctypes, Enum, Types
from ctypes import wintypes
from Helper import RESULT

class WinBioAuthenticator():
    def __init__(self, lib_path = r"C:\Windows\System32\winbio.dll", openSession = True) -> None:
        # Setting lib
        self.lib = ctypes.CDLL(lib_path)

        # Init variables
        self.unit_ids = []
        self.availableBiometricUnits = []
        self.session_handle = ctypes.c_uint32()
        self.session_handle_ptr = ctypes.pointer(self.session_handle)
        if not openSession:
            pass

    def openSession(self, WINBIO_TYPE = Enum.WINBIO_TYPE.FINGERPRINT, WINBIO_POOL = Enum.WINBIO_POOL.SYSTEM, WINBIO_FLAG = Enum.WINBIO_FLAG.DEFAULT):
        ret = self.lib.WinBioOpenSession(WINBIO_TYPE, WINBIO_POOL, WINBIO_FLAG, ctypes.c_void_p(None), 0, Enum.WINBIO_DB.DEFAULT, ctypes.byref(self.session_handle))

        #Check if operation failed
        job = RESULT(ret)

        if not job.state:
            print("Failed to open session, HRESULT: ", job.response)
            return job
        print("Successfully opened session, HRESULT: ", job.response)
        return job

# TODO - Implement the following method https://learn.microsoft.com/en-us/windows/win32/api/winbio/nf-winbio-winbioasyncopensession
#        def openAsyncSession(self, WINBIO_TYPE = Enum.WINBIO_TYPE.FINGERPRINT, WINBIO_POOL = Enum.WINBIO_POOL.SYSTEM, WINBIO_FLAG = Enum.WINBIO_FLAG.DEFAULT):


# TODO - Implement the following method https://learn.microsoft.com/en-us/windows/win32/api/winbio/nc-winbio-pwinbio_async_completion_callback
#    def asyncCallbackMethod():
#        pass

    def locateSensor(self):
        unit_id = ctypes.pointer(wintypes.ULONG())

        ret = self.lib.WinBioLocateSensor(self.session_handle, unit_id)

        job = RESULT(ret)
        if not job.state:
            print("Failed to locate sensor, HRESULT: ", job.response)
            return job
        print("Successfully located sensor.")
        job.response = unit_id
        return job
# TODO - Wait until async operations are supported
#    def monitorPresence(self, unit_id):
#        ret = self.lib.WinBioMonitorPresence(self.session_handle, unit_id)
#
#        job = RESULT(ret)
#        if not job.state:
#            print("Failed to monitor presence, HRESULT: ", job.response)
#            return job
#        print("Successfully monitored presence.")
#        return job

    def identify(self, subtype = Enum.WINBIO_FINGER_UNSPECIFIED.POS_01):
        unitid_ptr = ctypes.pointer(ctypes.c_ulong())
        identity_ptr = ctypes.pointer(Types.WINBIO_IDENTITY())
        subtype_ptr = ctypes.pointer(ctypes.c_ubyte())
        reject_detail_ptr = ctypes.pointer(ctypes.c_ulong())

        print("Starting Identification Process...")

        ret = self.lib.WinBioIdentify(self.session_handle_ptr.contents,unitid_ptr, identity_ptr, subtype_ptr, reject_detail_ptr)

        job = RESULT(ret)
        print("IDENTIFY -> {}".format(job))
        if not job.state:
            print("Failed to identify, HRESULT: ", job.response)
            return job
        print("Successfully identified, HRESULT: ", job.response)
        job.response = identity_ptr[0]
        self.free(ctypes.addressof(identity_ptr))
        return job

    def verify(self, subtype = Enum.WINBIO_FINGER_UNSPECIFIED.POS_01):
        identity_ptr = ctypes.pointer(self.identity)
        #subtype_ptr = ctypes.pointer(ctypes.c_ubyte(subtype))
        unitId_ptr = ctypes.pointer(ctypes.c_int32())
        reject_detail_ptr = ctypes.pointer(ctypes.c_ulong())
        match_ptr = ctypes.pointer(ctypes.c_bool())

        ret = self.lib.WinBioVerify(self.session_handle_ptr[0], subtype, identity_ptr, unitId_ptr, match_ptr, reject_detail_ptr)

        job = RESULT(ret)
        if not job.state:
            print("Failed to verify, HRESULT: ", job.response)
            return job
        print("Successfully verified, HRESULT: ", job.response)
        return job

    def enumerateBiometricUnits(self, WINBIO_TYPE = Enum.WINBIO_TYPE.FINGERPRINT):
        schema_ptr = ctypes.pointer(Types.WINBIO_UNIT_SCHEMA())
        schema_ptr_array = ctypes.pointer(schema_ptr)

        size = ctypes.c_int32()
        size_ptr = ctypes.pointer(size)

        ret = self.lib.WinBioEnumBiometricUnits(WINBIO_TYPE, schema_ptr_array, size_ptr)

        self.unit_ids = schema_ptr_array

        if schema_ptr_array.contents is not None:
            # Secure array list before free/delete
            self.availableBiometricUnits = schema_ptr[0]
            self.free(schema_ptr)
            schema_ptr = None

        job = RESULT(ret)

        if not job.state:
            print("Failed to enumerate Biometric Units, HRESULT: ", job.response)
            return -1
        print("Successfully enumerated Biometric Units, HRESULT: ", job.response)
        job.response = {"size": size, "schema": schema_ptr}
        return job

    def cancel(self):
        ret = self.lib.WinBioCancel(self.session_handle_ptr[0])

        job = RESULT(ret)
        if not job.state:
            return job
        return job

    def free(self, address):
        ret = self.lib.WinBioFree(address)

        job = RESULT(ret)
        if not job.state:
            return job
        return job
# Following methods need local system permissions on windows
# Currently deactivated
#    def acquireFocus(self):
#        ret = self.lib.WinBioAcquireFocus()
#        failed = FAILED(ret)
#        if(failed[0]):
#            print("Failed to acquire focus, HRESULT: ", failed[1])
#            return Types.Result(False, failed[1])
#        print("Acquire focus, HRESULT: ", hex(ret))
#        return Types.Result(True, failed[1])
#
#    def releaseFocus(self):
#        ret = self.lib.WinBioRealeaseFocus()
#
#        failed = FAILED(ret)
#        if(failed[0]):
#            return Types.Result(False, failed[1])
#        return Types.Result(True, failed[1])
#
#    def enrollBegin(self, subfactor = Enum.SUBFACTOR.WINBIO_ANSI_381_POS_LH_INDEX_FINGER):
#        ret = self.lib.WinBioEnrollBegin(self.session_handle, self.unit_id)
#
#        failed = FAILED(ret)
#        if(failed[0]):
#            return Types.Result(False, failed[1])
#        return Types.Result(True, failed[1])
#
#    def enrollCapture(self):
#        rejectDetail = ctypes.c_ulong()
#        ret = self.lib.WinBioEnrollCapture(self.session_handle, ctypes.byref(rejectDetail))
#        print(ret)
#        print(rejectDetail)
#        failed = FAILED(ret)
#        if(failed[0]):
#            return Types.Result(False, failed[1])
#        return Types.Result(True, failed[1])
#
#
#
#
#        print("Successfully enumerated Biometric Units,  HRESULT: ", hex(ret))
#        return size_ptr[0]



    