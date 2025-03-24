#!/bin/bash

# 创建必要的目录
mkdir -p pseudo tmp

# 下载赝势文件
cd pseudo
wegt https://pseudopotentials.quantum-espresso.org/upf_files/Sn.pbesol-dn-kjpaw_psl.1.0.0.UPF
wget https://www.quantum-espresso.org/upf_files/Ti.pbe-spn-kjpaw_psl.1.0.0.UPF
wget https://www.quantum-espresso.org/upf_files/O.pbe-n-kjpaw_psl.1.0.0.UPF
cd ..

# 准备计算
python prepare_calculation.py

# 运行SCF计算
cd scf
mpirun -np 4 pw.x < sto_tio.pwi > sto_tio.scf.out
cd ..

# 运行NSCF计算
cd nscf
mpirun -np 4 pw.x < sto_tio.pwi > sto_tio.nscf.out
cd ..

# 运行声子计算
cd ph
mpirun -np 4 ph.x < ph.in > ph.out
cd ..

# 运行q2r.x将动力学矩阵转换为实空间力常数
cd ph
q2r.x < q2r.in > q2r.out
cd ..

# 运行EPW计算
cd epw
mpirun -np 4 epw.x < epw.in > epw.out
cd ..

# 使用ElphBolt计算超导转变温度
cd epw
python ../calculate_tc.py