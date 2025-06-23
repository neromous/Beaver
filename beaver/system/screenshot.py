"""
系统截屏功能模块

提供跨平台的系统截屏功能，支持全屏和窗口截屏
"""

import os
import time
import subprocess
from datetime import datetime
from typing import Dict, Any, Optional


# ================================
# 第一层：原始功能函数
# ================================

def screenshot_processor(
    output_path: Optional[str] = None,
    region: Optional[Dict[str, int]] = None,
    window_id: Optional[str] = None,
    delay: int = 0
) -> Dict[str, Any]:
    """
    截屏处理器，执行实际的截屏操作
    
    Args:
        output_path: 输出文件路径，None时自动生成
        region: 截屏区域 {"x": 0, "y": 0, "width": 800, "height": 600}
        window_id: 窗口ID（Linux下有效）
        delay: 延迟秒数
        
    Returns:
        Dict: {"success": bool, "result": {...}, "error": str}
    """
    try:
        import platform
        system = platform.system().lower()
        
        # 延迟执行
        if delay > 0:
            time.sleep(delay)
        
        # 生成输出路径
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"screenshot_{timestamp}.png"
        
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 根据系统执行截屏
        if system == "linux":
            success = _linux_screenshot(output_path, region, window_id)
        elif system == "darwin":  # macOS
            success = _macos_screenshot(output_path, region)
        elif system == "windows":
            success = _windows_screenshot(output_path, region)
        else:
            return {
                "success": False,
                "error": f"不支持的操作系统: {system}"
            }
        
        if success and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            return {
                "success": True,
                "result": {
                    "path": os.path.abspath(output_path),
                    "size": file_size,
                    "region": region,
                    "timestamp": datetime.now().isoformat()
                }
            }
        else:
            return {
                "success": False,
                "error": "截屏失败或文件未生成"
            }
            
    except ImportError as e:
        return {
            "success": False,
            "error": f"缺少依赖库: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"截屏失败: {str(e)}"
        }


def _linux_screenshot(output_path: str, region: Optional[Dict], window_id: Optional[str]) -> bool:
    """Linux系统截屏实现"""
    try:
        # 尝试使用不同的截屏工具
        tools = ["gnome-screenshot", "scrot", "import", "xwd"]
        
        for tool in tools:
            if _command_exists(tool):
                cmd = _build_linux_command(tool, output_path, region, window_id)
                if cmd:
                    result = subprocess.run(cmd, shell=True, capture_output=True)
                    return result.returncode == 0
        
        return False
    except Exception:
        return False


def _macos_screenshot(output_path: str, region: Optional[Dict]) -> bool:
    """macOS系统截屏实现"""
    try:
        cmd = ["screencapture", "-x"]  # -x 不播放声音
        
        if region:
            x, y = region.get("x", 0), region.get("y", 0)
            w, h = region.get("width", 800), region.get("height", 600)
            cmd.extend(["-R", f"{x},{y},{w},{h}"])
        
        cmd.append(output_path)
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    except Exception:
        return False


def _windows_screenshot(output_path: str, region: Optional[Dict]) -> bool:
    """Windows系统截屏实现"""
    try:
        # 使用Python的PIL库
        from PIL import ImageGrab
        
        if region:
            bbox = (
                region.get("x", 0),
                region.get("y", 0),
                region.get("x", 0) + region.get("width", 800),
                region.get("y", 0) + region.get("height", 600)
            )
            screenshot = ImageGrab.grab(bbox=bbox)
        else:
            screenshot = ImageGrab.grab()
        
        screenshot.save(output_path)
        return True
    except ImportError:
        # 回退到PowerShell方法
        return _windows_powershell_screenshot(output_path)
    except Exception:
        return False


def _windows_powershell_screenshot(output_path: str) -> bool:
    """Windows PowerShell截屏方法"""
    try:
        ps_script = f'''
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $Screen = [System.Windows.Forms.SystemInformation]::VirtualScreen
        $bitmap = New-Object System.Drawing.Bitmap $Screen.Width, $Screen.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($Screen.Left, $Screen.Top, 0, 0, $bitmap.Size)
        $bitmap.Save("{output_path}")
        $graphics.Dispose()
        $bitmap.Dispose()
        '''
        
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True
        )
        return result.returncode == 0
    except Exception:
        return False


def _build_linux_command(tool: str, output_path: str, region: Optional[Dict], window_id: Optional[str]) -> Optional[str]:
    """构建Linux截屏命令"""
    # 确保输出路径被正确引用
    quoted_path = f'"{output_path}"'
    
    if tool == "gnome-screenshot":
        cmd = f"gnome-screenshot -f {quoted_path}"
        if window_id:
            cmd += f" -w"
        return cmd
    
    elif tool == "scrot":
        cmd = f"scrot"
        if region:
            x, y = region.get("x", 0), region.get("y", 0)
            w, h = region.get("width", 800), region.get("height", 600)
            cmd += f" -a {x},{y},{w},{h}"
        if window_id:
            cmd += f" -s"  # 选择窗口模式
        cmd += f" {quoted_path}"
        return cmd
    
    elif tool == "import":  # ImageMagick
        if region:
            w, h = region.get("width", 800), region.get("height", 600)
            x, y = region.get("x", 0), region.get("y", 0)
            cmd = f"import -window root -crop {w}x{h}+{x}+{y} {quoted_path}"
        else:
            cmd = f"import -window root {quoted_path}"
        return cmd
    
    return None


