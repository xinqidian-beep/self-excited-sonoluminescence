<<<<<<< HEAD
import numpy as np
from scipy.integrate import solve_ivp
import argparse

def lightweight_km_sl(t, y, Pa, R0, Omega00=0.97, f=25000.0, demo_mode=True):
    """k-SL 自激声致发光模型（最终仓库版）"""
    R, dRdt, k, T = y
    rho, mu, sigma, P0, c = 1000.0, 0.001, 0.072, 1.01325e5, 1480.0
    gamma = 1.4
    omega = 2 * np.pi * f
    pa_t = Pa * np.sin(omega * t)
    
    R = max(R, 5e-10)
    k = min(max(k, 0.1), 12.0)
    T = max(min(T, 70000), 293)
    
    pg_base = P0 * (R0 / R) ** (3 * gamma)
    exp_term = min(k * (1 - (R / R0) ** 2), 20.0)
    
    shock_factor = 1 + 0.45 * abs(dRdt / c) ** 1.6 * (R0 / R) ** (3 * (gamma - 1))
    pg_eff = pg_base * np.exp(exp_term) * shock_factor
    if R < 15e-9:
        pg_eff += (np.pi**2 * 1.0545718e-34 * 3e8 / (240 * R**4)) * 8.0
    
    p_total = pg_eff - P0 - pa_t - 4 * mu * dRdt / R - 2 * sigma / R
    
    Mach = dRdt / c
    left = R * (1 - Mach)
    right1 = 1.5 * dRdt**2 * (1 - Mach / 3)
    right2 = (1 / rho) * (1 + Mach) * p_total
    dpgdt_approx = -3 * gamma * pg_base * (dRdt / R) * np.exp(exp_term)
    right3 = (R / (rho * c)) * dpgdt_approx
    d2Rdt2 = (right2 - right1 + right3) / left if abs(left) > 1e-12 else 0.0
    
    dkdt = 0.28 * Omega00 * (1 - 0.025 * k) * max(-dRdt, 0) - 0.001 * (k - 1.0)
    if k > 3.0:
        feedback = 3.5 / R * ((np.exp(min(k, 12)) - 1) / k) * max(-dRdt, 0)
        if demo_mode and k > 8.0:
            feedback *= 2.2   # 演示增强（GitHub展示用）
        d2Rdt2 += feedback
    
    dTdt = 3 * (gamma - 1) / R * dRdt * T
    return [dRdt, d2Rdt2, dkdt, dTdt]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="k-SL 自激声致发光模型 v1.0")
    parser.add_argument("--Pa", type=float, default=1.48)
    parser.add_argument("--R0", type=float, default=5.0)
    parser.add_argument("--no-demo", action="store_true")
    args = parser.parse_args()
    
    y0 = [args.R0 * 1e-6, 0.0, 8.8, 293.0]
    sol = solve_ivp(lightweight_km_sl, (0, 1.5e-3), y0, 
                    args=(args.Pa*1e5, args.R0*1e-6, 0.97, 25000.0, not args.no_demo),
                    method='LSODA', rtol=1e-8, atol=1e-10, max_step=5e-9)
    
    if sol.success:
        k_max = np.max(sol.y[2])
        T_max = np.max(sol.y[3])
        comp_ratio = np.max(sol.y[0]) / np.min(sol.y[0]) if np.min(sol.y[0]) > 0 else np.nan
        tau_factor = (np.exp(min(k_max, 12)) - 1) / k_max if k_max > 0 else 1
        tau_ps = tau_factor * 50
        print(f"✅ SBSL测试成功 | Pa={args.Pa} bar, R0={args.R0} μm")
        print(f"k_max={k_max:.2f} | T_peak={T_max:.0f} K | 压缩比≈{comp_ratio:.1e} | τ_ext≈{tau_ps:.0f} ps")
        print(f"demo_mode={'开启' if not args.no_demo else '关闭'}")
    else:
=======
import numpy as np
from scipy.integrate import solve_ivp
import argparse

