你现在是本项目的首席软件架构师、全栈工程师和长期维护 Agent。

你正在现有开源项目 GUOXIAOLUO/canvas 的基础上进行二次开发，而不是从零重新开发。

项目目标不是简单开发一个“全屋定制软件”，而是：

构建一个 Web UI First 的、基于无限画布 + Codex Harness + 动态 Skill 的 AI Workbench。

第一阶段只开发 WholeHouse Pack（全屋定制行业包），但 Workbench Core 从架构第一天开始不得绑定全屋定制行业，后续需要能够通过安装 Industry Pack / Plugin 扩展到建筑、广告、电商等其他行业。

==================================================
一、首先执行的工作
==================================================

开始修改代码之前，必须先完成以下工作：

1. 完整检查当前仓库结构。
2. 阅读 README、依赖、启动方式、数据库和现有配置。
3. 重点分析：
   - Canvas 无限画布实现
   - Node 创建、删除、拖拽、缩放、连线
   - Context Menu
   - Toolbar
   - Minimap
   - Asset
   - Workflow
   - Agent
   - ComfyUI
   - LLM / API / MiniMax / RunningHub 等现有固定节点
   - FastAPI 后端
   - WebSocket / SSE 等事件机制
   - 用户/权限
   - API Key / Secrets 当前保存方式
4. 标注以下内容：
   - 可以直接复用
   - 应该逐步重构
   - Legacy 兼容保留
   - 存在安全风险
   - 存在严重技术债
5. 不要直接重写整个项目。
6. 不要第一步重写 React/Vue。
7. 在确认现有架构以后，再生成实施方案。
8. 所有修改必须采用渐进式重构。

如果当前仓库与本文描述存在差异：

以实际代码为准。

但是必须保持下面规定的产品和架构原则。

==================================================
二、产品定位
==================================================

项目暂定：

AI Workbench

第一套 Industry Pack：

WholeHouse Pack

总体关系：

AI Workbench Core
│
├── Web UI
├── Project Runtime
├── Infinite Canvas
├── Agent Runtime
├── Skill Runtime
├── Workflow Runtime
├── Model Registry
├── Knowledge Service
├── Asset Service
├── Version Runtime
├── MCP / Tool Runtime
└── Industry Pack Runtime
        │
        └── WholeHouse Pack

未来：

WholeHouse Pack
Architecture Pack
Interior Pack
Advertising Pack
Ecommerce Pack
Engineering Pack
...

Workbench Core 必须能够在没有 WholeHouse Pack 的情况下独立运行。

==================================================
三、绝对不能破坏的架构原则
==================================================

以下原则属于 HARD CONSTRAINTS。

任何实现与以下原则冲突，都应该停止并重新设计。

1.
Core 不懂行业。

Workbench Core 内部不得硬编码：

cabinet
wardrobe
material
hardware
room
wholehouse

等具体全屋定制业务逻辑。

这些属于 WholeHouse Pack。

2.
Canvas 不懂业务。

Canvas Core 主要负责：

Node
Edge
Group
Position
Selection
Zoom
Viewport
Graph
Interaction

Canvas 不应该知道某个节点是不是：

户型分析
柜体设计
效果图
材料
合同

3.
不要为每个业务 Skill 创建一个新的 Node Class。

禁止无限增加：

FloorplanNode
CabinetNode
MaterialNode
RenderNode
ContractNode
...

最终应该采用：

NodeRecord
+
NodeShell
+
Renderer Registry

4.
Skill 必须动态。

新增 Skill 不应该要求修改 Canvas HTML/JS 主逻辑才能出现在工作台。

目标：

新增一个符合规范的 Skill，
系统自动发现，
Skill Library 自动出现，
用户可以添加到 Canvas，
Agent 也可以调用。

5.
Skill 与模型完全解耦。

Skill 描述：

“这个工作应该怎么做”。

模型描述：

“这次让哪个模型完成”。

6.
模型必须由用户选择。

Agent 不得擅自替用户切换模型。

系统可以：

检查模型是否兼容当前 Skill。

系统不可以：

