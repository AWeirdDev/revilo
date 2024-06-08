from .windows_ps import psstr, run_powershell as ps

# https://stackoverflow.com/questions/2969321
# SOLUTION by Jeremy

SCREENSHOT_TEMPLATE = r"""[Reflection.Assembly]::LoadWithPartialName("System.Drawing")
function screenshot([Drawing.Rectangle]$bounds, $path) {
   $bmp = New-Object Drawing.Bitmap $bounds.width, $bounds.height
   $graphics = [Drawing.Graphics]::FromImage($bmp)

   $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size)

   $bmp.Save($path)

   $graphics.Dispose()
   $bmp.Dispose()
}

Add-Type -AssemblyName System.Windows.Forms
$screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bounds = [Drawing.Rectangle]::FromLTRB(0, 0, $screen.Width, $screen.Height)
screenshot $bounds {where}
"""


def take_screenshot(
    path: str = "./screenshot.png",
    *,
    unappropriately_disable_user_privacy_warning: bool = False,
):
    """Takes a screenshot and saves it to the specified path.

    Args:
        path (str): The path to save the screenshot to. Defaults to "./screenshot.png".
        unappropriately_disable_user_privacy_warning (bool): Disable the user privacy warning.
    """
    ps(SCREENSHOT_TEMPLATE, {"where": psstr(path)})

    if not unappropriately_disable_user_privacy_warning:
        from .windows_notifications import push_notification

        push_notification("Revilo (Windows API)", "Took a screenshot")


# https://stackoverflow.com/questions/46351885
# SOLUTION by Justin Rich from social.technet.microsoft.com
GET_CURRENT_APP_TEMPLATE = r"""Add-Type  @"
 using System;
 using System.Runtime.InteropServices;
 using System.Text;
public class APIFuncs
   {
    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
   public static extern int GetWindowText(IntPtr hwnd,StringBuilder
lpString, int cch);
    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
   public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
       public static extern Int32 GetWindowThreadProcessId(IntPtr hWnd,out
Int32 lpdwProcessId);
    [DllImport("user32.dll", SetLastError=true, CharSet=CharSet.Auto)]
       public static extern Int32 GetWindowTextLength(IntPtr hWnd);
    }
"@

$w = [apifuncs]::GetForegroundWindow()
$len = [apifuncs]::GetWindowTextLength($w)
$sb = New-Object text.stringbuilder -ArgumentList ($len + 1)
$rtnlen = [apifuncs]::GetWindowText($w,$sb,$sb.Capacity)
Write-Host "$($sb.tostring())"
"""


def get_current_app():
    """Returns the name of the current application.

    Returns:
        str: The name of the current application.
    """
    return ps(GET_CURRENT_APP_TEMPLATE).strip()
