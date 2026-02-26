---
title: 经济学ChatGPT使用指北
tags:
  - 杂谈
date: 2023-09-23 02:11:23
---


> 一年来我高强度使用 ChatGPT 作为我的日常学术工具。我惊讶于他为学术带来的高效，也遗憾于在审查，开源环境单薄等各种因素的限制下大部分人对他的了解仅仅停留于了解。ChatGPT 并没有成为大多数经济研究生甚至老师的工具箱中的一环。本篇整合了一些大佬以及我日常使用的方法，希望对奋斗在学术的 junior 节省一些宝贵的时间。

---

## Prompt Engineering

Prompt Engineering 旨在开发和优化提示以有效地利用语言模型 (LMs) 进行各种应用和研究主题。Prompt 是科学利用 chatgpt 的第一步，也是我学习 `ChatGPT` 的开始。我的经验是尽量给他必要的 `content` 而不是直接问他问题的答案。但这也与前沿的 `ChatGPT` 使用姿势相去甚远。

一个简单的方法是在写 prompt 时谨记 CLAR 原则和 LACES 问题模型，这两个方法可以帮助您构建高质量的提问 prompts，提高与 AI 交互的效率和效果。

### CLAR 原则

CLAR 原则是一个用于指导您撰写 prompts 的简单原则，其中每个字母代表一个关键方面：

- Clear（明确）：确保问题或指令表述清晰明了，避免使用模糊或不确定的词汇。
- Logical（合乎逻辑）：让问题或指令符合逻辑，便于 AI 理解和回答。
- Accurate（准确）：使用准确的术语和信息，提高 AI 生成的答案质量。
- Relevant（相关）：确保问题或指令与所需结果密切相关，避免无关内容。

### LACES 问题模型

LACES 问题模型是一个更具体的提问 prompts 构建方法。它包括以下五个要素：

- Limitation（限定条件）：为问题或指令增加限定条件，有助于获得更具针对性的答案。
- Assignment（分配角色）：在指令中为 AI 分配角色，帮助 AI 更好地理解预期的回答。
- Context（背景或上下文）：提供问题或指令的背景信息，有助于 AI 更好地理解问题。
- Example（示例）：为指令提供示例，以便 AI 能够参考并生成类似的答案。
- Step by Step（拆分任务）：将问题或指令拆分为较小的部分，使 AI 更容易处理。

## Prompt 开源项目

不得不承认，自己写 prompt 有时还是低效的，不如直接看看开源的其他人的使用方法，下面是一些可能有帮助的答案：

1. [**Best practices for prompt engineering with OpenAI API**](https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api) 该文档是 OpenAI 自己发布的有关 prompt 的最佳实践，给出了一些比较使用的使用例子。但是时间较为久远，站在 2023.9 来看并不再令人惊讶。
2. Github 上有一系列有趣的 prompt 开源项目，我选取了一些高 star 和中文社区实践典范。

