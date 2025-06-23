"""
Beaver - 基于 DSL 的可扩展功能框架

主要功能：
- DSL 函数注册和调度
- 数据结构遍历和转换
- 插件化的样式和功能模块
"""

from beaver.core.decorators import bf_element
from beaver.core.dispatcher import dispatch, dispatcher_node, DSLProcessor
from beaver.core.registry import bf_help, RegistryManager
from beaver.core.traversal import postwalk, prewalk, DataWalker

# 导入样式模块（自动注册函数）
import beaver.styles.text
import beaver.styles.markdown

# 导入功能模块（自动注册函数）
import beaver.func.utils.string_ops
import beaver.func.io.file_ops

# 导入文件IO模块（自动注册函数）
# import beaver.file_io.operations  # 模块不存在，暂时注释
import beaver.file_io.upload

# 导入nexus模块（自动注册函数）
import beaver.nexus.messages
import beaver.nexus.sync_llm

# 导入system模块（自动注册函数）
import beaver.system.screenshot

# 导入CLI模块（自动注册函数）
import beaver.cli.edn_runner

# 导入帮助系统模块（自动注册函数）
import beaver.core.help_system

__version__ = "0.1.0"
__author__ = "Beaver Team"

# 主要 API
__all__ = [
    # 装饰器
    'bf_element',
    
    # 调度器
    'dispatch',
    'dispatcher_node', 
    'DSLProcessor',
    
    # 注册表
    'bf_help',
    'RegistryManager',
    
    # 遍历工具
    'postwalk',
    'prewalk',
    'DataWalker',
]


def get_version():
    """获取版本信息"""
    return __version__


def list_all_commands():
    """列出所有可用命令"""
    return RegistryManager.list_commands()


def list_commands_by_category(category: str):
    """按类别列出命令"""
    return RegistryManager.list_by_category(category)


# 便捷函数
def execute(expr):
    """执行 DSL 表达式的便捷函数"""
    return dispatch(expr)


def process_nested(expr, processor_fn=None):
    """处理嵌套 DSL 表达式的便捷函数"""
    if processor_fn is None:
        processor_fn = dispatcher_node
    return postwalk(processor_fn, expr) 