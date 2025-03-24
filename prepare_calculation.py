import os
import numpy as np
from ase.io import read
from ase.calculators.espresso import Espresso, EspressoProfile
from ase.calculators.calculator import FileIOCalculator
from ase.spacegroup.symmetrize import check_symmetry
from ase.visualize import view

# 读取CIF文件
atoms = read("STO-TiO_Cm-atoms.cif", format='cif')
#check_symmetry(atoms, symprec=1e-5, verbose=True)
#view(atoms)

# 设置计算参数
pseudopotentials = {'Sn': 'Sn.pbesol-dn-kjpaw_psl.1.0.0.UPF',
                   'Ti': 'Ti.pbe-spn-kjpaw_psl.1.0.0.UPF',
                   'O': 'O.pbe-n-kjpaw_psl.1.0.0.UPF'}

# 创建工作目录
if not os.path.exists('scf'):
    os.makedirs('scf')
if not os.path.exists('nscf'):
    os.makedirs('nscf')
if not os.path.exists('ph'):
    os.makedirs('ph')
if not os.path.exists('epw'):
    os.makedirs('epw')

# 创建SCF计算输入
scf_input_data = {
    'control': {
        'calculation': 'scf',
        'restart_mode': 'from_scratch',
        'prefix': 'sto_tio',
        'pseudo_dir': './pseudo',
        'outdir': './tmp',
        'verbosity': 'high',
    },
    'system': {
        'ecutwfc': 60,
        'ecutrho': 480,
        'occupations': 'smearing',
        'smearing': 'mp',
        'degauss': 0.02,
    },
    'electrons': {
        'conv_thr': 1.0e-10,
        'mixing_beta': 0.7,
    },
}

espresso_profile = EspressoProfile(
    command=['pw.x'],  # MPI 并行运行，4 个进程
    pseudo_dir='./pseudopotentials/'  # 伪势文件路径
)

# 创建SCF计算器
calc_scf = Espresso(
    pseudopotentials=pseudopotentials,
    input_data=scf_input_data,
    kpts=(8, 8, 4),
    directory='scf',
    profile=espresso_profile
)

# 将计算器附加到原子对象
atoms.calc = calc_scf

# 生成SCF输入文件
calc_scf.write_input(atoms)

# 创建NSCF计算输入
nscf_input_data = scf_input_data.copy()
nscf_input_data['control']['calculation'] = 'nscf'
nscf_input_data['electrons']['diago_full_acc'] = True
nscf_input_data['system']['nosym'] = True
nscf_input_data['system']['noinv'] = True

# 创建NSCF计算器
calc_nscf = Espresso(
    pseudopotentials=pseudopotentials,
    input_data=nscf_input_data,
    kpts=(16, 16, 8),  # 更密的k点网格用于NSCF计算
    directory='nscf'
)

# 生成NSCF输入文件
FileIOCalculator.write_input(calc_nscf, atoms)

print("已生成SCF和NSCF输入文件")
print("请下载所需的赝势文件并放入pseudo目录")
print("接下来请运行SCF计算，然后是NSCF计算")