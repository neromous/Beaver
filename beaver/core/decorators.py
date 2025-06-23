"""
核心装饰器模块

提供用于注册 DSL 函数的装饰器。
"""

from functools import wraps
from typing import Dict, Any, Callable
from beaver.core.registry import REGISTRY


def bf_element(name: str, **meta: Any) -> Callable:
    """
    装饰器：注册 DSL 元素并附带元数据
    
    Args:
        name: DSL 命令名称
        **meta: 元数据，如 description, category, usage 等
    
    Returns:
        装饰器函数
    
    Example:
        @bf_element('note/create', description='创建笔记', category='Note')
        def note_create(title, content): 
            return {'title': title, 'content': content}
    """
    def decorator(fn: Callable) -> Callable:
        # 注册到全局注册表
        REGISTRY[name] = {'fn': fn, 'meta': meta}

        @wraps(fn)  # 维持原函数签名 & 文档
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper
    return decorator 