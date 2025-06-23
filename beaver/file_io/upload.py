"""
文件上传处理模块

将各种媒体文件转换为 OpenAI API 兼容的格式
支持图片、视频、音频文件的处理和编码
"""

import os
import base64
import mimetypes
from pathlib import Path
from typing import Dict, Any, Optional, List

# 可选的magic库导入
try:
    import magic
    HAS_MAGIC = True
except ImportError:
    HAS_MAGIC = False


# ================================
# 第一层：原始功能函数
# ================================

def file_upload_processor(
    file_path: str,
    media_type: str,
    detail: str = "auto",
    max_size_mb: float = 20.0
) -> Dict[str, Any]:
    """
    文件上传处理器，将文件转换为OpenAI API格式
    
    Args:
        file_path: 文件路径
        media_type: 媒体类型 ("image", "video", "audio")
        detail: 图片详细级别 ("low", "high", "auto")
        max_size_mb: 最大文件大小限制(MB)
        
    Returns:
        Dict: {"success": bool, "result": {...}, "error": str}
    """
    try:
        # 验证文件存在
        if not os.path.exists(file_path):
            return {
                "success": False,
                "error": f"文件不存在: {file_path}"
            }
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size_mb > max_size_mb:
            return {
                "success": False,
                "error": f"文件大小 {file_size_mb:.2f}MB 超过限制 {max_size_mb}MB"
            }
        
        # 获取文件信息
        file_info = _get_file_info(file_path)
        
        # 验证媒体类型
        if not _validate_media_type(file_info["mime_type"], media_type):
            return {
                "success": False,
                "error": f"文件类型 {file_info['mime_type']} 不匹配媒体类型 {media_type}"
            }
        
        # 读取并编码文件
        encoded_data = _encode_file_to_base64(file_path)
        
        # 构建OpenAI API格式
        media_dict = _build_openai_media_dict(
            encoded_data, 
            file_info, 
            media_type, 
            detail
        )
        
        return {
            "success": True,
            "result": {
                "media_dict": media_dict,
                "file_info": file_info,
                "media_type": media_type,
                "detail": detail,
                "size_mb": round(file_size_mb, 2)
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"文件处理失败: {str(e)}"
        }


def _get_file_info(file_path: str) -> Dict[str, Any]:
    """获取文件详细信息"""
    path_obj = Path(file_path)
    
    # 获取MIME类型
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # 使用python-magic获取更准确的MIME类型（如果可用）
    if HAS_MAGIC:
        try:
            mime_type = magic.from_file(file_path, mime=True)
        except Exception:
            # 回退到mimetypes
            if not mime_type:
                mime_type = "application/octet-stream"
    else:
        # 没有magic库时回退到mimetypes
        if not mime_type:
            mime_type = "application/octet-stream"
    
    return {
        "filename": path_obj.name,
        "extension": path_obj.suffix.lower(),
        "mime_type": mime_type,
        "size": os.path.getsize(file_path),
        "absolute_path": os.path.abspath(file_path)
    }


def _validate_media_type(mime_type: str, media_type: str) -> bool:
    """验证文件MIME类型是否匹配指定的媒体类型"""
    type_mappings = {
        "image": ["image/"],
        "video": ["video/"],
        "audio": ["audio/"]
    }
    
    if media_type not in type_mappings:
        return False
    
    valid_prefixes = type_mappings[media_type]
    return any(mime_type.startswith(prefix) for prefix in valid_prefixes)


def _encode_file_to_base64(file_path: str) -> str:
    """将文件编码为base64字符串"""
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode('utf-8')


def _build_openai_media_dict(
    encoded_data: str, 
    file_info: Dict[str, Any], 
    media_type: str, 
    detail: str
) -> Dict[str, Any]:
    """构建OpenAI API兼容的媒体字典"""
    
    # 构建data URL
    data_url = f"data:{file_info['mime_type']};base64,{encoded_data}"
    
    if media_type == "image":
        return {
            "type": "image_url",
            "image_url": {
                "url": data_url,
                "detail": detail
            }
        }
    elif media_type == "video":
        return {
            "type": "video",
            "video": {
                "url": data_url,
                "mime_type": file_info["mime_type"],
                "filename": file_info["filename"]
            }
        }
    elif media_type == "audio":
        return {
            "type": "audio",
            "audio": {
                "url": data_url,
                "mime_type": file_info["mime_type"],
                "filename": file_info["filename"]
            }
        }
    else:
        raise ValueError(f"不支持的媒体类型: {media_type}")


def batch_upload_processor(
    file_paths: List[str],
    media_types: Optional[List[str]] = None,
    detail: str = "auto",
    max_size_mb: float = 20.0
) -> Dict[str, Any]:
    """
    批量文件上传处理器
    
    Args:
        file_paths: 文件路径列表
        media_types: 媒体类型列表（可选，自动检测）
        detail: 图片详细级别
        max_size_mb: 最大文件大小限制
        
    Returns:
        Dict: {"success": bool, "results": [...], "errors": [...]}
    """
    try:
        results = []
        errors = []
        
        for i, file_path in enumerate(file_paths):
            # 确定媒体类型
            if media_types and i < len(media_types):
                media_type = media_types[i]
            else:
                media_type = _auto_detect_media_type(file_path)
                if not media_type:
                    errors.append(f"无法检测文件 {file_path} 的媒体类型")
                    continue
            
            # 处理单个文件
            result = file_upload_processor(file_path, media_type, detail, max_size_mb)
            
            if result["success"]:
                results.append(result["result"])
            else:
                errors.append(f"{file_path}: {result['error']}")
        
        return {
            "success": len(errors) == 0,
            "results": results,
            "errors": errors,
            "processed_count": len(results),
            "error_count": len(errors)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"批量处理失败: {str(e)}"
        }


def _auto_detect_media_type(file_path: str) -> Optional[str]:
    """自动检测文件的媒体类型"""
    try:
        file_info = _get_file_info(file_path)
        mime_type = file_info["mime_type"]
        
        if mime_type.startswith("image/"):
            return "image"
        elif mime_type.startswith("video/"):
            return "video"
        elif mime_type.startswith("audio/"):
            return "audio"
        else:
            return None
            
    except Exception:
        return None


# ================================
# 第二层：Wrapper函数
# ================================

def img_upload_wrapper(file_path: str, detail: str = "auto") -> str:
    """图片上传wrapper函数"""
    result = file_upload_processor(file_path, "image", detail)
    
    if result["success"]:
        data = result["result"]
        file_info = data["file_info"]
        
        output_lines = [
            f"🖼️ 图片上传成功",
            f"📄 文件名: {file_info['filename']}",
            f"📊 文件大小: {data['size_mb']} MB",
            f"🎨 MIME类型: {file_info['mime_type']}",
            f"🔍 详细级别: {data['detail']}",
            f"💾 已转换为OpenAI API格式"
        ]
        
        return "\n".join(output_lines)
    else:
        return f"❌ 图片上传失败: {result['error']}"


def video_upload_wrapper(file_path: str) -> str:
    """视频上传wrapper函数"""
    result = file_upload_processor(file_path, "video")
    
    if result["success"]:
        data = result["result"]
        file_info = data["file_info"]
        
        output_lines = [
            f"🎬 视频上传成功",
            f"📄 文件名: {file_info['filename']}",
            f"📊 文件大小: {data['size_mb']} MB",
            f"🎭 MIME类型: {file_info['mime_type']}",
            f"💾 已转换为OpenAI API格式"
        ]
        
        return "\n".join(output_lines)
    else:
        return f"❌ 视频上传失败: {result['error']}"


def audio_upload_wrapper(file_path: str) -> str:
    """音频上传wrapper函数"""
    result = file_upload_processor(file_path, "audio")
    
    if result["success"]:
        data = result["result"]
        file_info = data["file_info"]
        
        output_lines = [
            f"🎵 音频上传成功",
            f"📄 文件名: {file_info['filename']}",
            f"📊 文件大小: {data['size_mb']} MB",
            f"🎶 MIME类型: {file_info['mime_type']}",
            f"💾 已转换为OpenAI API格式"
        ]
        
        return "\n".join(output_lines)
    else:
        return f"❌ 音频上传失败: {result['error']}"


def batch_upload_wrapper(file_paths: List[str]) -> str:
    """批量上传wrapper函数"""
    result = batch_upload_processor(file_paths)
    
    if result["success"]:
        output_lines = [
            f"📦 批量上传成功",
            f"✅ 成功处理: {result['processed_count']} 个文件",
            f"❌ 处理失败: {result['error_count']} 个文件"
        ]
        
        # 显示每个成功文件的信息
        for i, file_result in enumerate(result["results"], 1):
            file_info = file_result["file_info"]
            media_type = file_result["media_type"]
            icon = {"image": "🖼️", "video": "🎬", "audio": "🎵"}.get(media_type, "📄")
            
            output_lines.append(
                f"  {i}. {icon} {file_info['filename']} ({file_result['size_mb']} MB)"
            )
        
        return "\n".join(output_lines)
    else:
        error_summary = "\n".join([f"  - {error}" for error in result["errors"]])
        return f"❌ 批量上传失败:\n{error_summary}"


# ================================
# 第三层：DSL命令注册
# ================================

from beaver.core.decorators import bf_element

@bf_element(
    ':file.upload/img',
    description='将图片文件转换为OpenAI API格式',
    category='FileUpload',
    usage="[':file.upload/img', 'image.jpg'] 或 [':file.upload/img', 'image.jpg', 'high']"
)
def img_upload_command(file_path: str, detail: str = "auto"):
    """
    图片上传命令
    
    用法:
    - [:file.upload/img "image.jpg"] - 默认详细级别
    - [:file.upload/img "image.jpg" "high"] - 高详细级别
    - [:file.upload/img "image.jpg" "low"] - 低详细级别
    """
    if not isinstance(file_path, str):
        return "❌ 文件路径必须是字符串"
    
    if detail not in ["auto", "low", "high"]:
        return "❌ detail参数必须是 'auto', 'low' 或 'high'"
    
    return img_upload_wrapper(file_path, detail)


@bf_element(
    ':file.upload/video',
    description='将视频文件转换为OpenAI API格式',
    category='FileUpload',
    usage="[':file.upload/video', 'video.mp4']"
)
def video_upload_command(file_path: str):
    """
    视频上传命令
    
    用法: [:file.upload/video "video.mp4"]
    """
    if not isinstance(file_path, str):
        return "❌ 文件路径必须是字符串"
    
    return video_upload_wrapper(file_path)


@bf_element(
    ':file.upload/audio',
    description='将音频文件转换为OpenAI API格式',
    category='FileUpload',
    usage="[':file.upload/audio', 'audio.mp3']"
)
def audio_upload_command(file_path: str):
    """
    音频上传命令
    
    用法: [:file.upload/audio "audio.mp3"]
    """
    if not isinstance(file_path, str):
        return "❌ 文件路径必须是字符串"
    
    return audio_upload_wrapper(file_path)


@bf_element(
    ':file.upload/batch',
    description='批量上传多个媒体文件',
    category='FileUpload',
    usage="[':file.upload/batch', ['img1.jpg', 'video1.mp4', 'audio1.mp3']]"
)
def batch_upload_command(file_paths: List[str]):
    """
    批量上传命令
    
    用法: [:file.upload/batch ["image.jpg", "video.mp4", "audio.mp3"]]
    """
    if not isinstance(file_paths, list):
        return "❌ 文件路径列表必须是数组"
    
    if not all(isinstance(path, str) for path in file_paths):
        return "❌ 所有文件路径都必须是字符串"
    
    return batch_upload_wrapper(file_paths)


@bf_element(
    ':file.upload/get-data',
    description='获取上传文件的OpenAI API数据',
    category='FileUpload',
    usage="[':file.upload/get-data', 'image.jpg', 'image']"
)
def get_upload_data_command(file_path: str, media_type: str):
    """
    获取上传数据命令（返回原始字典）
    
    用法: [:file.upload/get-data "image.jpg" "image"]
    """
    if not isinstance(file_path, str):
        return "❌ 文件路径必须是字符串"
    
    if media_type not in ["image", "video", "audio"]:
        return "❌ 媒体类型必须是 'image', 'video' 或 'audio'"
    
    result = file_upload_processor(file_path, media_type)
    
    if result["success"]:
        return str(result["result"]["media_dict"])
    else:
        return f"❌ 获取数据失败: {result['error']}"