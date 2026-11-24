# 维护与贡献

从仓库根目录用 Python 3.10 或更高版本运行下面的命令。调度检查只使用标准库，生成物放在临时目录。

```sh
python scripts/check_package.py
```

提交改动时写清它解决的备赛问题。改代码时给可复跑命令、结果和一个边界或反例。改论文流程时提供匿名样例或合成数据，以及可复核的导出结果。保留第三方 Skill 的固定版本和随附许可。[第三方来源](THIRD_PARTY.md)

发布前用解压后的完整 ZIP 运行同一命令。如果更新论文模板或示例，从源码所在目录独立编译，检查摘要、目录跳转、图和参考文献。README、手册、网页和更新日志的入口与版本需一致。[终稿复核](docs/final-delivery.md) · [发布记录](https://github.com/szy0387-beep/mcm-agent-skills/releases)

改月度预测时，用已安装 NumPy 和 Matplotlib 的环境运行 `python -m unittest discover -s tests`。装有 Tectonic 时，运行 `python scripts/check_package.py --compile-latex` 编译三个论文例子。

## 第三方技能

维护时先对照固定提交、许可和本库适配，再更新 `third-party-skills.json` 的 `sha256`。计算方式见 [vendor_bundle.py](scripts/vendor_bundle.py)。CI 会核对每个专项目录的路径与文件原始字节。

缺失目录可用同版本 ZIP 离线恢复。例如运行 `python scripts/install_extras.py --all --archive "mcm-agent-skills-2.7.0.zip"`。已存在的目录先校验，缺失的目录用通过校验的文件恢复。省略 `--archive` 会尝试下载主分支 ZIP，校验不匹配时请使用对应发行包。
