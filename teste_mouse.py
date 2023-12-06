import pyautogui

# Espera 5 segundos para que você possa posicionar o mouse
pyautogui.PAUSE = 10

# Clica e arrasta para selecionar a área
x1, y1 = pyautogui.position()
pyautogui.mouseDown(x1, y1)
x2, y2 = pyautogui.position()
pyautogui.mouseUp(x2, y2)

# Exibe as coordenadas de onde você clicou e onde soltou o botão do mouse
print("Clicou em:", x1, y1)
print("Soltou em:", x2, y2)
