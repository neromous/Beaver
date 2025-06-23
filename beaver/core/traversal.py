"""
数据结构遍历工具模块

提供深度优先遍历和数据转换功能。
"""

from collections.abc import Mapping, Sequence, Set
from typing import Any, Callable, Union


def _is_atomic(x: Any) -> bool:
    """
    判定是否原子（不可再递归）
    
    Args:
        x: 待判断的对象
        
    Returns:
        是否为原子对象
    """
    return not isinstance(x, (Mapping, Sequence, Set)) or isinstance(x, (str, bytes, bytearray))


def postwalk(f: Callable[[Any], Any], data: Any) -> Any:
    """
    后序遍历并可变换数据结构
    
    Args:
        f: 转换函数，接收已遍历完子节点后的元素，返回新值
        data: 任意嵌套的 list/tuple/set/dict/原子值
        
    Returns:
        转换后的数据结构
    """
    if _is_atomic(data):
        return f(data)  # 原子直接执行 f

    # ---- 可递归结构 ----
    if isinstance(data, Mapping):
        transformed = {k: postwalk(f, v) for k, v in data.items()}
        return f(transformed)

    elif isinstance(data, list):
        transformed = [postwalk(f, v) for v in data]
        return f(transformed)

    elif isinstance(data, tuple):
        transformed = tuple(postwalk(f, v) for v in data)
        return f(transformed)

    elif isinstance(data, set):
        transformed = {postwalk(f, v) for v in data}
        return f(transformed)

    else:  # 其他可迭代类型按原样返回
        return f(data)


def prewalk(f: Callable[[Any], Any], data: Any) -> Any:
    """
    前序遍历并可变换数据结构
    
    Args:
        f: 转换函数，在遍历子节点前执行
        data: 任意嵌套的数据结构
        
    Returns:
        转换后的数据结构
    """
    transformed_data = f(data)
    
    if _is_atomic(transformed_data):
        return transformed_data

    # ---- 可递归结构 ----
    if isinstance(transformed_data, Mapping):
        return {k: prewalk(f, v) for k, v in transformed_data.items()}

    elif isinstance(transformed_data, list):
        return [prewalk(f, v) for v in transformed_data]

    elif isinstance(transformed_data, tuple):
        return tuple(prewalk(f, v) for v in transformed_data)

    elif isinstance(transformed_data, set):
        return {prewalk(f, v) for v in transformed_data}

    else:
        return transformed_data


def walk(inner: Callable[[Any], Any], outer: Callable[[Any], Any], data: Any) -> Any:
    """
    通用遍历函数
    
    Args:
        inner: 内部遍历函数
        outer: 外部转换函数
        data: 数据结构
        
    Returns:
        转换后的数据结构
    """
    if _is_atomic(data):
        return outer(data)

    if isinstance(data, Mapping):
        transformed = {k: inner(v) for k, v in data.items()}
        return outer(transformed)

    elif isinstance(data, list):
        transformed = [inner(v) for v in data]
        return outer(transformed)

    elif isinstance(data, tuple):
        transformed = tuple(inner(v) for v in data)
        return outer(transformed)

    elif isinstance(data, set):
        transformed = {inner(v) for v in data}
        return outer(transformed)

    else:
        return outer(data)


class DataWalker:
    """数据遍历器，提供更灵活的遍历控制"""
    
    def __init__(self, transform_fn: Callable[[Any], Any]):
        """
        初始化遍历器
        
        Args:
            transform_fn: 转换函数
        """
        self.transform_fn = transform_fn
        self.visit_count = 0
        self.max_depth = None
        self.current_depth = 0
    
    def set_max_depth(self, depth: int) -> None:
        """设置最大遍历深度"""
        self.max_depth = depth
    
    def walk(self, data: Any, mode: str = 'post') -> Any:
        """
        遍历数据结构
        
        Args:
            data: 待遍历的数据
            mode: 遍历模式，'pre' 或 'post'
            
        Returns:
            遍历结果
        """
        self.visit_count = 0
        self.current_depth = 0
        
        if mode == 'pre':
            return self._prewalk(data)
        else:
            return self._postwalk(data)
    
    def _postwalk(self, data: Any) -> Any:
        """内部后序遍历实现"""
        self.visit_count += 1
        
        if self.max_depth and self.current_depth >= self.max_depth:
            return data
        
        if _is_atomic(data):
            return self.transform_fn(data)

        self.current_depth += 1
        
        try:
            if isinstance(data, Mapping):
                transformed = {k: self._postwalk(v) for k, v in data.items()}
                return self.transform_fn(transformed)

            elif isinstance(data, list):
                transformed = [self._postwalk(v) for v in data]
                return self.transform_fn(transformed)

            elif isinstance(data, tuple):
                transformed = tuple(self._postwalk(v) for v in data)
                return self.transform_fn(transformed)

            elif isinstance(data, set):
                transformed = {self._postwalk(v) for v in data}
                return self.transform_fn(transformed)

            else:
                return self.transform_fn(data)
        finally:
            self.current_depth -= 1
    
    def _prewalk(self, data: Any) -> Any:
        """内部前序遍历实现"""
        self.visit_count += 1
        
        if self.max_depth and self.current_depth >= self.max_depth:
            return data
        
        transformed_data = self.transform_fn(data)
        
        if _is_atomic(transformed_data):
            return transformed_data

        self.current_depth += 1
        
        try:
            if isinstance(transformed_data, Mapping):
                return {k: self._prewalk(v) for k, v in transformed_data.items()}

            elif isinstance(transformed_data, list):
                return [self._prewalk(v) for v in transformed_data]

            elif isinstance(transformed_data, tuple):
                return tuple(self._prewalk(v) for v in transformed_data)

            elif isinstance(transformed_data, set):
                return {self._prewalk(v) for v in transformed_data}

            else:
                return transformed_data
        finally:
            self.current_depth -= 1 