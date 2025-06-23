#!/usr/bin/env python3
"""
Beaver Nexus Messages Module

消息向量到映射的转换模块
目标：将 '[":user" "foo" "bar"]' 转换为 {"role": "user", "content": "...."}
支持多媒体内容：[":user", "text", [":file.upload/img", "path"]] -> message-with-media

三层架构：
1. 原始功能函数
2. Wrapper 函数（文本化结果）
3. 注册函数（DSL 命令）
"""

from typing import Dict, List, Any, Optional, Union
import json


def _is_upload_command(item: Any) -> bool:
    """检查一个项目是否是文件上传命令"""
    if not isinstance(item, list) or len(item) < 2:
        return False
    
    first_element = item[0]
    if not isinstance(first_element, str):
        return False
    
    upload_commands = [
        ":file.upload/img",
        ":file.upload/video", 
        ":file.upload/audio",
        ":file.upload/get-data"
    ]
    
    return first_element in upload_commands


def _execute_upload_command(upload_cmd: List[str]) -> Optional[Dict[str, Any]]:
    """执行文件上传命令并返回媒体字典"""
    try:
        from beaver.file_io.upload import file_upload_processor
        
        if len(upload_cmd) < 2:
            return None
            
        command = upload_cmd[0]
        
        if command == ":file.upload/img":
            file_path = upload_cmd[1]
            detail = upload_cmd[2] if len(upload_cmd) > 2 else "auto"
            
            result = file_upload_processor(file_path, "image", detail)
            if result["success"]:
                return result["result"]["media_dict"]
                
        elif command == ":file.upload/video":
            file_path = upload_cmd[1]
            
            result = file_upload_processor(file_path, "video")
            if result["success"]:
                return result["result"]["media_dict"]
                
        elif command == ":file.upload/audio":
            file_path = upload_cmd[1]
            
            result = file_upload_processor(file_path, "audio")
            if result["success"]:
                return result["result"]["media_dict"]
                
        elif command == ":file.upload/get-data":
            if len(upload_cmd) < 3:
                return None
            file_path = upload_cmd[1]
            media_type = upload_cmd[2]
            
            result = file_upload_processor(file_path, media_type)
            if result["success"]:
                return result["result"]["media_dict"]
        
        return None
        
    except Exception:
        return None


def _process_content_with_media(content_parts: List[Any]) -> Union[str, List[Dict[str, Any]]]:
    """
    处理可能包含媒体的内容部分
    
    参数:
        content_parts: 内容部分列表，可能包含文本和上传命令
    
    返回:
        Union[str, List[Dict]]: 纯文本或包含媒体的内容数组
    """
    if not content_parts:
        return ""
    
    text_parts = []
    media_items = []
    
    for part in content_parts:
        if _is_upload_command(part):
            # 这是一个文件上传命令
            media_dict = _execute_upload_command(part)
            if media_dict:
                media_items.append(media_dict)
        else:
            # 这是文本内容
            text_parts.append(str(part))
    
    # 如果没有媒体项目，返回纯文本
    if not media_items:
        return " ".join(text_parts) if text_parts else ""
    
    # 如果有媒体项目，构建内容数组
    content_array = []
    
    # 添加文本内容（如果有）
    text_content = " ".join(text_parts).strip()
    if text_content:
        content_array.append({
            "type": "text",
            "text": text_content
        })
    
    # 添加媒体项目
    content_array.extend(media_items)
    
    return content_array


# ================================
# 第一层：原始功能函数
# ================================

def vector_to_message_converter(vector: List[Any]) -> Dict[str, Any]:
    """
    将向量格式转换为消息映射格式
    支持多媒体内容（文本+图片/视频/音频）
    
    参数:
        vector: 向量格式，如 [":user", "hello", "world"] 或 [":user", "text", [":file.upload/img", "path"]]
    
    返回:
        Dict[str, Any]: 消息映射，如 {"role": "user", "content": "hello world"} 
                       或 {"role": "user", "content": [{"type": "text", "text": "..."}, {"type": "image_url", ...}]}
    
    异常:
        ValueError: 无效的向量格式
    """
    if not isinstance(vector, list) or len(vector) < 1:
        raise ValueError("向量必须是包含至少1个元素的列表")
    
    # 提取角色（第一个元素，去掉冒号前缀）
    role_element = vector[0]
    if not isinstance(role_element, str) or not role_element.startswith(':'):
        raise ValueError(f"第一个元素必须是角色关键字（以:开头），得到: {role_element}")
    
    role = role_element[1:]  # 去掉冒号前缀
    
    # 验证角色有效性
    valid_roles = ["system", "user", "assistant", "function", "tool"]
    if role not in valid_roles:
        raise ValueError(f"无效的角色: {role}，有效角色: {valid_roles}")
    
    # 提取内容（剩余元素）
    content_parts = vector[1:]
    
    if len(content_parts) == 0:
        content = ""
    else:
        # 处理可能包含媒体的内容
        content = _process_content_with_media(content_parts)
    
    return {
        "role": role,
        "content": content
    }


