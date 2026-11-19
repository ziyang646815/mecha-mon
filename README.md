# MECHA·MON Framework · Python 项目生成器

一个 **"样子货"级别**的项目框架：用 Python 作为单一数据源，一键生成策划文档、UE5 GAS 代码骨架和可交互的 HTML 演示原型。用来快速对齐概念、给投资人/团队/合作方做演示，之后再逐步替换成真实内容。

## 快速开始

```bash
cd MechaMonFramework
python main.py
```

生成物：

| 产物 | 路径 | 说明 |
|---|---|---|
| 游戏设计文档 | `docs/01_游戏设计文档_GDD.md` | 玩法、属性、机甲、养成、竞技 |
| 技术架构 | `docs/02_技术架构_UE5_GAS.md` | GAS 分层、标签、伤害管线、网络架构 |
| 项目规划 | `docs/03_项目规划_路线图.md` | 4 阶段里程碑、团队配置、风险 |
| 竞技规则 | `docs/04_竞技规则与数值.md` | 伤害公式、状态表、平衡约束 |
| UE5 代码骨架 | `generated/ue5/Source/MechaMon/` | ASC / AttributeSet / Ability / Tags / BattleManager |
| HTML 演示原型 | `demo/index.html` | 对战模拟 + 图鉴 + 架构 + 路线图，双击即开 |

单独生成：`python main.py docs|ue5|demo|check`

## 目录结构

```
MechaMonFramework/
├── config/
│   ├── game_data.py        # 单一数据源：机甲/属性/技能/克制/路线图
│   └── project_config.py   # 项目元数据与路径
├── generators/
│   ├── doc_generator.py    # 文档生成
│   ├── ue5_generator.py    # UE5 GAS C++ 骨架生成
│   └── demo_generator.py   # HTML 原型生成
├── templates/
│   └── demo_template.html  # 自包含 HTML 模板
├── docs/                   # 生成：策划与技术文档
├── generated/ue5/          # 生成：C++ 骨架
└── demo/index.html         # 生成：交互演示
```

## 设计思路

1. **单一数据源**：`config/game_data.py` 定义全部游戏数据，文档/代码/演示自动保持一致，改一处全同步。
2. **能演示**：`demo/index.html` 是真能玩的回合制模拟器——选机甲、放技能、属性克制结算、AI 反击、自动演示，无需任何依赖。
3. **能落地**：生成的 UE5 C++ 骨架命名与结构符合 GAS 规范，拷贝到 UE5 工程即可继续开发，`TODO` 标出了需要填充的核心逻辑。
4. **纯标准库**：Python 生成器零第三方依赖，任何环境都能跑。

## 下一步

- 导入 `generated/ue5/Source/MechaMon` 到 UE5 工程，补充 `TODO` 逻辑
- 用文档中的数值框架做平衡性模拟
- 逐步把 HTML 原型替换为真实 UE5 战斗画面

> 这是概念验证阶段的框架产物，不是可发布游戏。
