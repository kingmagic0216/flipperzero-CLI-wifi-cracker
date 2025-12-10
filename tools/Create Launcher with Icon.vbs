Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\WiFi Cracker.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = oWS.CurrentDirectory & "\..\🚀 START WiFi Cracker (GUI).pyw"
oLink.WorkingDirectory = oWS.CurrentDirectory & "\.."
oLink.Description = "Launch WiFi Cracker Web App"
' Try to use a system icon (lock icon from shell32.dll)
oLink.IconLocation = "shell32.dll,48"
oLink.Save

' Also create one in the app folder
sLinkFile2 = oWS.CurrentDirectory & "\..\WiFi Cracker.lnk"
Set oLink2 = oWS.CreateShortcut(sLinkFile2)
oLink2.TargetPath = oWS.CurrentDirectory & "\..\🚀 START WiFi Cracker (GUI).pyw"
oLink2.WorkingDirectory = oWS.CurrentDirectory & "\.."
oLink2.Description = "Launch WiFi Cracker Web App"
oLink2.IconLocation = "shell32.dll,48"
oLink2.Save

WScript.Echo "Shortcuts created with icons!"

