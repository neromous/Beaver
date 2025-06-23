"""
全局注册表模块

管理所有 DSL 函数的注册和查询。
"""

from typing import Dict, Any, Optional, Callable

# 全局注册表：cmd → {'fn': callable, 'meta': {...}}
REGISTRY: Dict[str, Dict[str, Any]] = {}


class RegistryManager:
    """注册表管理器"""
    
    @staticmethod
    def register(name: str, fn: Callable, meta: Dict[str, Any]) -> None:
        """
        注册一个 DSL 函数
        
        Args:
            name: 命令名称
            fn: 函数对象
            meta: 元数据字典
        """
        REGISTRY[name] = {'fn': fn, 'meta': meta}
    
    @staticmethod
    def get_function(name: str) -> Optional[Callable]:
        """
        获取已注册的函数
        
        Args:
            name: 命令名称
            
        Returns:
            函数对象，如果不存在则返回 None
        """
        entry = REGISTRY.get(name)
        return entry['fn'] if entry else None
    
    @staticmethod
    def get_metadata(name: str) -> Optional[Dict[str, Any]]:
        """
        获取命令的元数据
        
        Args:
            name: 命令名称
            
        Returns:
            元数据字典，如果不存在则返回 None
        """
        entry = REGISTRY.get(name)
        return entry['meta'] if entry else None
    
    @staticmethod
    def list_commands() -> Dict[str, Dict[str, Any]]:
        """
        列出所有已注册的命令
        
        Returns:
            命令名称到元数据的映射
        """
        return {k: v['meta'] for k, v in REGISTRY.items()}
    
    @staticmethod
    def list_by_category(category: str) -> Dict[str, Dict[str, Any]]:
        """
        按类别列出命令
        
        Args:
            category: 类别名称
            
        Returns:
            该类别下的命令映射
        """
        return {
            k: v['meta'] 
            for k, v in REGISTRY.items() 
            if v['meta'].get('category') == category
        }
    
    @staticmethod
    def command_exists(name: str) -> bool:
        """
        检查命令是否存在
        
        Args:
            name: 命令名称
            
        Returns:
            命令是否存在
        """
        return name in REGISTRY
    
    @staticmethod
    def clear() -> None:
        """清空注册表（主要用于测试）"""
        REGISTRY.clear()


def bf_help(cmd: Optional[str] = None) -> Dict[str, Any]:
    """
    Help 系统
    
    Args:
        cmd: 命令名称，如果为 None 则显示所有命令
        
    Returns:
        命令的元数据或所有命令的元数据映射
        
    Raises:
        KeyError: 当指定的命令不存在时
    """
    if cmd is None:
        return RegistryManager.list_commands()
    
    if not RegistryManager.command_exists(cmd):
        raise KeyError(f'Command `{cmd}` 未注册')
    
    return RegistryManager.get_metadata(cmd) 