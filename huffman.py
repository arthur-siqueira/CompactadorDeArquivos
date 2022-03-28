import os
from re import sub

"""
Os objetos dessa classe serão os nós para a árvore binária de huffman
"""

class No:
    conteudo = 0
    bin = ""

    def __init__(self, conteudo, freq, bin, left, right):
        """
        :param conteudo: caractere que será guardado por cada nó
        :param freq: frequencia dos caracteres no texto
        :param bin: código em binário que representa o caminho da raiz até dado nó
        :param left: o filho da esquerda
        :param right: o filho da direita
        """
        self.conteudo = conteudo
        self.freq = freq
        self.bin = bin
        self.left = left
        self.right = right

    def __repr__(self):
        return repr((self.conteudo, self.freq, self.bin))

    def ehFolha(self):
        return self.left is None and self.right is None


"""
Essa classe cria uma lista com todos os caracteres do texto lido, atribui um nó a cada caractere e 
ordena em ordem crescente de frequência, a partir dessa lista será criada a árvore binária

raiz - Quando a árvore estiver completa será o primeiro e único elemento
texto - É uma lista de caracteres que representa todo o texto
"""

class ListaNos:
    raiz = 0
    texto = ''

    def __init__(self, lista):
        """
        :param lista: cria uma lista com o texto
        """
        self.texto = lista

    def insereRaiz(self, novo):
        """
        Insere a raiz na lista que corresponde ao primeiro elemento
        :param novo: Valor que será o primeiro elemento na lista
        :return: A lista com o primeiro elemento
        """
        self.raiz = [novo]
        return

    def insere(self, novo):
        """
        Isere o último elemento da lista
        :param novo: Último elemento da lista
        :return: Retorna a lista com o último elemento
        """
        for item in self.raiz:
            if item.conteudo == novo.conteudo:
                item.freq += 1
                self.raiz = sorted(self.raiz, key=lambda no: no.freq)
                return  # FINALIZA

        self.raiz += [novo]
        self.raiz = sorted(self.raiz, key=lambda no: no.freq)

        return

    def criaLista(self):
        """
        Cria uma lista de caracteres através do texto
        :return: A lista
        """
        for l in self.texto:
            if self.raiz == 0:



                self.insereRaiz(No(l, 1, '', None, None))

            else:
                # SE A LISTA NÃO ESTIVER VAZIA
                # INSERI O ELEMENTO
                self.insere(No(l, 1, '', None, None))

        return


    def criaArvore(self):
        """
        Cria a árvore de huffman
        :return: A árvore
        """

        self.criaLista()

        while len(self.raiz) > 1:

            novo = No("", self.raiz[0].freq + self.raiz[1].freq, '', self.raiz[0],
                      self.raiz[1])

            del self.raiz[0]
            del self.raiz[0]

            self.raiz += [novo]
            self.raiz = sorted(self.raiz, key=lambda no: no.freq)

        return



class ArvoreHuffman:

    def criaCodigoBin(self, no):
        """
        Gera um código em binário para cada nó
        :param no: O nó que será usado como parametro para criar o código binário
        :return: O código binário do nó
        """
        if no is None:
            return

        if no.left is not None:
            no.left.bin = no.bin + '1'
            self.criaCodigoBin(no.left)

        if no.right is not None:
            no.right.bin = no.bin + '0'
            self.criaCodigoBin(no.right)
        return

    def criaTextoBin(self, arv, texto):
        """
        Cria a sequência de códigos binários
        :param arv: árvore que está utilizando
        :param texto: texto original
        :return: Sequência de códigos binários
        """
        resultado = ''
        for letter in texto:
            resultado += self.codigoBin(arv, letter)

        novo = bytes(resultado, encoding="utf-8")
        return novo


    def codigoBin(self, arv, letter):
        """
        Retorna o código de um caractere específico da árvore
        :param arv: Árvore que está sendo utilizada
        :param letter: O caractere específico
        :return: código do caractere
        """
        bin = ''
        if arv.conteudo == letter:
            bin = arv.bin

        if arv.left is not None:
            bin = self.codigoBin(arv.left, letter)

        if bin == '':
            if arv.right is not None:
                bin = self.codigoBin(arv.right, letter)

        return bin

    def decodificarBin(self, arv, textBin):
        """
        A partir da árvore e da sequência em binário resgata o texto original
        :param arv: Árvore que está sendo utilizada
        :param textBin: Sequência em binário
        :return: retorna o texto original descodificado
        """
        arvore = arv
        result = ""
        for bin in textBin:
            if bin == 49:
                if arvore.left is not None:
                    arvore = arvore.left
                    if arvore.left is None and arvore.right is None:
                        result += (arvore.conteudo)
                        arvore = arv
            else:
                if arvore.right is not None:
                    arvore = arvore.right
                    if arvore.left is None and arvore.right is None:
                        result += (arvore.conteudo)
                        arvore = arv

        return result



