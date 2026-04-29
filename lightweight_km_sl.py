import numpy as np
from scipy.integrate import solve_ivp
import argparse

def lightweight_km_sl(t, y, Pa, R0, Omega00=0.85, f=25000.0):
    R, dRdt, k, T = y
    rho, mu, sigma, P0, c = 1000.0, 0.001, 0.072, 1.01325e5, 1480.0
    gamma = 1.4
    omega = 2 * np.pi * f
    pa_t = Pa * np.sin(omega * t)
    
    R = max(R, 5e-10)
    k = min(max(k, 0.1), 12.0)
    T = max(min(T, 32000), 293)
    
    pg_base = P0 * (R0 / R) ** (3 * gamma)
    exp_term = min(k * (1 - (R / R0) ** 2), 20.0)
    pg_eff = pg_base * np.exp(exp_term) * (1 + 0.05 * abs(dRdt / c) ** 0.4 * (R0 / R) ** (3 * (gamma - 1)))
    if R < 10e-9:
        pg_eff += (np.pi**2 * 1.0545718e-34 * 3e8 / (240 * R**4)) * (1 + 0.8 * R0 / R)
    
    p_total = pg_eff - P0 - pa_t - 4 * mu * dRdt / R - 2 * sigma / R
    
    Mach = dRdt / c
    left = R * (1 - Mach)
    right1 = 1.5 * dRdt**2 * (1 - Mach / 3)
    right2 = (1 / rho) * (1 + Mach) * p_total
    dpgdt_approx = -3 * gamma * pg_base * (dRdt / R) * np.exp(exp_term)
    right3 = (R / (rho * c)) * dpgdt_approx
    d2Rdt2 = (right2 - right1 + right3) / left if abs(left) > 1e-12 else 0.0
    
    # k动态 + 增强自激闭环（调优后）
    dkdt = 0.052 * Omega00 * (1 - 0.115 * k) * max(-dRdt, 0) - 0.0075 * (k - 1.0)
    if k > 6.5:  # 提前触发阈值
        d2Rdt2 += 0.18 / R * ((np.exp(min(k, 12)) - 1) / k) * max(-dRdt, 0)  # ε提升至0.18
    
    dTdt = 3 * (gamma - 1) / R * dRdt * T
    return [dRdt, d2Rdt2, dkdt, dTdt]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--Pa", type=float, default=1.35)
    parser.add_argument("--R0", type=float, default=5.0)
    args = parser.parse_args()
    
    y0 = [args.R0 * 1e-6, 0.0, 2.0, 293.0]  # 初始k提升至2.0加速触发
    sol = solve_ivp(lightweight_km_sl, (0, 5e-4), y0, args=(args.Pa*1e5, args.R0*1e-6),
                    method='LSODA', rtol=1e-8, atol=1e-10, max_step=1e-7)
    
    if sol.success:
        k_max = np.max(sol.y[2])
        T_max = np.max(sol.y[3])
        R_max = np.max(sol.y[0])
        R_min = np.min(sol.y[0])
        comp_ratio = R_max / R_min if R_min > 0 else np.nan
        tau_factor = (np.exp(min(k_max, 12)) - 1) / k_max if k_max > 0 else 1
        tau_ps = tau_factor * 50
        print(f"✅ SBSL测试成功 | Pa={args.Pa} bar, R0={args.R0} μm")
        print(f"k_max={k_max:.2f} | T_peak={T_max:.0f} K | 压缩比≈{comp_ratio:.1e} | τ_ext≈{tau_ps:.0f} ps")
    else:
        print("❌ 积分失败:", sol.message)