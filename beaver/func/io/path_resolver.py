"""
路径解析器模块

用于处理文件操作中的路径解析问题，支持：
1. 检测当前工作目录 
2. 处理相对路径和绝对路径
3. 支持跨目录使用 bf 脚本
"""

import os
from pathlib import Path
from typing import Union, Optional

class PathResolver:
    """路径解析器"""
    
    def __init__(self):
        # 缓存当前工作目录，防止在脚本执行过程中变化
        self._cwd = os.getcwd()
        self._script_dir = None
        
        # 权限沙箱：允许访问的目录白名单（绝对路径列表）
        # 为空时表示不限制。
        self._allowed_dirs = []
        
    def set_script_directory(self, script_path: str) -> None:
        """
        设置脚本所在目录
        
        Args:
            script_path: 脚本文件的绝对路径
        """
        self._script_dir = os.path.dirname(os.path.abspath(script_path))
    
    def get_current_directory(self) -> str:
        """
        获取当前工作目录
        
        Returns:
            当前工作目录的绝对路径
        """
        return self._cwd
    
    def get_script_directory(self) -> Optional[str]:
        """
        获取脚本所在目录
        
        Returns:
            脚本所在目录的绝对路径，如果未设置则返回None
        """
        return self._script_dir
    
    def resolve_path(self, file_path: Union[str, Path]) -> str:
        """
        解析文件路径，将相对路径转换为绝对路径
        
        Args:
            file_path: 待解析的文件路径
            
        Returns:
            解析后的绝对路径
        """
        file_path = str(file_path)

        if os.path.isabs(file_path):
            abs_path = os.path.abspath(file_path)
        else:
            # 对于相对路径，相对于当前工作目录解析
            abs_path = os.path.abspath(os.path.join(self._cwd, file_path))
        
        # 沙箱校验
        if not self._is_path_allowed(abs_path):
            raise PermissionError(f"路径 '{file_path}' 不在允许的沙箱目录内，已被拒绝访问")
        
        return abs_path
    
    def resolve_relative_to_cwd(self, file_path: Union[str, Path]) -> str:
        """
        将路径解析为相对于当前工作目录的绝对路径
        
        Args:
            file_path: 文件路径
            
        Returns:
            相对于当前工作目录的绝对路径
        """
        file_path = str(file_path)
        
        if os.path.isabs(file_path):
            return file_path
            
        return os.path.abspath(os.path.join(self._cwd, file_path))
    
    def normalize_path(self, file_path: Union[str, Path]) -> str:
        """
        标准化路径，处理 ../ 和 ./ 等相对路径符号
        
        Args:
            file_path: 文件路径
            
        Returns:
            标准化后的路径
        """
        return os.path.normpath(str(file_path))
    
    def get_relative_path(self, file_path: Union[str, Path], base_path: Optional[str] = None) -> str:
        """
        获取相对于基础路径的相对路径
        
        Args:
            file_path: 目标文件路径
            base_path: 基础路径，默认为当前工作目录
            
        Returns:
            相对路径
        """
        if base_path is None:
            base_path = self._cwd
            
        abs_file_path = os.path.abspath(str(file_path))
        abs_base_path = os.path.abspath(base_path)
        
        return os.path.relpath(abs_file_path, abs_base_path)
    
    def is_under_directory(self, file_path: Union[str, Path], directory: Union[str, Path]) -> bool:
        """
        检查文件是否在指定目录下
        
        Args:
            file_path: 文件路径
            directory: 目录路径
            
        Returns:
            如果文件在目录下返回True，否则返回False
        """
        abs_file_path = os.path.abspath(str(file_path))
        abs_directory = os.path.abspath(str(directory))
        
        try:
            os.path.relpath(abs_file_path, abs_directory)
            return abs_file_path.startswith(abs_directory)
        except ValueError:
            # 在Windows上，如果路径在不同驱动器上会抛出ValueError
            return False
    
    def create_path_info(self, file_path: Union[str, Path]) -> dict:
        """
        创建路径信息字典
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含路径信息的字典
        """
        resolved_path = self.resolve_path(file_path)
        
        return {
            'original': str(file_path),
            'resolved': resolved_path,
            'normalized': self.normalize_path(resolved_path),
            'relative_to_cwd': self.get_relative_path(resolved_path),
            'is_absolute': os.path.isabs(str(file_path)),
            'exists': os.path.exists(resolved_path),
            'is_file': os.path.isfile(resolved_path),
            'is_directory': os.path.isdir(resolved_path),
            'dirname': os.path.dirname(resolved_path),
            'basename': os.path.basename(resolved_path),
            'current_directory': self._cwd,
            'script_directory': self._script_dir
        }

    # ---------------------------------------------------------------------
    # 允许目录白名单相关 API
    # ---------------------------------------------------------------------

    def set_allowed_directories(self, dirs):
        """一次性设置允许访问的目录白名单

        Args:
            dirs: Iterable[str | Path] 目录路径集合
        """
        abs_dirs = [os.path.abspath(str(d)) for d in dirs]
        self._allowed_dirs = abs_dirs

    def add_allowed_directory(self, dir_path):
        """向白名单追加一个目录"""
        abs_dir = os.path.abspath(str(dir_path))
        if abs_dir not in self._allowed_dirs:
            self._allowed_dirs.append(abs_dir)

    def clear_allowed_directories(self):
        """清空白名单，表示无限制"""
        self._allowed_dirs = []

    def list_allowed_directories(self):
        """返回当前白名单列表"""
        return list(self._allowed_dirs)

    # ---------------------------------------------------------------------
    # 内部工具方法
    # ---------------------------------------------------------------------

    def _is_path_allowed(self, abs_path: str) -> bool:
        """判断绝对路径是否位于白名单目录下"""
        if not self._allowed_dirs:  # 空白名单 -> 不限制
            return True

        # 确保比较时目录末尾带路径分隔符，防止 /foo 与 /foobar 混淆
        for allow_dir in self._allowed_dirs:
            allow_dir_with_sep = os.path.join(allow_dir, '')
            if abs_path.startswith(allow_dir_with_sep) or abs_path == allow_dir:
                return True
        return False