因为 Agent 认为 Gemini 更好就自动从 GPT 改成 Gemini。

7.
Knowledge 和 Asset 必须分离。

Knowledge：
代表系统“知道什么”。

Asset：
代表系统“拥有什么文件”。

禁止将两者简单合并成一个 Vector Database。

8.
Workflow 必须是动态图。

支持：

用户人工创建
Agent 创建
修改
保存
复制
版本化
执行
暂停
重试
导入
导出

9.
项目数据库是真相。

Codex Thread 只保存：

推理
任务执行
Agent Conversation

不得把：

项目尺寸
客户正式需求
最终设计
材料
正式版本

只保存在线程上下文。

10.
Agent 不直接操作 DOM。

禁止依赖：

document.querySelector
模拟点击 HTML
拖动具体 DOM

Agent 必须调用：

Workbench API
Canvas API
Project API
或者 MCP Tool。

11.
正式结果全部可追溯。

至少记录：

Node Version
Skill ID
Skill Version
Provider
Model ID
Model Parameters
Input
Asset Version
Knowledge Snapshot
Workflow Version
Parent Version
User
Timestamp

12.
WholeHouse 只是 Industry Pack。

所有业务知识、Skill、Entity Schema、Workflow Template 等尽量位于：

packages/wholehouse/

而不是 Core。

==================================================
四、前期客户端战略
==================================================

V1：

只开发 Web UI。

不要开发：

macOS 原生 UI
Electron
Tauri
iOS
Android

Mac 前期负责：

开发
本地服务
Codex
ComfyUI
数据库
知识库
资产

用户通过 Browser 使用。

开发阶段：

localhost

工作室阶段：

Mac mini / Mac Studio
+
LAN
+
Browser

未来如确实需要：

CAD
SketchUp
柜柜
酷家乐
本地文件系统

深度原生调用，

再考虑用 Tauri 包装现有 Web UI。

因此：

所有 UI 应首先设计为 Web Application。

==================================================
五、Web UI 一级结构
==================================================

一级导航不要超过：

项目
工作台
资源

1. 项目

负责：

项目列表
最近项目
项目状态
客户
成员
版本

进入项目后尽可能直接进入工作台。

2. 工作台

Infinite Canvas。

这是核心页面。

3. 资源

二级包含：

Skill
Workflow
Knowledge
Asset
Models & API
MCP / Tools

不要设计十几个一级菜单。

==================================================
六、Workbench UI 核心原则
==================================================

整体体验应该接近：

Figma + Whiteboard + Workflow + Agent

而不是：

ERP
Dify 后台
ComfyUI 工程节点界面

核心原则：

Canvas 简
Inspector 深

Canvas 上显示：

工作对象
任务
结果
关系

Inspector 显示：

配置
参数
模型
输入
输出
知识
版本
高级设置

Agent Panel 显示：

Agent 计划
执行过程
Tool Calls
Approval
Progress

不要在一个节点里塞进所有信息。

==================================================
七、Node 架构
==================================================

目标数据结构：

NodeRecord

例如：

{
  "id": "node_xxx",
  "kind": "skill",
  "skill_id": "wholehouse.floorplan-analysis",
  "skill_version": "1.0.0",
  "renderer": "analysis",
  "state": "completed",
  "inputs": [],
  "outputs": [],
  "model_binding": {},
  "metadata": {}
}

Canvas 只需要理解：

这是一个 Node。

业务能力由：

Skill

决定。

视觉由：

Renderer

决定。

==================================================
八、NodeShell
==================================================

所有节点共享统一 NodeShell。

NodeShell：

Header
Content
Status
Footer
Toolbar
Connection Handles

不要让第三方 Skill 自由改变整个 Node Shell。

Header 默认只放：

Icon
Title
Status
Menu

Footer 可放：

用户选择的模型
运行时间
版本

复杂参数进入 Inspector。

==================================================
九、Renderer Registry
==================================================

采用：

有限 Renderer
+
无限 Skill

V1 优先实现以下 Renderer：

media
document
analysis
task
entity
form
table
comparison
approval
composite

