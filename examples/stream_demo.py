#!/usr/bin/env python3
"""
Beaver 流式推理功能演示

展示如何使用流式OpenAI API推理功能，实现实时文本生成
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def demo_basic_streaming():
    """基础流式聊天演示"""
    print("🌊 基础流式聊天演示")
    print("-" * 40)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import stream_simple_chat, collect_stream_response
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        print(f"使用模型: {model}")
        
        # 示例问题
        questions = [
            "请用一句话介绍人工智能",
            "写一个简短的Python函数示例",
            "推荐一本好书并说明理由"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n💬 问题 {i}: {question}")
            print("🤖 AI回复: ", end="", flush=True)
            
            # 流式输出，实时显示
            full_response = ""
            for chunk in stream_simple_chat(
                prompt=question,
                api_url=api_url,
                api_key=api_key,
                model=model,
                max_tokens=150,
                timeout=30
            ):
                print(chunk, end="", flush=True)
                full_response += chunk
                time.sleep(0.02)  # 模拟打字机效果
            
            print()  # 换行
            print(f"📊 完整回复长度: {len(full_response)} 字符")
        
        return True
        
    except Exception as e:
        print(f"❌ 基础流式演示失败: {e}")
        return False

def demo_streaming_with_callback():
    """带回调函数的流式演示"""
    print("\n📞 带回调函数的流式演示")
    print("-" * 40)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import stream_simple_chat
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        # 统计信息
        stats = {
            'chunks': 0,
            'total_chars': 0,
            'words': 0
        }
        
        # 回调函数
        def on_chunk_received(chunk):
            stats['chunks'] += 1
            stats['total_chars'] += len(chunk)
            # 简单计算单词数
            if chunk.strip():
                stats['words'] += len(chunk.split())
            
            # 实时显示统计
            print(f"\r📊 已接收: {stats['chunks']} 块 | {stats['total_chars']} 字符 | {stats['words']} 词", 
                  end="", flush=True)
        
        question = "请写一首关于春天的诗"
        print(f"💬 问题: {question}")
        print("🤖 AI回复:")
        
        # 使用回调的流式聊天
        full_response = ""
        for chunk in stream_simple_chat(
            prompt=question,
            api_url=api_url,
            api_key=api_key,
            model=model,
            max_tokens=200,
            timeout=30,
            on_chunk=on_chunk_received
        ):
            full_response += chunk
        
        print(f"\n📝 完整诗歌:\n{full_response}")
        print(f"\n📊 最终统计: {stats['chunks']} 块, {stats['total_chars']} 字符, {stats['words']} 词")
        
        return True
        
    except Exception as e:
        print(f"❌ 回调演示失败: {e}")
        return False

def demo_streaming_conversation():
    """流式多轮对话演示"""
    print("\n💬 流式多轮对话演示")
    print("-" * 40)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import stream_chat_completion
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        # 构建多轮对话
        messages = [
            {"role": "system", "content": "你是一个有用的编程助手"},
            {"role": "user", "content": "我想学习Python"},
            {"role": "assistant", "content": "太好了！Python是一门很棒的编程语言。你想从哪里开始呢？"},
            {"role": "user", "content": "请推荐一些学习资源和路径"}
        ]
        
        # 显示对话历史
        print("📜 对话历史:")
        for msg in messages:
            role_icons = {"system": "⚙️", "user": "👤", "assistant": "🤖"}
            icon = role_icons.get(msg['role'], '💬')
            print(f"{icon} {msg['role']}: {msg['content']}")
        
        print("\n🤖 AI继续回复: ", end="", flush=True)
        
        # 流式多轮对话
        full_response = ""
        for chunk in stream_chat_completion(
            messages=messages,
            api_url=api_url,
            api_key=api_key,
            model=model,
            temperature=0.7,
            max_tokens=300,
            timeout=30
        ):
            # 提取文本内容
            if 'choices' in chunk and chunk['choices']:
                choice = chunk['choices'][0]
                if 'delta' in choice and 'content' in choice['delta']:
                    content = choice['delta']['content']
                    if content:
                        print(content, end="", flush=True)
                        full_response += content
                        time.sleep(0.01)
        
        print(f"\n\n📝 完整回复:\n{full_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ 多轮对话演示失败: {e}")
        return False

def demo_streaming_with_progress():
    """带进度显示的流式演示"""
    print("\n📊 带进度显示的流式演示")
    print("-" * 40)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import stream_simple_chat, stream_with_progress
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        question = "请解释什么是机器学习"
        print(f"💬 问题: {question}")
        
        # 创建流
        stream = stream_simple_chat(
            prompt=question,
            api_url=api_url,
            api_key=api_key,
            model=model,
            max_tokens=200,
            timeout=30
        )
        
        # 使用进度显示的流处理
        print("🔄 开始流式处理...")
        full_response = ""
        for chunk in stream_with_progress(stream, show_progress=True, chunk_delay=0.05):
            full_response += chunk
        
        print(f"\n📝 完整回复:\n{full_response}")
        
        return True
        
    except Exception as e:
        print(f"❌ 进度演示失败: {e}")
        return False

def demo_streaming_different_temperatures():
    """不同温度参数的流式演示"""
    print("\n🌡️ 不同温度参数的流式演示")
    print("-" * 40)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import stream_simple_chat, collect_stream_response
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        question = "用几个词描述人工智能"
        temperatures = [0.1, 0.7, 1.5]
        
        print(f"💬 问题: {question}")
        
        for temp in temperatures:
            print(f"\n🌡️ 温度 {temp}:")
            print("🤖 回复: ", end="", flush=True)
            
            # 不同温度的流式输出
            stream = stream_simple_chat(
                prompt=question,
                api_url=api_url,
                api_key=api_key,
                model=model,
                temperature=temp,
                max_tokens=50,
                timeout=20
            )
            
            response = collect_stream_response(stream)
            print(response)
        
        return True
        
    except Exception as e:
        print(f"❌ 温度演示失败: {e}")
        return False

def demo_interactive_streaming():
    """交互式流式聊天演示"""
    print("\n🎮 交互式流式聊天演示")
    print("-" * 40)
    print("输入 'quit' 退出，输入 'clear' 清空历史")
    
    try:
        from beaver.config import config_manager
        from beaver.inference import stream_chat_completion
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        # 对话历史
        messages = [{"role": "system", "content": "你是一个友好的助手"}]
        
        while True:
            # 获取用户输入
            user_input = input("\n👤 你: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 再见！")
                break
            
            if user_input.lower() == 'clear':
                messages = [{"role": "system", "content": "你是一个友好的助手"}]
                print("🧹 历史已清空")
                continue
            
            if not user_input:
                continue
            
            # 添加用户消息
            messages.append({"role": "user", "content": user_input})
            
            print("🤖 AI: ", end="", flush=True)
            
            # 流式回复
            ai_response = ""
            for chunk in stream_chat_completion(
                messages=messages,
                api_url=api_url,
                api_key=api_key,
                model=model,
                temperature=0.7,
                max_tokens=200,
                timeout=30
            ):
                if 'choices' in chunk and chunk['choices']:
                    choice = chunk['choices'][0]
                    if 'delta' in choice and 'content' in choice['delta']:
                        content = choice['delta']['content']
                        if content:
                            print(content, end="", flush=True)
                            ai_response += content
            
            # 添加AI回复到历史
            if ai_response:
                messages.append({"role": "assistant", "content": ai_response})
            
            print()  # 换行
        
        return True
        
    except KeyboardInterrupt:
        print("\n👋 用户中断，再见！")
        return True
    except Exception as e:
        print(f"❌ 交互演示失败: {e}")
        return False

def main():
    """运行所有流式推理演示"""
    print("🌊 Beaver 流式推理功能演示")
    print("=" * 60)
    
    demos = [
        demo_basic_streaming,
        demo_streaming_with_callback, 
        demo_streaming_conversation,
        demo_streaming_with_progress,
        demo_streaming_different_temperatures
    ]
    
    passed = 0
    for demo in demos:
        if demo():
            passed += 1
    
    print(f"\n📊 演示结果: {passed}/{len(demos)} 个成功")
    
    if passed > 0:
        print("\n🎉 流式推理演示完成！")
        print("\n💡 快速使用指南:")
        print("```python")
        print("from beaver.inference import stream_simple_chat")
        print("")
        print("# 实时流式输出")
        print("for chunk in stream_simple_chat('你好', api_url, api_key, model):")
        print("    print(chunk, end='', flush=True)")
        print("")
        print("# 收集完整响应")
        print("from beaver.inference import collect_stream_response")
        print("response = collect_stream_response(stream)")
        print("```")
        
        # 询问是否进行交互演示
        choice = input("\n🎮 是否进行交互式演示? (y/n): ").strip().lower()
        if choice == 'y':
            demo_interactive_streaming()
    else:
        print("❌ 流式推理演示失败")

if __name__ == '__main__':
    main() 