# 全局路径解析器实例
_global_resolver = PathResolver()

def get_path_resolver() -> PathResolver:
    """获取全局路径解析器实例"""
    return _global_resolver

def set_working_directory(directory: Union[str, Path]) -> None:
    """
    设置工作目录（仅影响路径解析，不改变进程的工作目录）
    
    Args:
        directory: 工作目录路径
    """
    global _global_resolver
    _global_resolver._cwd = os.path.abspath(str(directory))

def set_script_directory(script_path: str) -> None:
    """
    设置脚本目录
    
    Args:
        script_path: 脚本文件路径
    """
    global _global_resolver
    _global_resolver.set_script_directory(script_path)

def resolve_file_path(file_path: Union[str, Path]) -> str:
    """
    解析文件路径的便捷函数
    
    Args:
        file_path: 文件路径
        
    Returns:
        解析后的绝对路径
    """
    # 直接调用 PathResolver 的解析方法，其中已包含白名单校验
    return _global_resolver.resolve_path(file_path)

def get_current_directory() -> str:
    """获取当前工作目录"""
    return _global_resolver.get_current_directory()

# ============================
# 白名单便捷函数
# ============================

def set_allowed_directories(dirs):
    """一次性设置允许访问的目录白名单"""
    _global_resolver.set_allowed_directories(dirs)

def add_allowed_directory(dir_path):
    """向白名单追加一个目录"""
    _global_resolver.add_allowed_directory(dir_path)

def clear_allowed_directories():
    """清空白名单限制"""
    _global_resolver.clear_allowed_directories()

def list_allowed_directories():
    """返回白名单列表"""
    return _global_resolver.list_allowed_directories() 