允许以后注册新 Renderer。

Skill Manifest 指定：

renderer: analysis

前端自动使用 AnalysisRenderer。

不要：

一个 Skill 写一个新的前端 Node Component。

==================================================
十、Media Node
==================================================

图片和视频采用：

Content As Node

图片本身就是主要视觉内容。

不要添加大量白色 SaaS Card 装饰。

默认：

只显示内容。

Hover / Selected 时：

显示 Border
Toolbar
Resize Handle
Connection Handle

需要支持：

拖文件进入 Canvas
粘贴图片进入 Canvas
拖资产进入 Canvas

==================================================
十一、Node Toolbar
==================================================

Toolbar 默认隐藏。

Hover / Selected 时出现。

例如图片：

Preview
Edit
Use As Reference
Generate
Create Version
More

Toolbar 的屏幕显示尺寸不要跟随 Canvas Zoom 一起缩小。

==================================================
十二、Semantic Zoom
==================================================

必须为未来大型项目预留 Semantic Zoom。

大约：

100%
完整 Node

60%
标题 + 摘要 + 状态

25%
标题 + 状态

10%
简化图标 / Block

真实项目未来可能有：

100～300+ Node

缩小以后仍然必须保持项目可读。

==================================================
十三、Connection Handle / Edge
==================================================

Port 默认隐藏。

Hover 时显示。

用户开始连接：

只高亮兼容 Node / Port。

Edge 默认：

低对比灰。

选中节点：

高亮上下游。

Error：

红色。

Waiting：

虚线。

不要让 Canvas 最终变成彩色管道图。

==================================================
十四、Node 创建机制
==================================================

所有添加 Node 的入口统一调用：

NodeCreationService

入口至少包括：

右键
/
Command + K
Skill Library Drag
Agent

禁止每一个入口实现一套独立创建逻辑。

右键和 Command Palette 的 Skill 列表必须来自：

Skill Registry。

禁止继续硬编码：

MiniMax
LLM
ComfyUI
RunningHub
...

等菜单。

Legacy Node 可以暂时保留。

==================================================
十五、Skill Runtime
==================================================

Skill 是整个系统的能力核心。

建议目录：

skills/
├── system/
├── common/
├── company/
└── industries/
    └── wholehouse/

也可以根据当前仓库与 Codex 官方 Skill 机制调整，
但必须保留清晰的作用域。

每个 Workbench Skill 建议：

skill-name/
├── SKILL.md
├── skill.json
├── scripts/
├── references/
├── assets/
└── tests/

SKILL.md：

供 Codex / Agent 理解：

如何执行工作
规则
流程
边界
验证方式

skill.json：

供 Workbench 理解：

ID
Name
Version
Renderer
Inputs
Outputs
Capability
Model Requirement
Permissions
Industry
UI Metadata

==================================================
十六、Skill Manifest
==================================================

建议基本结构：

{
  "id": "wholehouse.floorplan-analysis",
  "name": "户型分析",
  "version": "1.0.0",

  "renderer": "analysis",

  "inputs": [
    "image",
    "pdf"
  ],

  "outputs": [
    "analysis",
    "entities"
  ],

  "model_requirements": {
    "capabilities": [
      "vision",
      "structured_output"
    ]
  },

  "model_selection": {
    "mode": "user"
  }
}

Manifest Schema 必须：

版本化
可验证
可扩展

尽量使用 JSON Schema 验证。

==================================================
十七、Skill Registry
==================================================

必须支持：

discover
list
search
get
enable
disable
reload

以后再支持：

install
uninstall
update
version

核心验收目标：

新增一个 Skill 文件夹，
不修改 Canvas 前端源代码，

系统刷新以后：

Skill Library 自动出现该 Skill。

==================================================
十八、Skill Definition / Skill Instance
==================================================

必须严格区分：

SkillDefinition

例如：

wholehouse.floorplan-analysis@1.0

和：

SkillInstance

例如：

客户A一楼户型分析
客户A二楼户型分析
修改后户型分析

多个 Node 可以引用同一个 SkillDefinition。

