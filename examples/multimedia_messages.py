#!/usr/bin/env python3
"""
Beaver DSL 多媒体消息功能演示

演示如何使用增强的 :user 标签和相关命令处理多媒体内容
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from beaver import execute
from beaver.inference.action_stream import parse_edn, edn_to_python

def eval_edn(edn_str):
    """解析并执行EDN字符串"""
    try:
        parsed = parse_edn(edn_str)
        python_data = edn_to_python(parsed)
        return execute(python_data)
    except Exception as e:
        return f"❌ 解析/执行失败: {e}"

def main():
    print("🚀 Beaver DSL 多媒体消息功能演示")
    print("=" * 60)
    
    # 创建测试文件
    print("\n📝 创建测试文件...")
    
    # 创建小PNG图片
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    with open("demo.png", "wb") as f:
        f.write(png_data)
    
    with open("demo.mp4", "w") as f:
        f.write("fake video content")
    
    print("✅ 测试文件创建完成")
    
    try:
        # 示例1：传统纯文本用户消息
        print("\n1️⃣ 传统纯文本用户消息")
        print("-" * 40)
        print("命令: [:user \"Hello world\"]")
        result = eval_edn('[:user "Hello world"]')
        print(f"结果:\n{result}")
        
        # 示例2：多部分文本消息
        print("\n2️⃣ 多部分文本消息")
        print("-" * 40)
        print("命令: [:user \"foo\" \"bar\" \"baz\"]")
        result = eval_edn('[:user "foo" "bar" "baz"]')
        print(f"结果:\n{result}")
        
        # 示例3：文本+图片的多媒体消息
        print("\n3️⃣ 文本+图片多媒体消息")
        print("-" * 40)
        print("命令: [:user \"请分析这个图片\" [:file.upload/img \"demo.png\"]]")
        result = eval_edn('[:user "请分析这个图片" [:file.upload/img "demo.png"]]')
        print(f"结果:\n{result}")
        
        # 示例4：纯图片消息
        print("\n4️⃣ 纯图片消息")
        print("-" * 40)
        print("命令: [:user [:file.upload/img \"demo.png\"]]")
        result = eval_edn('[:user [:file.upload/img "demo.png"]]')
        print(f"结果:\n{result}")
        
        # 示例5：文本+视频消息
        print("\n5️⃣ 文本+视频消息")
        print("-" * 40)
        print("命令: [:user \"这是一个视频\" [:file.upload/video \"demo.mp4\"]]")
        result = eval_edn('[:user "这是一个视频" [:file.upload/video "demo.mp4"]]')
        print(f"结果:\n{result}")
        
        # 示例6：多媒体消息详细信息显示
        print("\n6️⃣ 多媒体消息详细信息")
        print("-" * 40)
        print("命令: [:msg/multimedia [:user \"图片描述\" [:file.upload/img \"demo.png\"]]]")
        result = eval_edn('[:msg/multimedia [:user "图片描述" [:file.upload/img "demo.png"]]]')
        print(f"结果:\n{result}")
        
        # 示例7：其他角色的消息
        print("\n7️⃣ 系统和助手消息")
        print("-" * 40)
        
        print("系统消息:")
        result = eval_edn('[:system "You are a helpful AI assistant."]')
        print(f"{result}\n")
        
        print("助手消息:")
        result = eval_edn('[:assistant "I can help you with image analysis."]')
        print(f"{result}")
        
        # 示例8：使用传统 v2m 命令
        print("\n8️⃣ 使用传统 v2m 命令处理多媒体")
        print("-" * 40)
        print("命令: [:msg/v2m [:user \"文本\" [:file.upload/img \"demo.png\"]]]")
        result = eval_edn('[:msg/v2m [:user "文本" [:file.upload/img "demo.png"]]]')
        print(f"结果:\n{result}")
        
        print("\n🎯 实际应用场景")
        print("-" * 40)
        print("""
这些功能的实际应用场景：

1. 图片理解和分析：
   [:user "这张图片里有什么？" [:file.upload/img "photo.jpg"]]

2. 视频内容分析：
   [:user "总结这个视频的内容" [:file.upload/video "meeting.mp4"]]

3. 多模态对话：
   [:user "比较这两张图片" [:file.upload/img "img1.jpg"] [:file.upload/img "img2.jpg"]]

4. 音频处理：
   [:user "转录这个音频文件" [:file.upload/audio "speech.mp3"]]

5. 复杂的多媒体查询：
   [:user "基于这个图片" [:file.upload/img "chart.png"] "和视频" [:file.upload/video "demo.mp4"] "生成报告"]

6. 与 :nexus/sync 集成使用：
   [":nexus/sync" {"provider": "openai", "model": "gpt-4-vision"} 
    [:user "分析图片" [:file.upload/img "image.jpg"]]]
        """)
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 清理测试文件
        print("\n🧹 清理测试文件...")
        for filename in ["demo.png", "demo.mp4"]:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"  - 删除 {filename}")
        print("✅ 清理完成")

if __name__ == "__main__":
    main() 