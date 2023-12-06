import os
import time
import pyautogui as pi
import cv2
import pytesseract as py
import re
import colorama
from colorama import Fore, Back, Style
from pytesseract.pytesseract import TesseractError
from float import float, getcontext

getcontext().prec = 5

py.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config_py = '-c CONFIGVAR=VALUE --dpi 600 --psm 6 --oem 3'

path_output = 'env/output/'
path_csv = 'csv/'

colorama.init()

def _printRegion(path, tipo, img, ext, x, y, w, h):
    try:
        # imagem_tipo = (path+tipo+img, np.uint8)[0]
        param1 = w-x
        param2 = h-y
        pi.screenshot(path+tipo+img+ext, region=(x, y,
                      param1, param2))  # x, y, w, h
        # Otsu's thresholding after Gaussian filtering
        imagem = cv2.imread(path+tipo+img+ext)
        # hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

        # rows, cols = imagem.shape[:2]

        # Gaussian blur#######################################################
        blur = cv2.GaussianBlur(imagem, (3,3), 3, (3,3), cv2.BORDER_CONSTANT)
        sharpen = cv2.addWeighted(imagem, .6, blur, .3, 0)

        imagem_gray = cv2.cvtColor(sharpen, cv2.COLOR_BGR2GRAY)  # aplica gray
        # cv2.imwrite(path+'gray
        _, hold1 = cv2.threshold(
            imagem_gray, 125, 255, cv2.THRESH_BINARY_INV)            
        cv2.imwrite(path+'hold1_'+img+ext, hold1)

        # gray = cv2.bitwise_not(hold1)
        # cv2.imwrite(path+'gray_'+img+ext, gray)
        # hold2 = cv2.adaptiveThreshold(
        #     gray2, 255, cv2.BORDER_CONSTANT, cv2.THRESH_BINARY, 5, 10, 5)
        # cv2.imwrite(path+'hold2_'+img+ext, hold2)

        hold2 = cv2.adaptiveThreshold(
            hold1, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 25, 5)
        cv2.imwrite(path+'hold2_'+img+ext, hold2)

    except TesseractError as error:
        print(f'PYTESSERACT ERROR - {img}')
############################################


def _readDataImage(path, tipo, img, ext):

    imagem = cv2.imread(path+tipo+img+ext)
    stringfile = py.image_to_string(imagem, config=config_py)
    # print(stringfile)
    priceRs = stringfile.splitlines()
    # print(priceRs)
    
    return_data = []     

    # removing all '' elements
    for elem in priceRs:
        if elem != '':
            return_data.append(elem)
            # print(f'REMOVED {img} >>> {elem}')
      
    # print(f'DATA: {return_data}')        

    # permitir:
    # 0 a 9 = \u0030-\u0039
    # ',', '.', '-' = \u002C, \u002E, \u002D
    # regex = re.compile(r'[0-9,.-]+')
    regex = re.compile('[\u0030-\u0039\u002C\u002E]')
    data = []

    for p in return_data:  

        try:
            # reg = re.search(regex, p)
            # print(f'-------- ELEMENT {p} --------')  
            # print(f'LEITURA REGEX: {reg.span()[0]}')
            # print(f'LEITURA {img} = {p}')
            if p == '0,00':
                continue
            else: 
                # print(f'LEITURA = {p}')
                p = p.replace(',', '.').replace('.','') # this case for float number
                data.append(int(p)/100)

        except TypeError as error:   
            print(f'-------- ELEMENT {p} --------')                           
            print(f'{Back.LIGHTRED_EX}{Fore.WHITE}----- "TypeError" {img} - {error} -----')
            return False
        except ValueError as error:  
            print(f'-------- ELEMENT {p} --------')                             
            print(f'{Back.LIGHTYELLOW_EX}{Fore.WHITE}----- "ValueError" {img} - {error} -----')
            return False
        except AttributeError as error: 
            print(f'-------- ELEMENT {p} --------')                              
            print(f'{Back.LIGHTBLUE_EX}{Fore.WHITE}----- "AttributeError" {img} - {error} -----')
            return False
        except None as error:         
            print(f'-------- ELEMENT {p} --------')                     
            print(f'{Back.LIGHTRED_EX}{Fore.WHITE}----- "None" {img} - {error} -----')
            return False

    #time.sleep(1)

    # print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}DATA: {data}')
    return data