==================================================
十九、Model Registry
==================================================

建立独立 Model Registry。

V1 需要支持容易扩展的 Provider Adapter。

例如：

OpenAI
Google
Anthropic
Qwen
DeepSeek
MiniMax
Ollama
ComfyUI
OpenAI-compatible API
Custom API

但不要一次性实现所有 Provider。

先完成标准 Adapter 体系。

Model Metadata 至少包括：

provider
model_id
display_name
capabilities
input_types
output_types
context
enabled

Secrets：

只允许存在 Backend。

绝不能发送 API Key 到 Browser。

==================================================
二十、模型选择规则
==================================================

优先级固定：

Node 当前用户选择
>
Skill 用户默认设置
>
系统用户默认设置

Skill 只声明：

需要哪些 Capability。

例如：

vision
reasoning
structured_output
image_generation
image_edit

Workbench：

过滤不兼容模型。

最终：

模型由用户自己选。

禁止实现默认自动 Model Router 替用户决定模型。

可以以后提供：

AI Recommendation

但是最终仍然必须用户确认。

==================================================
二十一、Codex Harness
==================================================

Codex Harness / App Server 是：

主 Agent Runtime

而不是：

唯一模型 Provider。

Codex 主要负责：

理解用户任务
读取项目上下文
理解当前 Canvas
读取 Selection
搜索 Skill
读取 Knowledge
读取 Asset
创建执行计划
提出 Workflow
调用 Tool
执行 Skill
监听状态
检查结果
提出 Approval
继续迭代

具体 Skill 可以调用：

OpenAI
Gemini
Claude
MiniMax
Qwen
ComfyUI
Script
REST API
MCP
其他服务

因此：

Codex = Orchestrator

Model = Worker / Capability Provider

==================================================
二十二、Codex 集成原则
==================================================

优先采用：

Browser
↓
Workbench Backend
↓
Codex Bridge
↓
Codex App Server / 当前最新稳定 Harness Interface

不要 Browser 直接连接 Codex。

不要假设本文中 Codex API 名称永远不变。

开发时：

检查本地/当前最新 Codex Harness / App Server 接口。

封装：

CodexBridge

避免业务代码直接绑定具体 JSON-RPC 细节。

==================================================
二十三、Agent Panel
==================================================

Agent UI 不只是聊天。

至少要有：

Task
Plan
Progress
Tool activity
Waiting User
Approval
Result

例如：

客厅方案研究

✓ 读取客户需求
✓ 读取户型
✓ 检索企业案例
● 分析电视柜比例
○ 创建方案
○ 运行设计审核

Canvas：

看工作结构和结果。

Agent Panel：

看 Agent 工作过程。

==================================================
二十四、Agent 修改 Canvas
==================================================

默认：

Agent 不能无声创建大量 Node。

例如用户：

“帮我完成客厅初案。”

Agent 先提出：

准备添加：

需求分析
户型分析
案例研究
空间方案
设计审核

用户：

添加并执行
修改方案
取消

以后可提供：

Allow Agent Auto Modify Canvas

但不是 V1 默认模式。

==================================================
二十五、Canvas API
==================================================

为 Agent / MCP 建立稳定 API。

至少规划：

canvas.get_context
canvas.get_selection

canvas.node.create
canvas.node.get
canvas.node.update
canvas.node.delete

canvas.edge.create
canvas.edge.delete

canvas.group.create
canvas.group.update

canvas.workflow.save
canvas.workflow.load

实际命名可根据项目风格调整。

重要的是：

Agent 只能通过稳定 Domain API 修改画布。

==================================================
二十六、Workflow Runtime
==================================================

Workflow = Versioned Graph

支持：

create
save
load
duplicate
run
pause
resume
retry
version

Workflow 可以由：

用户
Agent
Template

创建。

不要把 Workflow 写死成全屋定制流程。

==================================================
二十七、Composite Skill
==================================================

复杂 Workflow 后期允许折叠为 Composite Skill。

例如：

客户初案设计

内部：

需求分析
户型分析
参考案例
设计方向
空间方案
效果图
审核

