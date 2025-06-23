#!/usr/bin/env python3
"""
Beaver 推理功能使用示例
展示如何使用同步版 OpenAI API 推理功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def demo_simple_chat():
    """简单聊天演示"""
    print("💬 简单聊天演示")
    print("-" * 30)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import simple_chat
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        # 提取配置信息
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        print(f"使用模型: {model}")
        
        # 简单对话
        questions = [
            "你好，请简单介绍一下自己",
            "请用一句话解释什么是人工智能",
            "推荐一本好书"
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n🤖 问题 {i}: {question}")
            
            try:
                response = simple_chat(
                    prompt=question,
                    api_url=api_url,
                    api_key=api_key,
                    model=model,
                    max_tokens=100,
                    timeout=20
                )
                print(f"✅ 回答: {response}")
                
            except Exception as e:
                print(f"❌ 出错: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def demo_with_system_prompt():
    """带系统提示词的聊天演示"""
    print("\n🎭 系统提示词演示")
    print("-" * 30)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import simple_chat
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        # 不同的系统提示词
        scenarios = [
            {
                "name": "诗人",
                "system_prompt": "你是一位古典诗人，请用诗歌的形式回答问题。",
                "question": "描述春天的美景"
            },
            {
                "name": "科学家",
                "system_prompt": "你是一位严谨的科学家，请用科学的方式解释现象。",
                "question": "为什么天空是蓝色的？"
            },
            {
                "name": "厨师",
                "system_prompt": "你是一位专业厨师，请提供烹饪建议。",
                "question": "如何做一道简单的家常菜？"
            }
        ]
        
        for scenario in scenarios:
            print(f"\n👤 角色: {scenario['name']}")
            print(f"🎯 问题: {scenario['question']}")
            
            try:
                response = simple_chat(
                    prompt=scenario['question'],
                    api_url=api_url,
                    api_key=api_key,
                    model=model,
                    system_prompt=scenario['system_prompt'],
                    max_tokens=150,
                    timeout=20
                )
                print(f"✅ 回答: {response}")
                
            except Exception as e:
                print(f"❌ 出错: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def demo_chat_completion():
    """原始聊天完成API演示"""
    print("\n🔧 原始API演示")
    print("-" * 30)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import chat_completion
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        # 构建消息列表（多轮对话）
        messages = [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": "我想学习Python编程"},
            {"role": "assistant", "content": "很好！Python是一门很棒的编程语言。你想从哪里开始？"},
            {"role": "user", "content": "请推荐一些入门资源"}
        ]
        
        print("📝 多轮对话:")
        for msg in messages:
            role_emoji = {"system": "⚙️", "user": "👤", "assistant": "🤖"}
            print(f"{role_emoji.get(msg['role'], '💬')} {msg['role']}: {msg['content']}")
        
        try:
            response = chat_completion(
                messages=messages,
                api_url=api_url,
                api_key=api_key,
                model=model,
                temperature=0.7,
                max_tokens=200,
                timeout=20
            )
            
            # 提取回复
            if response and 'choices' in response and response['choices']:
                reply = response['choices'][0]['message']['content']
                print(f"\n🤖 assistant: {reply}")
                
                # 显示使用信息
                if 'usage' in response:
                    usage = response['usage']
                    print(f"\n📊 使用统计:")
                    print(f"  输入tokens: {usage.get('prompt_tokens', 'N/A')}")
                    print(f"  输出tokens: {usage.get('completion_tokens', 'N/A')}")
                    print(f"  总计tokens: {usage.get('total_tokens', 'N/A')}")
            else:
                print("❌ 响应格式异常")
                
        except Exception as e:
            print(f"❌ API调用出错: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def demo_parameter_control():
    """参数控制演示"""
    print("\n🎛️ 参数控制演示")
    print("-" * 30)
    
    try:
        from beaver.config import config_manager
        from beaver.inference import simple_chat
        
        # 加载配置
        config = config_manager.load_config('resources/config.json')
        default_config = config['default']
        
        api_url = default_config['api/url']
        api_key = default_config['api/sk']
        model = default_config['api/model']
        
        question = "写一个关于人工智能的故事"
        
        # 不同温度值的对比
        temperatures = [0.2, 0.7, 1.2]
        
        for temp in temperatures:
            print(f"\n🌡️ 温度值: {temp}")
            
            try:
                response = simple_chat(
                    prompt=question,
                    api_url=api_url,
                    api_key=api_key,
                    model=model,
                    temperature=temp,
                    max_tokens=100,
                    timeout=20
                )
                print(f"📝 回答: {response[:100]}...")
                
            except Exception as e:
                print(f"❌ 出错: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def main():
    """运行所有演示"""
    print("🎉 Beaver 推理功能演示")
    print("=" * 50)
    
    demos = [
        demo_simple_chat,
        demo_with_system_prompt,
        demo_chat_completion,
        demo_parameter_control
    ]
    
    passed = 0
    for demo in demos:
        if demo():
            passed += 1
    
    print(f"\n📊 演示结果: {passed}/{len(demos)} 个成功")
    
    if passed > 0:
        print("\n🎉 推理功能演示完成！")
        print("\n💡 快速使用指南:")
        print("```python")
        print("from beaver.inference import simple_chat")
        print("")
        print("response = simple_chat(")
        print("    prompt='你好',")
        print("    api_url='your_api_url',")
        print("    api_key='your_api_key',")
        print("    model='your_model'")
        print(")")
        print("print(response)")
        print("```")
    else:
        print("❌ 所有演示都失败了，请检查配置")

if __name__ == '__main__':
    main() 