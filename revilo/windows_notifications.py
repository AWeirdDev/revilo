"""Windows - Toast Notifications.

https://github.com/GitHub30/toast-notification-examples/blob/main/README.md
"""

from typing import Literal, Optional, Sequence
from .windows_ps import psbool, psstr, run_powershell as ps


TOAST_TEMPLATE = r"""$headlineText = {title}
$bodyText = {body}
$logo = {logo}
$image = {image}

$xml = @"
<toast duration={duration} scenario={scenario}>
    <visual>
        <binding template="ToastGeneric">
            <text>$($headlineText)</text>
            <text>$($bodyText)</text>
            <image placement="appLogoOverride" src="$($logo)"/>
            <image src="$($image)"/>
            <text placement="attribution">{attr}</text>
        </binding>
    </visual>

    <actions>
        {actions}
    </actions>
    
    {addAudio}
</toast>
"@
$XmlDocument = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]::New()
$XmlDocument.loadXml($xml)
$AppId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]::CreateToastNotifier($AppId).Show($XmlDocument)
"""


AudioSegment = Literal[
    "ms-winsoundevent:Notification.Default",
    "ms-winsoundevent:Notification.IM",
    "ms-winsoundevent:Notification.Mail",
    "ms-winsoundevent:Notification.Reminder",
    "ms-winsoundevent:Notification.SMS",
    "ms-winsoundevent:Notification.Looping.Alarm",
    "ms-winsoundevent:Notification.Looping.Alarm2",
    "ms-winsoundevent:Notification.Looping.Alarm3",
    "ms-winsoundevent:Notification.Looping.Alarm4",
    "ms-winsoundevent:Notification.Looping.Alarm5",
    "ms-winsoundevent:Notification.Looping.Alarm6",
    "ms-winsoundevent:Notification.Looping.Alarm7",
    "ms-winsoundevent:Notification.Looping.Alarm8",
    "ms-winsoundevent:Notification.Looping.Alarm9",
    "ms-winsoundevent:Notification.Looping.Alarm10",
    "ms-winsoundevent:Notification.Looping.Call",
    "ms-winsoundevent:Notification.Looping.Call2",
    "ms-winsoundevent:Notification.Looping.Call3",
    "ms-winsoundevent:Notification.Looping.Call4",
    "ms-winsoundevent:Notification.Looping.Call5",
    "ms-winsoundevent:Notification.Looping.Call6",
    "ms-winsoundevent:Notification.Looping.Call7",
    "ms-winsoundevent:Notification.Looping.Call8",
    "ms-winsoundevent:Notification.Looping.Call9",
    "ms-winsoundevent:Notification.Looping.Call10",
]


class Action:
    """Represents an action."""

    def __init__(
        self,
        content: str,
        arguments: str,
        *,
        style: Literal["Success", "Critical", ""] = "",
        tooltip: str = "",
    ):
        self.content = content
        self.arguments = arguments
        self.style = style
        self.tooltip = tooltip

    def __str__(self):
        return (
            '<action content=%s activationType="protocol" arguments=%s hint-buttonStyle=%s hint-toolTip=%s />'
            % (
                psstr(self.content),
                psstr(self.arguments),
                psstr(self.style),
                psstr(self.tooltip),
            )
        )


def push_notification(
    title: str,
    message: str,
    *,
    attribution: str = "",
    logo: str = "",
    image: str = "",
    audio: Optional[AudioSegment] = None,
    audio_loops: bool = False,
    audio_silent: bool = False,
    duration: Literal["long", "short"] = "short",
    scenario: Literal["reminder", "alarm", "incomingCall", "urgent"] = "reminder",
    actions: Sequence[Action] = [],
) -> None:
    """Sends a push notification in Windows using PowerShell.

    Args:
        title (str): The title of the notification.
        message (str): The message of the notification.
        attribution (str): The attribution of the notification.
        logo (str): The path to the logo of the notification.
        image (str): The path to the image of the notification.
        audio (AudioSegment): The audio of the notification.
        audio_loops (bool): Loop the audio?
        audio_silent (bool): Silent audio?
        duration ("long" | "short"): The duration of the notification.
        scenario ("reminder" | "alarm" | "incomingCall" | "urgent" ): The scenario of the notification.
        actions (Sequence[Action]): The actions of the notification.

    Returns:
        None: It's just what I do.
    """
    ps(
        TOAST_TEMPLATE,
        {
            "title": psstr(title),
            "body": psstr(message),
            "attr": "" if not attribution else attribution,
            "logo": psstr(logo, noendl=True),
            "image": psstr(image, noendl=True),
            "addAudio": ""
            if not audio
            else '<audio src="%s" silent="%s" loop="%s"/>'
            % (audio, psbool(audio_silent), psbool(audio_loops)),
            "duration": psstr(duration),
            "scenario": psstr(scenario),
            "actions": "\n".join(list(map(str, actions))),
        },
    )
