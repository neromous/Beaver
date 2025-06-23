#!/usr/bin/env python3
"""
Beaver Action流式推理模块

支持AI输出中的DSL语法自动解析和执行，实现智能交互式推理。
当AI输出包含 [":p", "content"] 等DSL语法时，自动执行相应的渲染操作。
"""

import re
import json
import ast
from typing import Iterator, Dict, Any, Optional, Callable, List, Union
from dataclasses import dataclass, field

from .stream_client import (
    stream_chat_completion,
    stream_simple_chat,
    StreamChatError
)


@dataclass
class ActionResult:
    """Action执行结果"""
    success: bool
    action: Optional[List] = None
    rendered_output: Optional[str] = None
    error: Optional[str] = None
    raw_action: Optional[str] = None


@dataclass
class StreamActionState:
    """流式Action状态管理"""
    current_content: str = ""
    pending_actions: List[str] = field(default_factory=list)
    executed_actions: List[ActionResult] = field(default_factory=list)
    iteration_count: int = 0
    max_iterations: int = 3


class ActionStreamError(Exception):
    """Action流式推理异常"""
    pass


def extract_actions_from_text(text: str) -> List[str]:
    """
    从文本中提取 <action>...</action> 标签内的DSL语法
    
    支持格式：
    - <action>[":p", "content"]</action>
    - <action>[":md/h1", "title"]</action>
    - <action>[:str/upper, "text"]</action> (EDN格式)
    
    参数:
        text: 包含Action标签的文本
    
    返回:
        List[str]: 提取的Action内容列表
    """
    # 匹配 <action>...</action> 标签内的内容
    pattern = r'<action>\s*(.*?)\s*</action>'
    matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
    
    return [match.strip() for match in matches if match.strip()]


def parse_action_syntax(action_str: str) -> Optional[List[str]]:
    """
    解析Action语法字符串为列表，使用专业的EDN解析库
    
    参数:
        action_str: Action字符串，支持完整的EDN语法：
                   - 简单: [:p, "hello"]
                   - 复杂: [:div, {:class "container"}, [:p, "content"]]
                   - 嵌套: [:table, [:tr, [:td, "A"]]]
    
    返回:
        Optional[List[str]]: 解析后的列表，失败返回None
    """
    try:
        # 使用edn-format库进行专业EDN解析
        parsed_edn = parse_edn(action_str)
        
        # 转换为Python原生数据结构
        python_data = edn_to_python(parsed_edn)
        
        if isinstance(python_data, list) and len(python_data) >= 1:
            # 验证第一个元素是否为关键字格式
            if isinstance(python_data[0], str) and python_data[0].startswith(':'):
                return python_data
        
        return None
        
    except Exception as e:
        # 如果EDN解析失败，尝试直接作为JSON解析（向后兼容）
        return parse_json_fallback(action_str)


def parse_edn(edn_str: str):
    """
    使用edn-format库解析EDN字符串
    
    参数:
        edn_str: EDN格式字符串
    
    返回:
        解析后的EDN数据结构
    """
    try:
        import edn_format
        return edn_format.loads(edn_str)
    except ImportError:
        raise ImportError("需要安装edn-format库: pip install edn-format")
    except Exception as e:
        raise ValueError(f"EDN解析失败: {e}")


def edn_to_python(edn_data) -> any:
    """
    将EDN数据结构转换为Python原生数据结构
    
    处理EDN特有的类型：
    - Keyword -> 字符串 (":keyword")
    - ImmutableList -> list
    - ImmutableDict -> dict
    
    参数:
        edn_data: EDN数据结构
    
    返回:
        Python原生数据结构
    """
    try:
        import edn_format
        
        if isinstance(edn_data, edn_format.Keyword):
            # 关键字转换为字符串，保持单":"前缀
            # edn_format.Keyword的字符串表示已经包含":"，所以不需要再添加
            return str(edn_data)
            
        elif isinstance(edn_data, (edn_format.ImmutableList, list)):
            # 递归转换列表中的每个元素
            return [edn_to_python(item) for item in edn_data]
            
        elif isinstance(edn_data, (edn_format.ImmutableDict, dict)):
            # 递归转换字典中的键值对
            return {edn_to_python(k): edn_to_python(v) for k, v in edn_data.items()}
            
        else:
            # 其他类型直接返回（字符串、数字、布尔值等）
            return edn_data
            
    except ImportError:
        # 如果没有edn_format库，直接返回原数据
        return edn_data


