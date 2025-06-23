"""
系统功能模块

提供系统级别的操作功能，如截屏、系统信息等
"""

from .screenshot import (
    screenshot_processor,
    screenshot_wrapper,
    screenshot_command,
    screenshot_delayed_command,
    screenshot_region_command
)

__all__ = [
    'screenshot_processor',
    'screenshot_wrapper', 
    'screenshot_command',
    'screenshot_delayed_command',
    'screenshot_region_command'
] 