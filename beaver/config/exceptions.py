"""
配置管理模块的异常类
"""


class ConfigError(Exception):
    """配置相关的基础异常"""
    pass


class ConfigNotFoundError(ConfigError):
    """配置文件未找到异常"""
    pass


class ConfigParseError(ConfigError):
    """配置文件解析错误异常"""
    pass


class ConfigValidationError(ConfigError):
    """配置验证错误异常"""
    pass 