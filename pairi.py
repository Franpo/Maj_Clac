from maj import *
from maj_input import *
from collections import defaultdict
import time

#所有牌的编码，固定内容
maj_list = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,31,32,33,34,35,36,37]
yaocyu_list = [1,9,11,19,21,29,31,32,33,34,35,36,37]
tsu_list = [31,32,33,34,35,36,37]
ryu_list = [12,13,14,16,18,36]
#1-9m  11-19s 21-29p 31-34东南西北 35-37中发白

maj = "666789m4478s2349p"
print(maj)



class Pairi_Calc:
    
    def Create_Zone(maj):
        maj_zone = []
        for num in maj:
            if num in [1,11,21]:
                maj_zone.append(num)
                maj_zone.append(num+1)
                maj_zone.append(num+2)
            elif num in [9,19,29]:
                maj_zone.append(num)
                maj_zone.append(num-1)
                maj_zone.append(num-2)
            elif num in [2,12,22]:
                maj_zone.append(num)
                maj_zone.append(num-1)
                maj_zone.append(num+1)
                maj_zone.append(num+2)
            elif num in [8,18,28]:
                maj_zone.append(num)
                maj_zone.append(num+1)
                maj_zone.append(num-1)
                maj_zone.append(num-2)
            elif num in [31,32,33,34,35,36,37]:
                maj_zone.append(num)
            else:
                maj_zone.append(num)
                maj_zone.append(num+1)
                maj_zone.append(num+2)
                maj_zone.append(num-1)
                maj_zone.append(num-2)
        maj_zone = list(set(maj_zone))
        return maj_zone


    def Count_Mentsu(maj,maj_calced):
        lenth = len(maj)
        mentsu = 0
        if lenth >= 3:
            for num in range(0,lenth-2):
                if num not in maj_calced:
                    if maj[num] == maj[num+1] and maj[num] == maj[num+2] and num not in maj_calced:
                            maj_calced.append(num)
                            maj_calced.append(num+1)
                            maj_calced.append(num+2)
                            mentsu +=1

                    elif lenth >=5 and maj[num] not in tsu_list and maj[num] not in [9,19,29]:
                        qian = True
                        for numy in range(num+1,lenth):
                            if maj[num] +1 == maj[numy] and numy not in maj_calced:
                                qian = False
                                break
                        if qian == True:
                            #z为跳张，使13456类牌型变为13+456
                            over = False
                            for numz in range(num+1,lenth):
                                if over == True:
                                    break
                                if maj[num] +2 == maj[numz] and numz not in maj_calced:
                                    for numa in range(numz+1,lenth):
                                        if over == True:
                                            break
                                        if maj[numz] +1 == maj[numa] and numa not in maj_calced:
                                            for numb in range(numa+1,lenth):
                                                if over == True:
                                                    break
                                                if maj[numa] +1 == maj[numb] and numb not in maj_calced:
                                                    for numc in range(numb+1,lenth):
                                                        if maj[numb] +1 == maj[numc] and numc not in maj_calced:
                                                            maj_calced.append(numa)
                                                            maj_calced.append(numb)
                                                            maj_calced.append(numc)
                                                            mentsu += 1
                                                            over = True
                                                            break
                    over = False
                    for numy in range(num+1,lenth):
                        if over == True:
                            break
                        if maj[num]+1 == maj[numy] and num not in maj_calced and numy not in maj_calced and maj[num] not in tsu_list and maj[numy] not in tsu_list:
                            for numz in range(numy+1,lenth):
                                if maj[numy]+1 ==maj[numz] and numz not in maj_calced and maj[numz] not in tsu_list:
                                    maj_calced.append(num)
                                    maj_calced.append(numy)
                                    maj_calced.append(numz)
                                    mentsu += 1
                                    over = True
                                    break
        return mentsu,maj_calced


    def Count_Tatsu(maj,maj_calced,jyan):
        lenth = len(maj)
        tatsu = 0
        if lenth >= 2:
            for num in range(0,lenth-1):
                for numy in range(num+1,lenth):
                    if jyan == 99:
                        if maj[num] == maj[numy] and num not in maj_calced and numy not in maj_calced:
                            maj_calced.append(num)
                            maj_calced.append(numy)
                            tatsu += 1
                            break                              
                    else:
                        if maj[num] == maj[numy] and num not in maj_calced and numy not in maj_calced and maj[num] != maj[jyan]:
                            maj_calced.append(num)
                            maj_calced.append(numy)
                            tatsu += 1
                            break                       
                for numy in range(num+1,lenth):
                    if maj[num]+1 == maj[numy] and num not in maj_calced and numy not in maj_calced and maj[num] not in tsu_list:
                        maj_calced.append(num)
                        maj_calced.append(numy)
                        tatsu += 1
                        break
                for numy in range(num+1,lenth):
                    if maj[num]+2 == maj[numy] and maj[num] not in [9,19,29] and num not in maj_calced and numy not in maj_calced and maj[num] not in tsu_list:
                        maj_calced.append(num)
                        maj_calced.append(numy)
                        tatsu += 1
                        break
        return tatsu,maj_calced
                
    def Syantei_Calc_7tai(maj):
        if len(maj) != 14:
            syantei = 99
        else:
            maj = Dazi_Calc.Tenpai_Arrange(maj)
            jyan = Dazi_Calc.Maj_GetJyan(maj)
            syantei = 7 - len(jyan) - 1
        return syantei
    
    def Syantei_Calc_Kokushi(maj):
        if len(maj) != 14:
            syantei = 99
        else:
            maj = Dazi_Calc.Maj_GetL(maj)
            maj = Dazi_Calc.Tenpai_Arrange(maj)
            maj_one = list(set(maj))
            jyan = Dazi_Calc.Maj_GetJyan(maj)
            if jyan != []:
                syantei = 13 - len(maj_one) - 1
            else:
                syantei = 13 - len(maj_one)
        return syantei
    
    def Syantei_Calc(maj):
        maj = Dazi_Calc.Tenpai_Arrange(maj)
        lenth = len(maj)
        n = 99
        if lenth == 14:
            n = 4
        elif lenth == 11:
            n = 3
        elif lenth == 8:
            n = 2
        elif lenth == 5:
            n = 1
        elif lenth == 2:
            n = 0
        jyan = Dazi_Calc.Maj_GetJyan(maj)
        Syantei =99
        if n !=99:
            if jyan != []:
                mentsu = 0
                tatsu = 0
                maj_calced = []
                jyan_num = None
                #穷举雀头，判断面子搭子数量
                for jyan_num_temp in jyan:
                    maj_calced_temp = []
                    mentsu_temp = 0
                    maj_calced_temp.append(jyan_num_temp)
                    maj_calced_temp.append(jyan_num_temp+1)
                    mentsu_output = Pairi_Calc.Count_Mentsu(maj,maj_calced_temp)
                    mentsu_temp = mentsu_output[0]
                    maj_calced_temp = mentsu_output[1]
                    if mentsu_temp > mentsu:
                        mentsu = mentsu_temp
                        jyan_num = jyan_num_temp
                        tatsu_output = Pairi_Calc.Count_Tatsu(maj,maj_calced_temp,jyan_num_temp)
                        tatsu_temp = tatsu_output[0]
                        maj_calced_temp = tatsu_output[1]
                        tatsu = tatsu_temp
                        maj_calced = maj_calced_temp
                    elif mentsu_temp == mentsu:
                        mentsu = mentsu_temp
                        jyan_num = jyan_num_temp
                        tatsu_output = Pairi_Calc.Count_Tatsu(maj,maj_calced_temp,jyan_num_temp)
                        tatsu_temp = tatsu_output[0]
                        maj_calced_temp = tatsu_output[1]
                        if tatsu_temp > tatsu:
                            tatsu = tatsu_temp
                            maj_calced = maj_calced_temp
                #搭子数量超过n-面子数会溢出
                tatsu = min(n-mentsu,tatsu)
                Syantei_jyan = 2*n - 2*mentsu - tatsu -1
                #假定无雀头，判断单钓雀头的向听数
                mentsu_nojyan = 0
                tatsu_nojyan = 0
                maj_calced_nojyan = []
                mentsu_output = Pairi_Calc.Count_Mentsu(maj,maj_calced_nojyan)
                mentsu_nojyan = mentsu_output[0]
                maj_calced_nojyan = mentsu_output[1]
                tatsu_output = Pairi_Calc.Count_Tatsu(maj,maj_calced_nojyan,99)
                tatsu_nojyan = tatsu_output[0]
                maj_calced_nojyan = tatsu_output[1]
                tatsu_nojyan = min(n-mentsu_nojyan,tatsu_nojyan)
                #判断4型听牌溢出（4444 8888为一向听）
                overcount = False
                if len(maj) - len(maj_calced_nojyan) == 2 and len(maj) >= 8:
                    maj_temp = []
                    maj_temp += maj
                    for num in maj_calced_nojyan:
                        maj_temp[num] = 99
                    maj_temp = [num for num in maj_temp if num != 99]
                    pai_4 = []
                    for num in range(0,len(maj)-3):
                        if maj[num] == maj[num+3]:
                            pai_4.append(maj[num])
                    overcount = True
                    for num in maj_temp:
                        if num not in pai_4:
                            overcount = False
                            break
                Syantei_nojyan = 2*n - 2*mentsu_nojyan - tatsu_nojyan
                if overcount == True:
                    Syantei_nojyan += 1
                Syantei = min(Syantei_jyan,Syantei_nojyan)
            else:
                mentsu = 0
                tatsu = 0
                maj_calced = []
                mentsu_output = Pairi_Calc.Count_Mentsu(maj,maj_calced)
                mentsu = mentsu_output[0]
                maj_calced = mentsu_output[1]
                tatsu_output = Pairi_Calc.Count_Tatsu(maj,maj_calced,99)
                tatsu = tatsu_output[0]
                maj_calced = tatsu_output[1]
                tatsu = min(n-mentsu,tatsu)
                Syantei = 2*n - 2*mentsu - tatsu                   
        else:
            Syantei = 99
        return Syantei
        
    def Moche_Calc(maj):
        maj_zone = []
        maj_zone += maj_list
        #有问题，放弃使用区域法
        #maj_zone = Pairi_Calc.Create_Zone(maj)
        lenth = len(maj)
        #防止进第五张牌
        if lenth >=4:
            for num in range(0,lenth-3):
                if maj[num] == maj[num+3]:
                    maj_zone.remove(maj[num])
        syantei_7tai = Pairi_Calc.Syantei_Calc_7tai(maj)
        syantei_normal = Pairi_Calc.Syantei_Calc(maj)
        syantei_kokushi = Pairi_Calc.Syantei_Calc_Kokushi(maj)
        syantei_all = min(syantei_7tai,syantei_normal,syantei_kokushi)
        list_num = 0
        maj_removed = []
        moche_list = {}
        for numx in maj:
            maj_temp = []
            maj_temp += maj
            if numx not in maj_removed:
                maj_temp.remove(numx)
                maj_removed.append(numx)
                for numy in maj_zone:
                    maj_temp_2 = []
                    maj_temp_2 += maj_temp
                    maj_temp_2.append(numy)
                    syantei_7tai_new = Pairi_Calc.Syantei_Calc_7tai(maj_temp_2)
                    syantei_kokushi_new = Pairi_Calc.Syantei_Calc_Kokushi(maj_temp_2)
                    syantei_normal_new = Pairi_Calc.Syantei_Calc(maj_temp_2)
                    syantei_all_new = min(syantei_7tai_new,syantei_normal_new,syantei_kokushi_new)
                    if syantei_all_new < syantei_all:
                        moche_list[list_num] = [numx,numy]
                        list_num +=1
        #整理字典
        moche_list_refine = defaultdict(list) 
        for num in range(0,list_num):
            list_temp = moche_list[num]
            moche_list_refine[list_temp[0]].append(list_temp[1])
        return syantei_all,syantei_normal,syantei_7tai,syantei_kokushi,moche_list_refine
                    
    def Moche_Convert(maj):
        result = ""
        m = re.findall("\d+(?=m)", maj)
        m_all = ""
        for num in m:
            m_all += str(num)
        s = re.findall("\d+(?=s)", maj)
        s_all = ""
        for num in s:
            s_all += str(num)        
        p = re.findall("\d+(?=p)", maj)
        p_all = ""
        for num in p:
            p_all += str(num)
        z = re.findall("东|南|西|北|中|发|白", maj)          
        m = list(m_all)
        s = list(s_all)
        p = list(p_all)
        raw_maj = []
        for num in m:
            if num != "0":
                raw_maj.append(int(num))
        for num in s:
            if num != "0":
                raw_maj.append(int(num)+10)
        for num in p:
            if num != "0":
                raw_maj.append(int(num)+20)
        for num in z:
            if num == "东":
                raw_maj.append(31)
            if num == "南":
                raw_maj.append(32)
            if num == "西":
                raw_maj.append(33)
            if num == "北":
                raw_maj.append(34)
            if num == "中":
                raw_maj.append(35)
            if num == "发":
                raw_maj.append(36)
            if num == "白":
                raw_maj.append(37)
        raw_maj = Dazi_Calc.Tenpai_Arrange(raw_maj)
        lenth = len(raw_maj)
        if lenth not in [2,5,8,11,14]:
            result += "输入的牌数量，输入牌需满足(3n+2)条件。"
        for num in range(0,lenth-4):
            if raw_maj[num] == raw_maj[num+4]:
                result += "您的牌型中包含大量重复牌，系统提醒您，文明麻将，请勿印牌。"
                break
        moche_info = Pairi_Calc.Moche_Calc(raw_maj)
        kiru = moche_info[4]
        syantei_all = moche_info[0]
        syantei_normal = moche_info[1]
        syantei_7tai = moche_info[2]
        syantei_kokushi = moche_info[3]
        if result == "":
            if not kiru:
                result = "这副牌已经是和了型了。"
            else:
                if syantei_all == 0:
                    result += "听牌：\n"
                else:
                    result += "最小" + str(syantei_all) + "向听，一般型" + str(syantei_normal) +"向听"
                    if syantei_7tai <= syantei_normal:
                        result += "，七对" + str(syantei_7tai) + "向听"
                    if syantei_kokushi < 6:
                        result += "国士无双" +str(syantei_kokushi) +"向听"
                    result += "\n"
                for num in kiru:
                    remain = 0
                    result += "切"
                    char = Maj_Convert.Output(num)
                    result += char
                    result += " ，进："
                    for pai in kiru[num]:
                        remain += Dazi_Calc.Check_Remain(raw_maj,pai)
                        charpai = Maj_Convert.Output(pai)
                        result += charpai
                        result += " "
                    result += "共计" + str(remain) + "张。" + "\n"
        return result
        
start = time.clock()
moche = Pairi_Calc.Moche_Convert(maj)
print(moche)


                              
elapsed = (time.clock() - start)
print("用时",elapsed)
        




