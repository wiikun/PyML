import ctypes
import mmap
from typing import Callable,Any,Sequence

class BinFun:
    __slots__ = ("__data")
    def __init__(self,fun:Callable,buf:mmap.mmap):
        self.__data = (fun,buf)
    def __call__(self,*args:Any):
        return self.__data[0](*args)


def byte_to_fun(code:bytes,ftype:Sequence):
    
    buf = mmap.mmap(-1,len(code),flags=mmap.MAP_ANONYMOUS | mmap.MAP_SHARED
                    ,prot=mmap.PROT_WRITE|mmap.PROT_READ|mmap.PROT_EXEC)
    buf.write(code)
    ft = ctypes.CFUNCTYPE(*ftype)
    fun = ft(ctypes.addressof(ctypes.c_char.from_buffer(buf)))
    
    return BinFun(fun,buf)


def readff(name:str,ftype:Sequence):
    with open(name,"rb") as f:
        return byte_to_fun(f.read(),ftype)

if __name__ == "__main__":
    readff("prt.bin",(ctypes.c_ssize_t,ctypes.c_char_p,ctypes.c_size_t))(b"Hello, world\n",13)