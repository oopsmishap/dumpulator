#include <Windows.h>

void entrypoint()
{
    LoadLibraryA( "user32.dll" );
    LoadLibraryA( "shell32.dll" );
    LoadLibraryA( "bcrypt.dll" );
    LoadLibraryA( "WS2_32.dll" );
    LoadLibraryA( "advapi32.dll" );
    LoadLibraryA( "ole32.dll" );
    LoadLibraryA( "comctl32.dll" );
    __debugbreak(); // dump here
}