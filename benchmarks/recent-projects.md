# 近期样本选择

核验日期：2026-11-05。首发日期取 arXiv submission history 的 v1，会议年份另记。

用户要求以 Helios、Echo-Infinity 等近期项目为准。首轮优先 2026 年论文，保留用户明确指定的 2025 年项目作补充。引用量只作辅助，不把新论文的低累计引用量视为排除理由；目前不宣称以下项目均属高被引论文。

| 项目 | 首发日期及论文 | 原项目页 | 本轮角色与待检验能力 |
| --- | --- | --- | --- |
| Helios | [2026-03-04 / 2603.04379](https://arxiv.org/abs/2603.04379) | [项目页](https://pku-yuangroup.github.io/Helios-Page/) | 主样本：速度演示、长短视频对比、多任务结果的层级安排 |
| Echo-Infinity | [2026-06-03 / 2606.04527](https://arxiv.org/abs/2606.04527) | [项目页](https://echo-team-joy-future-academy-jd.github.io/Echo-Infinity/) | 主样本：超长视频的可浏览性、时间跨度表达、多提示词展示 |
| SAGE-GRPO | [2026-03-23 / 2603.21872](https://arxiv.org/abs/2603.21872) | [项目页](https://dungeonmassster.github.io/SAGE-GRPO-Page/) | 主样本：细微质量提升的可比较性、同输入方法对照、解释负担 |
| Rolling Forcing | [2025-09-29 / 2509.25161](https://arxiv.org/abs/2509.25161) | [项目页](https://kunhao-liu.github.io/Rolling_Forcing_Webpage/) | 补充：两分钟结果、滚动生成的展示节奏；项目页标注 ICLR 2026，不能据此写成 2026 年首发 |

上述“待检验能力”是实验设计判断，不是已完成的网页质量评测。Echo-Infinity 的网页标题使用 Learnable Evolving Memory，arXiv 标题使用 Learning Evolving Memory；采集脚本使用论文标题，避免身份匹配歧义。

## 比较方法

先读 PDF，提取核心效果、可展示证据及公平对比所需条件，再生成页面；记录已经看过原项目页这一事实，不将实验描述成盲测。原站用于事后比较，不能直接照抄其结构或把作者的所有设计视为最佳实践。

重点比较：多久看到代表性效果、视频在桌面和手机上是否足够大、同 prompt 对比是否可理解、联动播放是否可靠、超长视频能否快速定位、文字是否服务于观看。审美差异写成具体观察，不编造量化用户研究得分。

## 当前证据与进度

三篇主样本的 PDF 已下载并提取文字：Helios 39 页、Echo-Infinity 21 页、SAGE-GRPO 17 页。Helios 已完成[论文简报](helios-brief.md)、7 段素材核验、页面首版及[第一轮修订检查](helios-review.md)。Echo-Infinity 也已完成[论文简报](echo-brief.md)、7 段素材核验、浅色页面首版与[第二轮修订及迁移检查](echo-review.md)。SAGE-GRPO 的完整阅读笔记、页面生成与对比尚未完成。此前旧样本的下载结果不计入新样本完成度。

2026-11-05 查询 Semantic Scholar，按 arXiv ID 匹配：

- [Helios](https://www.semanticscholar.org/paper/4e7b7508ac30aed492f667cfc6e34b05872e8891)：78 citations，15 influential citations。
- [Echo-Infinity](https://www.semanticscholar.org/paper/335ebd446d1351b77c4e9af3056971b6eac980e7)：11 citations，1 influential citation。同日 OpenAlex 对同一 DOI 仅返回 1 citation，不能混用为一致口径。
- SAGE-GRPO 的两项索引查询均遇到 HTTP 429，引用量暂未核实。

计数仅反映各索引在查询时的收录，不等于完整引用总量，也不作为网页审美水平的证据。原始返回及 PDF 哈希保存在被 Git 忽略的 `outputs/benchmarks/<slug>/sources/provenance.json`。