def _command_exists(command: str) -> bool:
    """检查命令是否存在"""
    try:
        subprocess.run(["which", command], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


# ================================
# 第二层：Wrapper函数
# ================================

def screenshot_wrapper(
    output_path: Optional[str] = None,
    region: Optional[Dict[str, int]] = None,
    window_id: Optional[str] = None,
    delay: int = 0
) -> str:
    """
    截屏功能的wrapper函数
    
    Args:
        output_path: 输出文件路径
        region: 截屏区域
        window_id: 窗口ID
        delay: 延迟秒数
        
    Returns:
        str: 格式化的截屏结果
    """
    result = screenshot_processor(output_path, region, window_id, delay)
    
    if result["success"]:
        data = result["result"]
        file_size_mb = round(data["size"] / (1024 * 1024), 2)
        
        output_lines = [
            f"📸 截屏成功",
            f"📄 文件路径: {data['path']}",
            f"📊 文件大小: {file_size_mb} MB",
            f"⏰ 截屏时间: {data['timestamp']}"
        ]
        
        if data["region"]:
            region = data["region"]
            output_lines.append(f"🔲 截屏区域: {region['width']}x{region['height']} at ({region['x']},{region['y']})")
        else:
            output_lines.append("🖥️ 截屏类型: 全屏")
        
        return "\n".join(output_lines)
    else:
        return f"❌ 截屏失败: {result['error']}"


# ================================
# 第三层：DSL命令注册
# ================================

from beaver.core.decorators import bf_element

@bf_element(
    ':system/screenshot',
    description='系统截屏，支持全屏和区域截屏',
    category='System',
    usage="[':system/screenshot'] 或 [':system/screenshot', {'path': 'output.png', 'delay': 3}]"
)
def screenshot_command(options: Optional[Dict[str, Any]] = None):
    """
    系统截屏命令
    
    用法:
    - [:system/screenshot] - 全屏截屏
    - [:system/screenshot {"path": "screen.png"}] - 指定输出路径
    - [:system/screenshot {"delay": 3}] - 延迟3秒截屏
    - [:system/screenshot {"region": {"x": 100, "y": 100, "width": 800, "height": 600}}] - 区域截屏
    """
    if options is None:
        options = {}
    
    if not isinstance(options, dict):
        return "❌ 参数必须是字典格式"
    
    # 提取参数（处理EDN关键字格式）
    output_path = options.get("path") or options.get(":path")
    region = options.get("region") or options.get(":region")
    window_id = options.get("window_id") or options.get(":window_id")
    delay = options.get("delay", 0) or options.get(":delay", 0)
    
    # 参数验证
    if delay and not isinstance(delay, int):
        return "❌ delay参数必须是整数"
    
    if region and not isinstance(region, dict):
        return "❌ region参数必须是字典格式"
    
    if region:
        required_keys = ["x", "y", "width", "height"]
        missing_keys = [key for key in required_keys if key not in region]
        if missing_keys:
            return f"❌ region缺少必需的键: {missing_keys}"
    
    return screenshot_wrapper(output_path, region, window_id, delay)


@bf_element(
    ':system/screenshot-delayed',
    description='延迟截屏，给用户准备时间',
    category='System',
    usage="[':system/screenshot-delayed', 5]"
)
def screenshot_delayed_command(delay: int = 3):
    """
    延迟截屏命令
    
    用法: [:system/screenshot-delayed 5] - 延迟5秒后截屏
    """
    if not isinstance(delay, int) or delay < 0:
        return "❌ 延迟时间必须是非负整数"
    
    return screenshot_wrapper(delay=delay)


@bf_element(
    ':system/screenshot-region',
    description='区域截屏',
    category='System',
    usage="[':system/screenshot-region', 100, 100, 800, 600]"
)
def screenshot_region_command(x: int, y: int, width: int, height: int, output_path: Optional[str] = None):
    """
    区域截屏命令
    
    用法: [:system/screenshot-region 100 100 800 600] - 截取指定区域
    """
    # 参数验证
    params = [x, y, width, height]
    if not all(isinstance(p, int) and p >= 0 for p in params):
        return "❌ 坐标和尺寸参数必须是非负整数"
    
    if width <= 0 or height <= 0:
        return "❌ 宽度和高度必须大于0"
    
    region = {"x": x, "y": y, "width": width, "height": height}
    return screenshot_wrapper(output_path, region) 