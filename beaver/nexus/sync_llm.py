#!/usr/bin/env python3
"""
Beaver Nexus Sync LLM Module

同步LLM推理模块，集成消息转换和配置管理
目标：[":nexus/sync", {"provider": "", "model": ""}, [":msg/v2m", [":user", "foo"]]]

三层架构：
1. 原始功能函数
2. Wrapper 函数（文本化结果）
3. 注册函数（DSL 命令）
"""

from typing import Dict, List, Any, Optional, Union
import json
import time


# ================================
# 第一层：原始功能函数
# ================================

def sync_llm_processor(
    config: Dict[str, str], 
    messages_expr: List[Any]
) -> Dict[str, Any]:
    """
    同步LLM推理处理器
    
    参数:
        config: 配置字典，如 {"provider": "openai", "model": "gpt-4"}
        messages_expr: 消息表达式，如 [":msg/v2m", [":user", "hello"]]
    
    返回:
        Dict[str, Any]: 推理结果，包含回复内容和元数据
    
    异常:
        ValueError: 无效的配置或消息表达式
    """
    if not isinstance(config, dict):
        raise ValueError("配置必须是字典格式")
    
    if not isinstance(messages_expr, list):
        raise ValueError("消息表达式必须是列表格式")
    
    # 转换EDN关键字格式为Python字符串
    normalized_config = {}
    for key, value in config.items():
        # 处理EDN关键字（如 ':provider' -> 'provider'）
        if isinstance(key, str) and key.startswith(':'):
            normalized_key = key[1:]
        else:
            normalized_key = key
        normalized_config[normalized_key] = value
    
    # 验证配置
    required_fields = ["provider", "model"]
    for field in required_fields:
        if field not in normalized_config:
            raise ValueError(f"配置中缺少必需字段: {field}")
        if not normalized_config[field]:
            raise ValueError(f"配置字段 {field} 不能为空")
    
    provider = normalized_config["provider"]
    model = normalized_config["model"]
    
    try:
        # 导入必要模块
        from beaver.core.dispatcher import dispatch
        from beaver.inference.sync_client import chat_with_config
        
        # 第一步：处理消息表达式，转换为消息格式
        messages_result = dispatch(messages_expr)
        
        # 检查消息转换结果
        if isinstance(messages_result, str):
            # 如果返回的是字符串，尝试解析为JSON
            try:
                messages_data = json.loads(messages_result)
            except json.JSONDecodeError:
                raise ValueError(f"消息转换失败: {messages_result}")
        else:
            messages_data = messages_result
        
        # 验证消息格式
        if isinstance(messages_data, dict):
            # 单个消息，转换为列表
            messages_list = [messages_data]
        elif isinstance(messages_data, list):
            # 消息列表
            messages_list = messages_data
        else:
            raise ValueError(f"无效的消息格式: {type(messages_data)}")
        
        # 验证消息内容
        for i, msg in enumerate(messages_list):
            if not isinstance(msg, dict):
                raise ValueError(f"第{i+1}个消息不是字典格式: {msg}")
            if "role" not in msg or "content" not in msg:
                raise ValueError(f"第{i+1}个消息缺少role或content字段: {msg}")
        
        # 第二步：调用LLM API
        start_time = time.time()
        
        # 提取最后一条用户消息作为主要提示词
        user_messages = [msg for msg in messages_list if msg["role"] == "user"]
        system_messages = [msg for msg in messages_list if msg["role"] == "system"]
        
        if not user_messages:
            raise ValueError("消息列表中必须包含至少一条用户消息")
        
        # 使用最后一条用户消息作为提示词
        prompt = user_messages[-1]["content"]
        
        # 使用第一条系统消息作为系统提示词（如果存在）
        system_prompt = system_messages[0]["content"] if system_messages else None
        
        # 调用LLM
        response_text = chat_with_config(
            prompt=prompt,
            provider=provider,
            model=model,
            system_prompt=system_prompt
        )
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        # 构建结果
        result = {
            "success": True,
            "response": response_text,
            "config": {
                "provider": provider,
                "model": model
            },
            "messages": messages_list,
            "metadata": {
                "response_time": response_time,
                "message_count": len(messages_list),
                "user_message_count": len(user_messages),
                "system_message_count": len(system_messages)
            }
        }
        
        return result
        
    except Exception as e:
        # 返回错误结果
        return {
            "success": False,
            "error": str(e),
            "config": {
                "provider": provider,
                "model": model
            },
            "messages": None,
            "metadata": {
                "response_time": 0,
                "message_count": 0
            }
        }