def message_list_converter(vector_list: List[List[str]]) -> List[Dict[str, str]]:
    """
    将多个向量转换为消息列表
    
    参数:
        vector_list: 向量列表，如 [[":user", "hello"], [":assistant", "hi"]]
    
    返回:
        List[Dict[str, str]]: 消息列表
    """
    if not isinstance(vector_list, list):
        raise ValueError("输入必须是列表")
    
    messages = []
    for i, vector in enumerate(vector_list):
        try:
            message = vector_to_message_converter(vector)
            messages.append(message)
        except Exception as e:
            raise ValueError(f"转换第{i+1}个向量时失败: {e}")
    
    return messages


def message_validator(message: Dict[str, str]) -> bool:
    """
    验证消息格式是否正确
    
    参数:
        message: 消息字典
    
    返回:
        bool: 是否有效
    """
    if not isinstance(message, dict):
        return False
    
    # 转换EDN关键字格式为Python字符串
    normalized_message = {}
    for key, value in message.items():
        # 处理EDN关键字（如 ':role' -> 'role'）
        if isinstance(key, str) and key.startswith(':'):
            normalized_key = key[1:]
        else:
            normalized_key = key
        normalized_message[normalized_key] = value
    
    # 检查必需字段
    if "role" not in normalized_message or "content" not in normalized_message:
        return False
    
    # 检查角色有效性
    valid_roles = ["system", "user", "assistant", "function", "tool"]
    if normalized_message["role"] not in valid_roles:
        return False
    
    # 检查内容类型
    if not isinstance(normalized_message["content"], str):
        return False
    
    return True


def message_to_vector_converter(message: Dict[str, str]) -> List[str]:
    """
    将消息映射转换回向量格式（反向转换）
    
    参数:
        message: 消息字典，如 {"role": "user", "content": "hello world"}
    
    返回:
        List[str]: 向量格式，如 [":user", "hello", "world"]
    """
    if not message_validator(message):
        raise ValueError("无效的消息格式")
    
    # 转换EDN关键字格式为Python字符串
    normalized_message = {}
    for key, value in message.items():
        # 处理EDN关键字（如 ':role' -> 'role'）
        if isinstance(key, str) and key.startswith(':'):
            normalized_key = key[1:]
        else:
            normalized_key = key
        normalized_message[normalized_key] = value
    
    role = f":{normalized_message['role']}"
    content = normalized_message['content']
    
    # 如果内容为空，只返回角色
    if not content.strip():
        return [role]
    
    # 如果内容包含空格，保持为单个字符串
    # 否则按空格分割
    if ' ' in content:
        return [role, content]
    else:
        return [role, content]


# ================================
# 第二层：Wrapper 函数（文本化结果）
# ================================

def vector_to_message_wrapper(vector: List[Any]) -> str:
    """
    向量到消息转换的wrapper函数，返回文本化结果
    支持多媒体内容显示
    
    参数:
        vector: 向量格式
    
    返回:
        str: 转换结果的文本描述
    """
    try:
        result = vector_to_message_converter(vector)
        
        output_lines = [
            f"✅ 消息转换成功",
            f"👤 角色: {result['role']}"
        ]
        
        # 处理内容显示
        content = result['content']
        if isinstance(content, str):
            # 纯文本内容
            output_lines.append(f"💬 内容: {content}")
        elif isinstance(content, list):
            # 多媒体内容
            output_lines.append(f"📱 多媒体内容 ({len(content)} 项):")
            
            for i, item in enumerate(content, 1):
                if item.get('type') == 'text':
                    output_lines.append(f"  {i}. 📝 文本: {item['text']}")
                elif item.get('type') == 'image_url':
                    detail = item.get('image_url', {}).get('detail', 'auto')
                    output_lines.append(f"  {i}. 🖼️ 图片 (详细级别: {detail})")
                elif item.get('type') == 'video':
                    filename = item.get('video', {}).get('filename', '未知文件')
                    output_lines.append(f"  {i}. 🎬 视频: {filename}")
                elif item.get('type') == 'audio':
                    filename = item.get('audio', {}).get('filename', '未知文件')
                    output_lines.append(f"  {i}. 🎵 音频: {filename}")
                else:
                    output_lines.append(f"  {i}. ❓ 未知类型: {item.get('type', 'N/A')}")
        
        return "\n".join(output_lines)
        
    except Exception as e:
        return f"❌ 转换失败: {e}"


