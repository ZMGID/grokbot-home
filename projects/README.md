# projects/

## creative-controller/ — 仿 TourBox 创作控制器（ESP32-S3）

从旧号 `/workspace/creative-controller/` 原样复制（2026-10-08），项目说明见 `creative-controller/README.md`、`docs/`。

包含：KiCad 9 工程和生成脚本（`pcb/`，含嘉立创生产文件 `pcb/fab/`）、cadquery 外壳模型与 STEP/STL（`mechanical/`）、可直接切片的 STL/3MF（`print/`）、
固件源码和编译好的合并固件 `firmware/bin/creativedial-esp32s3-merged.bin`（约 1 MB）、电脑端配置软件（`software/`）、文档（审查报告、3D 打印说明）。

**排除**（构建缓存，可重新生成）：
- `firmware/.pio/`（约 70 MB，PlatformIO 构建缓存；`cd firmware && pio run` 重新生成）
- 所有 `__pycache__/`

**没有超过 50 MB 的单个文件**，所以没用 Git LFS，也没有跳过任何文件。最大的是 `mechanical/out/assembly.step`（约 10 MB）和 `top_shell.step`（约 6 MB）。

**未放进仓库**：旧号的 `/workspace/creative-controller-delivery.zip`（约 15 MB），它是同一批文件的打包版，需要时可从本目录重新打包：
`cd projects && zip -r creative-controller-delivery.zip creative-controller -x '*/.pio/*' '*/__pycache__/*'`

依赖工具（`setup.sh` 会装）：KiCad 9（kicad-cli）、Freerouting（`/workspace/freerouting.jar`）、cadquery 2.8、PlatformIO（espressif32@6.9.0）、PrusaSlicer、Python 3。
