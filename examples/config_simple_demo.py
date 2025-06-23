#!/usr/bin/env python3
"""
配置模块简化使用示例
展示配置加载和访问的基本功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from beaver.config import config_manager, get_api_config, list_api_providers
import json

def demo_basic_config_usage():
    """基础配置使用演示"""
    print("=== 基础配置使用演示 ===")
    
    # 列出所有可用的API提供商
    providers = list_api_providers()
    print(f"可用的API提供商:")
    for i, provider in enumerate(providers[:5], 1):
        print(f"  {i}. {provider}")
    
    print(f"总共找到 {len(providers)} 个提供商\n")

def demo_specific_provider_config():
    """特定提供商配置演示"""
    print("=== 特定提供商配置演示 ===")
    
    # 获取默认配置
    default_config = get_api_config('default')
    
    print("默认API配置:")
    print(f"  URL: {default_config.get('api/url', '未配置')}")
    print(f"  模型: {default_config.get('api/model', '未配置')}")
    sk = default_config.get('api/sk', '未配置')
    print(f"  密钥: {sk[:20] + '...' if sk and len(sk) > 20 else sk}")
    print()

def demo_config_comparison():
    """配置对比演示"""
    print("=== 配置对比演示 ===")
    
    # 选择几个提供商进行对比
    providers_to_compare = ['default', 'neko/grok-3', 'yunwu/gemini-1.5-pro']
    
    print("API提供商配置对比:")
    print(f"{'提供商':<25} {'API URL':<30} {'模型':<25} {'温度':<10}")
    print("-" * 90)
    
    for provider in providers_to_compare:
        config = get_api_config(provider)
        if config:
            url = config.get('api/url', '未配置')
            if len(url) > 25:
                url = url[:25] + "..."
            
            model = config.get('api/model', '未配置')
            if len(model) > 20:
                model = model[:20] + "..."
                
            temp = str(config.get('model/temperature', '未设置'))
            
            print(f"{provider:<25} {url:<30} {model:<25} {temp:<10}")
    print()

def demo_dynamic_config_access():
    """动态配置访问演示"""
    print("=== 动态配置访问演示 ===")
    
    # 演示如何通过路径访问嵌套配置
    config_paths = [
        'default/api/url',
        'neko/grok-3/api/model', 
        'yunwu/gemini-1.5-pro/model/temperature',
        'deepseek.origin/chat/model/top_p'
    ]
    
    # 验证路径是否存在的测试
    available_sections = config_manager.list_sections()
    print(f"可用的配置部分: {available_sections[:5]}...")  # 显示前5个
    
    print("使用路径形式访问嵌套配置值:")
    for path in config_paths:
        value = config_manager.get_config(path, '未找到')
        print(f"  {path}: {value}")
    print()

def demo_config_validation():
    """配置验证演示"""
    print("=== 配置验证演示 ===")
    
    # 检查配置完整性
    providers = list_api_providers()
    
    print("配置验证结果:")
    for provider in providers[:3]:  # 只检查前3个
        config = get_api_config(provider)
        
        # 检查必需字段
        required_fields = ['api/url', 'api/model', 'api/sk']
        missing_fields = [field for field in required_fields if not config.get(field)]
        
        if missing_fields:
            status = f"❌ 缺少字段: {', '.join(missing_fields)}"
        else:
            status = "✅ 配置完整"
        
        print(f"  {provider}: {status}")
    print()

def demo_environment_config():
    """环境变量配置演示"""
    print("=== 环境变量配置演示 ===")
    
    print("配置文件支持环境变量替换，格式如下:")
    example_config = {
        "api_key": "${API_KEY}",
        "debug_mode": "${DEBUG:-false}",
        "database_url": "${DATABASE_URL}"
    }
    
    print(json.dumps(example_config, indent=2, ensure_ascii=False))
    
    print("\n支持的格式:")
    print("  • ${VAR} - 简单变量替换")
    print("  • ${VAR:-default} - 带默认值的变量替换")
    print()

def demo_config_management():
    """配置管理演示"""
    print("=== 配置管理演示 ===")
    
    # 演示配置管理功能
    print("配置管理功能:")
    
    # 列出配置部分
    sections = config_manager.list_sections()
    print(f"  配置部分总数: {len(sections)}")
    
    # 检查特定部分
    has_default = config_manager.has_section('default')
    print(f"  是否有默认配置: {has_default}")
    
    # 获取配置部分
    if sections:
        first_section = config_manager.get_section(sections[0])
        print(f"  第一个配置部分 '{sections[0]}' 包含 {len(first_section)} 项配置")
    
    # 演示缓存功能
    print("  缓存状态: 已启用")
    config_manager.reload_config()
    print("  配置重新加载: 完成")
    print()

def main():
    """运行所有演示"""
    print("Beaver 配置模块使用示例")
    print("=" * 60)
    
    demos = [
        demo_basic_config_usage,
        demo_specific_provider_config,
        demo_config_comparison,
        demo_dynamic_config_access,
        demo_config_validation,
        demo_environment_config,
        demo_config_management
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"演示过程中出现错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main() 