| name                                                         | abstract                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| [github chatgpt-prompts-wiki-zh](https://github.com/AIzhibei/chatgpt-prompts-wiki-zh) | 包含最全的中文环境 prompt，更倾向于学术                       |
| [github awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) | 包含最全的中文环境 prompt                                     |
| [github chatgpt-prompts-for-academic-writing](https://github.com/ahmetbersoz/chatgpt-prompts-for-academic-writing) | 提供了一系列学术写作的 prompt                                 |
| [github Prompt-Engineering-Guide-Chinese](https://github.com/wangxuqi/Prompt-Engineering-Guide-Chinese) | 包含所有与 Prompt 工程相关的最新论文、学习指南、讲座、参考资料和工具 |
| https://github.com/binary-husky/gpt_academic                 | 专门用于学术的 ChatGPT 前端，支持多种大语言模型混合调用        |

3. AI 领域的绝对大神吴恩达和 openai 的特征工程师的教程可能是有帮助的，可以在 b 站观看这个免费视频。[【ChatGPT 提示工程师&AI 大神吴恩达教你写提示词｜ prompt engineering【完整中字九集全】]( https://www.bilibili.com/video/BV1Z14y1Z7LJ/?share_source=copy_web&vd_source=ec18e466006be740c52c036b6e803c87)
4. 现在流行起来了一种通过 chatgpt 自己生成合适的 Prompt 的新方法，这种技术被称为 `Prompt 逆向工程`。这是一个 [简单的实践](https://zhuanlan.zhihu.com/p/617524191)，更多的可以 follow 最新的论文及开源项目。



## 我的 Prompt

### IMPROVING LANGUAGE
```
Please analyze the logic and coherence among sentences within each paragraph in the following text. Identify any areas where the flow or connections between sentences could be improved,and provide specific suggestians to enhance the overall quality and readability to the content, Please only provide the text after improving and then give a list of the improvemments in English, Please improve the following text:
```

### TRANSLATE

```
我想让你充当英语翻译员、拼写纠正员和改进员。我会用任何语言与你交谈，你会检测语言，翻译它并用我的文本的更正和改进版本用英语回答。我希望你用更优美优雅的高级英语单词和句子替换我简化的 A0 级单词和句子。保持相同的意思，但使它们更符合学术规范。我要你只回复更正、改进，不要写任何解释。我的第一句话是“istanbulu cok seviyom burada olmak cok guzel”
```

### PYTHON 

```
我想让你在学校担任讲师，向初学者教授算法。您将使用 Python 编程语言提供代码示例。首先简单介绍一下什么是算法，然后继续给出简单的例子，包括冒泡排序和快速排序。稍后，等待我提示其他问题。一旦您解释并提供代码示例，我希望您尽可能将相应的可视化作为 ascii 艺术包括在内。
```

```
我想让你充当 stackoverflow 的帖子。我会问与 Python 编程相关的问题，你会回答应该是什么答案。我希望你只回答给定的答案，并在不够详细的时候写解释。不要写解释。当我需要用英语告诉你一些事情时，我会把文字放在大括号内{like this}。我的第一个问题是“如何将 http.Request 的主体读取到 Python 中的字符串”
```

### REGULAR EXPRESSION

```
我希望你充当正则表达式生成器。您的角色是生成匹配文本中特定模式的正则表达式。您应该以一种可以轻松复制并粘贴到支持正则表达式的文本编辑器或编程语言中的格式提供正则表达式。不要写正则表达式如何工作的解释或例子；只需提供正则表达式本身。我的第一个提示是生成一个匹配电子邮件地址的正则表达式。
```



## ChatGPT in Econ 

关于ChatGPT的经济学研究正在不断增加，这里面包括由发展经济学家领衔的RCT团队，也包括把[ChatGPT出台作为事件冲击](https://www.nber.org/papers/w31222)的`reg monkey` 。大体来看，真正有意思的还是[ChatGPT带来的生产力对劳动市场的长短期影响](https://www.nber.org/papers/w31627)。

关于经济学中ChatGPT的运用大致可以看这三篇Notes，给出了一些经济学家使用ChatGPT的新姿势。

- [A_User_s_Guide_to_GPT_and_LLMs_for_Economic_Research.pdf](https://economics.princeton.edu/wp-content/uploads/2023/05/A_User_s_Guide_to_GPT_and_LLMs_for_Economic_Research.pdf)

- [Generation Next: Experimentation with AI](https://www.nber.org/papers/w31679)
- [NBER Language Models and Cognitive Automation for Economic Research](https://www.nber.org/papers/w30957)

熊伟老师从[数据隐私](https://www.nber.org/papers/w31250)角度谈AI和大数据是一个特别好的角度切入ChatGPT，除此而外还有ACEMOGLU最新出版的[新书](https://shapingwork.mit.edu/power-and-progress/)从科技与权力看ChatGPT也是一个新的视角。



## 其他工具

- 如果你想用chatgpt帮助你阅读PDF文档的话，最佳工具是[ChatPDF](https://www.chatpdf.com/)，有人曾经用它做一些literature review工作，效果还很惊艳。但是我仍不建议你这么做，[正确阅读文献的姿势](http://www.xutianyang.com/2023/09/22/%E5%A6%82%E4%BD%95%E9%98%85%E8%AF%BB%E9%87%91%E8%9E%8D%E6%96%87%E7%8C%AE/)应该不包含囫囵吞枣
- 在碎片化阅读时代，一个可以汇总不同网站信息流，并给出略读与收藏的工具可能是重要的。我找到的最佳工具是[会读](https://zhuanlan.zhihu.com/p/633324001)。它目前仍在内测阶段，如果有兴趣可以尝试（但是需要付费。。。）市面上还有其他好多工具，我没有一一测试。
- 如果需要用大语言模型做一些“重活”，比如打标，本地知识库，会议纪要整理等等偏开发端的运用。不妨试试一些开源的大语言模型，ChatGLM，LLaMa-2，GPT4All。他们在本地环境下可以更好finetune，更重要的是他们完全免费。
- Claude2，百度文心一言是免费的，如果可以也可以尝试他们——尽管百度的效果真的不尽人意。