def pegaTexto(file_name):
    """
    Resgata o texto que será convertido
    :param file_name: O nome do arquivo
    :return: O texto que será usado
    """
    text = ""
    try:
        file = open(file_name, "r")
        text = file.read()
    except IOError:
        print("Erro ao abrir o arquivo")
    return text


def criaArquivo(file_name, text):
    """
    Cria um arquivo .bin
    :param file_name: Nome do arquivo que será criado
    :param text: sequência em binário
    :return: O arquivo criado
    """
    try:
        file = open(file_name, 'wb')
        file.write(text)
        file.close()
    except IOError:
        raise print("Erro ao criar o arquivo")

def criaArquivoTXT(file_name, text):
    """
    Cria um arquivo .txt
    :param file_name: Nome do arquivo
    :param text: Texto do arquivo
    :return: O arquivo criado
    """
    try:
        file = open(file_name, "w")
        file.write(text)
        file.close()
    except IOError:
        raise print("Erro ao criar arquivo")


def formataTamanho(tamanho):
    """
    Formata o tamanho dos arquivos
    :param tamanho: tamanho do arquivo em bytes
    :return: O tamanho formatado
    """
    texto = ""
    base = 1024
    kilo = base
    mega = base ** 2
    giga = base ** 3
    tera = base ** 4

    if tamanho < kilo:
        texto = "B"
    elif tamanho < mega:
        tamanho /= kilo
        texto = "K"
    elif tamanho < giga:
        tamanho /= mega
        texto = "M"
    elif tamanho < tera:
        tamanho /= giga
        texto = "G"

    tamanho = round(tamanho, 2)
    return f"{tamanho}{texto}".replace(",", ".")


# MENU

print("#################################")
print("###  COMPACTADOR DE ARQUIVOS  ###")
print("#################################")

print()

texto = str(input("Insira um texto: "))

print()

with open("texto.txt", "w") as arquivo:
    arquivo.write(texto)


lista = list(pegaTexto("texto.txt"))
at = ArvoreHuffman()
listaNos = ListaNos(lista)
listaNos.criaArvore()
at.criaCodigoBin(listaNos.raiz[0])
caracteres = []

criaArquivo("codigoBinCompact.bin", at.criaTextoBin(listaNos.raiz[0], listaNos.texto))

for caractere in lista:
    if caractere not in caracteres:
        caracteres.append(caractere)
print(caracteres)

print("CÓDIGOS BINÁRIOS PARA CADA CARACTERE:")
textoConvertido = ""
for c in pegaTexto("texto.txt"):
    string = c
    convertido = ' '.join(map(bin, bytearray(string, "utf-8")))
    convertido = sub("b", "", convertido)
    print(f"{c} = {convertido}")
    textoConvertido += convertido
textoConvertidoBin = bytes(textoConvertido, encoding="utf-8")

criaArquivo("original.bin", textoConvertidoBin)

print()
print("NOVOS CÓDIGOS BINÁRIOS PARA CADA CARACTERE:")
for c in caracteres:
    print(f"{c} = {at.codigoBin(listaNos.raiz[0], c)}")

tamanho = os.path.getsize("original.bin")
tamanhoNovo = os.path.getsize("codigoBinCompact.bin")

print()

print(f"tamanho original: {formataTamanho(tamanho)}")
print(f"tamanho compactado: {formataTamanho(tamanhoNovo)}")


criaArquivoTXT("arquivoDes.txt", at.decodificarBin(listaNos.raiz[0], at.criaTextoBin(listaNos.raiz[0], listaNos.texto)) )
