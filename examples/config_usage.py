#!/usr/bin/env python3
"""
Beaver 配置系统使用演示
展示新配置结构的完整功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from beaver.config import (
    config_manager,
    get_provider_config,
    get_new_api_config,
    get_model_config,
    list_providers,
    list_models,
    list_all_provider_models,
    get_default_provider,
    get_default_config,
    get_settings,
    validate_provider_config,
    find_provider_by_model_name,
    migrate_legacy_config
)

def demo_basic_usage():
    """基础使用演示"""
    print("🚀 基础配置使用演示")
    print("-" * 40)
    
    # 添加新配置文件
    config_manager.add_config_file('resources/config_new.json')
    
    # 列出提供商
    providers = list_providers()
    print(f"📋 可用提供商 ({len(providers)}个): {', '.join(providers)}")
    
    # 选择一个提供商查看其模型
    if providers:
        provider = providers[0]
        models = list_models(provider)
        print(f"🏷️  {provider} 的模型: {', '.join(models)}")
        
        # 获取第一个模型的配置
        if models:
            model = models[0]
            api_config = get_new_api_config(provider, model)
            print(f"🔗 {provider}/{model} API配置:")
            print(f"   URL: {api_config.get('url', '未配置')}")
            print(f"   模型: {api_config.get('model', '未配置')}")
            print(f"   密钥: {'***已配置***' if api_config.get('secret_key') else '未配置'}")
    print()

def demo_advanced_queries():
    """高级查询演示"""
    print("🔍 高级查询功能演示")
    print("-" * 40)
    
    # 搜索特定模型
    gemini_models = find_provider_by_model_name('gemini')
    print(f"🔎 包含 'gemini' 的模型 ({len(gemini_models)}个):")
    for model in gemini_models[:3]:
        print(f"   • {model['full_name']}")
    
    # 列出所有模型组合
    all_combinations = list_all_provider_models()
    print(f"📊 总计 {len(all_combinations)} 个提供商/模型组合")
    
    # 获取默认配置
    default = get_default_provider()
    print(f"⭐ 默认配置: {default}")
    print()

def demo_config_validation():
    """配置验证演示"""
    print("✅ 配置验证演示")
    print("-" * 40)
    
    providers = list_providers()
    valid_count = 0
    total_count = 0
    
    for provider in providers[:2]:  # 只验证前2个提供商
        models = list_models(provider)
        for model in models[:1]:  # 每个提供商只验证第一个模型
            total_count += 1
            result = validate_provider_config(provider, model)
            
            if result['valid']:
                status = "✅ 有效"
                valid_count += 1
            else:
                status = "❌ 无效"
            
            print(f"   {provider}/{model}: {status}")
            
            if result['missing_fields']:
                print(f"      缺少: {', '.join(result['missing_fields'])}")
            
            if result['warnings']:
                for warning in result['warnings']:
                    print(f"      ⚠️  {warning}")
    
    print(f"📈 验证结果: {valid_count}/{total_count} 个配置有效")
    print()

def demo_settings_management():
    """设置管理演示"""
    print("⚙️  设置管理演示")
    print("-" * 40)
    
    settings = get_settings()
    print("🔧 全局设置:")
    for key, value in settings.items():
        print(f"   {key}: {value}")
    print()

def demo_legacy_migration():
    """旧配置迁移演示"""
    print("🔄 配置迁移演示")
    print("-" * 40)
    
    try:
        # 加载旧配置
        legacy_config = config_manager.load_config('resources/config.json')
        print(f"📁 旧配置文件包含 {len(legacy_config)} 个顶级配置项")
        
        # 迁移
        new_config = migrate_legacy_config(legacy_config)
        
        # 显示迁移结果
        providers_count = len(new_config.get('providers', {}))
        print(f"🔄 迁移完成:")
        print(f"   提供商: {providers_count} 个")
        print(f"   默认配置: {new_config.get('default', {})}")
        print(f"   全局设置: {bool(new_config.get('settings'))}")
        
        # 显示一个迁移示例
        if 'providers' in new_config:
            first_provider = list(new_config['providers'].keys())[0]
            first_model = list(new_config['providers'][first_provider].keys())[0]
            sample = new_config['providers'][first_provider][first_model]
            print(f"📋 迁移示例 ({first_provider}/{first_model}):")
            print(f"   API配置: {bool(sample.get('api'))}")
            print(f"   模型配置: {bool(sample.get('model'))}")
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
    
    print()

def demo_practical_usage():
    """实际使用场景演示"""
    print("💼 实际使用场景演示")
    print("-" * 40)
    
    # 场景1: 获取特定提供商的API配置
    print("🎯 场景1: 获取生产环境API配置")
    api_config = get_new_api_config('neko', 'grok-3')
    if api_config:
        print(f"   ✅ 已获取 neko/grok-3 配置")
        print(f"   🌐 API端点: {api_config.get('url', '未配置')}")
    else:
        print("   ❌ 配置不存在")
    
    # 场景2: 动态选择最优模型
    print("\n🎯 场景2: 查找最快的模型")
    fast_models = find_provider_by_model_name('flash')
    if fast_models:
        print(f"   🚀 找到 {len(fast_models)} 个快速模型:")
        for model in fast_models[:2]:
            print(f"      • {model['full_name']}")
    
    # 场景3: 验证配置完整性
    print("\n🎯 场景3: 部署前配置检查")
    critical_providers = [('neko', 'grok-3'), ('yunwu', 'gemini-1.5-pro')]
    all_valid = True
    
    for provider, model in critical_providers:
        result = validate_provider_config(provider, model)
        if result['valid']:
            print(f"   ✅ {provider}/{model} 配置完整")
        else:
            print(f"   ❌ {provider}/{model} 配置不完整")
            all_valid = False
    
    print(f"   {'🚀 可以部署' if all_valid else '⚠️  需要修复配置'}")
    print()

def main():
    """运行所有演示"""
    print("🎉 Beaver 配置系统完整演示")
    print("=" * 60)
    
    demos = [
        demo_basic_usage,
        demo_advanced_queries,
        demo_config_validation,
        demo_settings_management,
        demo_legacy_migration,
        demo_practical_usage
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n📍 演示 {i}/{len(demos)}")
        try:
            demo()
        except Exception as e:
            print(f"❌ 演示出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("🏁 演示完成！")
    print("\n💡 提示:")
    print("   • 使用 get_new_api_config() 获取API配置")
    print("   • 使用 list_providers() 查看所有提供商")
    print("   • 使用 validate_provider_config() 验证配置")
    print("   • 查看 CONFIG_DESIGN.md 了解更多详情")

if __name__ == '__main__':
    main() 