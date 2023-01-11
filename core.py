import numpy as np
from datetime import datetime
import csv
from datetime import timedelta

class core():
    def __init__(self, filename, D_min, D_max, D_step, d):
        self.filename = filename
        self.D_min = D_min
        self.D_max = D_max
        self.D_step = D_step
        self.d = d
        self.D_result = 0

    # Fitting 할 함수, Fick's law의 Solution 함수
    def J_func(self, t, Js, D, d):
        # Js : flux at steady state, d : sample thickness, D : Diffusivity, t : time
        factor = Js*(4*d*d/(np.pi*D*t))**0.5
        sum = 0
        for n in range(7000):
            sum = sum + np.exp(-(d*d/(4*D*t))*(2*n+1)**2)

        return factor*sum

    ## csv 파일에 시간 부분에 시간, 분, 초를 초로 변환하는 함수
    def get_seconds(self, time_str):
        # print(len(time_str))
        
        if len(time_str) == 5:
            mm, ss = time_str.split(':')
            hh = 0
        else:
            hh, mm, ss = time_str.split(':')
            
        return int(hh) * 3600 + int(mm) * 60 + int(ss)

    # 입력해야 할 csv 파일 명 입력, 같은 폴더안에 있어야 함
    # Finally, the time and the flux J will be returned 
    def loadCSVFile(self):
        file = open(self.filename)
        rdr = csv.reader(file)
        
        time = np.array([])
        WVTR_raw = np.array([])

        ## csv 파일 중 time, WVTR 데이더 추출
        for line in rdr:
            time = np.append(time,float(self.get_seconds(line[0])))
            # time = np.append(time,float((line[0])))
            WVTR_raw = np.append(WVTR_raw,float(line[1]))

        Fconv = 1/86400*1/22.4*1e-3
        J = WVTR_raw*Fconv

        return time, J

    # time,J = loadCSVFile('ref.csv')
    def excute(self):
        time, J = self.loadCSVFile()
        # let the last comonenet is the flux at steady state
        Js=J[-1]
        self.D_result = self.iterativeMethod(time,J,D_start=self.D_min, D_end=self.D_max, D_step=self.D_step,Js=Js,d=self.d)
        time_fitted = np.logspace(0,4,2000)
        J_fitted = self.J_func(time_fitted, Js=Js, D=self.D_result, d=self.d) #
        self.writeCSVfile(time_fitted,J_fitted) 

    # Finally, the time and the flux J will be returned 
    def iterativeMethod(self,time, J, D_start, D_end, D_step, Js, d):
        Js = J[-1]
        D_array = []
        error_array = []
        # error = np.zeros_like(D_array)
        i = 0
        error = 1
        pre_error = 1000000
        D_value = D_start
        while error < pre_error and D_value <= D_end:
                pre_error = error
                J_temp = self.J_func(time,Js,D_value,d)
                D_array.append(D_value)
                error = np.average((J - J_temp)/J.T)
                error_array.append(error)
                # print(D_value)
                i = i + 1
                # D_step = D_value의 1%
                D_value = D_value + D_value/100
            # print(np.abs((error - pre_error)/error))
        
        print("Done!")
        print("D : "+ str(D_array[-1]) +" [m^2/s]") # D 값 출력 부분 수정, 단위 추가, float 형태를 string으로 변환
        return D_array[-1]

    def writeCSVfile(self,time,J):
        dt = datetime.now()
        dtname = dt.strftime("%Y-%m-%d %H:%M:%S")
        savename = self.filename[0:len(self.filename)-4] + "_result " + dtname + ".csv"
        print("File saved!")
        print("File name : " + savename) # 파일 이름명 출력
        f = open(savename,'w',newline='')
        wr = csv.writer(f)
        
        for i in range(len(time)):
            wr.writerow([time[i],J[i]])

        f.close()