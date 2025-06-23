"""
Beaver 配置管理模块

提供配置文件的加载、解析和管理功能
支持多种配置源和格式
"""

from .loader import (
    ConfigLoader, 
    config_manager, 
    load_config_from_resources, 
    get_api_config, 
    list_api_providers
)
from .helpers import (
    get_provider_config,
    get_api_config as get_new_api_config,
    get_model_config,
    get_default_provider,
    get_default_config,
    list_providers,
    list_models,
    list_all_provider_models,
    get_settings,
    get_setting,
    validate_provider_config,
    find_provider_by_model_name,
    get_legacy_api_config,
    migrate_legacy_config
)
from .exceptions import ConfigError, ConfigNotFoundError, ConfigParseError

__all__ = [
    # 核心类和管理器
    'ConfigLoader',
    'config_manager',
    
    # 基础函数（兼容旧版）
    'load_config_from_resources',
    'get_api_config',
    'list_api_providers',
    
    # 新的辅助函数
    'get_provider_config',
    'get_new_api_config',
    'get_model_config',
    'get_default_provider',
    'get_default_config',
    'list_providers',
    'list_models',
    'list_all_provider_models',
    'get_settings',
    'get_setting',
    'validate_provider_config',
    'find_provider_by_model_name',
    'get_legacy_api_config',
    'migrate_legacy_config',
    
    # 异常类
    'ConfigError',
    'ConfigNotFoundError', 
    'ConfigParseError'
] 