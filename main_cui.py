import core

filename = 'test.csv'
D_min = 1e-14
D_max = 1e-11
D_step = 1e-15
thickness = 22e-6

calc = core.core(filename,D_min,D_max,D_step,thickness)
calc.excute()