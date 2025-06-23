#!/usr/bin/env python3
"""
Beaver DSL 文件上传功能示例

演示如何使用新的文件上传命令将媒体文件转换为OpenAI API格式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from beaver import execute
from beaver.inference.action_stream import parse_edn, edn_to_python

def eval_edn(edn_str):
    """解析并执行EDN字符串"""
    parsed = parse_edn(edn_str)
    python_data = edn_to_python(parsed)
    return execute(python_data)

def main():
    print("🚀 Beaver DSL 文件上传功能示例")
    print("=" * 50)
    
    # 创建示例文件
    print("\n📝 创建示例文件...")
    
    # 创建小的PNG图片
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\xdac\xf8\x0f\x00\x00\x01\x00\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    with open("example.png", "wb") as f:
        f.write(png_data)
    
    with open("example.mp3", "w") as f:
        f.write("fake audio content")
    
    with open("example.mp4", "w") as f:
        f.write("fake video content")
    
    print("✅ 示例文件创建完成")
    
    try:
        # 示例1：基础图片上传
        print("\n1️⃣ 基础图片上传")
        print("-" * 30)
        result = eval_edn('[:file.upload/img "example.png"]')
        print(result)
        
        # 示例2：高质量图片上传
        print("\n2️⃣ 高质量图片上传")
        print("-" * 30)
        result = eval_edn('[:file.upload/img "example.png" "high"]')
        print(result)
        
        # 示例3：视频上传
        print("\n3️⃣ 视频文件上传")
        print("-" * 30)
        result = eval_edn('[:file.upload/video "example.mp4"]')
        print(result)
        
        # 示例4：音频上传
        print("\n4️⃣ 音频文件上传")
        print("-" * 30)
        result = eval_edn('[:file.upload/audio "example.mp3"]')
        print(result)
        
        # 示例5：批量上传
        print("\n5️⃣ 批量文件上传")
        print("-" * 30)
        result = eval_edn('[:file.upload/batch ["example.png", "example.mp4", "example.mp3"]]')
        print(result)
        
        # 示例6：获取OpenAI API数据
        print("\n6️⃣ 获取OpenAI API数据")
        print("-" * 30)
        result = eval_edn('[:file.upload/get-data "example.png" "image"]')
        print("OpenAI API 格式数据:")
        print(result)
        
        print("\n🎯 实际应用场景")
        print("-" * 30)
        print("""
这些命令可以在以下场景中使用：

1. 聊天机器人图片理解：
   [:file.upload/img "user_photo.jpg" "high"]

2. 视频内容分析：
   [:file.upload/video "demo_video.mp4"]

3. 音频转录或分析：
   [:file.upload/audio "recording.mp3"]

4. 批量媒体处理：
   [:file.upload/batch ["img1.jpg", "video1.mp4", "audio1.mp3"]]

5. 获取API格式数据用于自定义处理：
   [:file.upload/get-data "image.jpg" "image"]
        """)
        
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # 清理示例文件
        print("\n🧹 清理示例文件...")
        for filename in ["example.png", "example.mp3", "example.mp4"]:
            if os.path.exists(filename):
                os.remove(filename)
                print(f"  - 删除 {filename}")
        print("✅ 清理完成")

if __name__ == "__main__":
    main() 