def message_list_wrapper(vector_list: List[List[str]]) -> str:
    """
    消息列表转换的wrapper函数
    
    参数:
        vector_list: 向量列表
    
    返回:
        str: 转换结果的文本描述
    """
    try:
        messages = message_list_converter(vector_list)
        result_lines = [f"✓ 成功转换 {len(messages)} 条消息:"]
        
        for i, msg in enumerate(messages, 1):
            result_lines.append(f"{i}. [{msg['role']}] {msg['content']}")
        
        return "\n".join(result_lines)
    except Exception as e:
        return f"✗ 批量转换失败: {e}"


def message_validator_wrapper(message: Dict[str, str]) -> str:
    """
    消息验证的wrapper函数
    
    参数:
        message: 消息字典
    
    返回:
        str: 验证结果的文本描述
    """
    is_valid = message_validator(message)
    
    if is_valid:
        return f"✓ 消息格式有效: {message}"
    else:
        return f"✗ 消息格式无效: {message}"


def message_to_vector_wrapper(message: Dict[str, str]) -> str:
    """
    消息到向量转换的wrapper函数
    
    参数:
        message: 消息字典
    
    返回:
        str: 转换结果的文本描述
    """
    try:
        vector = message_to_vector_converter(message)
        return f"✓ 反向转换成功: {vector}"
    except Exception as e:
        return f"✗ 反向转换失败: {e}"


def message_batch_format_wrapper(messages: List[Dict[str, str]]) -> str:
    """
    消息批量格式化wrapper函数
    
    参数:
        messages: 消息列表
    
    返回:
        str: 格式化的消息内容
    """
    try:
        if not messages:
            return "✗ 消息列表为空"
        
        result_lines = []
        for i, msg in enumerate(messages, 1):
            if message_validator(msg):
                result_lines.append(f"[{msg['role']}] {msg['content']}")
            else:
                result_lines.append(f"[无效消息] {msg}")
        
        return "\n".join(result_lines)
    except Exception as e:
        return f"✗ 批量格式化失败: {e}"


# ================================
# 第三层：注册函数（DSL 命令）
# ================================

from beaver.core.decorators import bf_element

@bf_element(
    ':msg/v2m',
    description='将向量格式转换为消息映射',
    category='Messages',
    usage="[':msg/v2m', [':user', 'hello', 'world']]")
def vector_to_message_command(vector: List[str]):
    """
    处理向量到消息转换命令
    
    用法: [:msg/v2m [":user", "hello", "world"]]
    输出: {"role": "user", "content": "hello world"}
    """
    if not isinstance(vector, list):
        return "✗ 参数必须是向量（列表）格式"
    
    try:
        result = vector_to_message_converter(vector)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"✗ 转换失败: {e}"

@bf_element(
    ':msg/vector-to-message',
    description='将向量格式转换为消息映射（完整名称）',
    category='Messages',
    usage="[':msg/vector-to-message', [':user', 'hello']]")
def vector_to_message_full_command(vector: List[str]):
    """向量到消息转换的完整命令名称"""
    return vector_to_message_command(vector)

@bf_element(
    ':msg/batch',
    description='批量转换向量列表为消息列表',
    category='Messages',
    usage="[':msg/batch', [[':user', 'hello'], [':assistant', 'hi']]]")