def batch_sync_llm_processor(
    configs_and_messages: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    批量同步LLM推理处理器
    
    参数:
        configs_and_messages: 配置和消息表达式列表
    
    返回:
        List[Dict[str, Any]]: 批量推理结果列表
    """
    if not isinstance(configs_and_messages, list):
        raise ValueError("输入必须是列表格式")
    
    results = []
    for i, item in enumerate(configs_and_messages):
        try:
            if not isinstance(item, dict):
                raise ValueError(f"第{i+1}项不是字典格式")
            
            if "config" not in item or "messages" not in item:
                raise ValueError(f"第{i+1}项缺少config或messages字段")
            
            result = sync_llm_processor(item["config"], item["messages"])
            results.append(result)
            
        except Exception as e:
            # 添加错误结果
            results.append({
                "success": False,
                "error": f"处理第{i+1}项时出错: {str(e)}",
                "config": item.get("config", {}),
                "messages": None,
                "metadata": {"response_time": 0, "message_count": 0}
            })
    
    return results


def sync_llm_validator(config: Dict[str, str]) -> Dict[str, Any]:
    """
    验证同步LLM配置是否有效
    
    参数:
        config: 配置字典
    
    返回:
        Dict[str, Any]: 验证结果
    """
    try:
        from beaver.inference.sync_client import validate_openai_config
        from beaver.config.helpers import get_api_config
        
        if not isinstance(config, dict):
            return {"valid": False, "error": "配置必须是字典格式"}
        
        # 转换EDN关键字格式为Python字符串
        normalized_config = {}
        for key, value in config.items():
            # 处理EDN关键字（如 ':provider' -> 'provider'）
            if isinstance(key, str) and key.startswith(':'):
                normalized_key = key[1:]
            else:
                normalized_key = key
            normalized_config[normalized_key] = value
        
        provider = normalized_config.get("provider")
        model = normalized_config.get("model")
        
        if not provider or not model:
            return {"valid": False, "error": "配置中缺少provider或model"}
        
        # 获取API配置
        api_config = get_api_config(provider, model)
        if not api_config:
            return {"valid": False, "error": f"未找到 {provider}/{model} 的配置"}
        
        # 验证API连接
        validation_result = validate_openai_config(
            api_url=api_config.get('url'),
            api_key=api_config.get('secret_key'),
            model=api_config.get('model')
        )
        
        return validation_result
        
    except Exception as e:
        return {"valid": False, "error": f"验证过程出错: {str(e)}"}


# ================================
# 第二层：Wrapper 函数（文本化结果）
# ================================

def sync_llm_wrapper(config: Dict[str, str], messages_expr: List[Any]) -> str:
    """
    同步LLM推理的wrapper函数，返回文本化结果
    
    参数:
        config: 配置字典
        messages_expr: 消息表达式
    
    返回:
        str: 推理结果的文本描述
    """
    try:
        result = sync_llm_processor(config, messages_expr)
        
        if result["success"]:
            provider = result["config"]["provider"]
            model = result["config"]["model"]
            response_time = result["metadata"]["response_time"]
            message_count = result["metadata"]["message_count"]
            
            output_lines = [
                f"🤖 LLM推理成功 [{provider}/{model}]",
                f"⏱️ 响应时间: {response_time}秒",
                f"📨 处理消息数: {message_count}",
                "",
                "💬 AI回复:",
                result["response"]
            ]
            
            return "\n".join(output_lines)
        else:
            provider = result["config"]["provider"]
            model = result["config"]["model"]
            
            return f"❌ LLM推理失败 [{provider}/{model}]: {result['error']}"
            
    except Exception as e:
        return f"❌ 推理过程异常: {str(e)}"


def batch_sync_llm_wrapper(configs_and_messages: List[Dict[str, Any]]) -> str:
    """
    批量同步LLM推理的wrapper函数
    
    参数:
        configs_and_messages: 配置和消息表达式列表
    
    返回:
        str: 批量推理结果的文本描述
    """
    try:
        results = batch_sync_llm_processor(configs_and_messages)
        
        output_lines = [f"🔄 批量LLM推理完成 - 处理 {len(results)} 项:"]
        
        success_count = 0
        for i, result in enumerate(results, 1):
            if result["success"]:
                success_count += 1
                provider = result["config"]["provider"]
                model = result["config"]["model"]
                response_time = result["metadata"]["response_time"]
                
                output_lines.extend([
                    f"",
                    f"{i}. ✅ [{provider}/{model}] ({response_time}s)",
                    f"   {result['response'][:100]}{'...' if len(result['response']) > 100 else ''}"
                ])
            else:
                provider = result["config"].get("provider", "unknown")
                model = result["config"].get("model", "unknown")
                
                output_lines.extend([
                    f"",
                    f"{i}. ❌ [{provider}/{model}]",
                    f"   {result['error']}"
                ])
        
        output_lines.insert(1, f"📊 成功率: {success_count}/{len(results)}")
        
        return "\n".join(output_lines)
        
    except Exception as e:
        return f"❌ 批量推理异常: {str(e)}"


def sync_llm_validator_wrapper(config: Dict[str, str]) -> str:
    """
    同步LLM配置验证的wrapper函数
    
    参数:
        config: 配置字典
    
    返回:
        str: 验证结果的文本描述
    """
    result = sync_llm_validator(config)
    
    if result["valid"]:
        response_time = result.get("response_time", 0)
        return f"✅ 配置验证成功 ({response_time}秒)"
    else:
        error = result.get("error", "未知错误")
        return f"❌ 配置验证失败: {error}"


# ================================
# 第三层：注册函数（DSL 命令）
# ================================

from beaver.core.decorators import bf_element

@bf_element(
    ':nexus/sync',
    description='同步LLM推理，整合配置和消息转换',
    category='Nexus',
    usage="[':nexus/sync', {'provider': 'openai', 'model': 'gpt-4'}, [':msg/v2m', [':user', 'hello']]]")
def sync_llm_command(config: Dict[str, str], messages_expr: List[Any]):
    """
    同步LLM推理命令
    
    用法: [:nexus/sync {"provider": "openai", "model": "gpt-4"} [":msg/v2m" [":user" "hello"]]]
    """
    if not isinstance(config, dict):
        return "❌ 第一个参数必须是配置字典"
    
    if not isinstance(messages_expr, list):
        return "❌ 第二个参数必须是消息表达式列表"
    
    return sync_llm_wrapper(config, messages_expr)

@bf_element(
    ':nexus/sync-batch',
    description='批量同步LLM推理',
    category='Nexus',
    usage="[':nexus/sync-batch', [{'config': {...}, 'messages': [...]}]]")
def batch_sync_llm_command(configs_and_messages: List[Dict[str, Any]]):
    """
    批量同步LLM推理命令
    
    用法: [:nexus/sync-batch [{"config": {...}, "messages": [...]}]]
    """
    if not isinstance(configs_and_messages, list):
        return "❌ 参数必须是配置和消息表达式列表"
    
    return batch_sync_llm_wrapper(configs_and_messages)

@bf_element(
    ':nexus/validate',
    description='验证LLM配置是否有效',
    category='Nexus',
    usage="[':nexus/validate', {'provider': 'openai', 'model': 'gpt-4'}]")
def sync_llm_validate_command(config: Dict[str, str]):
    """
    LLM配置验证命令
    
    用法: [:nexus/validate {"provider": "openai", "model": "gpt-4"}]
    """
    if not isinstance(config, dict):
        return "❌ 参数必须是配置字典"
    
    return sync_llm_validator_wrapper(config)

@bf_element(
    ':nexus/quick-chat',
    description='快速聊天，使用默认配置',
    category='Nexus',
    usage="[':nexus/quick-chat', 'user prompt']")
def quick_chat_command(prompt: str):
    """
    快速聊天命令，使用默认配置
    
    用法: [:nexus/quick-chat "hello"]
    """
    if not isinstance(prompt, str):
        return "❌ 参数必须是字符串"
    
    try:
        from beaver.config.helpers import get_default_provider
        
        # 获取默认配置
        default_config = get_default_provider()
        if not default_config:
            return "❌ 未找到默认配置，请先设置默认的provider和model"
        
        provider = default_config.get("provider")
        model = default_config.get("model")
        
        if not provider or not model:
            return "❌ 默认配置不完整，缺少provider或model"
        
        config = {"provider": provider, "model": model}
        messages_expr = [":msg/v2m", [":user", prompt]]
        
        return sync_llm_wrapper(config, messages_expr)
        
    except Exception as e:
        return f"❌ 快速聊天失败: {str(e)}" 