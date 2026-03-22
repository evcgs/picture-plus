# Picture Plus 🎨 - 参考图风格匹配生图工具

根据参考图片风格，**一次性生成 9 张风格一致的新图片**。  
同时支持 **Google Gemini** 和 **字节火山引擎豆包 Seedream** 两种 API，可以任选其一使用。

## 功能特点

- ✅ **检查图片规格** - 生成前先查看参考图的分辨率、文件大小、宽高比
- ✅ **参考风格匹配** - 上传一张参考图，生成的新图会匹配它的风格
- ✅ **批量生成 9 张** - 一次生成 9 张，总有一张你满意（非常适合做 3x3 九宫格）
- ✅ **双 API 支持** - Google Gemini / 火山豆包 都可以用，国内推荐用火山
- ✅ **自动生成预览拼贴** - 自动输出一张 3x3 九宫格预览图，方便挑选
- ✅ **灵活尺寸** - 自动匹配参考图尺寸，也可以自定义宽高
- ✅ **两种使用方式** - 支持 OpenClaw 聊天窗口直接用，也支持命令行使用

## 安装

### 1. 安装技能
```bash
# 通过 OpenClaw skills 安装
npx skills add evcgs/picture-plus
```

或者手动克隆：
```bash
git clone https://github.com/evcgs/picture-plus.git
cd picture-plus
```

### 2. 安装 Python 依赖
```bash
pip3 install google-generativeai pillow
```

### 3. 配置 API Key

你至少需要配置一个 API Key：

| 服务商 | 获取地址 | 环境变量名 |
|--------|----------|------------|
| Google Gemini | [Google AI Studio](https://makersuite.google.com/app/apikey) | `GOOGLE_API_KEY` |
| 火山引擎豆包 | [Volcengine Ark](https://console.volcengine.com/ark) | `VOLCENGINE_API_KEY`（也可以用 `ARK_API_KEY`） |

把 API Key 添加到你的 `~/.openclaw/.env` 文件中：
```bash
# 编辑 ~/.openclaw/.env，加入下面两行（选一个就行）
echo "GOOGLE_API_KEY=你的GoogleAPIKey" >> ~/.openclaw/.env
echo "VOLCENGINE_API_KEY=你的火山APIKey" >> ~/.openclaw/.env
```

## 快速开始

### 方式一：在 OpenClaw 聊天中使用（推荐）

非常简单：

1. **直接把参考图发到聊天窗口**
2. **告诉你的需求**：  
   `生成 9 张常见生活用品，匹配这个风格，尺寸 1024x1024`
3. **等待生成** - 我会帮你运行，然后把 9 张图+预览拼贴都发给你！

**示例对话：**
```
你: [发送参考图]
你: 生成 9 张早餐食物，匹配这个极简扁平化风格，尺寸 1024x1024
我: ✓ 生成完成，发送 9张图 + 九宫格预览
```

### 方式二：命令行使用

#### 第一步：检查参考图规格
```bash
python3 scripts/inspect_image.py --image /path/to/reference.png
```

会输出：
- 文件格式、大小
- 分辨率
- 宽高比检测
- 推荐生成尺寸

#### 第二步：生成 9 张图片

**使用火山引擎豆包（国内推荐，不需要 VPN）：**
```bash
python3 scripts/generate_9_volc.py \
  --reference /path/to/reference.png \
  --prompt "这里写你的内容描述，要求匹配参考图风格" \
  --output ./输出目录
```

**使用 Google Gemini：**
```bash
python3 scripts/generate_9_gemini.py \
  --reference /path/to/reference.png \
  --prompt "这里写你的内容描述，要求匹配参考图风格" \
  --output ./输出目录
```

**指定自定义尺寸：**
```bash
# 加上 --width 和 --height 参数
python3 scripts/generate_9_volc.py \
  --reference /path/to/reference.png \
  --prompt "你的内容描述" \
  --width 1080 --height 1440 \
  --output ./output
```

**生成更少张数（1-4 张）：**
```bash
python3 scripts/generate_volc.py \
  --reference /path/to/reference.png \
  --prompt "你的内容描述" \
  --count 4 \
  --output ./output
```

## 输出文件说明

生成完成后，输出目录结构：
```
output-directory/
├── 01.png ~ 09.png    # 9 张单独的图片
├── collage-3x3.png     # 九宫格预览拼贴
└── metadata.json      # 生成信息元数据
```

## 推荐尺寸

| 用途 | 推荐尺寸 | 宽高比 |
|------|----------|--------|
| 方形图标/头像 | 1024 × 1024 | 1:1 |
| 公众号文中图片 | 1080 × 1440 | 3:4 |
| 公众号封面图 | 1280 × 720 | 16:9 |
| 手机壁纸 | 1080 × 2340 | 9:16 |

如果你不指定尺寸，**自动使用参考图的尺寸**。

## 提示词撰写技巧

要获得好的风格匹配效果，提示词建议包含：

1. **内容描述** - 你想要生成什么内容？
2. **明确要求匹配风格** - 加上一句 "严格匹配参考图片的风格"
3. **构图说明** - 比如 "居中构图，干净背景" 等

✅ **好示例：**
```
9个不同的咖啡杯，每张图一个咖啡杯。严格匹配参考图片的极简扁平化设计风格，干净纯色背景，居中构图。
```

❌ **不好示例（太模糊）：**
```
咖啡杯 一样风格
```

## 常见问题

**Q: Google 返回配额不足怎么办？**  
A: Google 免费版有每日配额限制，可以等 24 小时后再试，或者升级付费，或者改用火山引擎豆包。

**Q: 风格匹配不太准怎么办？**  
A: 因为是 AI 生成，不可能 100% 一模一样，所以我们一次生成 9 张，你选最接近的就好。提示词里加上 "严格匹配参考风格" 会有帮助。

**Q: 可以只生成 1 张吗？**  
A: 可以，用 `generate_gemini.py` 或 `generate_volc.py`，加上 `--count 1` 参数。

## 许可证

MIT
