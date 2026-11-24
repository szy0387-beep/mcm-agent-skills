# 维护与贡献

从仓库根目录用 Python 3.10 或更高版本运行下面的命令。调度检查只使用标准库，生成物放在临时目录。

```sh
python scripts/check_package.py
```

提交改动时写清它解决的备赛问题。改代码时给可复跑命令、结果和一个边界或反例。改论文流程时提供匿名样例或合成数据，以及可复核的导出结果。保留第三方 Skill 的固定版本和随附许可。[第三方来源](THIRD_PARTY.md)

发布前用解压后的完整 ZIP 运行同一命令。如果更新论文模板或示例，从源码所在目录独立编译，检查摘要、目录跳转、图和参考文献。README、手册、网页和更新日志的入口与版本需一致。[终稿复核](docs/final-delivery.md) · [发布记录](https://github.com/szy0387-beep/mcm-agent-skills/releases)