def parse_json_fallback(action_str: str) -> Optional[List[str]]:
    """
    JSON格式解析回退方案（向后兼容）
    
    参数:
        action_str: 可能是JSON格式的字符串
    
    返回:
        Optional[List[str]]: 解析后的列表，失败返回None
    """
    try:
        parsed = ast.literal_eval(action_str)
        
        if isinstance(parsed, list) and len(parsed) >= 1:
            if isinstance(parsed[0], str) and parsed[0].startswith(':'):
                return parsed
        
        return None
        
    except (ValueError, SyntaxError):
        return None


def convert_edn_to_json(edn_str: str) -> str:
    """
    将EDN格式转换为JSON格式（已弃用，保留用于向后兼容）
    
    注意：此函数已被parse_edn()和edn_to_python()取代，
    新实现支持完整的EDN语法而不仅仅是简单的正则表达式替换。
    
    参数:
        edn_str: EDN格式的字符串
    
    返回:
        str: JSON格式的字符串
    """
    # 尝试使用新的EDN解析器
    try:
        parsed = parse_edn(edn_str)
        python_data = edn_to_python(parsed)
        return str(python_data)
    except Exception:
        # 回退到旧的正则表达式方法
        pattern = r'(:\w+(?:/\w+)?)'
        
        def replace_keyword(match):
            keyword = match.group(1)
            return f'"{keyword}"'
        
        return re.sub(pattern, replace_keyword, edn_str)


def execute_action(action: List[str]) -> ActionResult:
    """
    执行DSL Action
    
    参数:
        action: 解析后的Action列表，如 [":p", "hello"]
    
    返回:
        ActionResult: 执行结果
    """
    try:
        from beaver.core import dispatch
        
        # 使用dispatch处理Action
        result = dispatch(action)
        
        return ActionResult(
            success=True,
            action=action,
            rendered_output=result,
            raw_action=str(action)
        )
        
    except Exception as e:
        return ActionResult(
            success=False,
            action=action,
            error=str(e),
            raw_action=str(action)
        )


