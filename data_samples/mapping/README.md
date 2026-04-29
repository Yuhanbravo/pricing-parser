# Mapping Samples

将开发态或脱敏后的产品映射表放在此目录。

当前仓库根目录已有一份 `产品与托管机构映射表.csv`，加载器可以直接读取；后续如果要切换到项目内固定路径，建议将规范化后的映射表放到本目录。

当前代码同时支持 canonical `.xlsx` mapping；对应自动化回归已包含在 `tests/test_mapping_loader.py`，覆盖 `load_mapping()` 与 `run_pipeline()` 两层路径。
