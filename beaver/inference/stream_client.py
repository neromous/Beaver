#!/usr/bin/env python3
"""
Beaver 流式推理客户端

提供流式OpenAI API调用功能，支持实时文本流输出。
设计目标：简单纯函数，无过度设计。
"""

import json
import requests
from typing import Iterator, Dict, Any, Optional, Callable
from urllib.parse import urljoin


class StreamChatError(Exception):
    """流式聊天异常"""
    pass


def _format_api_url(api_url: str) -> str:
    """格式化API URL，确保正确的端点"""
    if not api_url.endswith('/'):
        api_url += '/'
    
    if not api_url.endswith('chat/completions'):
        api_url = urljoin(api_url, 'chat/completions')
    
    return api_url


def _validate_stream_config(messages: list, api_url: str, api_key: str, model: str) -> None:
    """验证流式推理配置参数"""
    if not messages or not isinstance(messages, list):
        raise ValueError("messages必须是非空列表")
    
    if not api_url or not isinstance(api_url, str):
        raise ValueError("api_url必须是非空字符串")
    
    if not api_key or not isinstance(api_key, str):
        raise ValueError("api_key必须是非空字符串")
    
    if not model or not isinstance(model, str):
        raise ValueError("model必须是非空字符串")
    
    # 验证消息格式
    for msg in messages:
        if not isinstance(msg, dict) or 'role' not in msg or 'content' not in msg:
            raise ValueError("每条消息必须包含role和content字段")
        
        if msg['role'] not in ['system', 'user', 'assistant']:
            raise ValueError(f"无效的消息角色: {msg['role']}")


def stream_chat_completion(
    messages: list,
    api_url: str,
    api_key: str,
    model: str,
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    top_p: float = 1.0,
    stop: Optional[list] = None,
    timeout: int = 30
) -> Iterator[Dict[str, Any]]:
    """
    流式聊天完成API调用
    
    参数:
        messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
        api_url: API端点URL
        api_key: API密钥
        model: 模型名称
        temperature: 温度参数 (0-2)
        max_tokens: 最大token数
        top_p: Top-p参数 (0-1)
        stop: 停止词列表，如 ["</action>"]
        timeout: 超时时间（秒）
    
    返回:
        Iterator[Dict]: 流式响应块的迭代器
    
    异常:
        StreamChatError: 流式聊天相关错误
        requests.RequestException: 网络请求错误
    """
    # 验证参数
    _validate_stream_config(messages, api_url, api_key, model)
    
    # 格式化URL
    url = _format_api_url(api_url)
    
    # 构建请求数据
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "stream": True  # 启用流式响应
    }
    
    if max_tokens is not None:
        data["max_tokens"] = max_tokens
        
    if stop is not None:
        data["stop"] = stop
    
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # 发送流式请求
        response = requests.post(
            url,
            headers=headers,
            json=data,
            stream=True,  # 启用流式响应
            timeout=timeout
        )
        
        # 检查HTTP状态
        if response.status_code != 200:
            error_text = response.text
            raise StreamChatError(f"API调用失败 (状态码: {response.status_code}): {error_text}")
        
        # 强制设置正确的编码
        response.encoding = 'utf-8'
        
        # 逐行处理流式响应
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.strip():
                continue
            
            # 跳过非数据行
            if not line.startswith("data: "):
                continue
            
            # 提取数据部分
            data_part = line[6:]  # 移除 "data: " 前缀
            
            # 检查是否为结束标志
            if data_part == "[DONE]":
                break
            
            try:
                # 解析JSON数据
                chunk = json.loads(data_part)
                yield chunk
                
            except json.JSONDecodeError as e:
                # 跳过无效的JSON数据
                continue
    
    except requests.exceptions.Timeout:
        raise StreamChatError(f"请求超时 (超过{timeout}秒)")
    
    except requests.exceptions.ConnectionError:
        raise StreamChatError("连接失败，请检查网络和API端点")
    
    except requests.exceptions.RequestException as e:
        raise StreamChatError(f"请求异常: {str(e)}")


