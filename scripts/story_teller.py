# -*- coding: utf-8 -*-
'''
=================== License Information ===================
Author:     June Sirius
Email:      wojiaoziyou@gmail.com
Version:    Ver 7.3
Date:       May 17, 2021
===========================================================
'''
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from yaml import full_load, dump
from os import system, path
from time import time, localtime

np.random.seed(19)

class Story_Teller(object):
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

