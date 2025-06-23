"""
配置加载器 - 支持从多种来源加载JSON配置文件

功能特性：
- 支持多个配置文件路径
- 支持相对路径和绝对路径
- 支持环境变量替换
- 配置缓存和自动重载
- 路径键访问（如 'api/url'）
- 配置合并和继承
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from .exceptions import ConfigError, ConfigNotFoundError, ConfigParseError


class ConfigLoader:
    """配置加载器"""
    
    def __init__(self):
        self._configs: Dict[str, Dict] = {}
        self._config_files: List[str] = []
        self._cache_enabled = True
        
    def add_config_file(self, file_path: Union[str, Path]) -> 'ConfigLoader':
        """
        添加配置文件路径
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            返回自身以支持链式调用
        """
        file_path = str(file_path)
        if file_path not in self._config_files:
            self._config_files.append(file_path)
        return self
    
    def add_config_files(self, file_paths: List[Union[str, Path]]) -> 'ConfigLoader':
        """
        批量添加配置文件路径
        
        Args:
            file_paths: 配置文件路径列表
            
        Returns:
            返回自身以支持链式调用
        """
        for file_path in file_paths:
            self.add_config_file(file_path)
        return self
    
    def load_config(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        加载单个配置文件
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            配置字典
            
        Raises:
            ConfigNotFoundError: 配置文件不存在
            ConfigParseError: 配置文件解析失败
        """
        file_path = str(file_path)
        
        # 尝试不同的路径解析方式
        resolved_path = self._resolve_path(file_path)
        
        if not os.path.exists(resolved_path):
            raise ConfigNotFoundError(f"配置文件不存在: {file_path} (解析为: {resolved_path})")
        
        try:
            with open(resolved_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 进行环境变量替换
            content = self._substitute_env_vars(content)
            
            # 解析JSON
            config = json.loads(content)
            
            # 缓存配置
            if self._cache_enabled:
                self._configs[file_path] = config
                
            return config
            
        except json.JSONDecodeError as e:
            raise ConfigParseError(f"配置文件解析失败: {file_path}, 错误: {str(e)}")
        except Exception as e:
            raise ConfigError(f"加载配置文件时发生错误: {file_path}, 错误: {str(e)}")
    
    def load_all_configs(self) -> Dict[str, Any]:
        """
        加载所有配置文件并合并
        
        Returns:
            合并后的配置字典
        """
        merged_config = {}
        
        for file_path in self._config_files:
            try:
                config = self.load_config(file_path)
                merged_config = self._merge_configs(merged_config, config)
            except ConfigNotFoundError:
                # 配置文件不存在时继续加载其他文件
                continue
                
        return merged_config
    
    def get_config(self, key: Optional[str] = None, default: Any = None, file_path: Optional[str] = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持路径形式如 'api/url'，None表示获取整个配置
            default: 默认值
            file_path: 指定配置文件，None表示使用合并后的所有配置
            
        Returns:
            配置值
        """
        if file_path:
            # 获取指定文件的配置
            if file_path not in self._configs:
                try:
                    self.load_config(file_path)
                except (ConfigNotFoundError, ConfigParseError):
                    return default
            config = self._configs.get(file_path, {})
        else:
            # 获取合并后的所有配置
            config = self.load_all_configs()
        
        if key is None:
            return config
            
        # 支持路径键访问，如 'api/url'
        return self._get_nested_value(config, key, default)
    
    def get_section(self, section: str, default: Optional[Dict] = None) -> Dict[str, Any]:
        """
        获取配置部分
        
        Args:
            section: 配置部分名称
            default: 默认值
            
        Returns:
            配置部分字典
        """
        config = self.load_all_configs()
        return config.get(section, default or {})
    
    def list_sections(self) -> List[str]:
        """
        列出所有配置部分
        
        Returns:
            配置部分名称列表
        """
        config = self.load_all_configs()
        return list(config.keys())
    
    def has_section(self, section: str) -> bool:
        """
        检查是否存在指定配置部分
        
        Args:
            section: 配置部分名称
            
        Returns:
            是否存在
        """
        return section in self.list_sections()
    
    def reload_config(self, file_path: Optional[str] = None) -> 'ConfigLoader':
        """
        重新加载配置
        
        Args:
            file_path: 指定文件路径，None表示重新加载所有
            
        Returns:
            返回自身以支持链式调用
        """
        if file_path:
            if file_path in self._configs:
                del self._configs[file_path]
        else:
            self._configs.clear()
        return self
    
    def set_cache_enabled(self, enabled: bool) -> 'ConfigLoader':
        """
        设置是否启用配置缓存
        
        Args:
            enabled: 是否启用
            
        Returns:
            返回自身以支持链式调用
        """
        self._cache_enabled = enabled
        if not enabled:
            self._configs.clear()
        return self
    
    def _resolve_path(self, file_path: str) -> str:
        """解析文件路径"""
        # 如果是绝对路径，直接返回
        if os.path.isabs(file_path):
            return file_path
        
        # 尝试相对于当前工作目录
        if os.path.exists(file_path):
            return os.path.abspath(file_path)
        
        # 尝试相对于项目根目录
        project_root = self._find_project_root()
        if project_root:
            full_path = os.path.join(project_root, file_path)
            if os.path.exists(full_path):
                return full_path
        
        # 尝试相对于资源目录
        resource_paths = [
            os.path.join(project_root or '', 'resources', file_path) if project_root else None,
            os.path.join(project_root or '', 'config', file_path) if project_root else None,
            os.path.join(os.path.expanduser('~'), '.config', 'beaver', file_path),
        ]
        
        for path in resource_paths:
            if path and os.path.exists(path):
                return path
        
        # 如果都找不到，返回原路径
        return file_path
    
    def _find_project_root(self) -> Optional[str]:
        """查找项目根目录"""
        current = os.getcwd()
        while current != os.path.dirname(current):
            # 查找标志性文件
            for marker in ['requirements.txt', 'setup.py', 'pyproject.toml', '.git']:
                if os.path.exists(os.path.join(current, marker)):
                    return current
            current = os.path.dirname(current)
        return None
    
    def _substitute_env_vars(self, content: str) -> str:
        """替换环境变量"""
        # 支持 ${VAR} 和 $VAR 格式
        def replace_var(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, match.group(0))
        
        # 替换 ${VAR} 格式
        content = re.sub(r'\$\{([^}]+)\}', replace_var, content)
        # 替换 $VAR 格式
        content = re.sub(r'\$([A-Za-z_][A-Za-z0-9_]*)', replace_var, content)
        
        return content
    
    def _merge_configs(self, base: Dict, override: Dict) -> Dict:
        """合并配置字典"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def _get_nested_value(self, config: Dict, key: str, default: Any = None) -> Any:
        """获取嵌套配置值，支持 '/' 分隔的路径"""
        try:
            current = config
            parts = key.split('/')
            
            # 处理第一层键（如 'default'）
            if len(parts) >= 1:
                current = current[parts[0]]
                
            # 如果还有更多部分，组合成完整的子键
            if len(parts) > 1:
                sub_key = '/'.join(parts[1:])
                current = current[sub_key]
                
            return current
        except (KeyError, TypeError):
            return default


# 全局配置管理器实例
config_manager = ConfigLoader()

# 自动添加常见的配置文件路径
config_manager.add_config_files([
    'config.json',
    'resources/config.json',
    'config/config.json',
    'configs/ai_providers.json',  # 添加AI提供商配置文件
    'resources/config_new.json',  # 添加新的配置文件
    os.path.expanduser('~/.config/beaver/config.json')
])


def load_config_from_resources() -> Dict[str, Any]:
    """
    便捷函数：从resources目录加载config.json
    
    Returns:
        配置字典
    """
    try:
        return config_manager.load_config('resources/config.json')
    except (ConfigNotFoundError, ConfigParseError) as e:
        print(f"警告: {e}")
        return {}


def get_api_config(provider: str = 'default') -> Dict[str, Any]:
    """
    便捷函数：获取API配置
    
    Args:
        provider: 提供商名称，如 'default', 'neko/grok-3' 等
        
    Returns:
        API配置字典
    """
    config = config_manager.get_config()
    return config.get(provider, {})


def list_api_providers() -> List[str]:
    """
    便捷函数：列出所有API提供商
    
    Returns:
        提供商名称列表
    """
    config = config_manager.get_config()
    return [key for key in config.keys() if isinstance(config[key], dict) and 'api/url' in config[key]] 