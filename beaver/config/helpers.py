"""
配置辅助函数
提供便捷的配置访问方法，适配新的配置结构
"""

from typing import Dict, List, Optional, Any
from .loader import config_manager


def get_provider_config(provider: str, model: str) -> Dict[str, Any]:
    """
    获取指定提供商和模型的配置
    
    Args:
        provider: 提供商名称，如 'neko', 'yunwu'
        model: 模型名称，如 'grok-3', 'gemini-1.5-pro'
        
    Returns:
        配置字典
    """
    config = config_manager.load_all_configs()
    try:
        return config['providers'][provider][model]
    except KeyError:
        return {}


def get_api_config(provider: str, model: str) -> Dict[str, Any]:
    """
    获取API配置信息
    
    Args:
        provider: 提供商名称
        model: 模型名称
        
    Returns:
        API配置字典，包含 url, model, secret_key
    """
    provider_config = get_provider_config(provider, model)
    return provider_config.get('api', {})


def get_model_config(provider: str, model: str) -> Dict[str, Any]:
    """
    获取模型参数配置
    
    Args:
        provider: 提供商名称
        model: 模型名称
        
    Returns:
        模型配置字典，包含 temperature, top_p 等
    """
    provider_config = get_provider_config(provider, model)
    return provider_config.get('model', {})


def get_default_provider() -> Dict[str, str]:
    """
    获取默认提供商配置
    
    Returns:
        包含 provider 和 model 的字典
    """
    # 临时修复：直接从文件读取避免配置合并问题
    try:
        import json
        import os
        config_file = 'configs/ai_providers.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config.get('default', {})
    except Exception:
        pass
    return {}


def get_default_config() -> Dict[str, Any]:
    """
    获取默认提供商的完整配置
    
    Returns:
        默认配置字典
    """
    default = get_default_provider()
    if default and 'provider' in default and 'model' in default:
        return get_provider_config(default['provider'], default['model'])
    return {}


def list_providers() -> List[str]:
    """
    列出所有可用的提供商
    
    Returns:
        提供商名称列表
    """
    providers_config = config_manager.get_config('providers', {})
    return list(providers_config.keys())


def list_models(provider: str) -> List[str]:
    """
    列出指定提供商的所有模型
    
    Args:
        provider: 提供商名称
        
    Returns:
        模型名称列表
    """
    provider_config = config_manager.get_config(f'providers/{provider}', {})
    return list(provider_config.keys())


def list_all_provider_models() -> List[Dict[str, str]]:
    """
    列出所有提供商和模型的组合
    
    Returns:
        包含 provider 和 model 的字典列表
    """
    result = []
    for provider in list_providers():
        for model in list_models(provider):
            result.append({
                'provider': provider,
                'model': model,
                'full_name': f"{provider}/{model}"
            })
    return result


def get_settings() -> Dict[str, Any]:
    """
    获取全局设置
    
    Returns:
        设置字典
    """
    return config_manager.get_config('settings', {})


def get_setting(key: str, default: Any = None) -> Any:
    """
    获取指定设置项
    
    Args:
        key: 设置键名
        default: 默认值
        
    Returns:
        设置值
    """
    settings = get_settings()
    return settings.get(key, default)


def validate_provider_config(provider: str, model: str) -> Dict[str, Any]:
    """
    验证提供商配置的完整性
    
    Args:
        provider: 提供商名称
        model: 模型名称
        
    Returns:
        验证结果字典，包含 valid, missing_fields, warnings
    """
    config = get_provider_config(provider, model)
    api_config = config.get('api', {})
    
    required_api_fields = ['url', 'model', 'secret_key']
    missing_fields = [field for field in required_api_fields if not api_config.get(field)]
    
    warnings = []
    
    # 检查密钥长度
    secret_key = api_config.get('secret_key', '')
    if secret_key and len(secret_key) < 10:
        warnings.append('密钥长度可能过短')
    
    # 检查URL格式
    url = api_config.get('url', '')
    if url and not (url.startswith('http://') or url.startswith('https://')):
        warnings.append('API URL 格式可能不正确')
    
    return {
        'valid': len(missing_fields) == 0,
        'missing_fields': missing_fields,
        'warnings': warnings,
        'config': config
    }


def find_provider_by_model_name(model_name: str) -> List[Dict[str, str]]:
    """
    根据模型名称查找提供商
    
    Args:
        model_name: 模型名称（支持部分匹配）
        
    Returns:
        匹配的提供商模型组合列表
    """
    results = []
    all_combinations = list_all_provider_models()
    
    for combo in all_combinations:
        if model_name.lower() in combo['model'].lower():
            results.append(combo)
    
    return results


# 向后兼容的函数（兼容旧的配置格式）
def get_legacy_api_config(provider_model: str) -> Dict[str, Any]:
    """
    向后兼容函数：支持旧格式的提供商/模型访问
    
    Args:
        provider_model: 格式如 'neko/grok-3' 的字符串
        
    Returns:
        API配置字典
    """
    if '/' in provider_model:
        provider, model = provider_model.split('/', 1)
        return get_api_config(provider, model)
    else:
        # 尝试作为默认配置处理
        if provider_model == 'default':
            return get_api_config(**get_default_provider())
        return {}


def migrate_legacy_config(legacy_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    将旧格式配置迁移到新格式
    
    Args:
        legacy_config: 旧格式的配置字典
        
    Returns:
        新格式的配置字典
    """
    new_config = {
        'providers': {},
        'default': {
            'provider': 'openrouter',
            'model': 'gemini-2.5-flash'
        },
        'settings': {
            'cache_enabled': True,
            'timeout': 30,
            'retry_attempts': 3,
            'log_level': 'INFO'
        }
    }
    
    for key, value in legacy_config.items():
        if key == 'default':
            # 处理默认配置
            api_url = value.get('api/url', '')
            api_model = value.get('api/model', '')
            
            if 'openrouter' in api_url:
                new_config['default'] = {'provider': 'openrouter', 'model': 'gemini-2.5-flash'}
            continue
        
        # 解析提供商/模型
        if '/' in key:
            parts = key.split('/')
            if len(parts) == 2:
                provider, model = parts
                
                # 创建提供商结构
                if provider not in new_config['providers']:
                    new_config['providers'][provider] = {}
                
                # 转换配置
                api_config = {}
                model_config = {}
                
                for old_key, old_value in value.items():
                    if old_key.startswith('api/'):
                        new_key = old_key.replace('api/', '')
                        if new_key == 'sk':
                            new_key = 'secret_key'
                        api_config[new_key] = old_value
                    elif old_key.startswith('model/'):
                        new_key = old_key.replace('model/', '')
                        model_config[new_key] = old_value
                
                provider_config = {'api': api_config}
                if model_config:
                    provider_config['model'] = model_config
                
                new_config['providers'][provider][model] = provider_config
    
    return new_config 