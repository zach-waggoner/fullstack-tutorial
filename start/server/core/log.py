from typing import Any

from django.core.management.color import color_style
from django.utils.log import ServerFormatter


class ColoredServerFormatter(ServerFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.style = color_style(force_color=True)
