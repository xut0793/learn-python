## The Zen of Python

《Python之禅》（The Zen of Python）是 Python 语言的设计哲学和编程指导原则，由 Python 核心开发者 Tim Peters 撰写。它凝聚了 Python 社区对优雅、清晰、简洁代码的共同追求。

## 历史渊源

《Python之禅》的诞生与一次会议 T 恤的标语征集有关。

- 2001年秋：在筹备第十届国际 Python 大会（IPC 10，PyCon 的前身）时，主办方希望征集一条能代表 Python 文化的标语印在 T 恤上。
- 评选过程：社区提交了超过500条方案，但评审团迟迟无法定夺。在会议开始前，Tim Peters 和 Barry Warsaw 通过轮流淘汰的方式，最终从众多方案中选出了 import this。
- 彩蛋实现：选定标语后，团队意识到需要实现它。于是，Tim Peters 将早已写好的《Python之禅》通过 import this 这个命令输出。为了增加趣味性，this.py 模块的源码使用了 ROT-13 算法对原文进行了简单加密，使其本身成为一段“丑陋”的代码，与《Python之禅》的理念形成有趣的对比。
- 正式收录：这个有趣的“彩蛋”后来被正式收录为 PEP 20（Python Enhancement Proposal 20），成为 Python 的官方文档之一。

你可以在任何 Python 环境中输入 `import this` 来查看原文。

```text
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
>>>
```

翻译如下：

```text
1. Beautiful is better than ugly. 美丽胜于丑陋: 代码应该是优雅的，不仅仅是功能上的，还包括代码的外观和结构。

2. Explicit is better than implicit. 明了胜于晦涩：代码应该是容易理解的。使用清晰的命名和风格，使得代码可以自我解释。

3. Simple is better than complex. 简单胜于复杂：简单的实现优于复杂的。尽量保持代码简单，避免不必要的复杂性。

4. Complex is better than complicated. 复杂胜于凌乱：如果无法避免复杂性，代码之间的关系应该是清晰的，接口应该保持简洁。

5. Flat is better than nested. 扁平胜于嵌套：避免过多的嵌套层次，尽量保持代码的扁平结构。

6. Sparse is better than dense. 间隔胜于紧凑：合理的空间间隔可以提高代码的可读性，不要试图在一行代码中解决所有问题。

7. Readability counts. 可读性很重要：代码的可读性是非常重要的，它不仅影响代码的维护，也影响团队协作。

8. Special cases aren't special enough to break the rules. 特例不足以特殊到可以打破规则：不要因为某个特殊情况就破坏代码的整体一致性和规则。

9. Although practicality beats purity.  实用性胜于纯粹性：在追求代码完美的同时，也要考虑现实需求。

10. Errors should never pass silently. 错误不应被静默地忽略：程序出现错误时，应该明确地抛出异常，而不是悄无声息地忽略。静默的错误会隐藏问题，让调试变得极其困难。

11. Unless explicitly silenced.  除非你明确地让它闭嘴。这是对上一条的补充。只有在非常确定需要忽略某个特定错误时，才应该显式地捕获并处理它（例如使用 try...except 捕获特定异常）。

12. In the face of ambiguity, refuse the temptation to guess. 面对模棱两可，拒绝猜测的诱惑：当需求或逻辑不清晰时，不要靠猜测来编写代码。应该通过沟通、查阅文档等方式来明确意图，避免引入潜在的 bug。

13. There should be one-- and preferably only one --obvious way to do it. 应该有一种——最好只有一种——显而易见的方法来完成它。

14. Although that way may not be obvious at first unless you're Dutch. 虽然这种方法一开始可能并不明显，除非你是荷兰人。这是一句幽默的调侃。Python 的创始人吉多·范罗苏姆（Guido van Rossum）是荷兰人。这句话暗示，找到那个“唯一正确的方法”可能需要对 Python 有深刻的理解。

15. Now is better than never. 现在开始总比永不开始好。

16. Although never is often better than *right* now. 然而，永不开始常常好过立刻行动。这是对上一条的平衡。它提醒我们，在行动前需要深思熟虑，仓促的、未经思考的行动往往比不行动更糟糕。

17. If the implementation is hard to explain, it's a bad idea. 如果实现方法难以解释，那它就不是个好主意。一个优秀的解决方案应该是简单明了、易于向他人解释的。如果实现逻辑过于复杂和晦涩，很可能意味着设计本身存在缺陷。

18. If the implementation is easy to explain, it may be a good idea. 如果实现方法易于解释，那它可能是个好主意。与上一条相对，易于理解和沟通的方案，通常也是更优秀的方案。

19. Namespaces are one honking great idea -- let's do more of those! 命名空间是个绝妙的主意——让我们多来点吧！命名空间（如模块、类）是组织代码、避免命名冲突的强大工具。Python 鼓励开发者充分利用命名空间来构建清晰、模块化的程序。
```
