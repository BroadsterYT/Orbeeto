#pragma once
#ifdef _DEBUG
#ifndef _DBG_NEW

#include <crtdbg.h>

inline void* __operator_new(size_t __n) {
    return ::operator new(__n, _NORMAL_BLOCK, __FILE__, __LINE__);
}
inline void* _cdecl operator new(size_t __n, const char* __fname, int __line) {
    return ::operator new(__n, _NORMAL_BLOCK, __fname, __line);
}
inline void _cdecl operator delete(void* __p, const char*, int) {
    ::operator delete(__p);
}

#define _DBG_NEW new(__FILE__,__LINE__)
#define new _DBG_NEW


#endif // _DBG_NEW
#else

#define __operator_new(__n) operator new(__n)

#endif

#include "../Game.hpp"


class System {

};