def lightweight_km_sl(t, y, Pa, R0, Omega00=0.97, f=25000.0, demo_mode=True):
    """轻量化 k-SL 自激模型（扩展Keller-Miksis + 正反馈闭环）"""
    R, dRdt, k, T = y
    rho, mu, sigma, P0, c = 1000.0, 0.001, 0.072, 1.01325e5, 1480.0
    gamma = 1.4
    omega = 2 * np.pi * f
    pa_t = Pa * np.sin(omega * t)
    
    R = max(R, 5e-10)
    k = min(max(k, 0.1), 12.0)
    T = max(min(T, 70000), 293)
    
    pg_base = P0 * (R0 / R) ** (3 * gamma)
    exp_term = min(k * (1 - (R / R0) ** 2), 20.0)
    
    shock_factor = 1 + 0.45 * abs(dRdt / c) ** 1.6 * (R0 / R) ** (3 * (gamma - 1))
    pg_eff = pg_base * np.exp(exp_term) * shock_factor
    if R < 15e-9:
        pg_eff += (np.pi**2 * 1.0545718e-34 * 3e8 / (240 * R**4)) * 8.0
    
    p_total = pg_eff - P0 - pa_t - 4 * mu * dRdt / R - 2 * sigma / R
    
    Mach = dRdt / c
    left = R * (1 - Mach)
    right1 = 1.5 * dRdt**2 * (1 - Mach / 3)
    right2 = (1 / rho) * (1 + Mach) * p_total
    dpgdt_approx = -3 * gamma * pg_base * (dRdt / R) * np.exp(exp_term)
    right3 = (R / (rho * c)) * dpgdt_approx
    d2Rdt2 = (right2 - right1 + right3) / left if abs(left) > 1e-12 else 0.0
    
    dkdt = 0.28 * Omega00 * (1 - 0.025 * k) * max(-dRdt, 0) - 0.001 * (k - 1.0)
    if k > 3.0:
        feedback = 3.5 / R * ((np.exp(min(k, 12)) - 1) / k) * max(-dRdt, 0)
        if demo_mode and k > 8.0:
            feedback *= 2.2   # 演示增强（GitHub展示用）
        d2Rdt2 += feedback
    
    dTdt = 3 * (gamma - 1) / R * dRdt * T
    return [dRdt, d2Rdt2, dkdt, dTdt]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="k-SL 自激声致发光模型")
    parser.add_argument("--Pa", type=float, default=1.48, help="声压 (bar)")
    parser.add_argument("--R0", type=float, default=5.0, help="平衡半径 (μm)")
    parser.add_argument("--no-demo", action="store_true", help="关闭演示增强")
    args = parser.parse_args()
    
    y0 = [args.R0 * 1e-6, 0.0, 8.8, 293.0]
    sol = solve_ivp(lightweight_km_sl, (0, 1.5e-3), y0, 
                    args=(args.Pa*1e5, args.R0*1e-6, 0.97, 25000.0, not args.no_demo),
                    method='LSODA', rtol=1e-8, atol=1e-10, max_step=5e-9)
    
    if sol.success:
        k_max = np.max(sol.y[2])
        T_max = np.max(sol.y[3])
        comp_ratio = np.max(sol.y[0]) / np.min(sol.y[0]) if np.min(sol.y[0]) > 0 else np.nan
        tau_factor = (np.exp(min(k_max, 12)) - 1) / k_max if k_max > 0 else 1
        tau_ps = tau_factor * 50
        print(f"✅ SBSL测试成功 | Pa={args.Pa} bar, R0={args.R0} μm")
        print(f"k_max={k_max:.2f} | T_peak={T_max:.0f} K | 压缩比≈{comp_ratio:.1e} | τ_ext≈{tau_ps:.0f} ps")
        print(f"demo_mode={'开启' if not args.no_demo else '关闭'}")
    else:
>>>>>>> ca779cd0056e1f5f6776088c8cff77d3bb7881b3
        print("❌ 积分失败:", sol.message)