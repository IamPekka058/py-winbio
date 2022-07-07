class WINBIO_TYPE():
    # Note windows supports only FINGERPRINT
    MULTIPLE = 0x00000001
    FACIAL_FEATURES = 0x00000002
    VOICE = 0x00000004
    FINGERPRINT = 0x00000008
    IRIS = 0x00000010
    RETINA = 0x00000020
    HAND_GEOMETRY = 0x00000040
    SIGNATURE_DYNAMICS = 0x00000080
    KEYSTROKE_DYNAMICS = 0x00000100
    LIP_MOVEMENT = 0x00000200
    THERMAL_FACE_IMAGE = 0x00000400
    THERMAL_HAND_IMAGE = 0x00000800
    GAIT = 0x00001000
    SCENT = 0x00002000
    DNA = 0x00004000
    EAR_SHAPE = 0x00008000
    FINGER_GEOMETRY = 0x00010000
    PALM_PRINT = 0x00020000
    VEIN_PATTERN = 0x00040000
    FOOT_PRINT = 0x00080000

class WINBIO_POOL():
    UNKOWN = 0
    SYSTEM = 1
    PRIVATE = 2
    UNASSIGNED = 3

class WINBIO_FLAG():
    DEFAULT = 0x00000000

class HRESULT():
    S_OK = 0x00000000
    E_ABORT = 0x80004004
    E_ACCESSDENIED = 0x80070005
    E_FAIL = 0x80004005
    E_HANDLE = 0x80070006
    E_INVALIDARG = 0x80070057
    E_NOINTERFACE = 0x80004002
    E_NOTIMPL = 0x80004001
    E_OUTOFMEMORY = 0x8007000E
    E_POINTER = 0x80004003
    E_UNEXPECTED = 0x8000FFFF

class WINBIO_CAPABILITY():
    SENSOR = 0x00000001
    MATCHING = 0x00000002
    DATABASE = 0x00000004
    PROCESSING = 0x00000008
    ENCRYPTION = 0x00000010
    NAVIGATION = 0x00000020
    INDICATOR = 0x00000040