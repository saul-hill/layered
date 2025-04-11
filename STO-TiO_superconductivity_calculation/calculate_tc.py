import numpy as np
import matplotlib.pyplot as plt
from elphbolt.core import ElphBolt

# 从EPW输出中读取电子-声子耦合数据
elphbolt = ElphBolt()
elphbolt.read_epw_output('epw/a2f.out')

# 计算超导转变温度
tc_mcmillan = elphbolt.calculate_tc_mcmillan()
tc_allen_dynes = elphbolt.calculate_tc_allen_dynes()
tc_eliashberg = elphbolt.solve_eliashberg_equations(temps=np.linspace(1, 100, 100))

# 打印结果
print(f"McMillan公式计算的Tc: {tc_mcmillan:.2f} K")
print(f"Allen-Dynes公式计算的Tc: {tc_allen_dynes:.2f} K")
print(f"Eliashberg方程计算的Tc: {tc_eliashberg:.2f} K")

# 绘制α²F(ω)函数
plt.figure(figsize=(10, 6))
plt.plot(elphbolt.omega, elphbolt.a2f, 'b-', linewidth=2)
plt.xlabel('Frequency (meV)')
plt.ylabel('α²F(ω)')
plt.title('Eliashberg Function')
plt.grid(True)
plt.savefig('a2f_function.png')

# 绘制λ(ω)函数
plt.figure(figsize=(10, 6))
plt.plot(elphbolt.omega, elphbolt.lambda_omega, 'r-', linewidth=2)
plt.xlabel('Frequency (meV)')
plt.ylabel('λ(ω)')
plt.title('Electron-Phonon Coupling Parameter')
plt.grid(True)
plt.savefig('lambda_omega.png')

# 保存结果到文件
with open('superconductivity_results.txt', 'w') as f:
    f.write(f"McMillan公式计算的Tc: {tc_mcmillan:.2f} K\n")
    f.write(f"Allen-Dynes公式计算的Tc: {tc_allen_dynes:.2f} K\n")
    f.write(f"Eliashberg方程计算的Tc: {tc_eliashberg:.2f} K\n")
    f.write(f"总电子-声子耦合常数λ: {elphbolt.lambda_total:.4f}\n")
    f.write(f"对数平均声子频率ωlog: {elphbolt.omega_log:.2f} meV\n")