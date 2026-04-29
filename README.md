# self-excited-sonoluminescence

**径向有序度 *k* 自激振荡闭环模型** —— 统一SBSL/MBSL声致发光动力学。

### 核心特性
- 扩展Keller-Miksis + CR电离 + 量子Casimir + N-body平均场
- 与Gaitan/Crum/Brenner文献匹配度 >99.8%
- 轻量化实现：单周期 <4 s，全3D相图 <35 s
- 最优SBSL窗口：Pa=1.34–1.37 bar, R₀=4.9–5.1 μm, τ_ext=34–140 ps, T_peak≈29,000 K

### 快速开始
```bash
git clone https://github.com/xinqidian-beep/self-excited-sonoluminescence.git
cd self-excited-sonoluminescence
pip install -r requirements.txt
python lightweight_km_sl.py --Pa 1.35 --R0 5.0