############################################


def _readDataList(path, tipo, img, ext):

    imagem = cv2.imread(path+tipo+img+ext)
    stringfile = py.image_to_string(imagem, config=config_py)
    # print(stringfile)
    priceRs = stringfile.splitlines()
    # print(priceRs)
    
    return_data = []     

    # removing all '' elements
    for elem in priceRs:
        if elem != '':
            return_data.append(elem)
            # print(f'REMOVED {img} >>> {elem}')
      
    # print(f'DATA: {return_data}')        

    # permitir:
    # 0 a 9 = \u0030-\u0039
    # ',', '.', '-' = \u002C, \u002E, \u002D
    # regex = re.compile(r'[0-9,.-]+')
    regex = re.compile('[\u0030-\u0039\u002C\u002E]')
    data = []

    for p in return_data:  

        try:
            # reg = re.search(regex, p)
            # print(f'-------- ELEMENT {p} --------')  
            # print(f'LEITURA REGEX: {reg.span()[0]}')
            # print(f'LEITURA {img} = {p}'
            if p == 'cé': p ='C6'
            if p == 'Nulnvest': p = 'NUINVEST'
            if p == 'Nulnvest': p = 'NUINVEST'
            if p == 'Tullete': p = 'TULLETT'
            if p == '(P' or p == 'XP.': p = 'XP'
            p = str.upper(p)
            data.append(p)
            # print(f'LEITURA = {p}')
        except TypeError as error: 
            print(f'-------- ELEMENT {p} --------')                              
            print(f'{Back.LIGHTYELLOW_EX}{Fore.WHITE}----- "TypeError" {img} - {error} -----')
            return False
        except ValueError as error:  
            print(f'-------- ELEMENT {p} --------')                             
            print(f'{Back.LIGHTYELLOW_EX}{Fore.WHITE}----- "ValueError" {img} - {error} -----')
            return False
        except AttributeError as error:    
            print(f'-------- ELEMENT {p} --------')                           
            print(f'{Back.LIGHTBLUE_EX}{Fore.WHITE}----- "AttributeError" {img} - {error} -----')
            return False
        except None as error:     
            print(f'-------- ELEMENT {p} --------')                         
            print(f'{Back.LIGHTRED_EX}{Fore.WHITE}----- "None" {img} - {error} -----')
            return False

    #time.sleep(1)

    # print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}DATA: {data}')
    return data
############################################



