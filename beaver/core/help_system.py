"""
帮助系统模块

提供 DSL 命令的帮助和搜索功能。
"""

from typing import Dict, Any, Optional, List
import re
from beaver.core.decorators import bf_element
from beaver.core.registry import RegistryManager


def format_command_help(cmd_name: str, meta: Dict[str, Any]) -> str:
    """
    格式化单个命令的简洁帮助信息
    
    Args:
        cmd_name: 命令名称
        meta: 命令元数据
        
    Returns:
        格式化后的简洁帮助字符串
    """
    description = meta.get('description', '无描述')
    
    return f"**{cmd_name}**: {description}"


def format_command_details(cmd_name: str, meta: Dict[str, Any]) -> str:
    """
    格式化单个命令的详细信息
    
    Args:
        cmd_name: 命令名称
        meta: 命令元数据
        
    Returns:
        格式化后的详细信息字符串
    """
    description = meta.get('description', '无描述')
    category = meta.get('category', '未分类')
    usage = meta.get('usage', f"['{cmd_name}']")
    
    return f"""**{cmd_name}**
📝 描述: {description}
📂 分类: {category}
💡 用法: {usage}

💡 提示: 使用 `./bf '{usage}'` 执行此命令
"""


def format_overview() -> str:
    """
    格式化功能概览
    
    Returns:
        功能概览字符串
    """
    commands = RegistryManager.list_commands()
    
    # 按分类组织命令
    categories = {}
    for cmd_name, meta in commands.items():
        category = meta.get('category', '未分类')
        if category not in categories:
            categories[category] = []
        categories[category].append((cmd_name, meta))
    
    # 定义每个分类的核心命令（最常用的）
    core_commands = {
        'Text': [':p', ':bold', ':italic', ':rows'],
        'Markdown': [':md/h1', ':md/h2', ':md/list', ':md/link'],
        'FileIO': [':file/read', ':file/write', ':file/exists'],
        'StringOps': [':str/upper', ':str/lower', ':str/replace'],
        'System': [':system/screenshot'],
        'Help': [':help', ':help/search', ':help/find'],
        'Messages': [':user', ':system', ':assistant'],
        'Nexus': [':nexus/sync', ':nexus/quick-chat'],
        'FileUpload': [':file.upload/img', ':file.upload/video'],
        '文件执行': [':edn/run', ':edn/load']
    }
    
    # 构建简洁概览
    lines = [
        "# 🚀 Beaver DSL 功能概览",
        "",
        f"📊 总计: {len(commands)} 个命令，{len(categories)} 个模块",
        ""
    ]
    
    # 按分类显示核心命令
    for category, cmd_list in sorted(categories.items()):
        # 获取该分类的核心命令
        core_cmds = core_commands.get(category, [])
        
        # 如果有核心命令，优先显示核心命令；否则显示前3个
        if core_cmds:
            display_cmds = []
            for core_cmd in core_cmds:
                # 查找该核心命令是否在当前分类中
                for cmd_name, meta in cmd_list:
                    if cmd_name == core_cmd:
                        display_cmds.append((cmd_name, meta))
                        break
            # 如果核心命令不够，补充其他命令
            if len(display_cmds) < 3:
                for cmd_name, meta in sorted(cmd_list):
                    if cmd_name not in [c[0] for c in display_cmds]:
                        display_cmds.append((cmd_name, meta))
                        if len(display_cmds) >= 3:
                            break
        else:
            # 没有定义核心命令，显示前3个
            display_cmds = sorted(cmd_list)[:3]
        
        lines.append(f"## 📂 {category} ({len(cmd_list)} 个命令)")
        
        for cmd_name, meta in display_cmds:
            description = meta.get('description', '无描述')
            lines.append(f"• **{cmd_name}**: {description}")
        
        # 如果还有更多命令，显示提示
        if len(cmd_list) > len(display_cmds):
            remaining = len(cmd_list) - len(display_cmds)
            lines.append(f"  *...还有 {remaining} 个命令*")
        
        lines.append("")
    
    # 添加使用提示
    lines.extend([
        "---",
        "",
        "💡 **使用提示**:",
        f"• `[':help', '命令名']` - 快速查看命令描述",
        f"• `[':help/find', '命令名']` - 查看命令详细用法",
        f"• `[':help/search', '关键词']` - 搜索相关命令",
        f"• 示例: `./bf '[:help \":p\"]'` 或 `./bf '[:help/find \":file/read\"]'`"
    ])
    
    return "\n".join(lines)


