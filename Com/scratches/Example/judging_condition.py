# 多条件判断
files = ['ParticleScannerScan_0', 'Particle_1', 'Particle_2', 'Particle_3', 'Particle_4']
for file in files:
    judging_condition = lambda file: ('Particle' in file
                                      and 'Scanner' not in file
                                      and file not in [f'Particle_{i}' for i in range(2, 4)])
    if judging_condition(file):
        print(file)
