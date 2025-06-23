"""
DSL 调度器模块

负责解析和执行 DSL 表达式。
"""

from typing import List, Any, Union
from beaver.core.registry import RegistryManager


def dispatch(expr: List[Any]) -> Any:
    """
    根据 DSL 表达式调用对应的函数，支持深度递归解析嵌套表达式
    
    Args:
        expr: DSL 表达式，形如 ['command', arg1, arg2, ...]
        
    Returns:
        函数执行结果
        
    Raises:
        ValueError: 当表达式格式不正确时
        KeyError: 当命令未注册时
        
    Example:
        result = dispatch(['note/create', 'Title', 'Content'])
        result = dispatch([':file/write', 'test.txt', [':p', 'Hello ', 'World']])
    """
    if not isinstance(expr, list) or not expr:
        raise ValueError('DSL 表达式必须是非空 list')
    
    cmd, *args = expr
    
    if not isinstance(cmd, str):
        raise ValueError('DSL 命令必须是字符串')
    
    # 获取注册的函数
    fn = RegistryManager.get_function(cmd)
    if not fn:
        raise KeyError(f'Command `{cmd}` 未注册')
    
    # 深度递归解析参数中的嵌套 DSL 表达式
    # 导入 postwalk，避免循环导入
    from beaver.core.traversal import postwalk
    resolved_args = [postwalk(dispatcher_node, arg) for arg in args]
    
    # 执行函数
    return fn(*resolved_args)


def dispatcher_node(node: Any) -> Any:
    """
    节点处理器，用于 postwalk 遍历
    
    Args:
        node: 当前节点
        
    Returns:
        处理后的节点
    """
    # 若 node 是 DSL 向量（list 且首元素为 str），则执行
    if isinstance(node, list) and node and isinstance(node[0], str):
        try:
            return dispatch(node)  # 调度注册命令
        except KeyError:
            pass  # 非命令，保持原样
    return node  # 其他节点原样返回


class DSLProcessor:
    """DSL 处理器，提供更高级的处理功能"""
    
    def __init__(self):
        self.context = {}  # 执行上下文
    
    def set_context(self, **kwargs) -> None:
        """设置执行上下文"""
        self.context.update(kwargs)
    
    def process(self, expr: Union[List[Any], Any]) -> Any:
        """
        处理 DSL 表达式，支持上下文
        
        Args:
            expr: DSL 表达式或其他数据
            
        Returns:
            处理结果
        """
        if isinstance(expr, list) and expr and isinstance(expr[0], str):
            cmd = expr[0]
            args = expr[1:]
            
            # 检查是否为注册的命令
            if RegistryManager.command_exists(cmd):
                fn = RegistryManager.get_function(cmd)
                
                # 尝试注入上下文（如果函数支持）
                try:
                    # 简单的上下文注入策略
                    return fn(*args, **self.context)
                except TypeError:
                    # 如果函数不支持关键字参数，则只传位置参数
                    return fn(*args)
        
        return expr  # 非 DSL 表达式原样返回
    
    def validate_expression(self, expr: List[Any]) -> bool:
        """
        验证 DSL 表达式是否有效
        
        Args:
            expr: DSL 表达式
            
        Returns:
            是否有效
        """
        if not isinstance(expr, list) or not expr:
            return False
        
        if not isinstance(expr[0], str):
            return False
        
        return RegistryManager.command_exists(expr[0])
    
    def get_command_info(self, cmd: str) -> dict:
        """
        获取命令信息
        
        Args:
            cmd: 命令名称
            
        Returns:
            命令信息字典
        """
        if not RegistryManager.command_exists(cmd):
            return {'exists': False}
        
        meta = RegistryManager.get_metadata(cmd)
        return {
            'exists': True,
            'metadata': meta,
            'function': RegistryManager.get_function(cmd)
        } 