if __name__ == '__main__':

    #_____CONTROLES_____
    #___________________
    loop = True
    #___________________
    readData = True
    #___________________
    just_readAjuste = False
    #___________________
    calculateMediaAdj = True
    #___________________
    showResult = True
    #___________________

    coordsAdj_wdo = [174, 42, 308, 1015]
    coordsAdj_dolar = [482, 42, 602, 1015]

    #_____ALTERAR SEMPRE ABERTURA DO MERCADO____________
    day = '17 / 02 / 23'
    demonstrativo = {}

    pr8_ajuste = 0
    pr11_ajuste = 0
    maximo8 = 0
    minimo8 = 0
    maximo11 = 0
    minimo11 = 0
    pr8_ajuste = 0 # ponto de referência        
    pr11_ajuste = 0 # ponto de referência
    
    while loop:

        total_ajustes = 0
        countOfTimes = 0

        ###########################################################################
        # Setor: leitura da lista dos ajustes para calcular o Indice de Ajuste
        ###########################################################################
        if just_readAjuste:
            _printRegion(path_output, 'color_', 'ajustes', '.png',
                        coordsAdj_dolar[0], coordsAdj_dolar[1], coordsAdj_dolar[2], coordsAdj_dolar[3])
        else:
            _printRegion(path_output, 'color_', 'ajustes', '.png',
                        coordsAdj_dolar[0], coordsAdj_dolar[1], coordsAdj_dolar[2], coordsAdj_dolar[3])

            ajustes = (_readDataImage(path_output, 'hold2_',
                                    'ajustes', '.png'))                                    
            # print(f'{Back.LIGHTYELLOW_EX}{Fore.BLACK}Ajustes = {ajustes}')

            ordem_ativo = 0
            if ajustes != False:
                if ajustes == []:                               
                    print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}-----AJUSTES SEM DATA-----')
                else:
                    if calculateMediaAdj:
                        # print(f'Wdo >>> {wdo}')
                        for w in ajustes:
                            # print(f'w >>> {w}')
                            total_ajustes += float(w)
                            #___________________________________
                            demonstrativo[ordem_ativo] = float(w)
                            # print(f'Total_ajustes: {total_ajustes}')
                            ordem_ativo += 1
                            
                        demonstrativo["total_ajustes"] = float(total_ajustes)                        
                        pr8_ajuste = float(demonstrativo["total_ajustes"]/8)
                        pr11_ajuste = float(demonstrativo["total_ajustes"]/11)

                        if not pr8_ajuste or not pr11_ajuste:
                            print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}-----pr8_ajuste / pr11_ajuste NO OPERATION-----')
                            continue
                        else:
                            if maximo8 == 0 and maximo11 == 0:
                                maximo8 = pr8_ajuste
                                maximo11 = pr11_ajuste
                            if minimo8 == 0 and minimo11 == 0:
                                minimo8 = pr8_ajuste
                                minimo11 = pr11_ajuste
                            if pr8_ajuste < maximo8:
                                maximo8 = pr8_ajuste
                            if pr8_ajuste > maximo8 and pr8_ajuste > minimo8:
                                minimo8 = pr8_ajuste
                            if pr11_ajuste < maximo11:
                                maximo11 = pr11_ajuste
                            if pr11_ajuste > maximo11 and pr11_ajuste > minimo11:
                                minimo11 = pr11_ajuste

                            demonstrativo['maximo8'] = maximo8
                            demonstrativo['minimo8'] = minimo8
                            demonstrativo['maximo11'] = maximo11
                            demonstrativo['minimo11'] = minimo11
                            demonstrativo['pr8_ajuste'] = pr8_ajuste
                            demonstrativo['pr11_ajuste'] = pr11_ajuste
                            
                        print(f'{Back.BLACK}{Fore.WHITE}________________________________________')
                        print(f'> > REPORT AJUSTES - {day}{Back.RESET}{Fore.BLACK}')
                        for ord, value in enumerate(ajustes):
                            if ord >= 0 and ord < 10:
                                print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK} {ord+1}  >>\t{value}')
                            else:
                                print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK} {ord+1} >> \t{value}')
                            ordem_ativo += 1
                    else:                        
                        print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}-----CALCULATE AJUSTE - FALSE-----')
        # end if just_readAjuste


        if showResult:
            print(f'{Back.BLACK}{Fore.WHITE}________________________________________')
            print(f'> > REPORT P.R. - {day}\t{countOfTimes}')
            print(f'> TOTAL AJUSTES|\t{Back.RED}{Fore.BLACK}{demonstrativo["total_ajustes"]}{Back.RESET}{Fore.BLACK}')
            print(f'\tVALUE PR(p)\tMAX(%)\tMIN(%)')
            if pr8_ajuste or pr11_ajuste:
                print(f'..PR_8___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["pr8_ajuste"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["maximo8"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["minimo8"]}{Back.RESET}{Fore.BLACK}')
                print(f'..PR11___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["pr11_ajuste"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["maximo11"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["minimo11"]}{Back.RESET}{Fore.BLACK}')
                print(f'..MEDIA__ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{(demonstrativo["pr8_ajuste"]+demonstrativo["pr11_ajuste"])/2}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{(demonstrativo["maximo8"]+demonstrativo["maximo11"])/2}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{(demonstrativo["minimo8"]+demonstrativo["minimo11"])/2}{Back.RESET}{Fore.BLACK}')
            else:
                print(f'..PR_8____ {Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V\t\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V{Back.MAGENTA}{Fore.BLACK}')
                print(f'..PR11____ {Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V\t\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V{Back.MAGENTA}{Fore.BLACK}')
                print(f'..MEDIA___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V\t\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}N/V{Back.MAGENTA}{Fore.BLACK}')
        # end if showResult()

        # Limpa o console no Windows
        # if os.name == 'nt':
        #    _ = os.system('cls')

        time.sleep(1)
        countOfTimes += 1
        # end if calcularDOL()
    # end while
# end main