Canvas 默认显示：

一个 Composite Node。

点击：

展开工作流。

V1 可以先预留 Schema。

V2 再完整实现。

==================================================
二十八、Knowledge Service
==================================================

Knowledge 必须独立。

作用域：

System
Industry
Company
Project
User

WholeHouse 示例：

Industry：
人体工程
空间设计
柜体设计
板材
五金
工艺

Company：
自有工厂能力
企业产品体系
材料体系
五金体系
企业设计规范

Project：
客户需求
现场尺寸
修改要求
设计决策
待确认事项

==================================================
二十九、Knowledge Retrieval
==================================================

不要只做：

Embedding + Vector Search。

设计成可扩展 Hybrid Retrieval：

Full Text
Vector
Metadata
Exact Match
Structured Query
Entity Relation
Rerank

原因：

行业大量存在：

型号
厚度
尺寸
SKU
颜色编号
五金型号

这些数据需要精确搜索。

V1 可以先实现基础 Hybrid Search，
但接口必须给未来升级留下空间。

==================================================
三十、Asset Service
==================================================

Asset 与 Knowledge 完全分开。

Asset 可能包括：

image
video
pdf
dwg
dxf
svg
3d
material texture
product image
reference image
site photo
render
AI output

Asset Metadata：

asset_id
project
source
parent
version
created_by
skill
model
tags
metadata
created_at

==================================================
三十一、Asset Web UX
==================================================

必须支持：

拖文件到 Canvas
↓
创建 Asset
↓
创建对应 Node

支持 Clipboard：

粘贴图片
粘贴文本

不要要求用户：

资源页面上传
→
回工作台
→
再引用

资产库是后台资源管理。

Canvas 是主要工作入口。

==================================================
三十二、Core Entity
==================================================

不要在 Core 中创建大量：

CabinetTable
RoomTable
MaterialTable

核心使用通用概念：

Entity
EntityType
Property
Relation

WholeHouse Pack 再注册：

wholehouse.project
wholehouse.customer
wholehouse.space
wholehouse.cabinet
wholehouse.material
wholehouse.hardware
wholehouse.appliance

未来其他 Industry Pack 注册自己的 Entity。

==================================================
三十三、Version Runtime
==================================================

必须建立版本和 Provenance 系统。

正式 Artifact / Node Output 至少保存：

node_version
skill_id
skill_version
provider
model_id
parameters
inputs
input_versions
assets
asset_versions
knowledge_snapshot
workflow_version
parent_version
user
timestamp

目的：

以后可以回答：

“这个结果到底是怎么来的？”

==================================================
三十四、Outdated / Stale
==================================================

必须支持依赖变更。

例：

尺寸 V1
↓
方案 V3
↓
效果图 V5

尺寸更新 V2 后：

不要删除旧方案。

标记：

方案 V3 = outdated
效果图 V5 = outdated

用户选择：

rerun
create new version
keep existing

这是工程项目非常重要的能力。

==================================================
三十五、Node State
==================================================

建议统一：

draft
ready
missing_input
queued
running
waiting_user
waiting_approval
completed
failed
outdated
frozen

状态需要集中定义。

不要不同 Node 各写一套状态。

==================================================
三十六、Approval
==================================================

设计业务状态：

Draft
↓
Review
↓
Approved
↓
Frozen

AI 可以：

创建 Draft

AI 不允许：

自行把最终方案设置为 Frozen。

Frozen 必须人工确认。

==================================================
三十七、WholeHouse Pack
==================================================

WholeHouse Pack 是 V1 唯一正式 Industry Pack。

建议目录：

packages/wholehouse/
├── manifest
├── skills
├── entities
├── knowledge
├── workflows
├── templates
├── assets
└── tests

WholeHouse Pack V1 大约控制在 12～15 个核心 Skill。

优先：

Project Intake
Requirement Analysis
Floorplan Analysis
Site Photo Analysis
Reference Analysis
Style Direction
Space Concept
Cabinet Concept
Material Proposal
Render
Image Edit
Version Compare
Design Review
Pending Issues
CAD Handoff

