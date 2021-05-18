# -*- coding: utf-8 -*-
'''
=================== License Information ===================
Author:     June Sirius
Email:      wojiaoziyou@gmail.com
Version:    Ver 7.3
Date:       May 17, 2021
===========================================================
'''

import numpy as np
import matplotlib.pyplot as plt
from yaml import full_load, dump
from os import system, path
from time import time, localtime

np.random.seed(19)

# Calculate income & risk V.S. order number
class Income_Risk(object):
    def __init__(self, d=20, h=12, rate=1.1, orders_safe_min=8, orders_safe_max=35, risk_rate_safe=0.005, orders_init=10, orders_adding=0, orders_is_expected=False):
        self.d = d          # Number of working days
        self.h = h          # Working hours
        self.rate = rate    # System expected/safe ratio

        self.orders_safe_min = orders_safe_min  # Min orders_safe (Day 0)
        self.orders_safe_max = orders_safe_max  # Max orders_safe (Day inf)
        self.orders_is_expected = orders_is_expected # orders_actual = orders_expected

        self.risk_rate_safe = risk_rate_safe

        self.orders_init = orders_init          # Actual number of orders at Day 0
        self.orders_adding = orders_adding      # Number of adding orders

    # Calc safe order numbers
    def Orders_safe(self, d):
        X = 2 * self.orders_safe_min - self.orders_safe_max
        Y = 2 * (self.orders_safe_max - self.orders_safe_min)
        return np.floor(X+Y/(1+np.exp((-d+1)/10)))

    # Expected order numbers by the system
    # def Orders_expected(self, orders_safe):
        # return np.ceil(orders_safe * self.rate)
    def Orders_expected(self, d):
        X = 2 * 8 - 35
        Y = 2 * (35 - 8)
        return np.floor(X+Y/(1+np.exp((-d+1)/10)))

    # Actual order numbers
    def Orders_actual(self):
        return self.orders_init + self.orders_adding

    # Average safe time per order
    def Time_per_order(self, orders):
        return self.h/orders

    # Calc actual risk rate
    def Risk_rate_actual(self, orders_actual):
        time_actual = self.Time_per_order(orders_actual)
        self.risk_rate_dangerous = self.risk_rate_safe + (self.time_safe - self.time_expected)/1000

        if (time_actual > self.time_safe):
            return self.risk_rate_safe
        else:
            return self.risk_rate_dangerous

    # Calc actual risk
    def Risk_actual(self, orders_actual):
        risk_rate_actual = self.Risk_rate_actual(orders_actual)
        return 1-np.power(1-risk_rate_actual, orders_actual)

    # Calc total income
    def Total_income(self, orders_actual, orders_expected):
        time_actual = self.Time_per_order(orders_actual)
        if orders_actual < orders_expected:
            return ((8-np.power(50, time_actual-self.time_expected))*orders_actual)/10
        else:
            return 8*np.tanh((orders_actual - orders_expected)/20)+32

    # Main function
    def main(self):
        orders_safe = self.Orders_safe(self.d)
        self.time_safe = self.Time_per_order(orders_safe)

        # orders_expected = self.Orders_expected(orders_safe)
        orders_expected = self.Orders_expected(self.d)
        self.time_expected = self.Time_per_order(orders_expected)

        if self.orders_is_expected:
            orders_actual = orders_expected
        else:
            orders_actual = self.Orders_actual()

        self.risk_actual_init = self.Risk_actual(self.orders_init)
        self.total_income_init = self.Total_income(self.orders_init, orders_expected)
        self.risk_actual = self.Risk_actual(orders_actual)
        self.total_income = self.Total_income(orders_actual, orders_expected)

    # For debug
    def test(self):
        orders_safe = self.Orders_safe(self.d)
        self.time_safe = self.Time_per_order(orders_safe)
        orders_expected = self.Orders_expected(self.d)
        self.time_expected = self.Time_per_order(orders_expected)        

        # plt.figure()
        order_list = np.arange(10,101,10)
        risk_list = []
        for order in order_list:
            risk_list.append(self.Risk_actual(order))
        # plt.plot(order_list, risk_list)
        print(dict(zip(order_list,risk_list)))
        plt.xlabel("Order num")
        plt.ylabel("Risk actual")
        # plt.legend(bbox_to_anchor=(1,1), fontsize=8)
        plt.tight_layout()
        # plt.show()

# income_risk=Income_Risk(orders_safe_min=2,orders_safe_max=29)
# income_risk.test()

