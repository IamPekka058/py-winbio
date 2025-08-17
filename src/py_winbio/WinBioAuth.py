import ctypes
from ctypes import wintypes, POINTER
from . import constants, Types
from .Helper import RESULT

class WinBioAuthenticator():
    def __init__(self, lib_path=r"C:\Windows\System32\winbio.dll") -> None:
        self.lib = ctypes.CDLL(lib_path)
        self._define_prototypes()
        self.session_handle = Types.WINBIO_SESSION_HANDLE()

    def _define_prototypes(self):
        self.lib.WinBioOpenSession.argtypes = [
            wintypes.ULONG,
            wintypes.ULONG,
            wintypes.ULONG,
            POINTER(Types.WINBIO_UNIT_ID),
            ctypes.c_size_t,
            wintypes.ULONG,
            POINTER(Types.WINBIO_SESSION_HANDLE)
        ]
        self.lib.WinBioOpenSession.restype = ctypes.HRESULT

        self.lib.WinBioCloseSession.argtypes = [Types.WINBIO_SESSION_HANDLE]
        self.lib.WinBioCloseSession.restype = ctypes.HRESULT

        self.lib.WinBioEnumBiometricUnits.argtypes = [
            wintypes.ULONG,
            POINTER(POINTER(Types.WINBIO_UNIT_SCHEMA)),
            POINTER(ctypes.c_size_t)
        ]
        self.lib.WinBioEnumBiometricUnits.restype = ctypes.HRESULT

        self.lib.WinBioIdentify.argtypes = [
            Types.WINBIO_SESSION_HANDLE,
            POINTER(Types.WINBIO_UNIT_ID),
            POINTER(Types.WINBIO_IDENTITY),
            POINTER(Types.WINBIO_BIOMETRIC_SUBTYPE),
            POINTER(Types.WINBIO_REJECT_DETAIL)
        ]
        self.lib.WinBioIdentify.restype = ctypes.HRESULT

        self.lib.WinBioVerify.argtypes = [
            Types.WINBIO_SESSION_HANDLE,
            Types.PWINBIO_IDENTITY,
            Types.WINBIO_BIOMETRIC_SUBTYPE,
            POINTER(Types.WINBIO_UNIT_ID),
            POINTER(wintypes.BOOL),
            POINTER(Types.WINBIO_REJECT_DETAIL)
        ]
        self.lib.WinBioVerify.restype = ctypes.HRESULT

        self.lib.WinBioFree.argtypes = [ctypes.c_void_p]
        self.lib.WinBioFree.restype = ctypes.HRESULT

        self.lib.WinBioLocateSensor.argtypes = [Types.WINBIO_SESSION_HANDLE, POINTER(Types.WINBIO_UNIT_ID)]
        self.lib.WinBioLocateSensor.restype = ctypes.HRESULT

        self.lib.WinBioCancel.argtypes = [Types.WINBIO_SESSION_HANDLE]
        self.lib.WinBioCancel.restype = ctypes.HRESULT

    def openSession(self, bio_type=constants.WINBIO_TYPE.FINGERPRINT, pool=constants.WINBIO_POOL.SYSTEM, flag=constants.WINBIO_FLAG.DEFAULT, db=constants.WINBIO_DB.DEFAULT):
        ret = self.lib.WinBioOpenSession(bio_type, pool, flag, None, 0, db, ctypes.byref(self.session_handle))
        job = RESULT(ret)
        if not job.state:
            print(f"Failed to open session, HRESULT: {job.response}")
        else:
            print(f"Successfully opened session, HRESULT: {job.response}")
        return job

    def closeSession(self):
        ret = self.lib.WinBioCloseSession(self.session_handle)
        job = RESULT(ret)
        if not job.state:
            print(f"Failed to close session, HRESULT: {job.response}")
        else:
            print(f"Successfully closed session, HRESULT: {job.response}")
        return job

    def identify(self):
        print("Starting Identification Process...")
        unit_id = Types.WINBIO_UNIT_ID()
        identity = Types.WINBIO_IDENTITY()
        sub_factor = Types.WINBIO_BIOMETRIC_SUBTYPE()
        reject_detail = Types.WINBIO_REJECT_DETAIL()

        ret = self.lib.WinBioIdentify(
            self.session_handle,
            ctypes.byref(unit_id),
            ctypes.byref(identity),
            ctypes.byref(sub_factor),
            ctypes.byref(reject_detail)
        )

        job = RESULT(ret)
        if not job.state:
            print(f"Failed to identify, HRESULT: {job.response}")
        else:
            print(f"Successfully identified, HRESULT: {job.response}")
            job.response = identity
        return job

    def verify(self, identity, subtype=constants.WINBIO_FINGER_UNSPECIFIED.POS_01):
        unit_id = Types.WINBIO_UNIT_ID()
        match = wintypes.BOOL()
        reject_detail = Types.WINBIO_REJECT_DETAIL()

        ret = self.lib.WinBioVerify(
            self.session_handle,
            ctypes.byref(identity),
            subtype,
            ctypes.byref(unit_id),
            ctypes.byref(match),
            ctypes.byref(reject_detail)
        )

        job = RESULT(ret)
        if not job.state:
            print(f"Failed to verify, HRESULT: {job.response}")
        else:
            print(f"Successfully verified, HRESULT: {job.response}")
            job.response = bool(match.value)
        return job

    def enumerateBiometricUnits(self, bio_type=constants.WINBIO_TYPE.FINGERPRINT):
        schema_array = POINTER(Types.WINBIO_UNIT_SCHEMA)()
        unit_count = ctypes.c_size_t()

        ret = self.lib.WinBioEnumBiometricUnits(bio_type, ctypes.byref(schema_array), ctypes.byref(unit_count))

        job = RESULT(ret)
        if not job.state:
            print(f"Failed to enumerate Biometric Units, HRESULT: {job.response}")
            return job

        print(f"[DEBUG] HRESULT from WinBioEnumBiometricUnits: {hex(ret)}")
        print(f"[DEBUG] unit_count: {unit_count.value}")
        py_units = []
        try:
            for i in range(unit_count.value):
                print(f"[DEBUG] --- Processing unit {i} ---")
                unit_schema = schema_array[i]
                
                print(f"[DEBUG] Reading UnitId: {unit_schema.UnitId}")
                py_unit = {'UnitId': unit_schema.UnitId}

                print(f"[DEBUG] Reading PoolType: {unit_schema.PoolType}")
                py_unit['PoolType'] = unit_schema.PoolType

                print(f"[DEBUG] Reading BiometricFactor: {unit_schema.BiometricFactor}")
                py_unit['BiometricFactor'] = unit_schema.BiometricFactor

                print(f"[DEBUG] Reading SensorSubType: {unit_schema.SensorSubType}")
                py_unit['SensorSubType'] = unit_schema.SensorSubType

                print(f"[DEBUG] Reading Capabilities: {unit_schema.Capabilities}")
                py_unit['Capabilities'] = unit_schema.Capabilities

                print(f"[DEBUG] Reading DeviceInstanceId pointer: {unit_schema.DeviceInstanceId}")
                py_unit['DeviceInstanceId'] = unit_schema.DeviceInstanceId.decode('utf-8') if unit_schema.DeviceInstanceId else ''
                
                print(f"[DEBUG] Reading Description pointer: {unit_schema.Description}")
                py_unit['Description'] = unit_schema.Description.decode('utf-8') if unit_schema.Description else ''

                print(f"[DEBUG] Reading Manufacturer pointer: {unit_schema.Manufacturer}")
                py_unit['Manufacturer'] = unit_schema.Manufacturer.decode('utf-8') if unit_schema.Manufacturer else ''

                print(f"[DEBUG] Reading Model pointer: {unit_schema.Model}")
                py_unit['Model'] = unit_schema.Model.decode('utf-8') if unit_schema.Model else ''

                print(f"[DEBUG] Reading SerialNumber pointer: {unit_schema.SerialNumber}")
                py_unit['SerialNumber'] = unit_schema.SerialNumber.decode('utf-8') if unit_schema.SerialNumber else ''

                print(f"[DEBUG] Reading FirmwareVersion")
                py_unit['FirmwareVersion'] = {
                        'MajorVersion': unit_schema.FirmwareVersion.MajorVersion,
                        'MinorVersion': unit_schema.FirmwareVersion.MinorVersion
                    }
                
                print(f"[DEBUG] --- Finished unit {i} ---")
                py_units.append(py_unit)
        except Exception as e:
            print(f"[FATAL] Crashed while processing units. Error: {e}")

        self.free(schema_array)

        print(f"Successfully enumerated {len(py_units)} Biometric Units, HRESULT: {job.response}")
        job.response = py_units
        return job

    def cancel(self):
        ret = self.lib.WinBioCancel(self.session_handle)
        job = RESULT(ret)
        if not job.state:
            print(f"Failed to cancel, HRESULT: {job.response}")
        return job

    def free(self, ptr):
        self.lib.WinBioFree(ptr)

    def locateSensor(self):
        unit_id = Types.WINBIO_UNIT_ID()
        ret = self.lib.WinBioLocateSensor(self.session_handle, ctypes.byref(unit_id))
        job = RESULT(ret)
        if not job.state:
            print(f"Failed to locate sensor, HRESULT: {job.response}")
        else:
            print(f"Successfully located sensor, HRESULT: {job.response}")
            job.response = unit_id.value
        return job