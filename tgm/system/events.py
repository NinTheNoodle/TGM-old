"""Events relating to the sys module."""
from tgm.system import EventNamespace


sys_event = EventNamespace(
    "sys",
    control=[
        "update"
    ]
)