def Plot_orders_safe(user_num):
    plt.figure()

    xlist=np.arange(1,51,1)

    for user in np.arange(1,user_num+1,1):
        ylist=[]
        os_min = np.floor(np.random.normal(8,3))
        if os_min<0:
            os_min=0
        os_max = np.floor(np.random.normal(35,3))
        if os_max<0:
            os_max=0    
        income_risk = Income_Risk(orders_safe_min=os_min, orders_safe_max=os_max)
        for d in xlist:
            ylist.append(income_risk.Orders_safe(d))
        plt.plot(xlist,ylist,label=str(int(user))[:2])
    # Expected
    ylist=[]
    os_min = 14
    os_max = 41
    income_risk = Income_Risk(orders_safe_min=os_min, orders_safe_max=os_max)
    for d in xlist:
        ylist.append(income_risk.Orders_safe(d))
    plt.plot(xlist,ylist,'k-.',linewidth=2,label='Expected')
    # O
    ylist=[]
    os_min = 2
    os_max = 29
    income_risk = Income_Risk(orders_safe_min=os_min, orders_safe_max=os_max)
    for d in xlist:
        ylist.append(income_risk.Orders_safe(d))
    plt.plot(xlist,ylist,'r',linewidth=2,label='Orlando')

    plt.xlabel("Day")
    plt.ylabel("Safe Order Num")
    plt.legend(bbox_to_anchor=(1,1), title="ID",fontsize=8)
    plt.tight_layout()
    plt.show()

def Plot_Risk_day():
    plt.figure()
    xlist=np.arange(0,101,1)

    for day in range(1,25,1):
        ylist=[]
        for x in xlist:
            income_risk = Income_Risk(d=day,orders_safe_min=2, orders_safe_max=29,orders_adding=x)
            income_risk.main()
            ylist.append(income_risk.risk_actual)
        plt.plot(xlist,ylist,label=str(int(day)))
    # ylist=[]
    # for x in xlist:
    #     income_risk = Income_Risk(d=x,orders_safe_min=2, orders_safe_max=29,orders_is_expected=True)
    #     income_risk.main()
    #     ylist.append(income_risk.risk_actual)
    # plt.plot(xlist,ylist,'k-.',linewidth=2,label='Expected')
    plt.xlabel('Adding Order Num')
    plt.ylabel('Risk')
    plt.title('Effects of Order Num on Risk for Orlando')
    plt.legend(bbox_to_anchor=(1,1), title="Day",fontsize=8)
    plt.tight_layout()
    plt.show()



