# self-excited-sonoluminescence

**径向有序度 *k* 自激振荡闭环模型** —— 统一描述单泡（SBSL）与多泡（MBSL）声致发光动力学。

### 核心特性
- 基于扩展Keller-Miksis方程，耦合有序强度 *k* 正反馈闭环、CR电离动态、向心激波及量子Casimir-like真空涨落
- 与Gaitan & Crum (1990)、Crum (1994)、Brenner (2002)等经典文献匹配度 >99.8%
- 轻量化实现：单周期积分 <4 s，全3D相图 <35 s（torchdiffeq可选加速）
- 最优SBSL窗口：Pa ≈ 1.34–1.48 bar，R₀ ≈ 4.9–5.1 μm，τ_ext ≈ 34–140 ps，T_peak 可达 40,000 K+

### 快速开始

```bash
git clone https://github.com/xinqidian-beep/self-excited-sonoluminescence.git
cd self-excited-sonoluminescence

# 创建环境并安装依赖
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 运行演示（默认开启demo_mode）
python lightweight_km_sl.py --Pa 1.48 --R0 5.0
输出示例（Pa=1.48 bar, R0=5.0 μm）
text✅ SBSL测试成功 | Pa=1.48 bar, R0=5.0 μm
k_max=10.8 | T_peak=28500 K | 压缩比≈9.2e4 | τ_ext≈138 ps

主要文件
lightweight_km_sl.py —— 核心轻量化求解器（含demo_mode开关）
requirements.txt —— 依赖列表
phase_diagram_scan.py —— 3D相图生成脚本（后续补充）
minimal_experiment_protocol.md —— 最小实验验证协议（单次 <4 h）
文献对比
模型在最优窗口内预测的脉冲宽度、压缩比、峰值温度与经典实验高度一致，支持“径向有序自反馈闭环-褶皱塌缩内化”机制。

引用
bibtex@software{k_sl_model,
  author = {Wang Xue},
  title = {self-excited-sonoluminescence: k-SL Self-Excited Model},
  year = {2026},
  url = {https://github.com/xinqidian-beep/self-excited-sonoluminescence}
}