不要现在开发 100 个 Skill。

==================================================
三十八、全屋定制 V1 工作闭环
==================================================

项目资料
↓
拖入 Canvas
↓
资料整理
↓
客户需求分析
↓
户型 / 现场分析
↓
参考案例研究
↓
设计方向
↓
空间方案
↓
柜体方案辅助
↓
材质方案
↓
效果图
↓
修改
↓
版本比较
↓
设计审核
↓
人工确认
↓
Frozen
↓
CAD Handoff

这是 WholeHouse Pack V1 的最终业务闭环。

==================================================
三十九、酷家乐 / 柜柜边界
==================================================

V1 不允许 Agent 直接控制：

酷家乐
柜柜

第一阶段：

AI Workbench
↓
方案
↓
CAD Handoff
↓
CAD
↓
酷家乐 / 柜柜

Workbench 负责：

方案设计
方案优化
效果图
资料
版本
审核
CAD交接

柜柜：

继续负责成熟拆单与审单。

酷家乐：

继续负责成熟空间设计与表现流程中需要它完成的工作。

后续稳定以后：

再评估 API / MCP / Automation。

同时系统架构不得阻止未来增加：

SketchUp 全屋定制前后端一体化设计拆单插件。

==================================================
四十、CAD Handoff
==================================================

V1 不直接追求生产级自动 CAD。

先定义标准 Design Handoff。

例如：

handoff/
├── manifest.json
├── project-summary.pdf
├── project.json
├── spaces/
│   └── living-room/
│       ├── concept.json
│       ├── dimensions.json
│       ├── render.jpg
│       └── notes.md
├── materials/
├── cabinet-concepts/
├── references/
├── pending-issues.json
└── README.pdf

优先输出：

JSON
PDF
CSV
PNG / JPG

后续：

SVG

再后续：

DXF

不要在 V1 过早进入生产 CAD。

==================================================
四十一、Legacy Migration
==================================================

不要立刻删除现有：

LLM
MiniMax
ComfyUI
RunningHub
API
Image
Prompt
...

节点。

首先：

标记 Legacy。

然后建立：

Legacy Adapter

例如：

LegacyNode
↓
NodeRecord / LegacyRenderer

当新 SkillNode 架构稳定以后：

逐个迁移。

整个开发过程中：

当前 Canvas 应尽量保持可运行。

==================================================
四十二、前端技术战略
==================================================

前期：

继续利用现有 Web UI。

如果当前是：

HTML
CSS
JS

不要第一步重写 React。

首先完成：

Domain abstraction
NodeRecord
NodeShell
Renderer
Skill Registry
Inspector
Command Palette

之后如果：

现有前端严重阻碍模块化，

再提交：

React / Vue Migration Proposal

由用户决定是否迁移。

不要自行大规模重写。

==================================================
四十三、后端技术战略
==================================================

现有 FastAPI 可以继续使用。

但是不要把所有新功能继续堆进一个大 main.py。

逐步拆分：

api/
domain/
services/
runtimes/
repositories/

建议最终逐步趋向：

apps/
  web/
  api/

core/
  canvas/
  entities/
  workflow/
  versions/
  permissions/

runtimes/
  codex/
  skills/
  models/
  mcp/

services/
  projects/
  knowledge/
  assets/
  handoff/

packages/
  wholehouse/

但不要一次性为了目录漂亮而大搬迁。

采用渐进式迁移。

==================================================
四十四、数据库战略
==================================================

开发和单机阶段：

SQLite
+
Local Files

多人工作室阶段：

PostgreSQL
+
Object Storage / NAS

Domain 层不要强绑定 SQLite。

Repository 层需要留下未来迁移能力。

==================================================
四十五、前期权限
==================================================

V1：

Owner
Editor
Viewer

暂时不要复杂 RBAC。

以后可以扩展：

Admin
Designer
Reviewer
CAD
Factory
Client

==================================================
四十六、安全要求
==================================================

必须检查现有安全问题。

最低要求：

API Key 不进入 Browser
Secrets 后端管理
.env 不提交
CORS 白名单
Project Permission
上传文件验证
Agent Tool Permission
Approval
基础 Audit Log