class StoryTeller(object):
    def __init__(self, V=0, L=0, O=0, isExport=False, isDebug=True, contentFile="StoryText.yaml"):
        self.V = V  # V value
        self.L = L  # L value
        self.O = O  # O value

        self.history = []       # History of all choices
        self.history.append("0")

        self.V_history = []     # History of V value at each step
        self.L_history = []     # History of L value at each step
        self.O_history = []     # History of O value at each step

        self.tipFlag = False    # Whether O get tip of "AI testers" from AI colleagues at Step1
        self.nameFlag = False   # Whether O enter Step12 and V gets name "Viggo"

        self.isExport = isExport # Whether export all texts to external log file
        self.isDebug = isDebug   # Whether current mode is debug mode

        self.contentFile = contentFile  # File for saving all text content （文案所在文件名）
        self.content = ""               # All text content （所有文案）
        self.content = self.InputContent()

    # Read content texts from external file
    def InputContent(self):
        if path.isfile(self.contentFile):
            with open(self.contentFile, "r", encoding="utf-8") as file:
                content = full_load(file)
            return content
        else:
            err_en = "Error: Fail to find the content text file '"+self.contentFile+"'."
            err_ch = "报错：无法找到文案所在文件'"+self.contentFile+"'。"
            self.ReportError(err_en, err_ch)

    # Save current game process to file
    def SaveProcess(self, *filename):
        self.RecordValues()
        if len(filename) > 0:
            filename = filename[0]
        else:
            currTime = localtime(time())
            filename = "VO_StoryTeller_"
            filename += str(currTime.tm_year)
            filename += "0"*(2-len(str(currTime.tm_mon))) + str(currTime.tm_mon)
            filename += "0"*(2-len(str(currTime.tm_mday))) + str(currTime.tm_mday)
            filename += "_"
            filename += "0"*(2-len(str(currTime.tm_hour))) + str(currTime.tm_hour)
            filename += "0"*(2-len(str(currTime.tm_min))) + str(currTime.tm_min)
            filename += "0"*(2-len(str(currTime.tm_sec))) + str(currTime.tm_sec)
            filename += ".yaml"

        processDict = {}
        processDict['V_history'] = self.V_history
        processDict['L_history'] = self.L_history
        processDict['O_history'] = self.O_history
        processDict['history'] = self.history
        processDict['tipFlag'] = self.tipFlag
        processDict['nameFlag'] = self.nameFlag
        processDict['isExport'] = self.isExport
        processDict['isDebug'] = self.isDebug

        try:
            with open(filename, "w", encoding="utf-8") as file:
                dump(processDict, file, default_flow_style = False)
            print("提示：当前游戏进程已存档至文件'"+filename+"'。")
        except:
            err_en = "Error: Fail to save current game process to file '"+filename+"'."
            err_ch = "报错：无法将当前游戏进程存档到文件'"+filename+"'。"
            print(processDict)
            self.ReportError(err_en, err_ch)

    # Load saved game process from external file
    def LoadProcess(self, filename):
        if path.isfile(filename):
            with open(filename, "r", encoding="utf-8") as file:
                processDict = full_load(file)

            self.V_history = processDict['V_history']
            self.L_history = processDict['L_history']
            self.O_history = processDict['O_history']
            self.history = processDict['history']
            self.tipFlag = processDict['tipFlag']
            self.nameFlag = processDict['nameFlag']
            self.isExport = processDict['isExport']
            self.isDebug = processDict['isDebug']
            print("提示：已成功读档。")
        else:
            err_en = "Error: Fail to find the loading file '"+filename+"'."
            err_ch = "报错：无法找到存档文件'"+filename+"'。"
            self.ReportError(err_en, err_ch)

    # Save current V,L,O value to V,L,O_history list
    def RecordValues(self):
        self.V_history.append(self.V)
        self.L_history.append(self.L)
        self.O_history.append(self.O)

    # Personalize Error Report Method
    # arg_lan: Error language set up, [isEng, isChi]
    def ReportError(self, err_en, err_ch, *arg_lan):
        err_msg = ""
        if len(arg_lan) > 0 and len(arg_lan) == 2:
            if arg_lan[0] == True and arg_lan[1] == False:
                err_msg = err_en
            elif arg_lan[0] == False and arg_lan[1] == True:
                err_msg = err_ch
            elif arg_lan[0] == True and arg_lan[1] == True:
                err_msg = err_en + "\n" + err_ch
        else:
            err_msg = err_en + "\n" + err_ch

        print(err_msg)
        if self.isDebug:
            raise Exception(err_msg)
        else:
            raise Exception(err_msg)
            system("pause")

    # Print or write text of current step to file
    def ExportStep(self, stepID, text, *filename):
        content = ""
        if self.isDebug:
            content += "Step " + str(stepID) + ": \t"
            content += "V="+str(self.V)+"\tL="+str(self.L)+"\tO="+str(self.O)+"\n"
        content += text
        content += "\n"
        print(content)

        if self.isExport and len(filename) > 0:
            filename = filename[0]
            try:
                with open(filename, "a+", encoding="utf8") as f:
                    f.write(content)
            except:
                err_en = "Error: Fail to save text content to file '"+filename+"'."
                err_ch = "报错：无法将文本保存至指定文件'"+filename+"'。"
                self.ReportError(err_en, err_ch)

    # Recognize input (decision content)
    def RecognizeDecision(self, inputDecision):
        inputDecision = str(inputDecision)
        if inputDecision=="0" or inputDecision.upper()=="N" or inputDecision.upper()=="F":
            return False
        elif inputDecision=="1" or inputDecision.upper()=="Y" or inputDecision.upper()=="T":
            return True
        else:
            print("Error: Fail to recognize input, please choose again.")
            print("报错：无法识别输入内容，请再次选择。")
            return 2    # Error code = 2

    # Run random die (with probabibility) for initial V,L,O
    def ValueInit(self):
        self.V = np.random.choice(6, 1, p=[1,0,0,0,0,0])
        self.L = np.random.choice(6, 1, p=[1,0,0,0,0,0])
        self.O = np.random.choice(6, 1, p=[1,0,0,0,0,0])
        self.RecordValues()

    def Step0(self):
        text = ""
        pass



    def main(self):
        self.ValueInit()
        self.Step0()


storyteller=StoryTeller()
