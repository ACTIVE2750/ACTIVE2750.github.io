import os
import ffmpeg

def convert_gif_to_mp4(input_gif_path, output_mp4_path, fps=10, width=1280, height=720):
    """
    使用ffmpeg-python将GIF转换为MP4
    """
    try:
        # 构建FFmpeg命令链
        (
            ffmpeg
            .input(input_gif_path)
            .filter('fps', fps=fps)          # 设置输出帧率
            .filter('scale', width, height)  # 强制缩放分辨率
            .output(
                output_mp4_path,
                vcodec='libx264',     # H.264编码
                pix_fmt='yuv420p',    # 兼容像素格式
                preset='medium',      # 编码速度/质量平衡
                crf=23,               # 质量系数（0-51，越小质量越高）
                movflags='faststart'  # 流式播放优化
            )
            .overwrite_output()       # 自动覆盖已有文件
            .run(quiet=True)         # 静默模式运行
        )
        print(f"成功转换: '{input_gif_path}' -> '{output_mp4_path}'")

    except ffmpeg.Error as e:
        print(f"FFmpeg错误: {e.stderr.decode('utf8')}")
    except Exception as e:
        print(f"其他错误: {str(e)}")

def convert_all_gifs_in_directory(directory=".", fps=10, width=1280, height=720):
    """
    批量转换目录下所有GIF
    """
    output_dir = os.path.join(directory, "converted_mp4s")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(directory):
        if filename.lower().endswith(".gif"):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(
                output_dir,
                f"{os.path.splitext(filename)[0]}.mp4"
            )
            
            print(f"正在处理: {filename}")
            convert_gif_to_mp4(input_path, output_path, fps, width, height)

if __name__ == "__main__":
    # 配置参数
    CONFIG = {
        "fps": 10,
        "width": 1280,
        "height": 720,
        "target_dir": os.getcwd()
    }

    print(f"开始转换目录: {CONFIG['target_dir']}")
    convert_all_gifs_in_directory(
        CONFIG['target_dir'],
        CONFIG['fps'],
        CONFIG['width'],
        CONFIG['height']
    )
    print(f"\n转换完成！输出目录: {os.path.join(CONFIG['target_dir'], 'converted_mp4s')}")