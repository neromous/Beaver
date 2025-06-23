"""
Beaver 推理模块

提供OpenAI兼容的API推理功能，包括同步和流式调用
"""

from .sync_client import (
    chat_completion,
    simple_chat,
    chat_with_config,
    validate_openai_config,
    OpenAIChatError
)

from .stream_client import (
    stream_chat_completion,
    stream_simple_chat,
    stream_chat_with_config,
    collect_stream_response,
    stream_with_progress,
    validate_stream_config,
    StreamChatError
)

from .action_stream import (
    stream_with_action,
    stream_with_action_simple,
    stream_with_action_config,
    extract_actions_from_text,
    parse_action_syntax,
    parse_edn,
    edn_to_python,
    convert_edn_to_json,
    execute_action,
    ActionResult,
    ActionStreamError
)

__all__ = [
    # 同步推理
    'chat_completion',
    'simple_chat', 
    'chat_with_config',
    'validate_openai_config',
    'OpenAIChatError',
    
    # 流式推理
    'stream_chat_completion',
    'stream_simple_chat',
    'stream_chat_with_config',
    'collect_stream_response',
    'stream_with_progress',
    'validate_stream_config',
    'StreamChatError',
    
    # Action流式推理
    'stream_with_action',
    'stream_with_action_simple',
    'stream_with_action_config',
    'extract_actions_from_text',
    'parse_action_syntax',
    'parse_edn',
    'edn_to_python',
    'convert_edn_to_json',
    'execute_action',
    'ActionResult',
    'ActionStreamError'
] 