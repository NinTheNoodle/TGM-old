"""Events relating to the sys module."""
from tgm.sys import EventNamespace


sys_event = EventNamespace(
    "sys",
    control=[
        "update"
    ]
)
