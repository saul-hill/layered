import numpy as np
import matplotlib.pyplot as plt
import re

# 从EPW输出文件中提取超导相关数据
def extract_superconductivity_data(epw_output_file):
    with open(epw_output_file, 'r') as f:
        content = f.read()
    
    # 提取λ值
    lambda_match = re.search(r'lambda\s*:\s*([\d\.]+)', content)
    lambda_total = float(lambda_match.group(1)) if lambda_match else None
    
    # 提取ωlog值
    omega_log_match = re.search(r'omega_log\s*:\s*([\d\.]+)\s*\(K\)', content)
    omega_log_K = float(omega_log_match.group(1)) if omega_log_match else None
    omega_log_meV = omega_log_K * 0.08617 if omega_log_K else None  # 转换K到meV
    
    # 提取McMillan Tc
    tc_mcmillan_match = re.search(r'McMillan\s*Tc\s*:\s*([\d\.]+)\s*\(K\)', content)
    tc_mcmillan = float(tc_mcmillan_match.group(1)) if tc_mcmillan_match else None
    
    # 提取Allen-Dynes Tc
    tc_allen_dynes_match = re.search(r'Allen-Dynes\s*Tc\s*:\s*([\d\.]+)\s*\(K\)', content)
    tc_allen_dynes = float(tc_allen_dynes_match.group(1)) if tc_allen_dynes_match else None
    
    # 提取a2F数据
    a2f_section_match = re.search(r'Eliashberg\s*spectral\s*function[\s\S]*?(?=\n\n)', content)
    a2f_data = []
    if a2f_section_match:
        a2f_lines = a2f_section_match.group(0).strip().split('\n')[1:]  # 跳过标题行
        for line in a2f_lines:
            values = line.split()
            if len(values) >= 3:
                omega = float(values[0])  # 频率，通常以meV为单位
                a2f = float(values[1])    # α²F(ω)
                lambda_omega = float(values[2])  # λ(ω)
                a2f_data.append((omega, a2f, lambda_omega))
    
    return {
        'lambda_total': lambda_total,
        'omega_log_K': omega_log_K,
        'omega_log_meV': omega_log_meV,
        'tc_mcmillan': tc_mcmillan,
        'tc_allen_dynes': tc_allen_dynes,
        'a2f_data': a2f_data
    }

# 从EPW输出中读取数据
epw_output_file = 'epw/epw.out'
data = extract_superconductivity_data(epw_output_file)

# 打印结果
print(f"McMillan公式计算的Tc: {data['tc_mcmillan']:.2f} K")
print(f"Allen-Dynes公式计算的Tc: {data['tc_allen_dynes']:.2f} K")
print(f"总电子-声子耦合常数λ: {data['lambda_total']:.4f}")
print(f"对数平均声子频率ωlog: {data['omega_log_meV']:.2f} meV ({data['omega_log_K']:.2f} K)")

# 如果有a2F数据，绘制图形
if data['a2f_data']:
    omega, a2f, lambda_omega = zip(*data['a2f_data'])
    
    # 绘制α²F(ω)函数
    plt.figure(figsize=(10, 6))
    plt.plot(omega, a2f, 'b-', linewidth=2)
    plt.xlabel('Frequency (meV)')
    plt.ylabel('α²F(ω)')
    plt.title('Eliashberg Function')
    plt.grid(True)
    plt.savefig('a2f_function_epw.png')
    
    # 绘制λ(ω)函数
    plt.figure(figsize=(10, 6))
    plt.plot(omega, lambda_omega, 'r-', linewidth=2)
    plt.xlabel('Frequency (meV)')
    plt.ylabel('λ(ω)')
    plt.title('Electron-Phonon Coupling Parameter')
    plt.grid(True)
    plt.savefig('lambda_omega_epw.png')

# 保存结果到文件
with open('superconductivity_results_epw.txt', 'w') as f:
    f.write(f"McMillan公式计算的Tc: {data['tc_mcmillan']:.2f} K\n")
    f.write(f"Allen-Dynes公式计算的Tc: {data['tc_allen_dynes']:.2f} K\n")
    f.write(f"总电子-声子耦合常数λ: {data['lambda_total']:.4f}\n")
    f.write(f"对数平均声子频率ωlog: {data['omega_log_meV']:.2f} meV ({data['omega_log_K']:.2f} K)\n")