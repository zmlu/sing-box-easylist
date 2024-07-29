#!/bin/bash

# 目标目录
TARGET_DIR="./sing-box"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Directory $TARGET_DIR does not exist."
  exit 1
fi

# 使用 find 命令递归查找所有JSON文件
find "$TARGET_DIR" -type f -name '*.txt' | while read -r file; do
  # 获取文件名（不带路径）和文件路径（不带扩展名）
  filename=$(basename "$file")
  filepath="${file%.*}"

  # 设置输出的SRS文件路径
  output_file="${filepath}.srs"

  # 调试输出
  echo "Compiling JSON file to SRS: $file"
  echo "Output file: $output_file"

  # 执行命令
  sing-box rule-set convert --type adguard --output "$output_file" "$file"

  # 检查命令是否成功
  if [ $? -ne 0 ]; then
    echo "Error processing file: $file"
  else
    echo "Successfully processed file: $file, output: $output_file"
  fi
done