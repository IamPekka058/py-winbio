import ctypes
import Enum, Types

def convert(hresult):
    return ctypes.c_int32(hresult).value

def FAILED(hr):
    if(hr == convert(Enum.HRESULT.E_ABORT)):
        return (True, "E_ABORT")

    if(hr == convert(Enum.HRESULT.E_ACCESSDENIED)):
        return (True, "E_ACCESSDENIED")

    if(hr == convert(Enum.HRESULT.E_FAIL)):
        return (True, "E_FAIL")

    if(hr == convert(Enum.HRESULT.E_HANDLE)):
        return (True, "E_HANDLE")
    
    if(hr == convert(Enum.HRESULT.E_INVALIDARG)):
        return (True, "E_INVALIDARG")
    
    if(hr == convert(Enum.HRESULT.E_NOINTERFACE)):
        return (True, "E_NOINTERFACE")
    
    if(hr == convert(Enum.HRESULT.E_NOTIMPL)):
        return (True, "E_NOTIMPL")

    if(hr == convert(Enum.HRESULT.E_OUTOFMEMORY)):
        return (True, "E_OUTOFMEMORY")

    if(hr == convert(Enum.HRESULT.E_POINTER)):
        return (True, "E_POINTER")
    
    if(hr == convert(Enum.HRESULT.E_UNEXPECTED)):
        return (True, "E_UNEXPECTED")

    if(hr == convert(Enum.HRESULT.S_OK)):
        return (False, "S_OK")
    
    return (True, "NO SPECIFIC ERROR")