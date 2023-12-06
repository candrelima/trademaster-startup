import time
import pyautogui as pi
import cv2
import pytesseract as py
import re
import colorama
from colorama import Fore, Back, Style
from pytesseract.pytesseract import TesseractError
from decimal import Decimal, getcontext

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

    #___________________
    loop = True
    replay = False
    #___________________
    readData = True
    just_readAjuste = False
    #___________________
    calculateMediaAdj = True
    calculateMedia = True
    #___________________
    readCorretoras = True
    calculateMediaLista = True
    calcularWDO = True
    calcularDOL = True
    #___________________
    showResult = True
    #___________________

    if replay:
        coordsAdj_dolar = [1745, 70, 1855, 937]
        coordsListMax = [1417, 80, 1591, 405]
        coordsListMin = [1417, 486, 1591, 811]
        coordsListMax_d = [1052, 80, 1236, 405]
        coordsListMin_d = [1052, 486, 1236, 811]
    else:
        coordsAdj_dolar = [1745, 70, 1855, 937]
        coordsListMax = [1417, 60, 1591, 385]
        coordsListMin = [1417, 466, 1591, 791]
        coordsListMax_d = [1052, 60, 1236, 385]
        coordsListMin_d = [1052, 466, 1236, 791]

    #_______WDO_____________
    mediaGeral = 0
    medias = []
    maximo8 = 0
    minimo8 = 0
    maximo11 = 0
    minimo11 = 0
    list_corretoras_max = []
    list_corretoras_min = []
    #_______DOL_____________
    mediaGeral_d = 0
    medias_d = []
    maximo8_d = 0
    minimo8_d = 0
    maximo11_d = 0
    minimo11_d = 0
    list_corretoras_max_d = []
    list_corretoras_min_d = []

    demonstrativo = {}
    demonstrativo_d = {}
    
    countOfTimes = 0

    # dados atrasado/inexistente: INTER, CLEAR, CITIGROUP = CITIBANK,
    # LIGA, MAXIMA, NECTON, RENASCENÇA, RICO, SOCOPA, SOLIDUS
    # TORO, VITREO, VOTORATIM, SICOOB
    ib_lista_distribuidoras = {
        'ACTIVTRADES': 55.84,
        'AGORA': 20.48,
        'ALFA': 14.1,
        'AMARIL': 35.66,
        'ATIVA': 11.98,
        'BANRISUL': 16.67,
        'BB': 16.72,
        'BGC LIQUIDEZ': 27.77,
        'BNP': 14.46,
        'BTG': 15.20,
        'BRADESCO': 15.82,
        'C6': 17.32,
        'CAPITAL': 14.28,
        'CITIGROUP': 15.4,
        'CLEAR': 18.9,
        'CODEPE': 115.59,
        'CREDIT': 18.94,
        'ELITE': 20.10,
        'FATOR': 25.45,
        'GENIAL': 11.09,
        'GERAL': 31.83,
        'GOLDMAN': 18.56,
        'GUIDE': -5.58,
        'H.COMMCOR': 24.62,
        'ICAP': 24.6,
        'IDEAL': 47.10,
        'INTER': 29.79,
        'INTL': 15.83,
        'ITAU': 14.72,
        'JP MORGAN': 16.06,
        'LEV': 18.86,
        'LIGA': 0,
        'MAXIMA': 11.7,
        'MERC.': 14.99,
        'MERRILL': 22.22,
        'MIRAE': 119.44,
        'MODAL': 13.60,
        'MORGAN': 23.66,
        'NECTON': 8.4,
        'NOVA FUTURA': 14.44,
        'NOVINVEST': 6.52,
        'NUINVEST': 21.6,
        'ORAMA': 11.75,
        'PLANNER': 6.86,
        'RB CAPITAL': 22.04,
        'RENASCENCA': 39.7,
        'RICO': 0,
        'SCOTIABANK': 27.66,
        'SAFRA': 12.36,
        'SANTANDER': 14.48,
        'SENSO': 47.83,
        'SICOOB': 0,
        'SICREDI': 16.13,
        'SITA': 57.84,
        'SOCOPA': 15.3,
        'SOLIDUS': 44.9,
        'TERRA': 20.81,
        'TORO': 25.6,
        'TULLETT': 24.04,
        'UBS': 30.29,
        'VITREO DTVMS.A': 44.8,
        'VOTORANTIM': 17.1,
        'WARREN': 10.18,
        'XP': 16.11
    }



    while loop:
        
        #_____ALTERAR SEMPRE ABERTURA DO MERCADO____________
        open_market = float('5215.0') 
        open_market_d = float('5211.5')
        day = '15 / 02 / 23'
        #_________OPEN_MARKET_DOL_______________
        demonstrativo_d['open_market_d'] = open_market_d        
        #_________OPEN_MARKET_WDO_______________
        demonstrativo['open_market'] = open_market
        #___________________________________________________
        loop = True





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

            ordem_ativo = 1
            if ajustes != False:
                if ajustes == []:                               
                    print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}-----AJUSTES SEM DATA-----')
                else:
                    if calculateMediaAdj:
                        # calc main
                        total_ajustes = 0
                        # print(f'Wdo >>> {wdo}')
                        for w in ajustes:
                            # print(f'w >>> {w}')
                            total_ajustes += float(w)
                            # print(f'Total_ajustes: {total_ajustes}')
                            
                        print(f'{Back.LIGHTWHITE_EX}{Fore.WHITE}________________________________________')
                        print(f'{Back.LIGHTWHITE_EX}{Fore.WHITE}>> RELAÇÃO DOS AJUSTES (pts)____________')
                        for x in ajustes:
                            if x >= 0:
                                print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}  {ordem_ativo} >>  {x}')
                            else:
                                print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}  {ordem_ativo} >> {x}')
                            ordem_ativo += 1
                        #___________________________________
                        demonstrativo['total_ajustes'] = total_ajustes
        # end if just_readAjuste





        #_____ACRESCENTAR "_d"__________
        # acrescentar _w ao final de todas as variáveis e argumentos
        # para diferenciar do if calcularDOL
        if calcularDOL:
            pr8_ajuste_d = 0
            pr11_ajuste_d = 0
            soma_alvo_max_d = 0
            media_alvo_max_d = 0
            razao_max_d = 0
            soma_alvo_min_d = 0
            media_alvo_min_d = 0
            razao_min_d = 0
            target_max_d = 0
            target_min_d = 0
            target_of_the_day_d = 0
            total_dist_max_d = 0
            total_dist_min_d = 0  

            # quantos distribuidores calcular
            max_dist_d = 10  
            
            #____INIT_RELATORIO_DOL_______________
            # 1___________________________________
            demonstrativo_d['maximo8_d'] = maximo8_d
            # 2___________________________________
            demonstrativo_d['minimo8_d'] = minimo8_d
            # 3___________________________________
            demonstrativo_d['maximo11_d'] = maximo11_d
            # 4___________________________________
            demonstrativo_d['minimo11_d'] = minimo11_d
            # 5___________________________________
            demonstrativo_d['pr8_ajuste_d'] = pr8_ajuste_d
            # 6___________________________________
            demonstrativo_d['pr11_ajuste_d'] = pr11_ajuste_d
            # 7_________SOMA_ALVO_MAX_D_____________
            demonstrativo_d['soma_alvo_max_d'] = soma_alvo_max_d
            # 8_________TOTAL_DIST_MAX_D____________
            demonstrativo_d['total_dist_max_d'] = total_dist_max_d
            # 9_________MEDIA_ALVO_MAX_D____________
            demonstrativo_d['media_alvo_max_d'] = media_alvo_max_d          
            # 10_________RAZAO_MAX_D_________________
            demonstrativo_d['razao_max_d'] = razao_max_d
            # 11_________TARGET_MAX_D________________
            demonstrativo_d['target_max_d'] = target_max_d       
            # 12_________SOMA_ALVO_MIN_D_____________
            demonstrativo_d['soma_alvo_min_d'] = soma_alvo_min_d
            # 13_________TOTAL_DIST_MIN_D____________
            demonstrativo_d['total_dist_min_d'] = total_dist_min_d
            # 14_________MEDIA_ALVO_MIN_D____________
            demonstrativo_d['media_alvo_min_d'] = media_alvo_min_d
            # 15__________RAZAO_MIN_D________________
            demonstrativo_d['razao_min_d'] = razao_min_d
            # 16_________TARGET_MIN_D________________
            demonstrativo_d['target_min_d'] = target_min_d
            # 17_________TARGET_OF_THE_DAY_D_________
            demonstrativo_d['target_of_the_day_d'] = target_of_the_day_d


            ###########################################################################
            # Setor: leitura da lista das corretoras para calcular o Indice de Basileia
            ###########################################################################
            if readCorretoras:
                _printRegion(path_output, 'color_', 'lista_max_d', '.png',
                            coordsListMax_d[0], coordsListMax_d[1], coordsListMax_d[2], coordsListMax_d[3])
                _printRegion(path_output, 'color_', 'lista_min_d', '.png',
                            coordsListMin_d[0], coordsListMin_d[1], coordsListMin_d[2], coordsListMin_d[3])

                lista_corretoras_min_d = (_readDataList(path_output, 'hold2_', 'lista_min_d', '.png'))              
                # print(f'{Back.LIGHTRED_EX}{Fore.BLACK}Lista Bear = {lista_corretoras_min_d}')

                lista_corretoras_max_d = (_readDataList(path_output, 'hold2_', 'lista_max_d', '.png'))              
                # print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}Lista Bull = {lista_corretoras_max_d}')

                if len(lista_corretoras_max_d) == 0:
                    print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}>> "DOL BULL MARKET" - NO DATA <<')
                if len(lista_corretoras_min_d) == 0:
                    print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}>> "DOL BEAR MARKET" - NO DATA <<')
                else:
                    if calculateMediaLista:
                        # exibindo distribuição BULL   
                        ordem = 1
                        if len(lista_corretoras_max_d) > 0:
                            for c in lista_corretoras_max_d:
                                if c not in ib_lista_distribuidoras:
                                    print(f'{Back.LIGHTWHITE_EX}{Fore.BLACK} < DOL MAX RECOGNIZED? {c} >')
                                    continue  
                                if total_dist_max_d == max_dist_d:
                                    break
                                for corretora, ib in ib_lista_distribuidoras.items():
                                    if c == corretora:
                                        if ib == 0:
                                            pass
                                            #print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}{ordem} - {corretora} = {ib}')
                                        else:
                                            soma_alvo_max_d += float(ib)
                                            total_dist_max_d += 1
                                            #print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}{ordem} - {corretora} = {ib}')
                                #print(f'{Back.MAGENTA}{Fore.WHITE}>>> TOTAL DISTRIBUIDORAS: {len(lista_corretoras_max_d)}')
                                ordem += 1
                            media_alvo_max_d = float(soma_alvo_max_d / float(total_dist_max_d))
                            razao_max_d = float(((open_market_d * media_alvo_max_d) / 100) / 10)

                        # exibindo distribuição BEAR
                        if len(lista_corretoras_min_d) > 0:
                            ordem = 1
                            for c in lista_corretoras_min_d:
                                if c not in ib_lista_distribuidoras:
                                    print(f'{Back.LIGHTWHITE_EX}{Fore.BLACK} < DOL MIN RECOGNIZED? {c} >')
                                    continue  
                                if total_dist_min_d == max_dist_d:
                                    break
                                for corretora, ib in ib_lista_distribuidoras.items():
                                    if c == corretora:
                                        if ib == 0:
                                            pass
                                            #print(f'{Back.LIGHTRED_EX}{Fore.WHITE}{ordem} - {corretora} = {ib}')
                                        else:
                                            soma_alvo_min_d += float(ib)
                                            total_dist_min_d += 1
                                            #print(f'{Back.LIGHTRED_EX}{Fore.WHITE}{ordem} - {corretora} = {ib}') 
                                #print(f'{Back.MAGENTA}{Fore.WHITE}>>> TOTAL DISTRIBUIDORAS: {len(lista_corretoras_min_d)}')
                                ordem += 1

                            media_alvo_min_d = float(soma_alvo_min_d / float(total_dist_min_d))
                            razao_min_d = float(((open_market_d * media_alvo_min_d) / 100) / 10)                    

                        if (soma_alvo_max_d >= soma_alvo_min_d):
                            target_max_d = float(open_market_d + razao_max_d)
                            target_max_d = float((open_market_d + target_max_d) / 2)
                        else:
                            target_min_d = float(open_market_d - razao_min_d)
                            target_min_d = float((open_market_d + target_min_d) / 2)

                        target_of_the_day_d = float((target_max_d + target_min_d))
                    
                        pr8_ajuste_d = float(demonstrativo['total_ajustes']/8)
                        pr11_ajuste_d = float(demonstrativo['total_ajustes']/11)

                        if maximo8_d == 0 and maximo11_d == 0:
                            maximo8_d = pr8_ajuste_d
                            maximo11_d = pr11_ajuste_d
                        if minimo8_d == 0 and minimo11_d == 0:
                            minimo8_d = pr8_ajuste_d
                            minimo11_d = pr11_ajuste_d

                        if pr8_ajuste_d < maximo8_d:
                            maximo8_d = pr8_ajuste_d
                        if pr8_ajuste_d > maximo8_d and pr8_ajuste_d > minimo8_d:
                            minimo8_d = pr8_ajuste_d

                        if pr11_ajuste_d < maximo11_d:
                            maximo11_d = pr11_ajuste_d
                        if pr11_ajuste_d > maximo11_d and pr11_ajuste_d > minimo11_d:
                            minimo11_d = pr11_ajuste_d  

                        #_________RELATORIO_DOL_______________
                        # 1___________________________________
                        demonstrativo_d['maximo8_d'] = maximo8_d
                        # 2___________________________________
                        demonstrativo_d['minimo8_d'] = minimo8_d
                        # 3___________________________________
                        demonstrativo_d['maximo11_d'] = maximo11_d
                        # 4___________________________________
                        demonstrativo_d['minimo11_d'] = minimo11_d
                        # 5___________________________________
                        demonstrativo_d['pr8_ajuste_d'] = pr8_ajuste_d
                        # 6___________________________________
                        demonstrativo_d['pr11_ajuste_d'] = pr11_ajuste_d
                        # 7___________________________________
                        demonstrativo_d['soma_alvo_max_d'] = soma_alvo_max_d
                        # 8___________________________________
                        demonstrativo_d['total_dist_max_d'] = total_dist_max_d
                        # 9___________________________________
                        demonstrativo_d['media_alvo_max_d'] = media_alvo_max_d          
                        # 10___________________________________
                        demonstrativo_d['razao_max_d'] = razao_max_d
                        # 11___________________________________
                        demonstrativo_d['target_max_d'] = target_max_d
                        # 12___________________________________
                        demonstrativo_d['soma_alvo_min_d'] = soma_alvo_min_d
                        # 13___________________________________
                        demonstrativo_d['total_dist_min_d'] = total_dist_min_d
                        # 14___________________________________
                        demonstrativo_d['media_alvo_min_d'] = media_alvo_min_d
                        # 15___________________________________
                        demonstrativo_d['razao_min_d'] = razao_min_d
                        # 16___________________________________
                        demonstrativo_d['target_min_d'] = target_min_d
                        # 17___________________________________
                        demonstrativo_d['target_of_the_day_d'] = target_of_the_day_d
                    else:
                        continue      
                    # end if calculateMediaLista
            # end if readCorretoras()

            if showResult:
                print(f'{Back.LIGHTWHITE_EX}{Fore.WHITE}________________________________________')
                print(f'{Back.LIGHTWHITE_EX}{Fore.WHITE}{Style.DIM}> > REPORT DOL - {day}\t{countOfTimes}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..OPEN_MARKET\t{demonstrativo_d["open_market_d"]} (DOLH23)')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}\t\tMAX\tMIN')
                if demonstrativo_d["total_dist_max_d"] < 10 or demonstrativo_d["total_dist_min_d"] < 10:
                    print(f'{Back.RED}{Fore.BLACK}{Style.DIM}..Total_Distrib\t{demonstrativo_d["total_dist_max_d"]}\t{demonstrativo_d["total_dist_min_d"]}\t(ALERTA){Back.MAGENTA}{Fore.BLACK}')
                else:
                    print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Total_Distrib\t{demonstrativo_d["total_dist_max_d"]}\t{demonstrativo_d["total_dist_min_d"]}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Total_IB_____\t{demonstrativo_d["soma_alvo_max_d"]}\t{demonstrativo_d["soma_alvo_min_d"]}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Media_IB(%)__\t{demonstrativo_d["media_alvo_max_d"]}\t{demonstrativo_d["media_alvo_min_d"]}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Razao_IB(p)__\t{demonstrativo_d["razao_max_d"]}\t{demonstrativo_d["razao_min_d"]}')

                if (soma_alvo_max_d >= soma_alvo_min_d):
                    print(f'{Back.GREEN}{Fore.BLACK}{Style.DIM}<< T_O_D >> {demonstrativo_d["target_of_the_day_d"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{Style.DIM}<< P_A - {demonstrativo["total_ajustes"]} >>{Back.MAGENTA}{Fore.BLACK}')
                else:
                    print(f'{Back.RED}{Fore.BLACK}{Style.DIM}<< T_O_D >> {demonstrativo_d["target_of_the_day_d"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{Style.DIM}<< P_A - {demonstrativo["total_ajustes"]} >>{Back.MAGENTA}{Fore.BLACK}')
                
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}\tVALUE PR(p)\tMAX(%)\tMIN(%)')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..PR_8___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo_d["pr8_ajuste_d"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo_d["maximo8_d"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo_d["minimo8_d"]}{Back.MAGENTA}{Fore.BLACK}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..PR11___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo_d["pr11_ajuste_d"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo_d["maximo11_d"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo_d["minimo11_d"]}{Back.MAGENTA}{Fore.BLACK}')
            # end if showResult()
        # end if calcularDOL()

        if calcularWDO:
            pr8_ajuste = 0
            pr11_ajuste = 0
            soma_alvo_max = 0
            media_alvo_max = 0
            razao_max = 0
            soma_alvo_min = 0
            media_alvo_min = 0
            razao_min = 0
            target_max = 0
            target_min = 0
            target_of_the_day = 0
            total_dist_max = 0
            total_dist_min = 0  

            # quantos distribuidores calcular
            max_dist = 10  

            #____INIT_RELATORIO_WDO_______________
            # 1___________________________________
            demonstrativo['maximo8'] = maximo8
            # 2___________________________________
            demonstrativo['minimo8'] = minimo8
            # 3___________________________________
            demonstrativo['maximo11'] = maximo11
            # 4___________________________________
            demonstrativo['minimo11'] = minimo11
            # 5___________________________________
            demonstrativo['pr8_ajuste'] = pr8_ajuste
            # 6___________________________________
            demonstrativo['pr11_ajuste'] = pr11_ajuste
            # 7_________SOMA_ALVO_MAX_____________
            demonstrativo['soma_alvo_max'] = soma_alvo_max
            # 8_________TOTAL_DIST_MAX____________
            demonstrativo['total_dist_max'] = total_dist_max
            # 9_________MEDIA_ALVO_MAX____________
            demonstrativo['media_alvo_max'] = media_alvo_max          
            # 10_________RAZAO_MAX_________________
            demonstrativo['razao_max'] = razao_max
            # 11_________TARGET_MAX________________
            demonstrativo['target_max'] = target_max 
            # 12_________SOMA_ALVO_MIN_____________
            demonstrativo['soma_alvo_min'] = soma_alvo_min
            # 13_________TOTAL_DIST_MIN____________
            demonstrativo['total_dist_min'] = total_dist_min
            # 14_________MEDIA_ALVO_MIN____________
            demonstrativo['media_alvo_min'] = media_alvo_min
            # 15_________RAZAO_MIN_________________
            demonstrativo['razao_min'] = razao_min
            # 16_________TARGET_MIN________________
            demonstrativo['target_min'] = target_min
            # 17_________TARGET_OF_THE_DAY_________
            demonstrativo['target_of_the_day'] = target_of_the_day

            ###########################################################################
            # Setor: leitura da lista das corretoras para calcular o Indice de Basileia
            ###########################################################################
            if readCorretoras:
                _printRegion(path_output, 'color_', 'lista_max', '.png',
                            coordsListMax[0], coordsListMax[1], coordsListMax[2], coordsListMax[3])
                _printRegion(path_output, 'color_', 'lista_min', '.png',
                            coordsListMin[0], coordsListMin[1], coordsListMin[2], coordsListMin[3])

                lista_corretoras_min = (_readDataList(path_output, 'hold2_', 'lista_min', '.png'))              
                # print(f'{Back.LIGHTRED_EX}{Fore.BLACK}Lista Bear = {lista_corretoras_min}')

                lista_corretoras_max = (_readDataList(path_output, 'hold2_', 'lista_max', '.png'))              
                # print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}Lista Bull = {lista_corretoras_max}')

                if len(lista_corretoras_max) == 0:
                    print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}>> " WDO BULL MARKET" - NO DATA <<')
                if len(lista_corretoras_min) == 0:
                    print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}>> "WDO BEAR MARKET" - NO DATA <<')
                if calculateMediaLista:
                    # exibindo distribuição BULL  
                    if len(lista_corretoras_max) > 0: 
                        ordem = 1
                        for c in lista_corretoras_max:
                            if c not in ib_lista_distribuidoras:
                                print(f'{Back.LIGHTWHITE_EX}{Fore.BLACK} < WDO MAX RECOGNIZED? {c} >')
                                continue  
                            if total_dist_max == max_dist:
                                break
                            for corretora, ib in ib_lista_distribuidoras.items():
                                if c == corretora:
                                    if ib == 0:
                                        pass
                                        #print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}{ordem} - {corretora} = {ib}')
                                    else:
                                        soma_alvo_max += float(ib)
                                        total_dist_max += 1
                                        #print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}{ordem} - {corretora} = {ib}')
                            #print(f'{Back.MAGENTA}{Fore.WHITE}>>> TOTAL DISTRIBUIDORAS: {len(lista_corretoras_max)}')
                            ordem += 1
                        media_alvo_max = float(soma_alvo_max / float(total_dist_max))
                        razao_max = float(((open_market * media_alvo_max) / 100) / 10)

                    # exibindo distribuição BEAR
                    if len(lista_corretoras_min) > 0:
                        ordem = 1
                        for c in lista_corretoras_min:
                            if c not in ib_lista_distribuidoras:
                                print(f'{Back.LIGHTWHITE_EX}{Fore.BLACK} < WDO MIN RECOGNIZED? {c} >')
                                continue  
                            if total_dist_min == max_dist:
                                break
                            for corretora, ib in ib_lista_distribuidoras.items():
                                if c == corretora:
                                    if ib == 0:
                                        pass
                                        #print(f'{Back.LIGHTRED_EX}{Fore.WHITE}{ordem} - {corretora} = {ib}')
                                    else:
                                        soma_alvo_min += float(ib)
                                        total_dist_min += 1
                                        #print(f'{Back.LIGHTRED_EX}{Fore.WHITE}{ordem} - {corretora} = {ib}')            
                            #print(f'{Back.MAGENTA}{Fore.WHITE}>>> TOTAL DISTRIBUIDORAS: {len(lista_corretoras_min)}')
                            ordem += 1

                        media_alvo_min = float(soma_alvo_min / float(total_dist_min))
                        razao_min = float(((open_market * media_alvo_min) / 100) / 10)                    

                    if (soma_alvo_max >= soma_alvo_min):
                        target_max = float(open_market + razao_max)
                        target_max = float((open_market + target_max) / 2)
                    else:
                        target_min = float(open_market - razao_min)
                        target_min = float((open_market + target_min) / 2)

                    target_of_the_day = float((target_max + target_min))
                
                    pr8_ajuste = float(demonstrativo['total_ajustes']/8)
                    pr11_ajuste = float(demonstrativo['total_ajustes']/11)

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

                    #_________RELATORIO_WDO_______________
                    # 1___________________________________
                    demonstrativo['maximo8'] = maximo8
                    # 2___________________________________
                    demonstrativo['minimo8'] = minimo8
                    # 3___________________________________
                    demonstrativo['maximo11'] = maximo11
                    # 4___________________________________
                    demonstrativo['minimo11'] = minimo11
                    # 5___________________________________
                    demonstrativo['pr8_ajuste'] = pr8_ajuste
                    # 6___________________________________
                    demonstrativo['pr11_ajuste'] = pr11_ajuste
                    # 7___________________________________
                    demonstrativo['soma_alvo_max'] = soma_alvo_max
                    # 8___________________________________
                    demonstrativo['total_dist_max'] = total_dist_max
                    # 9___________________________________
                    demonstrativo['media_alvo_max'] = media_alvo_max          
                    # 10___________________________________
                    demonstrativo['razao_max'] = razao_max
                    # 11___________________________________
                    demonstrativo['target_max'] = target_max
                    # 12___________________________________
                    demonstrativo['soma_alvo_min'] = soma_alvo_min
                    # 13___________________________________
                    demonstrativo['total_dist_min'] = total_dist_min
                    # 14___________________________________
                    demonstrativo['media_alvo_min'] = media_alvo_min
                    # 15___________________________________
                    demonstrativo['razao_min'] = razao_min
                    # 16___________________________________
                    demonstrativo['target_min'] = target_min
                    # 17___________________________________
                    demonstrativo['target_of_the_day'] = target_of_the_day
                else:
                    continue      
                # end if calculateMediaLista
            # end if readCorretoras

            if showResult:
                print(f'{Back.LIGHTWHITE_EX}{Fore.WHITE}________________________________________')
                print(f'{Back.LIGHTWHITE_EX}{Fore.WHITE}{Style.DIM}> > REPORT WDO - {day}\t{countOfTimes}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..OPEN_MARKET\t{demonstrativo["open_market"]} (WDOH23)')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}\t\tMAX\tMIN')
                if demonstrativo["total_dist_max"] < 10 or demonstrativo["total_dist_min"] < 10:
                    print(f'{Back.RED}{Fore.BLACK}{Style.DIM}..Total_Distrib\t{demonstrativo["total_dist_max"]}\t{demonstrativo["total_dist_min"]}\t(ALERTA){Back.MAGENTA}{Fore.BLACK}')
                else:
                    print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Total_Distrib\t{demonstrativo["total_dist_max"]}\t{demonstrativo["total_dist_min"]}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Total_IB_____\t{demonstrativo["soma_alvo_max"]}\t{demonstrativo["soma_alvo_min"]}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Media_IB(%)__\t{demonstrativo["media_alvo_max"]}\t{demonstrativo["media_alvo_min"]}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..Razao_IB(p)__\t{demonstrativo["razao_max"]}\t{demonstrativo["razao_min"]}')

                if (soma_alvo_max >= soma_alvo_min):
                    print(f'{Back.GREEN}{Fore.BLACK}{Style.DIM}<< T_O_D >> {demonstrativo["target_of_the_day"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{Style.DIM}<< P_A - {demonstrativo["total_ajustes"]} >>{Back.MAGENTA}{Fore.BLACK}')
                else:
                    print(f'{Back.RED}{Fore.BLACK}{Style.DIM}<< T_O_D >> {demonstrativo["target_of_the_day"]}\t<< P_A - {Back.LIGHTYELLOW_EX}{Fore.BLACK}{Style.DIM}{demonstrativo["total_ajustes"]} >>{Back.MAGENTA}{Fore.BLACK}')
                
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}\tVALUE PR(p)\tMAX(%)\tMIN(%)')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..PR_8___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["pr8_ajuste"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["maximo8"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["minimo8"]}{Back.MAGENTA}{Fore.BLACK}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..PR11___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["pr11_ajuste"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["maximo11"]}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{demonstrativo["minimo11"]}{Back.MAGENTA}{Fore.BLACK}')
                print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}..MEDIA___ {Back.LIGHTYELLOW_EX}{Fore.BLACK}{(demonstrativo["pr8_ajuste"]+demonstrativo["pr11_ajuste"])/2}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{(demonstrativo["maximo8"]+demonstrativo["maximo11"])/2}\t{Back.LIGHTYELLOW_EX}{Fore.BLACK}{(demonstrativo["minimo8"]+demonstrativo["minimo11"])/2}{Back.MAGENTA}{Fore.BLACK}')
            # end if showResult()
            print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM}{Back.LIGHTGREEN_EX}{Fore.BLACK} >> (PR8+PR11)/2________{(abs(demonstrativo["target_of_the_day"])+abs(demonstrativo_d["target_of_the_day_d"]))/2}{Back.MAGENTA}{Fore.BLACK}')
            print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM} * PA: Pontos de Ajuste (total){Back.MAGENTA}{Fore.BLACK}') 
            print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM} * T_O_D: Target of the Day{Back.MAGENTA}{Fore.BLACK}')
            print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM} * IB: Indice de Basileia{Back.MAGENTA}{Fore.BLACK}')
            print(f'{Back.MAGENTA}{Fore.BLACK}{Style.DIM} * PR: Patrimônio de Referência{Back.MAGENTA}{Fore.BLACK}')  
            
            countOfTimes += 1
        time.sleep(1)
        # end if calcularDOL()
    # end while
# end main