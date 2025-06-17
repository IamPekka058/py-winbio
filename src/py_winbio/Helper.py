import ctypes
import Enum, Types

def convert(hresult):
    return ctypes.c_int32(hresult).value

def RESULT(hr):
    if hr == convert(Enum.HRESULT.E_ABORT):
        return Types.Result(False, "E_ABORT")

    if hr == convert(Enum.HRESULT.E_ACCESSDENIED):
        return Types.Result(False, "E_ACCESSDENIED")

    if hr == convert(Enum.HRESULT.E_FAIL):
        return Types.Result(False, "E_FAIL")

    if hr == convert(Enum.HRESULT.E_HANDLE):
        return Types.Result(False, "E_HANDLE")
    
    if hr == convert(Enum.HRESULT.E_INVALIDARG):
        return Types.Result(False, "E_INVALIDARG")
    
    if hr == convert(Enum.HRESULT.E_NOINTERFACE):
        return Types.Result(False, "E_NOINTERFACE")
    
    if hr == convert(Enum.HRESULT.E_NOTIMPL):
        return Types.Result(False, "E_NOTIMPL")

    if hr == convert(Enum.HRESULT.E_OUTOFMEMORY):
        return Types.Result(False, "E_OUTOFMEMORY")

    if hr == convert(Enum.HRESULT.E_POINTER):
        return Types.Result(False, "E_POINTER")
    
    if hr == convert(Enum.HRESULT.E_UNEXPECTED):
        return Types.Result(False, "E_UNEXPECTED")

    if hr == convert(Enum.HRESULT.S_OK):
        return Types.Result(True, "S_OK")
    
    return Types.Result(False, "NO SPECIFIC ERROR, HRESULT: {}".format(hex(hr&0xFFFFFFFF)))