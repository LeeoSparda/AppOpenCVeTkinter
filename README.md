Image Processor GUI
Este é um aplicativo simples de processamento de imagem com uma interface gráfica do usuário (GUI) construída em Python usando as bibliotecas Tkinter e OpenCV. O aplicativo permite carregar uma imagem, aplicar várias operações de processamento de imagem e salvar a imagem resultante juntamente com um histórico das operações realizadas.

Pré-requisitos
Certifique-se de ter as seguintes bibliotecas instaladas:

Python 3.12
OpenCV (cv2)
NumPy
Tkinter
PIL (Python Imaging Library)
subprocess (para chamar outros scripts Python)
Você pode instalar essas dependências usando pip:
pip install opencv-python numpy pillow

Como usar
1.Clone este repositório ou copie o código do arquivo image_processor.py.
2.Execute o script Python image_processor.py.
3.Na interface gráfica, clique em "Load Image" para selecionar uma imagem.
4.Selecione uma operação na lista suspensa "Select Operation".
5.Clique em "Apply" para aplicar a operação selecionada à imagem carregada.
6.Você pode clicar em "Reset" para reverter para a imagem original.
7.Clique em "Save" para salvar a imagem processada junto com o histórico das operações.

Operações suportadas
O aplicativo suporta as seguintes operações de processamento de imagem:

Convert Color: Converta a imagem de BGR para escala de cinza ou RGB.
Apply Filter: Aplique um filtro de média à imagem.
Detect Edges: Detecte bordas na imagem usando o algoritmo Canny.
Binarize: Binarize a imagem usando um limiar.
Morphological Operations: Aplique operações morfológicas à imagem, como erosão.
Além disso, o aplicativo oferece a opção de selecionar uma região de interesse (ROI) na imagem e salvar a ROI separadamente.
