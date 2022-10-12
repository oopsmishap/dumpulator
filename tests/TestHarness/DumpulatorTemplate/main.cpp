#include <windows.h>
#include <winternl.h>

extern "C"
NTSYSCALLAPI
NTSTATUS
NTAPI
NtDisplayString(
    PUNICODE_STRING String
);

#define WIDEN_EXPAND(str) L ## str
#define WIDEN(str) WIDEN_EXPAND(str)

// Helper function to directly call NtDisplayString with a string
// This simplifies the trace output of Dumpulator
template<size_t Count>
void DebugPrint( const wchar_t( &str )[ Count ] )
{
    UNICODE_STRING ustr{ ( Count - 1 ) * 2, Count * 2, ( PWSTR )str };
    NtDisplayString( &ustr );
}

/* ================================== TEST START ======================================== */

extern "C" __declspec( dllexport ) int TestFunction1()
{
    DebugPrint( WIDEN( __FUNCTION__ ) );
    return 1;
}

extern "C" __declspec( dllexport ) int TestFunction2()
{
    DebugPrint( WIDEN( __FUNCTION__ ) );
    return 1;
}

extern "C" __declspec( dllexport ) int TestFunction3()
{
    DebugPrint( WIDEN( __FUNCTION__ ) );
    return 1;
}

/* ================================== TEST END ========================================= */

void Entrypoint()
{

}