def message_list_command(vector_list: List[List[str]]):
    """
    处理消息列表转换命令
    
    用法: [:msg/batch [[":user", "hello"], [":assistant", "hi"]]]
    """
    if not isinstance(vector_list, list):
        return "✗ 参数必须是向量列表"
    
    try:
        messages = message_list_converter(vector_list)
        return json.dumps(messages, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"✗ 批量转换失败: {e}"

@bf_element(
    ':msg/list-convert',
    description='批量转换向量列表为消息列表（完整名称）',
    category='Messages',
    usage="[':msg/list-convert', [向量列表]]")
def message_list_full_command(vector_list: List[List[str]]):
    """消息列表转换的完整命令名称"""
    return message_list_command(vector_list)

@bf_element(
    ':msg/check',
    description='验证消息格式是否正确',
    category='Messages',
    usage="[':msg/check', {'role': 'user', 'content': 'hello'}]")
def message_validator_command(message: Dict[str, str]):
    """
    处理消息验证命令
    
    用法: [:msg/check {"role": "user", "content": "hello"}]
    """
    return message_validator_wrapper(message)

@bf_element(
    ':msg/validate',
    description='验证消息格式是否正确（完整名称）',
    category='Messages',
    usage="[':msg/validate', {消息字典}]")
def message_validator_full_command(message: Dict[str, str]):
    """消息验证的完整命令名称"""
    return message_validator_command(message)

@bf_element(
    ':msg/m2v',
    description='将消息映射转换回向量格式',
    category='Messages',
    usage="[':msg/m2v', {'role': 'user', 'content': 'hello world'}]")
def message_to_vector_command(message: Dict[str, str]):
    """
    处理消息到向量转换命令
    
    用法: [:msg/m2v {"role": "user", "content": "hello world"}]
    """
    if not isinstance(message, dict):
        return "✗ 参数必须是消息字典"
    
    return message_to_vector_wrapper(message)

@bf_element(
    ':msg/message-to-vector',
    description='将消息映射转换回向量格式（完整名称）',
    category='Messages',
    usage="[':msg/message-to-vector', {消息字典}]")
def message_to_vector_full_command(message: Dict[str, str]):
    """消息到向量转换的完整命令名称"""
    return message_to_vector_command(message)

@bf_element(
    ':msg/fmt',
    description='格式化显示消息列表',
    category='Messages',
    usage="[':msg/fmt', [消息列表]]")
def message_format_command(messages: List[Dict[str, str]]):
    """
    处理消息格式化命令
    
    用法: [:msg/fmt [消息列表]]
    """
    if not isinstance(messages, list):
        return "✗ 参数必须是消息列表"
    
    return message_batch_format_wrapper(messages)

@bf_element(
    ':msg/format',
    description='格式化显示消息列表（完整名称）',
    category='Messages',
    usage="[':msg/format', [消息列表]]")
def message_format_full_command(messages: List[Dict[str, str]]):
    """消息格式化的完整命令名称"""
    return message_format_command(messages)


# ================================
# 快捷命令：直接角色命令
# ================================

@bf_element(
    ':user',
    description='创建用户消息（支持多媒体）',
    category='Messages',
    usage="[':user', 'text'] 或 [':user', 'text', [':file.upload/img', 'path']]")
def user_message_command(*content_parts):
    """
    用户消息快捷命令，支持多媒体内容
    
    用法:
    - [:user "hello world"] - 纯文本消息
    - [:user "看这个图片" [":file.upload/img" "image.jpg"]] - 文本+图片
    - [:user "分析视频" [":file.upload/video" "video.mp4"]] - 文本+视频
    - [:user [":file.upload/img" "image.jpg"]] - 纯图片消息
    """
    try:
        # 构建向量格式：[":user", ...content_parts]
        vector = [":user"] + list(content_parts)
        
        # 使用现有的转换器
        result = vector_to_message_converter(vector)
        
        # 返回JSON格式的消息
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return f"❌ 用户消息创建失败: {e}"


@bf_element(
    ':system',
    description='创建系统消息',
    category='Messages',
    usage="[':system', 'system prompt']")
def system_message_command(*content_parts):
    """
    系统消息快捷命令
    
    用法: [:system "You are a helpful assistant"]
    """
    try:
        vector = [":system"] + list(content_parts)
        result = vector_to_message_converter(vector)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"❌ 系统消息创建失败: {e}"


@bf_element(
    ':assistant',
    description='创建助手消息',
    category='Messages',
    usage="[':assistant', 'response text']")
def assistant_message_command(*content_parts):
    """
    助手消息快捷命令
    
    用法: [:assistant "Hello! How can I help you?"]
    """
    try:
        vector = [":assistant"] + list(content_parts)
        result = vector_to_message_converter(vector)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"❌ 助手消息创建失败: {e}"


@bf_element(
    ':msg/multimedia',
    description='创建多媒体消息（显示详细信息）',
    category='Messages',
    usage="[':msg/multimedia', [':user', 'text', [':file.upload/img', 'path']]]")
def multimedia_message_command(vector: List[Any]):
    """
    多媒体消息处理命令，显示详细的转换信息
    
    用法: [:msg/multimedia [":user", "描述文本", [":file.upload/img", "image.jpg"]]]
    """
    if not isinstance(vector, list):
        return "❌ 参数必须是向量（列表）格式"
    
    try:
        # 使用wrapper函数显示详细信息
        return vector_to_message_wrapper(vector)
    except Exception as e:
        return f"❌ 多媒体消息处理失败: {e}" 