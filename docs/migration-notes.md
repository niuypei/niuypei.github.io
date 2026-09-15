# Minimal Light 迁移与内容更新记录

更新日期：2026-09-15

## 当前结果

- 模板：用户选定的 A · Minimal Light，英文单页学术主页。
- 本地预览：[http://localhost:8000/](http://localhost:8000/)。
- 简介、研究方向、教育与奖项已更新；侧栏使用用户指定的 AI Infra Engineer，正文以学术和开源信息为主。
- 论文共 **12 条：6 篇期刊、5 篇会议、1 篇预印本**，保留完整作者顺序和本人姓名强调。
- 支持论文资源链接、展开 BibTeX 和整份书目下载。
- 按用户指定，将 **Demystifying the Cost of Serverless Computing: Towards a Win-Win Deal** 置于期刊论文第 1 条；其余论文在各类型内保持本人一作优先，一作与非一作分别按发表时间倒序，同年按已核实的月日排序，作者列表本身保持原顺序。
- 获奖论文条目与 Honors & Awards 同时标注 **2024 IEEE TPDS Best Paper Award**，并提供官方名单链接。
- Python 标准库从 `content/` 生成静态 HTML 与 BibTeX；无需 JavaScript，字体在本地托管。
- 用户已验收页面并授权提交、推送至 `origin/main`；线上部署状态以 GitHub Pages 构建结果为准。

## 来源与核验范围

### 用户提供的资料

教育与学术奖项来自用户提供的简历，仅只读提取允许公开的学术字段。博士经历由旧稿的开始时间更新为 **2016.09–2023.06，华中科技大学计算机系统结构博士**；硕士为 **2014.09–2016.06，华中科技大学计算机技术**；本科为 **2009.09–2013.06，河南大学计算机科学与技术**。导师 Fangming Liu 与简历及旧学术资料一致。

奖项补充了 IEEE INFOCOM Best-in-Session Presentation Award（2018）、博士学业奖学金和校级荣誉；相同奖项的多个学年合并展示，保留不同奖项等级。随后补充华为开发者大赛——代码上太空赛道优胜奖（简历同段标注 2022 年），以及用户明确提供的华为奖学金（2021 年）。英文以 Prize Winner 表达获奖，不推断一等奖或冠军；赛道英文为描述性翻译。

用户指定的 [Google Scholar 档案](https://scholar.google.com/citations?user=bP99ILMAAAAJ&hl=en) 入口已按用户最终要求从侧栏移除。此前读取论文列表时返回 **HTTP 429**，因此**尚未核对 Scholar 的完整条目、总数与分页**，不能将当前结果描述为完整同步。待取得用户粘贴的完整列表后逐项对齐。

### 论文补充与正式出版信息

通过 DBLP 发现候选条目，再依据 IEEE 向 Crossref 提交的出版元数据、作者手稿和 arXiv 核实新增的四条：

| 论文 | 正式记录 |
| --- | --- |
| ComboFunc | TPDS 35(11):1989–2005, 2024 |
| Joint Optimization of Parallelism and Resource Configuration for Serverless Function Steps | TPDS 35(4):560–576, 2024 |
| Demystifying the Cost of Serverless Computing: Towards a Win-Win Deal | TPDS 35(1):59–72, 2024 |
| Rollout-Training Co-Design for Efficient LLM-Based Multi-Agent Reinforcement Learning | arXiv:2602.09578, 2026；单列预印本 |

简历中的待刊年份和旧稿日期可能早于正式刊期，网页与 BibTeX 使用正式出版信息。预印本不推断正式刊会。原作者手稿仅用于历史核验，不把其中的占位卷期当作出版依据；当前网页统一使用官方论文入口。

逐条作者、DOI、卷期页码及来源见 [论文更新记录](publication-update-2026-09-15.json)。当前 12 条与 DBLP 作者书目匹配；这不等于已确认它们在指定 Scholar 档案中的收录情况。

### 旧站保留内容

头像、邮箱、8 条历史论文记录、Tricircle 开源贡献暂沿用 [旧学术主页](https://newypei.github.io/)。这是此前明确说明的本地迁移来源假设；头像和邮箱仍可由用户校对。初次论文核验记录位于 `docs/legacy-source/`；原始页面和未经筛选的提取结果已移到项目外保留，避免公开旧联系方式及完整 CV 入口。

历史条目的关键修正：TCC 论文使用正式刊年 2022；PostMan 的 ATC 2019 和 TPDS 2022 版本分别保留；CollaborateCom 的会议年份 2015 与论文集出版年份 2016 分别记录；相似题目的 MONET 和会议论文保留各自作者顺序。

## 论文排序与最佳论文奖

12 篇论文补充了 `publication_date`，采用正式刊期、论文集出版时间或 arXiv 初投日期，并保留来源原有的年／月／日精度。逐项来源见 [发表日期核验](publication-dates-2026-09-15.json)。`display_year` 仅作展示，期刊和会议各版本分别保留。

用户本轮明确指定 **Demystifying the Cost of Serverless Computing: Towards a Win-Win Deal** 排在期刊论文第 1 条。该论文在 `content/publications.json` 中设置 `pinned: true`，在所属期刊类型内置顶；其余论文继续采用各类型内本人一作优先、一作与非一作各自按发表日期倒序的规则。本次仅调整论文展示次序，作者顺序、奖项信息和论文及幻灯片链接保持原样。

[IEEE Computer Society 官方获奖名单](https://www.computer.org/publications/best-paper-awards-archive#winners) 将 Fangming Liu、Yipei Niu 的 **Demystifying the Cost of Serverless Computing: Towards a Win-Win Deal** 列为 **2024 年 TPDS 最佳论文奖获奖论文**。另一个[官方获奖页面](https://www.computer.org/publications/best-paper-award-winners)与其一致。核验内容通过官方页面的搜索结果读取；直接访问返回 403。奖项年份为 2024，未推断颁奖日期。证据见 [奖项核验记录](best-paper-award-2024.json)。

奖项数据统一维护在该论文的 `award` 字段，由生成器同时显示在论文下方和荣誉栏目；论文题目均使用纯文本，奖项名称保留官方名单链接。用户指定的期刊首位展示由该论文的 `pinned: true` 控制。

## 公开内容边界

- 用户明确指定的 AI Infra Engineer 标签可在侧栏和页面标题显示；不添加公司及其他任职细节。用户明确要求的奖项及奖学金主办方名称可出现在荣誉中，不作为任职信息。
- 侧栏标签及页面标题统一使用 AI Infra Engineer。
- 原 CV 下载入口和旧 CV 文件已从网站目录移除；本轮提供的完整简历未复制进项目。包含旧联系方式或 CV 入口的历史 HTML 和原始提取文件也已移出仓库。
- 不添加电话、地址、内部工作项目或业绩数字；本地排除词只存于项目外的临时文件。
- 论文链接仍指向原始学术文献，页面不提取或展示其作者机构信息。

## 资源与验证

- 按用户最新要求，仅删除网站目录中的 **8 篇论文全文 PDF**；恢复并保留全部 **4 份原始幻灯片 PDF**，同时保留头像与生成的 BibTeX。论文全文和幻灯片分别管理。
- 8 篇 IEEE 论文统一使用 IEEE Xplore 官方文章页，原 PDF/Preprint 按钮改为 IEEE Xplore。DOI 与文章编号由出版社 Crossref 记录核对；IEEE 的浏览器验证限制导致本轮未验证直接 PDF 下载，不生成猜测的 PDF 地址。记录见 [IEEE 链接核验](ieee-official-links-2026-09-15.json)。
- 另 4 篇按真实来源链接：2 篇 Springer、1 篇 USENIX、1 篇 arXiv。USENIX 官网明确给出了论文 PDF 和演示幻灯片链接；arXiv 预印本保留官网 PDF。未将这些论文误配到 IEEE 或 ACM。
- 幻灯片入口优先使用已核实的官网链接：USENIX Slides 继续使用官方外链；INFOCOM 2015、2017、2018 尚无已核实的官方 Slides 入口，恢复使用原本地文件 `INFOCOM2015-Slides.pdf`、`INFOCOM2017-Slides-v3.pdf`、`INFOCOM2018-Slides-v5.pdf`。USENIX 的原始 `atc19_slides.pdf` 也保留在 `assets/files/` 中供存档。
- 四篇有幻灯片的论文通过 `local_slides` 记录本地存档路径；该字段不参与生成，实际 Slides 按钮由 `links` 配置。历史来源快照在项目外保留，不参与提交或主页构建。
- `python3 scripts/build.py` 与 `python3 scripts/check_site.py` 已通过：**12 篇论文、12 处 BibTeX、9 个本地资源引用**，其中新增的 3 个引用为 INFOCOM 本地 Slides 链接；生成文件一致，锚点唯一，引用标签目标存在。检查允许已明确登记的本地 Slides，继续禁止本地论文全文 PDF。
- 预印本输出为 `@misc`，包含 arXiv 编号、归档名称与学科分类。
- 本地 HTTP 返回的主页和 BibTeX 与生成文件逐字节一致；4 份恢复的本地 Slides 与旧站快照的 SHA-256 一致，HTTP 均返回 200 和 `application/pdf`；`git diff --check` 通过。
- 教育、奖项和论文记录已独立复核；旧计划文档中的任职表述已清理。本轮用户授权的两个荣誉名称作为允许公开的奖项处理。
- Browser 工具无可用浏览器，尚未完成桌面／手机视觉实测。响应式样式可在本地预览中查看。

## 待办

- [x] 按简历更新学位、专业、起止时间和学术奖项。
- [x] 补充四条有公开出版记录支持的论文，生成 12 条书目。
- [x] 移除公司与完整 CV 入口，展示身份采用用户明确指定的 AI Infra Engineer。
- [x] 按用户最终要求移除 Google Scholar 入口。
- [x] 补充代码上太空赛道优胜奖（2022）与华为奖学金（2021）。
- [x] 所有论文全文入口使用官方来源，仅删除本地论文全文 PDF。
- [x] 恢复并保留全部 4 份原始 Slides PDF；USENIX 使用官方 Slides 入口，3 篇 INFOCOM 使用原本地 Slides 入口。
- [x] 将用户指定的 Demystifying the Cost of Serverless Computing 通过 `pinned: true` 置于期刊首位，其余论文保持各类型内一作优先、各组内时间倒序。
- [x] 在获奖论文及荣誉栏目注明 2024 IEEE TPDS 最佳论文奖，并链接官方名单。
- [ ] 取得 Scholar 完整列表后，核实条目是否存在遗漏或多余。
- [ ] 完成桌面和手机浏览器视觉验收。
- [x] 用户验收并授权提交、推送至 GitHub 仓库。
- [ ] 核实 GitHub Pages 的线上部署结果。

日常更新方式见 [README](../README.md)。