def stream_with_action(
    prompt: str,
    api_url: str,
    api_key: str,
    model: str,
    system_prompt: Optional[str] = None,
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    timeout: int = 30,
    max_iterations: int = 3,
    on_content: Optional[Callable[[str], None]] = None,
    on_action: Optional[Callable[[List[str], ActionResult], None]] = None,
    auto_execute: bool = True,
    include_actions_in_output: bool = True
) -> Iterator[Dict[str, Any]]:
    """
    带Action支持的流式聊天
    
    当AI输出包含DSL语法时，自动解析并执行相应的操作。
    支持多轮推理，当检测到Action时会继续对话。
    
    参数:
        prompt: 用户输入
        api_url: API端点URL
        api_key: API密钥
        model: 模型名称
        system_prompt: 系统提示词
        temperature: 温度参数
        max_tokens: 最大token数
        timeout: 超时时间
        max_iterations: 最大推理轮数
        on_content: 内容回调函数
        on_action: Action执行回调函数
        auto_execute: 是否自动执行Action
        include_actions_in_output: 是否在输出中包含Action
    
    返回:
        Iterator[Dict]: 流式事件迭代器
        
        事件类型:
        - {"type": "content", "data": "文本内容"}
        - {"type": "action_detected", "data": action_list}
        - {"type": "action_executed", "data": ActionResult}
        - {"type": "iteration_start", "data": iteration_number}
        - {"type": "complete", "data": final_state}
    """
    # 初始化状态
    state = StreamActionState(max_iterations=max_iterations)
    
    # 构建初始消息
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": prompt})
    
    try:
        while state.iteration_count < max_iterations:
            state.iteration_count += 1
            
            yield {
                "type": "iteration_start",
                "data": {
                    "iteration": state.iteration_count,
                    "max_iterations": max_iterations
                }
            }
            
            # 重置当前内容
            state.current_content = ""
            
            # 使用stop words来检测action结束
            stop_words = ["</action>"]
            
            # 流式获取AI响应，使用stop words
            for chunk in stream_chat_completion(
                messages=messages,
                api_url=api_url,
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stop=stop_words,
                timeout=timeout
            ):
                # 提取文本内容
                if 'choices' in chunk and chunk['choices']:
                    choice = chunk['choices'][0]
                    
                    if 'delta' in choice and 'content' in choice['delta']:
                        content = choice['delta']['content']
                        
                        if content:
                            state.current_content += content
                            
                            # 触发内容回调
                            if on_content:
                                on_content(content)
                            
                            yield {
                                "type": "content",
                                "data": content
                            }
                    
                    # 检查是否因为stop word而结束
                    if 'finish_reason' in choice and choice['finish_reason'] == 'stop':
                        # 可能是遇到了</action>，手动添加结束标签以完成action
                        if '<action>' in state.current_content and '</action>' not in state.current_content:
                            state.current_content += '</action>'
                            yield {
                                "type": "content", 
                                "data": "</action>"
                            }
                        break
            
            # 检查是否包含Action
            actions = extract_actions_from_text(state.current_content)
            
            if actions:
                # 处理检测到的Actions
                has_valid_action = False
                action_results = []
                
                for action_str in actions:
                    parsed_action = parse_action_syntax(action_str)
                    
                    if parsed_action:
                        has_valid_action = True
                        
                        yield {
                            "type": "action_detected",
                            "data": {
                                "raw": action_str,
                                "parsed": parsed_action
                            }
                        }
                        
                        # 执行Action（如果启用自动执行）
                        if auto_execute:
                            result = execute_action(parsed_action)
                            action_results.append(result)
                            
                            # 触发Action回调
                            if on_action:
                                on_action(parsed_action, result)
                            
                            yield {
                                "type": "action_executed",
                                "data": result
                            }
                
                # 如果有有效的Action，继续推理
                if has_valid_action and state.iteration_count < max_iterations:
                    # 添加AI响应到消息历史
                    messages.append({"role": "assistant", "content": state.current_content})
                    
                    # 构建Action执行结果
                    effects_content = []
                    for result in action_results:
                        if result.success:
                            effects_content.append(f"Action {result.action} 执行成功:")
                            effects_content.append(f"渲染结果: {result.rendered_output}")
                        else:
                            effects_content.append(f"Action {result.action} 执行失败: {result.error}")
                    
                    # 添加效果反馈
                    if effects_content:
                        effects_message = "\n".join(effects_content)
                        messages.append({
                            "role": "user", 
                            "content": f"<effects>\n{effects_message}\n</effects>\n\n请继续你的回答。"
                        })
                    
                    # 继续下一轮推理
                    continue
                else:
                    # 没有有效Action或达到最大迭代次数，结束推理
                    break
            else:
                # 没有检测到Action，结束推理
                break
        
        # 添加最终响应到消息历史
        if state.current_content:
            messages.append({"role": "assistant", "content": state.current_content})
        
        # 返回完成状态
        yield {
            "type": "complete",
            "data": {
                "final_content": state.current_content,
                "total_iterations": state.iteration_count,
                "executed_actions": state.executed_actions,
                "final_messages": messages
            }
        }
        
    except Exception as e:
        if isinstance(e, StreamChatError):
            raise
        else:
            raise ActionStreamError(f"Action流式推理失败: {str(e)}")


