import core

print("Input filename (ex. test.csv)")
filename = input()

print("Plese input the range of the expected diffusion coefficient D")
# minimum Diffusitivity 입력
print("Input D_min : ? (ex. 1e-14) [m^2/s]")
D_min = float(input())

######### maximum Diffusitivity 입력
print("Input D_max : ? (ex. 1e-11) [m^2/s]")
D_max = float(input())

print("D_step : D/100")
D_step = 1e-15
######### sample thickness 입력
print("Input thickness : ? (ex. 22e-6) [m]")
thickness = float(input())

calc = core.core(filename,D_min,D_max,D_step,thickness)
calc.excute()