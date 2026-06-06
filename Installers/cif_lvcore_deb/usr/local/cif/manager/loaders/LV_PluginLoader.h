#include "extcode.h"
#define __stdcall
#define __cdecl

#ifdef __cplusplus
extern "C" {
#endif

/*!
 * PluginLoader_Loader
 */
void __cdecl PluginLoader_Loader(uint32_t PID, char LoaderName[]);

MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

void __cdecl SetExecuteVIsInPrivateExecutionSystem(Bool32 value);

#ifdef __cplusplus
} // extern "C"
#endif