def search_commands(query: str) -> List[tuple]:
    """
    搜索命令
    
    Args:
        query: 搜索关键词
        
    Returns:
        匹配的命令列表 [(cmd_name, meta, score)]
    """
    commands = RegistryManager.list_commands()
    results = []
    
    query_lower = query.lower()
    query_parts = query_lower.split()
    
    for cmd_name, meta in commands.items():
        score = 0
        searchable_text = f"{cmd_name} {meta.get('description', '')} {meta.get('category', '')}".lower()
        
        # 精确匹配命令名
        if query_lower in cmd_name.lower():
            score += 100
        
        # 精确匹配描述或分类
        if query_lower in meta.get('description', '').lower():
            score += 50
        
        if query_lower in meta.get('category', '').lower():
            score += 30
        
        # 部分匹配
        for part in query_parts:
            if part in searchable_text:
                score += 10
        
        # 模糊匹配（包含查询中的字符）
        if any(char in searchable_text for char in query_lower):
            score += 1
        
        if score > 0:
            results.append((cmd_name, meta, score))
    
    # 按分数排序
    results.sort(key=lambda x: x[2], reverse=True)
    return results


def format_search_results(query: str, results: List[tuple]) -> str:
    """
    格式化搜索结果
    
    Args:
        query: 搜索关键词
        results: 搜索结果列表
        
    Returns:
        格式化后的搜索结果字符串
    """
    if not results:
        return f"🔍 未找到与 '{query}' 相关的命令\n\n💡 尝试其他关键词: 'file', 'text', 'md', 'str' 等"
    
    lines = [
        f"🔍 搜索 '{query}' 找到 {len(results)} 个命令",
        ""
    ]
    
    # 只显示前5个最相关的结果
    for i, (cmd_name, meta, score) in enumerate(results[:5]):
        description = meta.get('description', '无描述')
        category = meta.get('category', '未分类')
        
        lines.append(f"{i+1}. **{cmd_name}** ({category}) - {description}")
    
    if len(results) > 5:
        lines.append(f"\n💡 还有 {len(results) - 5} 个结果，使用 `[':help', '命令名']` 查看详情")
    
    return "\n".join(lines)


@bf_element(
    ':help',
    description='显示DSL命令的帮助信息和功能概览',
    category='Help',
    usage="[':help'] 或 [':help', '命令名']")
def help_command(cmd_name: Optional[str] = None):
    """
    DSL帮助命令 - 提供功能概览或特定命令帮助
    
    用法:
    - [:help] - 显示所有可用命令的功能概览
    - [:help "命令名"] - 显示特定命令的详细帮助
    """
    if cmd_name is None:
        # 显示功能概览
        return format_overview()
    
    # 显示特定命令帮助
    if not RegistryManager.command_exists(cmd_name):
        available_commands = list(RegistryManager.list_commands().keys())
        suggestions = [cmd for cmd in available_commands if cmd_name.lower() in cmd.lower()]
        
        error_msg = f"❌ 命令 '{cmd_name}' 不存在"
        if suggestions:
            error_msg += f"\n\n💡 您是否想要查找: {', '.join(suggestions[:5])}"
        
        return error_msg
    
    meta = RegistryManager.get_metadata(cmd_name)
    return format_command_help(cmd_name, meta)


@bf_element(
    ':help/search',
    description='搜索DSL命令，支持模糊搜索',
    category='Help', 
    usage="[':help/search', '关键词']")
def help_search_command(query: str):
    """
    DSL搜索命令 - 根据关键词搜索相关命令
    
    用法:
    - [:help/search "file"] - 搜索文件相关命令
    - [:help/search "text format"] - 搜索文本格式化相关命令
    """
    if not query or not query.strip():
        return "❌ 请提供搜索关键词\n\n💡 示例: [':help/search', 'file']"
    
    results = search_commands(query.strip())
    return format_search_results(query.strip(), results)


@bf_element(
    ':help/find',
    description='查看命令的详细信息和用法',
    category='Help',
    usage="[':help/find', '命令名']")
def help_find_command(cmd_name: str):
    """
    DSL命令详细信息查看 - 显示命令的完整详情
    
    用法:
    - [:help/find ":file/read"] - 查看文件读取命令的详细信息
    - [:help/find ":p"] - 查看段落命令的详细信息
    """
    if not cmd_name or not cmd_name.strip():
        return "❌ 请提供命令名\n\n💡 示例: [':help/find', ':file/read']"
    
    cmd_name = cmd_name.strip()
    
    # 显示命令详细信息
    if not RegistryManager.command_exists(cmd_name):
        available_commands = list(RegistryManager.list_commands().keys())
        suggestions = [cmd for cmd in available_commands if cmd_name.lower() in cmd.lower()]
        
        error_msg = f"❌ 命令 '{cmd_name}' 不存在"
        if suggestions:
            error_msg += f"\n\n💡 您是否想要查找:\n"
            for i, suggestion in enumerate(suggestions[:3], 1):
                error_msg += f"  {i}. {suggestion}\n"
        
        return error_msg
    
    meta = RegistryManager.get_metadata(cmd_name)
    return format_command_details(cmd_name, meta) 