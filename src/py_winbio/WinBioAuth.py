import ctypes, Enum
from Helper import FAILED

class WinBioAuthenticator():
    def __init__(self, lib_path = r"C:\Windows\System32\winbio.dll", openSession = True) -> None:
        # Setting lib
        self.lib = ctypes.CDLL(lib_path)
        # Init variables
        self.session_handle = ctypes.c_uint32()
        self.session_handle_ptr = ctypes.pointer(self.session_handle)
        if(openSession == False):
            return None
        #Open session
        self.WinBioOpenSession()
    
    def WinBioOpenSession(self, WINBIO_TYPE = Enum.WINBIO_TYPE.FINGERPRINT, WINBIO_POOL = Enum.WINBIO_POOL.SYSTEM, WINBIO_FLAG = Enum.WINBIO_FLAG.DEFAULT):
        ret = self.lib.WinBioOpenSession(WINBIO_TYPE, WINBIO_POOL, WINBIO_FLAG, None, 0, None, self.session_handle_ptr)
        if(FAILED(ret)[0]):
            print("Open Failed!")
            print(FAILED(ret)[1])
            return False
        return True


    