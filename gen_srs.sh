#!/bin/bash

# 检查是否传入了参数
if [ -z "$1" ]; then
  echo "Usage: $0 <target-directory>"
  exit 1
fi

# 目标目录
TARGET_DIR="$1"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Directory $TARGET_DIR does not exist."
  exit 1
fi

# 遍历目录下的所有文件
for file in "$TARGET_DIR"/*; do
  if [ -f "$file" ]; then
    # 获取文件名（不带路径）和文件路径（不带扩展名）
    filename=$(basename "$file")
    filepath="${file%.*}"

    # 检查文件是否为JSON文件
    if [[ "$filename" == *.json ]]; then
      # 设置输出的SRS文件路径
      output_file="${filepath}.srs"

      # 执行命令
      sing-box rule-set compile --output "$output_file" "$file"

      # 检查命令是否成功
      if [ $? -ne 0 ]; then
        echo "Error processing file: $file"
      else
        echo "Successfully processed file: $file, output: $output_file"
      fi
    fi
  fi
done