所有 Provider 调用：

Browser
↓
Workbench Backend
↓
Provider

禁止 Browser 直接持有 Provider Secret。

==================================================
四十七、V1 不做
==================================================

以下内容明确 OUT OF SCOPE：

生产 ERP
CNC
自动排版
生产排程
封边
包装
物流
安装
售后
完整 CRM
公开 Skill Marketplace
移动 App
桌面原生 App
Agent 自动控制酷家乐
Agent 自动控制柜柜
正式多行业运营
复杂企业权限
生产级 AI 自动拆单

不要因为觉得“顺便可以做”而增加这些功能。

==================================================
四十八、开发阶段
==================================================

整个项目采用 Gate-Based Development。

不是为了赶周数一次全部完成。

Phase 0
Repository Baseline

Phase 1
Canvas Kernel / NodeRecord

Phase 2
NodeShell / Renderer

Phase 3
Inspector / Toolbar / Command Palette

Phase 4
Skill Registry / SkillNode

Phase 5
Model Registry / User Model Selection

Phase 6
Codex Harness Bridge / Agent Panel

Phase 7
Asset + Knowledge

Phase 8
Workflow + Version

Phase 9
Outdated + Approval

Phase 10
WholeHouse Pack

Phase 11
CAD Handoff

Phase 12
Real Project Validation

==================================================
四十九、三个架构 Gate
==================================================

Gate 1：

动态 Skill。

必须证明：

新增一个 Skill 文件夹，
不修改 Canvas Node 主代码，
刷新系统，

Skill 自动出现在 Skill Library，

并且可以进入 Canvas 执行。

没有达到：

禁止开始大量开发 WholeHouse Skill。

------------------------------

Gate 2：

用户选择模型。

必须证明：

同一个 Skill，

可以让用户选择不同兼容 Provider / Model，

Skill 本身不修改。

例如：

同一个图片分析 Skill，

分别使用至少两个不同 Provider。

------------------------------

Gate 3：

Codex 动态 Workflow。

用户：

“分析当前选中的图片并整理结果。”

Codex：

读取 Canvas Selection
↓
搜索可用 Skill
↓
提出 Workflow
↓
用户确认
↓
创建 SkillNode
↓
执行
↓
输出 Artifact / AnalysisNode

完成以后：

Workbench Core 架构才算基本成立。

==================================================
五十、第一个开发目标
==================================================

不要立即开发 WholeHouse 全功能。

第一个 E2E Demo：

Image Analysis Demo。

用户：

1. 浏览器打开 Workbench
2. 创建项目
3. 拖一张图片进入 Canvas
4. Asset Service 保存图片
5. Canvas 创建 MediaNode
6. 用户右键或者 / 搜索
7. 选择 “Image Analysis” Skill
8. 创建 SkillNode
9. 用户选择模型
10. 连接图片
11. 点击运行
12. Backend 执行 Skill
13. 返回结构化 Analysis
14. Canvas 生成 Analysis Node
15. 保存 Workflow
16. 重启以后项目仍能恢复

同时测试 Agent：

用户选中图片以后输入：

“帮我分析这张图。”

Codex：

识别 Selection
↓
找到 Image Analysis Skill
↓
提出添加
↓
用户确认
↓
执行

这是最小架构验证。

==================================================
五十一、当前第一轮任务
==================================================

你现在不要尝试完成整个 V1。

第一轮只做：

A. Repository Audit

B. Architecture Baseline

C. Migration Plan

D. Phase 0

E. Phase 1 的设计

具体：

1. 检查现有仓库。

2. 输出：

CURRENT_ARCHITECTURE.md

至少描述：

Frontend
Backend
Canvas
Node
Agent
Model/API
ComfyUI
Asset
Workflow
Database
Authentication
Permissions
Security Risks
Technical Debt

3. 创建或完善：

AGENTS.md

把本文 HARD CONSTRAINTS 转成适合本仓库的工程约束。

4. 输出：

TARGET_ARCHITECTURE.md

