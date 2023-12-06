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

        except ValueError as error:                              
            print(f'{Back.LIGHTYELLOW_EX}{Fore.WHITE}----- ERROR {img} - {error} -----')
            return False
        except AttributeError as error:                              
            print(f'{Back.LIGHTBLUE_EX}{Fore.WHITE}----- ERROR {img} - {error} -----')
            return False
        except None as error:                             
            print(f'{Back.LIGHTRED_EX}{Fore.WHITE}----- ERROR {img} - {error} -----')
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
            if p == 'Tullete': p = 'TULLETT'
            if p == '(P' or p == 'XP.': p = 'XP'
            p = str.upper(p)
            data.append(p)
            # print(f'LEITURA = {p}')

        except ValueError as error:                              
            print(f'{Back.LIGHTYELLOW_EX}{Fore.WHITE}----- ERROR {img} - {error} -----')
            return False
        except AttributeError as error:                              
            print(f'{Back.LIGHTBLUE_EX}{Fore.WHITE}----- ERROR {img} - {error} -----')
            return False
        except None as error:                             
            print(f'{Back.LIGHTRED_EX}{Fore.WHITE}----- ERROR {img} - {error} -----')
            return False

    #time.sleep(1)

    # print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}DATA: {data}')
    return data
############################################



if __name__ == '__main__':
    loop = True
    just_readAjuste = False
    readData = True

    calculateMediaAdj = True
    calculateMedia = True

    calculateMediaLista = True
    readCorretoras = True

    showResult = True
    replay = False

    if replay:
        coordsAdj_dolar = [1745, 70, 1855, 937]
        coordsListMax = [1394, 78, 1591, 400]
        coordsListMin = [1394, 481, 1591, 803]
    else:
        coordsAdj_dolar = [1745, 70, 1855, 937]
        coordsListMax = [1394, 58, 1591, 380]
        coordsListMin = [1394, 461, 1591, 783]  

    countOfTimes = 0
    mediaGeral = 0 
    medias = []
    maximo = -1
    minimo = 1
    list_corretoras_max = []
    list_corretoras_min = []

    demonstrativo = {}
    
    # dados atrasado/inexistente: INTER, CLEAR, CITIGROUP,
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
        'CITIGROUP': 0,
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
        'MERRIL': 22.22,
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
        'VITREO DTVMS.A.': 44.8,
        'VOTORANTIM': 17.1,
        'WARREN': 10.18,
        'XP': 16.11
    }

    while loop:
        loop = True
        ajustes = 0
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
        
        open_market = float('5238.0')   
               
        #_________IB_MAX_TARGET_____________
        demonstrativo['soma_alvo_max'] = soma_alvo_max
        #___________________________________
        demonstrativo['media_alvo_max'] = media_alvo_max          
        #___________________________________
        demonstrativo['razao_max'] = razao_max
        #___________________________________
        demonstrativo['target_max'] = target_max            
        #___________________________________

        #_________IB_MIN_TARGET_____________
        demonstrativo['soma_alvo_min'] = soma_alvo_min
        #___________________________________
        demonstrativo['media_alvo_min'] = media_alvo_min
        #___________________________________
        demonstrativo['razao_min'] = razao_min
        #___________________________________
        demonstrativo['target_min'] = target_min

        #___________________________________
        demonstrativo['target_of_the_day'] = target_of_the_day
        #___________________________________    

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

            if lista_corretoras_max == [] or lista_corretoras_min == []:
                print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}>>> MERCADO SEM DATA...')
                continue

        if calculateMediaLista:                
            print(f'{Back.WHITE}')
            # exibindo distribuição BULL   
            print(f'{Back.MAGENTA}{Fore.WHITE}>>> TOTAL DISTRIBUIDORAS: {len(lista_corretoras_max)}')
            ordem = 1
            for c in lista_corretoras_max:
                if total_dist_max == max_dist:
                    break
                for corretora, ib in ib_lista_distribuidoras.items():
                    if c == corretora:
                        if ib == 0:
                            print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}{ordem} - {corretora} = {ib}')
                        else:
                            soma_alvo_max += float(ib)
                            total_dist_max += 1
                            print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}{ordem} - {corretora} = {ib}')
                ordem += 1
            media_alvo_max = float(soma_alvo_max / float(total_dist_max))
            razao_max = float(((open_market * media_alvo_max) / 100) / 10)
            print(f'{Back.GREEN}{Fore.WHITE}TOTAL IB: {soma_alvo_max} % >> MEDIA IB: {media_alvo_max} %')
            print(f'{Back.GREEN}{Fore.WHITE}RAZÃO IB: {razao_max} p')

                
            print(f'{Back.WHITE}')
            # exibindo distribuição BEAR
            total_dist_min = 0            
            print(f'{Back.MAGENTA}{Fore.WHITE}>>> TOTAL DISTRIBUIDORAS: {len(lista_corretoras_min)}')
            ordem = 1
            for c in lista_corretoras_min:
                if total_dist_min == max_dist:
                    break
                for corretora, ib in ib_lista_distribuidoras.items():
                    if c == corretora:
                        if ib == 0:
                            print(f'{Back.LIGHTRED_EX}{Fore.WHITE}{ordem} - {corretora} = {ib}')
                        else:
                            soma_alvo_min += float(ib)
                            total_dist_min += 1
                            print(f'{Back.LIGHTRED_EX}{Fore.WHITE}{ordem} - {corretora} = {ib}')
                ordem += 1

            media_alvo_min = float(soma_alvo_min / float(total_dist_min))
            razao_min = float(((open_market * media_alvo_min) / 100) / 10)                         
            print(f'{Back.RED}{Fore.WHITE}TOTAL IB: {soma_alvo_min} % >> MEDIA IB: {media_alvo_min} %')            
            print(f'{Back.RED}{Fore.WHITE}RAZÃO IB: {razao_min} p')
            

            if (soma_alvo_max >= soma_alvo_min):
                target_max = float(open_market + razao_max)
                target_max = float((open_market + target_max) / 2)
            else:
                target_min = float(open_market - razao_min)
                target_min = float((open_market + target_min) / 2)

            target_of_the_day = float((target_max + target_min))

            if (soma_alvo_max >= soma_alvo_min):
                print(f'{Back.GREEN}{Fore.WHITE}>> FINAL TARGET ({float(razao_max / razao_min)} %)<<')
                print(f'{Back.GREEN}{Fore.WHITE}>>   {target_of_the_day}   <<')
            else:
                print(f'{Back.RED}{Fore.WHITE}>> FINAL TARGET ({float(razao_max / razao_min)} %)<<')
                print(f'{Back.RED}{Fore.WHITE}>>   {target_of_the_day}   <<')

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

            if ajustes == []:                               
                print(f'{Back.LIGHTCYAN_EX}{Fore.BLACK}-----AJUSTES SEM DATA-----')
                continue

            if calculateMediaAdj:
                # calc main
                total_ajustes = 0
                # print(f'Wdo >>> {wdo}')
                for w in ajustes:
                    # print(f'w >>> {w}')
                    total_ajustes += float(w)
                    # print(f'Total_ajustes: {total_ajustes}')

                    if w < maximo:
                        maximo = float(w)
                    if w > maximo or w > minimo :
                        minimo = float(w)
            

                print(f'{Back.WHITE}')
                print(f'{Back.MAGENTA}{Fore.WHITE}{countOfTimes}>> PONTOS DE AJUSTE: {total_ajustes}')
                pr8_ajuste = float(total_ajustes/8)
                pr11_ajuste = float(total_ajustes/11)
                print(f'{Back.MAGENTA}{Fore.WHITE}>> PR 8%: {pr8_ajuste} / PR 11%: {pr11_ajuste}')
                print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}>> AJUSTES <<')
                for x in ajustes:
                    print(f'{Back.LIGHTGREEN_EX}{Fore.BLACK}.... {x}')
                countOfTimes += 1
                
                #___________________________________
                demonstrativo['total_ajustes'] = total_ajustes
                #___________________________________
                demonstrativo['maximo'] = maximo
                #___________________________________
                demonstrativo['minimo'] = minimo
                #___________________________________
                demonstrativo['pr8_ajuste'] = pr8_ajuste
                #___________________________________
                demonstrativo['pr11_ajuste'] = pr11_ajuste
                #___________________________________
                
                if showResult:
                    pass
            # end if calculateMedia

            time.sleep(0.5)
        # end if readAjuste()

    # end while