def stream_simple_chat(
    prompt: str,
    api_url: str,
    api_key: str,
    model: str,
    system_prompt: Optional[str] = None,
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    timeout: int = 30,
    on_chunk: Optional[Callable[[str], None]] = None
) -> Iterator[str]:
    """
    简化的流式聊天函数
    
    参数:
        prompt: 用户输入
        api_url: API端点URL
        api_key: API密钥
        model: 模型名称
        system_prompt: 系统提示词（可选）
        temperature: 温度参数
        max_tokens: 最大token数
        timeout: 超时时间
        on_chunk: 接收到文本块时的回调函数
    
    返回:
        Iterator[str]: 文本块的迭代器
    
    异常:
        StreamChatError: 流式聊天相关错误
    """
    # 构建消息
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})
    
    # 调用流式完成API
    try:
        for chunk in stream_chat_completion(
            messages=messages,
            api_url=api_url,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout
        ):
            # 提取文本内容
            if 'choices' in chunk and chunk['choices']:
                choice = chunk['choices'][0]
                
                if 'delta' in choice and 'content' in choice['delta']:
                    content = choice['delta']['content']
                    
                    if content:  # 跳过空内容
                        # 执行回调函数
                        if on_chunk:
                            on_chunk(content)
                        
                        yield content
    
    except Exception as e:
        if isinstance(e, StreamChatError):
            raise
        else:
            raise StreamChatError(f"流式聊天失败: {str(e)}")


def stream_chat_with_config(
    prompt: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    timeout: int = 30,
    on_chunk: Optional[Callable[[str], None]] = None
) -> Iterator[str]:
    """
    使用配置的流式聊天函数
    
    参数:
        prompt: 用户输入
        provider: 提供商名称（可选，使用默认）
        model: 模型名称（可选，使用默认）
        system_prompt: 系统提示词
        temperature: 温度参数
        max_tokens: 最大token数
        timeout: 超时时间
        on_chunk: 接收到文本块时的回调函数
    
    返回:
        Iterator[str]: 文本块的迭代器
    
    异常:
        StreamChatError: 流式聊天相关错误
    """
    try:
        from beaver.config import get_new_api_config, get_default_provider
        
        # 获取默认配置
        if not provider or not model:
            default = get_default_provider()
            provider = provider or default.get('provider')
            model = model or default.get('model')
        
        if not provider or not model:
            raise StreamChatError("未指定provider和model，且没有默认配置")
        
        # 获取API配置
        api_config = get_new_api_config(provider, model)
        
        if not api_config:
            raise StreamChatError(f"未找到 {provider}/{model} 的配置")
        
        # 检查必需的配置项
        required_keys = ['url', 'secret_key', 'model']
        missing_keys = [k for k in required_keys if not api_config.get(k)]
        
        if missing_keys:
            raise StreamChatError(f"配置缺少必需项: {missing_keys}")
        
        # 调用流式聊天
        return stream_simple_chat(
            prompt=prompt,
            api_url=api_config['url'],
            api_key=api_config['secret_key'],
            model=api_config['model'],
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            on_chunk=on_chunk
        )
    
    except ImportError:
        raise StreamChatError("无法导入配置模块")
    
    except Exception as e:
        if isinstance(e, StreamChatError):
            raise
        else:
            raise StreamChatError(f"配置流式聊天失败: {str(e)}")


def collect_stream_response(stream_iterator: Iterator[str]) -> str:
    """
    收集流式响应为完整文本
    
    参数:
        stream_iterator: 流式文本迭代器
    
    返回:
        str: 完整的响应文本
    """
    return "".join(stream_iterator)


def stream_with_progress(
    stream_iterator: Iterator[str],
    show_progress: bool = True,
    chunk_delay: float = 0.0
) -> Iterator[str]:
    """
    带进度显示的流式输出
    
    参数:
        stream_iterator: 流式文本迭代器
        show_progress: 是否显示进度
        chunk_delay: 每个块之间的延迟（秒）
    
    返回:
        Iterator[str]: 包装后的文本块迭代器
    """
    import time
    
    chunk_count = 0
    
    for chunk in stream_iterator:
        chunk_count += 1
        
        if show_progress:
            print(f"\r[块 {chunk_count}] 接收中...", end="", flush=True)
        
        yield chunk
        
        if chunk_delay > 0:
            time.sleep(chunk_delay)
    
    if show_progress:
        print(f"\r[完成] 共接收 {chunk_count} 个文本块", flush=True)


def validate_stream_config(api_url: str, api_key: str, model: str) -> bool:
    """
    验证流式API配置是否有效
    
    参数:
        api_url: API端点URL
        api_key: API密钥
        model: 模型名称
    
    返回:
        bool: 配置是否有效
    """
    try:
        # 发送一个简单的测试请求
        test_messages = [{"role": "user", "content": "test"}]
        
        stream = stream_chat_completion(
            messages=test_messages,
            api_url=api_url,
            api_key=api_key,
            model=model,
            max_tokens=1,
            timeout=10
        )
        
        # 尝试获取第一个响应块
        next(stream, None)
        return True
        
    except Exception:
        return False 