def stream_with_action_simple(
    prompt: str,
    api_url: str,
    api_key: str,
    model: str,
    system_prompt: Optional[str] = None,
    max_iterations: int = 3,
    **kwargs
) -> Dict[str, Any]:
    """
    简化的Action流式推理函数
    
    参数:
        prompt: 用户输入
        api_url: API端点URL
        api_key: API密钥
        model: 模型名称
        system_prompt: 系统提示词
        max_iterations: 最大推理轮数
        **kwargs: 其他参数
    
    返回:
        Dict: 推理结果
        - content: 完整的AI回复内容
        - actions: 执行的Action列表
        - iterations: 推理轮数
        - success: 是否成功
    """
    content_parts = []
    executed_actions = []
    iterations = 0
    
    try:
        for event in stream_with_action(
            prompt=prompt,
            api_url=api_url,
            api_key=api_key,
            model=model,
            system_prompt=system_prompt,
            max_iterations=max_iterations,
            **kwargs
        ):
            if event["type"] == "content":
                content_parts.append(event["data"])
            
            elif event["type"] == "action_executed":
                executed_actions.append(event["data"])
            
            elif event["type"] == "iteration_start":
                iterations = event["data"]["iteration"]
            
            elif event["type"] == "complete":
                break
        
        return {
            "success": True,
            "content": "".join(content_parts),
            "actions": executed_actions,
            "iterations": iterations
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "content": "".join(content_parts),
            "actions": executed_actions,
            "iterations": iterations
        }


def stream_with_action_config(
    prompt: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
    max_iterations: int = 3,
    **kwargs
) -> Iterator[Dict[str, Any]]:
    """
    使用配置的Action流式推理
    
    参数:
        prompt: 用户输入
        provider: 提供商名称
        model: 模型名称
        system_prompt: 系统提示词
        max_iterations: 最大推理轮数
        **kwargs: 其他参数
    
    返回:
        Iterator[Dict]: 流式事件迭代器
    """
    try:
        from beaver.config import get_new_api_config, get_default_provider
        
        # 获取默认配置
        if not provider or not model:
            default = get_default_provider()
            provider = provider or default.get('provider')
            model = model or default.get('model')
        
        if not provider or not model:
            raise ActionStreamError("未指定provider和model，且没有默认配置")
        
        # 获取API配置
        api_config = get_new_api_config(provider, model)
        
        if not api_config:
            raise ActionStreamError(f"未找到 {provider}/{model} 的配置")
        
        # 检查必需的配置项
        required_keys = ['url', 'secret_key', 'model']
        missing_keys = [k for k in required_keys if not api_config.get(k)]
        
        if missing_keys:
            raise ActionStreamError(f"配置缺少必需项: {missing_keys}")
        
        # 调用Action流式推理
        yield from stream_with_action(
            prompt=prompt,
            api_url=api_config['url'],
            api_key=api_config['secret_key'],
            model=api_config['model'],
            system_prompt=system_prompt,
            max_iterations=max_iterations,
            **kwargs
        )
    
    except ImportError:
        raise ActionStreamError("无法导入配置模块")
    
    except Exception as e:
        if isinstance(e, ActionStreamError):
            raise
        else:
            raise ActionStreamError(f"配置Action流式推理失败: {str(e)}")


def test_action_parsing():
    """测试Action解析功能"""
    test_cases = [
        '[":p", "hello world"]',
        '[":md/h1", "标题"]',
        '[":str/upper", "text"]',
        '无效的action',
        '[":bold", "粗体", "额外参数"]'
    ]
    
    print("🧪 测试Action解析功能:")
    
    for case in test_cases:
        print(f"\n输入: {case}")
        result = parse_action_syntax(case)
        print(f"结果: {result}")
        
        if result:
            action_result = execute_action(result)
            print(f"执行: {action_result}")


if __name__ == "__main__":
    test_action_parsing() 