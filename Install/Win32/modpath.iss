// ----------------------------------------------------------------------------
//
// Inno Setup Ver:  5.1.8
// Script Version:  1.2.4
// Author:          Jared Breland <jbreland@legroom.net>
// Homepage:		http://www.legroom.net/mysoft
//
// Script Function:
//	Enable modification of system path directly from Inno Setup installers
//
// Instructions:
//      Hacked about and simplified by LPK.
//      To use add an AfterInstall function to the relevant task.
//
//	Copy modpath.iss to the same directory as your setup script
//
//	Add this statement to your [Setup] section
//		ChangesEnvironment=yes
//
//	Add this statement to your [Tasks] section
//	You can change the Description and Flags, but the Name must be modifypath
//		Name: modifypath; Description: &Add application directory to your system path; Flags: unchecked
//
//	Add the following to the end of your [Code] section
//	Result should be set to the path that you want to add
//		function ModPathDir(): String;
//		begin
//			Result := ExpandConstant('{app}');
//		end;
//		#include "modpath.iss"
//
// ----------------------------------------------------------------------------

procedure AddPath( pathdir:String);
var
	oldpath:	String;
	newpath:	String;
	pathArr:	TArrayOfString;
	i:			Integer;
begin
	// Modify WinNT path
    // Get current path, split into an array
    RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', oldpath);
    oldpath := oldpath + ';';
    i := 0;
    while (Pos(';', oldpath) > 0) do begin
        SetArrayLength(pathArr, i+1);
        pathArr[i] := Copy(oldpath, 0, Pos(';', oldpath)-1);
        oldpath := Copy(oldpath, Pos(';', oldpath)+1, Length(oldpath));
        i := i + 1;

        // Check if current directory matches app dir
        if pathdir = pathArr[i-1] then begin
            // if uninstalling, remove dir from path
            if IsUninstaller() = true then begin
                continue;
            // if installing, abort because dir was already in path
            end else begin
                exit;
                abort;
            end;
        end;

        // Add current directory to new path
        if i = 1 then begin
            newpath := pathArr[i-1];
        end else begin
            newpath := newpath + ';' + pathArr[i-1];
        end;
    end;

    // Append app dir to path if not already included
    if IsUninstaller() = false then
        newpath := newpath + ';' + pathdir;

    // Write new path
    RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', newpath);

	// Write file to flag modifypath was selected
	//   Workaround since IsTaskSelected() cannot be called at uninstall and AppName and AppId cannot be "read" in Code section
	if IsUninstaller() = false then
		SaveStringToFile(ExpandConstant('{app}') + '\uninsTasks.txt', WizardSelectedTasks(False), False);
end;

procedure RemovePath( pathdir:String);
var
	savepath:	String;
	oldpath:	String;
	newpath:	String;
	pathArr:	TArrayOfString;
	i:			Integer;
begin
    // remove from path anything that starts with pathdir, used to clear old versions on upgrade
	// Modify WinNT path
    // Get current path, split into an array
    RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', oldpath);
    savepath := oldpath;
    oldpath := oldpath + ';';
    i := 0;
    while (Pos(';', oldpath) > 0) do begin
        SetArrayLength(pathArr, i+1);
        pathArr[i] := Copy(oldpath, 0, Pos(';', oldpath)-1);
        oldpath := Copy(oldpath, Pos(';', oldpath)+1, Length(oldpath));
        i := i + 1;

        // Add current directory to new path
        // if not head of existing.
        if Pos( pathdir, pathArr[i-1] ) <> 1 then begin
            if i = 1 then begin
                newpath := pathArr[i-1];
            end else begin
                newpath := newpath + ';' + pathArr[i-1];
            end;
        end;
        
    end;

    // Write new path
    if savepath <> newpath then begin
        RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', newpath);
    end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
//	if CurStep = ssPostInstall then
//		if IsTaskSelected('modifypath') then
//			ModPath();
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
//var
//	appdir:			String;
//	selectedTasks:	String;
begin
//	appdir := ExpandConstant('{app}')
//	if CurUninstallStep = usUninstall then begin
//		if LoadStringFromFile(appdir + '\uninsTasks.txt', selectedTasks) then
//			if Pos('modifypath', selectedTasks) > 0 then
//				ModPath();
//		DeleteFile(appdir + '\uninsTasks.txt')
//	end;
end;
