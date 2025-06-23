"""
同步版 OpenAI API 客户端

提供简单的聊天完成推理功能
"""

import json
import requests
from typing import Dict, List, Any, Optional, Union


class OpenAIChatError(Exception):
    """OpenAI 聊天API异常"""
    pass


def chat_completion(
    messages: List[Dict[str, str]], 
    api_url: str,
    api_key: str,
    model: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    timeout: int = 30,
    **kwargs
) -> Dict[str, Any]:
    """
    调用 OpenAI 兼容的聊天完成 API
    
    Args:
        messages: 消息列表，格式如 [{"role": "user", "content": "hello"}]
        api_url: API 端点 URL
        api_key: API 密钥
        model: 模型名称
        temperature: 温度参数，控制随机性
        max_tokens: 最大token数
        timeout: 请求超时时间（秒）
        **kwargs: 其他API参数
        
    Returns:
        API 响应字典
        
    Raises:
        requests.RequestException: 网络请求异常
        ValueError: 参数错误
    """
    # 验证必需参数
    if not messages:
        raise ValueError("messages 不能为空")
    if not api_url:
        raise ValueError("api_url 不能为空")
    if not api_key:
        raise ValueError("api_key 不能为空")
    if not model:
        raise ValueError("model 不能为空")
    
    # 确保URL格式正确
    if not api_url.endswith('/chat/completions'):
        if api_url.endswith('/'):
            api_url = api_url + 'chat/completions'
        else:
            api_url = api_url + '/chat/completions'
    
    # 构建请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    # 构建请求体
    payload = {
        'model': model,
        'messages': messages,
        'temperature': temperature,
        **kwargs
    }
    
    # 添加 max_tokens 如果指定
    if max_tokens is not None:
        payload['max_tokens'] = max_tokens
    
    try:
        # 发送请求
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        
        # 检查状态码
        response.raise_for_status()
        
        # 解析响应
        return response.json()
        
    except requests.exceptions.Timeout:
        raise requests.RequestException(f"请求超时 ({timeout}秒)")
    except requests.exceptions.ConnectionError:
        raise requests.RequestException("连接失败")
    except requests.exceptions.HTTPError as e:
        try:
            error_detail = response.json()
            error_msg = error_detail.get('error', {}).get('message', str(e))
        except:
            error_msg = str(e)
        raise requests.RequestException(f"HTTP错误 {response.status_code}: {error_msg}")
    except json.JSONDecodeError:
        raise requests.RequestException("响应格式错误，无法解析JSON")


def simple_chat(
    prompt: str,
    api_url: str,
    api_key: str, 
    model: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    timeout: int = 30,
    **kwargs
) -> str:
    """
    简化的聊天函数，直接返回文本回复
    
    Args:
        prompt: 用户提示词
        api_url: API 端点 URL
        api_key: API 密钥
        model: 模型名称
        system_prompt: 系统提示词（可选）
        temperature: 温度参数
        max_tokens: 最大token数
        timeout: 请求超时时间（秒）
        **kwargs: 其他API参数
        
    Returns:
        AI 回复的文本内容
        
    Raises:
        requests.RequestException: 网络请求异常
        ValueError: 参数错误或响应格式错误
    """
    # 构建消息列表
    messages = []
    
    # 添加系统提示词
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # 添加用户提示词
    messages.append({"role": "user", "content": prompt})
    
    try:
        # 调用聊天完成API
        response = chat_completion(
            messages=messages,
            api_url=api_url,
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            **kwargs
        )
        
        # 提取回复内容
        if 'choices' not in response:
            raise ValueError("API响应中没有choices字段")
        
        if not response['choices']:
            raise ValueError("API响应中choices为空")
        
        choice = response['choices'][0]
        
        if 'message' not in choice:
            raise ValueError("API响应中没有message字段")
        
        message = choice['message']
        
        if 'content' not in message:
            raise ValueError("API响应中没有content字段")
        
        return message['content']
        
    except requests.RequestException:
        # 重新抛出网络异常
        raise
    except Exception as e:
        # 包装其他异常
        raise ValueError(f"处理API响应时出错: {str(e)}")


def chat_with_config(
    prompt: str,
    provider: str,
    model: str,
    system_prompt: Optional[str] = None,
    **kwargs
) -> str:
    """
    使用配置文件中的设置进行聊天
    
    Args:
        prompt: 用户提示词
        provider: 提供商名称
        model: 模型名称
        system_prompt: 系统提示词（可选）
        **kwargs: 其他参数
        
    Returns:
        AI 回复的文本内容
    """
    try:
        from beaver.config.helpers import get_api_config, get_model_config
        
        # 获取API配置
        api_config = get_api_config(provider, model)
        if not api_config:
            raise ValueError(f"未找到 {provider}/{model} 的配置")
        
        # 获取模型配置
        model_config = get_model_config(provider, model)
        
        # 合并参数
        api_params = {
            'api_url': api_config.get('url'),
            'api_key': api_config.get('secret_key'),
            'model': api_config.get('model'),
            'temperature': model_config.get('temperature', 0.7),
            **kwargs
        }
        
        # 验证必需参数
        for key in ['api_url', 'api_key', 'model']:
            if not api_params[key]:
                raise ValueError(f"配置中缺少 {key}")
        
        return simple_chat(
            prompt=prompt,
            system_prompt=system_prompt,
            **api_params
        )
        
    except ImportError:
        raise ValueError("配置模块不可用，请使用 simple_chat 函数")


def validate_openai_config(api_url: str, api_key: str, model: str) -> Dict[str, Any]:
    """
    验证 OpenAI API 配置是否有效
    
    Args:
        api_url: API 端点 URL
        api_key: API 密钥
        model: 模型名称
        
    Returns:
        验证结果字典，包含 valid, error, response_time
    """
    test_messages = [{"role": "user", "content": "hello"}]
    
    import time
    start_time = time.time()
    
    try:
        response = chat_completion(
            messages=test_messages,
            api_url=api_url,
            api_key=api_key,
            model=model,
            max_tokens=10,
            timeout=10
        )
        
        response_time = time.time() - start_time
        
        return {
            'valid': True,
            'error': None,
            'response_time': round(response_time, 2),
            'response': response
        }
        
    except Exception as e:
        response_time = time.time() - start_time
        
        return {
            'valid': False,
            'error': str(e),
            'response_time': round(response_time, 2),
            'response': None
        } 