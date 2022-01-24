import multiprocessing
import os
import pickle
import random
import sys
import time

import mouse
from imagesearch import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import uic
import playsound
import threading
import keyboard
import resource_rc

form_class = uic.loadUiType("Weing 3.2V.ui")[0]
class Form(QDialog, form_class):
    path = os.getcwd() + "\\"
    patternPath=path+"pattern\\"
    routinePath = patternPath + "routine\\"
    buffPath = patternPath + "buff\\"
    mesoPath = patternPath + "meso\\"
    skillAPath = patternPath + "skillA\\"
    skillBPath = patternPath + "skillB\\"
    mesoimage = path + 'resource\\meso.png'
    buffimage = path + 'resource\\buff.png'
    skillAimage = path + 'resource\\skillA.png'
    skillBimage = path + 'resource\\skillB.png'
    bufflist = dict()
    mesolist = dict()
    routinelist = dict()
    skillAlist = dict()
    skillBlist = dict()
    curstate="stop"
    recordmode=False
    recordpath=""
    recordname=""
    deleteFile=""
    def recordFileCheck(self):
        fList = os.listdir(self.patternPath+self.recordname+"\\")
        fileList = list()
        for file in fList:
            if self.recordname in file:
                fileList.append(int("".join(file.split(self.recordname))))
        fileList.sort()
        none = []
        if len(fileList) == 0:
            startNum = 0
            endNum = 0
        if len(fileList) == 1:
            startNum = fileList[0]
            endNum = fileList[0]
            if startNum != 0:
                none.append(0)
        if len(fileList) >= 2:
            startNum = fileList[0]
            endNum = fileList[-1]
        for i in range(0, endNum + 1):
            if i not in fileList:
                none.append(i)
        return startNum, endNum, none
    def recordWating(self):
        if len(self.recordFileCheck()[2]) == 0:
            self.printing(" - 누락된 번호없음")
        else:
            self.printing(" - 누락된 번호:" + str(self.recordFileCheck()[2]))
        r = threading.Thread(target=self.record)
        r.daemon=True
        r.start()

    def record(self):
        while (True):
            if self.recordmode==False:
                break
            if self.recordHotkeyCheck.isChecked()==False:
                continue
            (startnum,lastnum,none) = self.recordFileCheck()
            if len(none) == 0:
                count = lastnum + 1
            else:
                count = none[0]
                self.printing(" - 누락된 번호를 우선적으로 채웁니다: " + str(none[0]))
            if self.recordHotkeyCheck.isChecked()==False:
                continue
            if self.recordmode==False:
                break
            while(True):
                time.sleep(0.05)
                if self.recordmode == False:
                    break
                if mouse.is_pressed("right"):
                    break
            if self.recordmode==False:
                break
            if self.recordHotkeyCheck.isChecked()==False:
                continue
            self.mesoBtn.setEnabled(False)
            self.buffBtn.setEnabled(False)
            self.routineBtn.setEnabled(False)
            self.skillABtn.setEnabled(False)
            self.skillBBtn.setEnabled(False)
            self.stateimg("record")
            self.play1()
            self.printing('┌ 녹화가 시작되었습니다. (녹화번호: ' + str(count) + ")")
            recorded = keyboard.record()
            self.printing('└ 녹화가 종료되었습니다.')
            self.stateimg("stop")
            self.mesoBtn.setEnabled(True)
            self.buffBtn.setEnabled(True)
            self.routineBtn.setEnabled(True)
            self.skillABtn.setEnabled(True)
            self.skillBBtn.setEnabled(True)
            self.play2()
            with open(self.recordpath+self.recordname + str(count), 'wb') as file:
                pickle.dump(recorded, file)
            file.close()
            if self.recordname=="meso":
                self.mesolist[count]=recorded
                self.mesoPR()
            if self.recordname=="buff":
                self.bufflist[count]=recorded
                self.buffPR()
            if self.recordname=="routine":
                self.routinelist[count]=recorded
                self.routinePR()
            if self.recordname=="skillA":
                self.skillAlist[count]=recorded
                self.skillAPR()
            if self.recordname=="skillB":
                self.skillBlist[count]=recorded
                self.skillBPR()
            self.fileListView.addItem(str(self.recordname + str(count)))
            self.fileListView.scrollToBottom()
    def deleteFileSelect(self):
        self.deleteFile = self.recordpath+str(self.fileListView.currentItem().text())
    def fileDelete(self):
        if self.deleteFile != "":
            os.remove(self.deleteFile)
            self.fileListView.clear()
            name = (self.recordpath).split("\\")[-2]
            print(name)
            self.printing("[system] "+self.deleteFile.split("\\")[-1]+" 패턴이 삭제되었습니다.")
            for i in self.fileCheck(self.recordpath):
                self.fileListView.addItem(name+str(i))
            if self.recordname=="meso":
                del self.mesolist[int(self.deleteFile.split("\\")[-1].split("meso")[-1])]
                a=threading.Thread(target=self.mesoPR)
                a.start()
                a.join()
            if self.recordname=="buff":
                del self.bufflist[int(self.deleteFile.split("\\")[-1].split("buff")[-1])]
                a=threading.Thread(target=self.buffPR)
                a.start()
                a.join()
            if self.recordname=="routine":
                del self.routinelist[int(self.deleteFile.split("\\")[-1].split("routine")[-1])]
                a=threading.Thread(target=self.routinePR)
                a.start()
                a.join()
            if self.recordname=="skillA":
                del self.skillAlist[int(self.deleteFile.split("\\")[-1].split("skillA")[-1])]
                a=threading.Thread(target=self.skillAPR)
                a.start()
                a.join()
            if self.recordname=="skillB":
                del self.skillBlist[int(self.deleteFile.split("\\")[-1].split("skillB")[-1])]
                a=threading.Thread(target=self.skillBPR)
                a.start()
                a.join()
        self.deleteFile=""
    def mesoRecord(self):
        if self.recordmode==False:
            self.setRecord(self.mesoPath)
            self.printing("[system] 메소회수 패턴 녹화모드를 실행합니다.")
            self.printing(" - 녹화모드중에는 루프를 실행할 수 없습니다.")
            self.recordWating()
            name = (self.recordpath).split("\\")[-2]
            for i in self.mesolist.keys():
                self.fileListView.addItem(name+str(i))
        else:
            self.printing("[system] 녹화모드를 종료합니다.")
            self.setFixedSize(320,452)
            self.fileListView.clear()
            self.recordmode = False
    def buffRecord(self):
        if self.recordmode==False:
            self.setRecord(self.buffPath)
            self.printing("[system] 버프리필 패턴 녹화모드를 실행합니다.")
            self.printing(" - 녹화모드중에는 루프를 실행할 수 없습니다.")
            self.recordWating()
            name = (self.recordpath).split("\\")[-2]
            for i in self.bufflist.keys():
                self.fileListView.addItem(name+str(i))
        else:
            self.printing("[system] 녹화모드를 종료합니다.")
            self.setFixedSize(320,452)
            self.fileListView.clear()
            self.recordmode = False
    def routineRecord(self):
        if self.recordmode==False:
            self.setRecord(self.routinePath)
            self.printing("[system] 일반 패턴 녹화모드를 실행합니다.")
            self.printing(" - 녹화모드중에는 루프를 실행할 수 없습니다.")
            self.recordWating()
            name = (self.recordpath).split("\\")[-2]
            for i in self.routinelist.keys():
                self.fileListView.addItem(name+str(i))
        else:
            self.printing("[system] 녹화모드를 종료합니다.")
            self.setFixedSize(320,452)
            self.fileListView.clear()
            self.recordmode = False
    def skillARecord(self):
        if self.recordmode == False:
            self.setRecord(self.skillAPath)
            self.printing("[system] 스킬A 패턴 녹화모드를 실행합니다.")
            self.printing(" - 녹화모드중에는 루프를 실행할 수 없습니다.")
            self.recordWating()
            name = (self.recordpath).split("\\")[-2]
            for i in self.skillAlist.keys():
                self.fileListView.addItem(name+str(i))
        else:
            self.printing("[system] 녹화모드를 종료합니다.")
            self.setFixedSize(320,452)
            self.recordmode = False
            self.fileListView.clear()
    def skillBRecord(self):
        if self.recordmode == False:
            self.setRecord(self.skillBPath)
            self.printing("[system] 스킬B 패턴 녹화모드를 실행합니다.")
            self.printing(" - 녹화모드중에는 루프를 실행할 수 없습니다.")
            self.recordWating()
            name = (self.recordpath).split("\\")[-2]
            for i in self.skillBlist.keys():
                self.fileListView.addItem(name+str(i))
        else:
            self.printing("[system] 녹화모드를 종료합니다.")
            self.setFixedSize(320,452)
            self.recordmode = False
            self.fileListView.clear()
    def setRecord(self,path):
        self.setFixedSize(320,777)
        self.recordpath=path
        self.recordname=path.split('\\')[-2]
        self.recordmode=True
    def stateimg(self,state):
        if state=="stop":
            self.curstate=state
            self.state.setText(
                "<html><head/><body><p><img src=\"" + self.path + "./resource/stop.png\"/></p></body></html>")
        if state=="running":
            self.curstate=state
            self.state.setText(
                "<html><head/><body><p><img src=\"" + self.path + "./resource/running.png\"/></p></body></html>")
        if state=="record":
            self.curstate=state
            self.state.setText(
                "<html><head/><body><p><img src=\"" + self.path + "./resource/record.png\"/></p></body></html>")
        if state=="viol":
            self.state.setText(
                "<html><head/><body><p><img src=\"" + self.path + "./resource/violdetected.png\"/></p></body></html>")
        if state=="rune":
            self.state.setText(
                "<html><head/><body><p><img src=\"" + self.path + "./resource/runedetected.png\"/></p></body></html>")
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weing 3.2V")
        self.setWindowIcon(QIcon(self.path+'resource\\aing.ico'))
        self.setGeometry(1550,50,0,0)
        self.setFixedSize(320,452)
        self.patternRefresh()
        self.playstart()
        self.stateimg("stop")
        self.printing("[system] 위잉 3.2버전 로드되었습니다.")
        self.printing(" - 업데이트날짜: 2021/02/08")
        self.mesoBtn.clicked.connect(self.mesoRecord)
        self.buffBtn.clicked.connect(self.buffRecord)
        self.routineBtn.clicked.connect(self.routineRecord)
        self.skillABtn.clicked.connect(self.skillARecord)
        self.skillBBtn.clicked.connect(self.skillBRecord)
        self.fileListView.itemClicked.connect(self.deleteFileSelect)
        self.deleteBtn.clicked.connect(self.fileDelete)
        self.label_2.setText(
            "<html><head/><body><p><img src=\"" + self.path + "./resource/aing.ico\"/></p></body></html>")
        self.label_7.setText(
            "<html><head/><body><p><img src=\"" + self.path + "./resource/recordMode.png\"/></p></body></html>")
        wait = threading.Thread(target=self.waiting)
        checking = threading.Thread(target=self.checker)
        #clickchecking = threading.Thread(target=self.clickChecker)
        #clickcheckbox = threading.Thread(target=self.clickCheckbox)
        checking.daemon=True
        wait.daemon=True
        #clickchecking.daemon=True
        #clickcheckbox.daemon=True
        wait.start()
        checking.start()
        #clickchecking.start()
        #clickcheckbox.start()

    def test(self):
        if self.deleteFile =="":
            self.printing("[Warning] 녹화된 버프 패턴이 존재하지 않습니다.")
            return
        else:
            self.recordmode=False
            with open(self.deleteFile, 'rb') as file:
                testfile=(pickle.load(file))
            file.close()
            self.play3()
            self.printing('┌ 테스트 패턴 실행 : 패턴번호> '+self.deleteFile.split("\\")[-1])
            delay = random.uniform(0.93, 1.0)
            ret = keyboard.play(testfile, stop='-', speed_factor=round(delay, 3))
            if keyboard.is_pressed('up'):
                keyboard.release('up')
            if keyboard.is_pressed('down'):
                keyboard.release('down')
            if keyboard.is_pressed('left'):
                keyboard.release('left')
            if keyboard.is_pressed('right'):
                keyboard.release('right')
            self.printing('└ 테스트 패턴 종료')
            self.play1()
            self.recordmode=True
            return



    def fileCheck(self,path):
        pathName = path.split("\\")[-2]
        fList = os.listdir(path)
        fileList = list()
        for file in fList:
            if pathName in file:
                fileList.append(int("".join(file.split(pathName))))
        fileList.sort()
        return fileList

    def fileLoader(self, path, lis):
        name = path.split("\\")[-2]
        fileL=self.fileCheck(path)
        for i in fileL:
            with open(path + name + str(i), 'rb') as file:
                lis[i]=(pickle.load(file))
            file.close()
    def allLoad(self):
        self.fileLoader(self.mesoPath, self.mesolist)
        self.fileLoader(self.buffPath,self.bufflist)
        self.fileLoader(self.routinePath,self.routinelist)
        self.fileLoader(self.skillAPath,self.skillAlist)
        self.fileLoader(self.skillBPath,self.skillBlist)
    def patternRefresh(self):
        self.allLoad()
        self.mesoPR()
        self.buffPR()
        self.routinePR()
        self.skillAPR()
        self.skillBPR()
    def mesoPR(self):
        self.mesoCnt.setText(str(len(self.mesolist))+"개")
    def buffPR(self):
        self.buffCnt.setText(str(len(self.bufflist))+"개")
    def routinePR(self):
        self.routineCnt.setText(str(len(self.routinelist))+"개")
    def skillAPR(self):
        self.skillACnt.setText(str(len(self.skillAlist))+"개")
    def skillBPR(self):
        self.skillBCnt.setText(str(len(self.skillBlist))+"개")

    def play1(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\1.mp3",)).start()

    def play2(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\2.mp3",)).start()

    def play3(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\3.mp3",)).start()

    def playmeso(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\meso.wav",)).start()

    def playbuff(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\buff.wav",)).start()

    def playstart(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\start.mp3",)).start()

    def playvioletta(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\violetta.mp3",)).start()

    def playrune(self):
        threading.Thread(target=playsound.playsound,args=(self.path + "resource\\rune.wav",)).start()

    def printing(self,string):
        self.printer.addItem(string)
        if self.printer.count()>14:
            self.printer.takeItem(0)
    def clickChecker(self):
        while(True):
            time.sleep(0.2)
            if self.clickcheck.isChecked()==True:
                time.sleep(8)
                x,y= imagesearch(self.path + 'resource\\maple.png', precision=0.8)
                mx,my= mouse.get_position()
                arrx=[80,250,420,590,760,930]
                arry=[90,180,270,360,450,540,630,700]
                for i in arrx[2:4]:
                    self.movenclick(i,90,x,y)
                for i in arrx[1:]:
                    self.movenclick(i,220,x,y)
                for i in arrx[1:]:
                    self.movenclick(i,350,x,y)
                for i in arrx:
                    self.movenclick(i,480,x,y)
                for i in arrx:
                    self.movenclick(i,610,x,y)
                time.sleep(1)

    def movenclick(self,x,y,ax,ay):
        if self.clickcheck.isChecked()==True:
            mouse.move(x+ax,y+ay)
            time.sleep(0.2)
            mouse.click()

    def clickCheckbox(self):
        while(True):
            mouse.wait('middle')
            self.clickcheck.toggle()
            time.sleep(0.25)
    def waiting(self):
        while (True):
            t = threading.Thread(target=self.roop)
            while (True):
                t = threading.Thread(target=self.roop)
                if keyboard.is_pressed('tab'):
                    self.recordHotkeyCheck.toggle()
                    time.sleep(0.25)
                if self.hotkeycheck.isChecked():
                    if self.recordmode==True:
                        if keyboard.is_pressed('-'):
                            if not t.is_alive():
                                if self.testCheck.isChecked()==True:
                                    t = threading.Thread(target=self.test)
                                    t.daemon=True
                                    t.start()
                                    self.mesoBtn.setEnabled(False)
                                    self.buffBtn.setEnabled(False)
                                    self.routineBtn.setEnabled(False)
                                    self.skillABtn.setEnabled(False)
                                    self.skillBBtn.setEnabled(False)
                                    t.join()
                                    self.mesoBtn.setEnabled(True)
                                    self.buffBtn.setEnabled(True)
                                    self.routineBtn.setEnabled(True)
                                    self.skillABtn.setEnabled(True)
                                    self.skillBBtn.setEnabled(True)
                                    time.sleep(0.3)
                                    t = threading.Thread(target=self.roop)
                    if self.recordmode==False:
                        if keyboard.is_pressed('-'):
                            if not t.is_alive():
                                t.daemon=True
                                t.start()
                                self.mesoBtn.setEnabled(False)
                                self.buffBtn.setEnabled(False)
                                self.routineBtn.setEnabled(False)
                                self.skillABtn.setEnabled(False)
                                self.skillBBtn.setEnabled(False)
                                t.join()
                                self.mesoBtn.setEnabled(True)
                                self.buffBtn.setEnabled(True)
                                self.routineBtn.setEnabled(True)
                                self.skillABtn.setEnabled(True)
                                self.skillBBtn.setEnabled(True)
                                self.printing("[system] 루프가 종료되었습니다.")
                                time.sleep(0.3)

    def skillA(self):
        if len(self.skillAlist)==0:
            self.printing("[Warning] 녹화된 스킬A 패턴이 존재하지 않습니다.")
            return False
        randomNum = random.randint(0, len(self.skillAlist) - 1)
        delay = random.uniform(0.93, 1.0)
        self.printing('┌ 스킬A 패턴 실행 : 패턴번호> skillA ' + str(randomNum))
        ret=keyboard.play(self.skillAlist[randomNum], stop='-', speed_factor=round(delay, 3))
        self.printing('└ 스킬A 패턴 종료')
        return ret

    def skillB(self):
        if len(self.skillBlist)==0:
            self.printing("[Warning] 녹화된 스킬B 패턴이 존재하지 않습니다.")
            return False
        randomNum = random.sample(self.skillBlist.keys(),1)[0]
        delay = random.uniform(0.93, 1.0)
        self.printing('┌ 스킬B 패턴 실행 : 패턴번호> skillA ' + str(randomNum))
        ret=keyboard.play(self.skillBlist[randomNum], stop='-', speed_factor=round(delay, 3))
        self.printing('└ 스킬B 패턴 종료')
        return ret

    def routine(self):
        if len(self.routinelist)==0:
            self.printing("[Warning] 녹화된 일반 패턴이 존재하지 않습니다.")
            return False
        randomNum = random.sample(self.routinelist.keys(),1)[0]
        self.printing('┌ 일반패턴 실행 : 패턴번호> routine ' + str(randomNum))
        delay = random.uniform(0.93, 1.0)
        ret=keyboard.play(self.routinelist[randomNum], stop='-', speed_factor=round(delay, 3))
        self.printing('└ 일반패턴 종료')
        return ret

    def buff(self):
        if len(self.bufflist)==0:
            self.printing("[Warning] 녹화된 버프 패턴이 존재하지 않습니다.")
            return False
        randomNum = random.sample(self.bufflist.keys(),1)[0]
        self.printing('┌ 버프패턴 실행 : 패턴번호> buff ' + str(randomNum))
        delay = random.uniform(0.93, 1.0)
        ret=keyboard.play(self.bufflist[randomNum], stop='-', speed_factor=round(delay, 3))
        self.printing('└ 버프패턴 종료')
        return ret

    def meso(self):
        if len(self.mesolist)==0:
            self.printing("[Warning] 녹화된 메소회수 패턴이 존재하지 않습니다.")
            return False
        randomNum = random.sample(self.mesolist.keys(),1)[0]
        self.printing('┌ 회수패턴 실행 : 패턴번호> meso ' + str(randomNum))
        delay = random.uniform(0.93, 1.0)
        ret=keyboard.play(self.mesolist[randomNum], stop='-', speed_factor=round(delay, 3))
        time.sleep(0.4)
        self.printing('└ 회수패턴 종료')
        return ret
    stopFlag=True
    def stopcheck(self):
        while(True):
            if keyboard.is_pressed('-'):
                self.stopFlag=True
                break

    def roop(self):
        self.play3()
        self.stateimg("running")
        self.printing("[system] 루프가 시작되었습니다.")
        time.sleep(0.5)
        self.stopFlag=False
        threading.Thread(target=self.stopcheck).start()
        while (True):
            if self.stopFlag: break
            p1 = imagesearch(self.mesoimage)
            if self.stopFlag: break
            p2 = imagesearch(self.buffimage)
            if self.stopFlag: break
            p3 = imagesearch(self.skillAimage)
            if self.stopFlag: break
            p4 = imagesearch(self.skillBimage)
            if self.stopFlag: break
            time.sleep(round(random.uniform(0.38, 0.49), 2))
            if p2[0] != -1:
                self.playbuff()
                if (self.buff()):
                    continue
                break
            if p1[0] != -1:
                self.playmeso()
                if (self.meso()):
                    continue
                break
            if p3[0] != -1:
                if (self.skillA()):
                    continue
                break
            if p4[0] != -1:
                if (self.skillB()):
                    continue
                break
            if (self.routine()):
                continue
            break

        if keyboard.is_pressed('up'):
            keyboard.release('up')
        if keyboard.is_pressed('down'):
            keyboard.release('down')
        if keyboard.is_pressed('left'):
            keyboard.release('left')
        if keyboard.is_pressed('right'):
            keyboard.release('right')
        self.play1()
        self.stateimg("stop")
        return

    def checker(self):
        while (True):
            time.sleep(0.2)
            if self.violcheck.isChecked():
                if imagesearch(self.path + 'resource\\violetta.png', precision=0.8)[0] != -1:
                    self.printing(" - [!] 비올레타가 감지되었습니다.")
                    if self.stopFlag==False:
                        self.printing(" - 루프를 자동으로 종료합니다.")
                        self.stopFlag = True
                        keyboard.stopFlag=True
                    self.stateimg("viol")
                    self.playvioletta()
                    time.sleep(2)
                    continue
            if self.clickcheck.isChecked():
                if imagesearch(self.path + 'resource\\click.png', precision=0.8)[0] != -1:
                    self.printing(" - [!] 거짓말탐지기가 감지되었습니다.")
                    if self.stopFlag==False:
                        self.printing(" - 루프를 자동으로 종료합니다.")
                        self.stopFlag = True
                        keyboard.stopFlag=True
                    self.stateimg("viol")
                    self.playvioletta()
                    time.sleep(2)
                    continue
            if imagesearch(self.path + 'resource\\change.png', precision=0.98)[0] != -1:
                if self.stopFlag == False:
                    self.printing(" - [!] 맵이동 혹은 화면전환이 감지되었습니다.")
                    self.printing(" - 루프를 자동으로 종료합니다.")
                    self.stopFlag = True
                    keyboard.stopFlag=True
                    self.playvioletta()
                    time.sleep(2)
                    continue
            if self.runecheck.isChecked():
                if self.stopFlag == False:
                    if imagesearch(self.path + 'resource\\rune.png', precision=0.9)[0] != -1:
                        self.printing(" - [!] 룬이 감지되었습니다.")
                        self.printing(" - 루프를 자동으로 종료합니다.")
                        self.stopFlag = True
                        keyboard.stopFlag=True
                        self.stateimg("rune")
                        self.playrune()
                        time.sleep(2)
                        continue
            self.stateimg(self.curstate)
if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    Window = Form()
    Window.show()
    app.exec_()