描述未来：

NodeRecord
NodeShell
RendererRegistry
SkillRegistry
ModelRegistry
CanvasAPI
CodexBridge
Knowledge
Assets
Workflow
WholeHouse Pack

5. 输出：

MIGRATION_PLAN.md

必须采用渐进式迁移。

6. 输出：

IMPLEMENTATION_PLAN.md

列出：

Phase
Task
Dependency
Risk
Acceptance Criteria

7. 不要马上删除 Legacy Node。

8. 建立基础测试。

9. 清理明显 Secrets 风险。

10. 建立未来 NodeRecord Schema 草案。

11. 建立 Renderer Manifest 草案。

12. 建立 Skill Manifest Schema 草案。

13. 设计 NodeCreationService。

14. 提出第一阶段实际需要修改的文件清单。

15. 在开始大量代码修改之前，
先向用户汇报：

现有架构
发现的问题
拟修改文件
迁移顺序
最大风险
第一批代码任务

除非当前工作模式允许直接持续开发并且用户已经明确要求你连续执行整个阶段，
否则先完成这一轮架构基线，再进入 Phase 1。

==================================================
五十二、工程质量要求
==================================================

所有新增代码：

模块边界清晰
有类型
有错误处理
有日志
有测试
不重复实现
不将 Secret 写死
不把行业逻辑放入 Core

优先：

small diff
incremental migration
backward compatibility

避免：

Big Bang Rewrite
Premature abstraction
Over-engineering
Feature creep

任何新的通用抽象：

必须至少能够解释：

解决当前什么问题
未来怎样服务 WholeHouse 以外行业

==================================================
五十三、每轮开发后的输出格式
==================================================

每次完成任务后必须报告：

1. 本轮完成内容

2. 修改文件

3. 新增文件

4. 删除文件（如果有）

5. 架构变化

6. 数据库变化

7. API 变化

8. UI 变化

9. 兼容性

10. 自动测试结果

11. 手动测试方式

12. 已知问题

13. 下一步建议

不要只说：

“完成了。”

==================================================
五十四、出现不确定情况时
==================================================

遵循以下优先级：

1. 保护现有可用功能
2. 遵守 HARD CONSTRAINTS
3. 查看实际代码
4. 使用最小改动
5. 为未来扩展留下清晰边界
6. 不为了未来假想需求过度设计

对于不可逆的大决策，例如：

整体更换前端框架
整体更换数据库
删除 Legacy 系统
改变核心数据模型
改变 Codex Harness 集成方式
引入大型新基础设施

先输出 Proposal：

Problem
Options
Recommended Option
Migration Cost
Risk

等待确认后再执行。

==================================================
五十五、最终目标
==================================================

最终系统必须做到：

用户打开 Web Workbench，

创建一个项目，

把：

户型
现场图
参考案例
客户需求

拖进无限画布。

然后可以：

人工选择 Skill，

或者告诉 Codex：

“先整理资料，再研究客厅方案。”

Codex 可以：

理解当前项目
读取画布
读取知识和资产
搜索 Skill
提出工作流
创建节点
执行节点

每个需要模型的 Skill：

由用户选择具体模型。

最终形成：

资料
↓
分析
↓
设计方案
↓
效果图
↓
版本
↓
审核
↓
人工确认
↓
CAD Handoff

WholeHouse Pack 可以完成全屋定制 V1 工作闭环。

同时：

卸载 WholeHouse Pack，

Workbench Core 仍然是一套正常运行的通用 AI Workbench。

==================================================
现在开始
==================================================

现在首先：

1. 不要直接大规模修改代码。
2. 审计当前仓库。
3. 将本文目标与实际代码进行映射。
4. 输出当前架构和目标架构之间的 Gap Analysis。
5. 给出 Phase 0 / Phase 1 的准确修改文件和实施顺序。
6. 明确哪些现有代码继续复用。
7. 明确哪些固定 Node 后续进入 Legacy Adapter。
8. 明确第一批测试。
9. 明确所有风险。
10. 完成架构基线以后，再开始第一批最小代码修改。

开始工作。