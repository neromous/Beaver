"""
Beaver 样式模块

包含各种文本样式和格式化的 DSL 函数。
"""

# 导入所有样式模块以注册函数
from . import text
from . import markdown

__all__ = [
    'text',
    'markdown',
] 