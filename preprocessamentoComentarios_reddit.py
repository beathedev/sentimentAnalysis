# Objetivo principal: Aplicar as etapas 1, 2 e 3 e obter textos bem préprocessados
#  Etapa1: Padronização do texto, remoção de emojis, remoção de links e símbolos;
#  Etapa 2: Remover stopwords, ruídos e  remoção de pontuações;
#  Etapa 3: Aplicar o Stemming e a tokenização no texto já pré-processado nas etapas anteriores, com auxílio da biblioteca NLTK.
#
#  Remover_emojis: busca os unicodes dos emojis, símbolos, pictograma, símbolos do ios, etc.
# ##


import pandas as pd
import re
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from varGlobal import path, client_id, client_secret, user_agent

# Carregar os dados da planilha com os comentários em bruto
dados = pd.read_excel(f'{path}comentarioBruto.xlsx')

# Função para remover emojis
def remover_emojis(texto):
    # unicode dos emoticons
    emojisCodigo = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # símbolos e pictogramas
                               u"\U0001F680-\U0001F6FF"  # transporte e símbolos de mapas
                               u"\U0001F1E0-\U0001F1FF"  # bandeiras (iOS)
                               u"\U00002500-\U00002BEF"  # caracteres chineses
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    
    textoLimpo = emojisCodigo.sub(r'', texto)
    
    return textoLimpo

# Função para pré-processamento do texto - Etapa 1
def preprocessamento_etapa1(texto):
    # Padronização do texto
    texto = texto.lower().strip()
    
    # Remover links
    texto = re.sub(r'http\S+', '', texto)

    # Remover símbolos especificados
    texto = re.sub(r'[;/.!`"|:?,%$¨¨¬&#@=\\()<>\[\]*-]', '', texto)
    
    # Remover emojis
    texto = remover_emojis(texto)

    return texto

# Função para pré-processamento do texto - Etapa 2
def preprocessamento_etapa2(texto):
    # Remover stopwords e ruídos
    stop_words = set(stopwords.words('portuguese'))
    
    # Adicionar stopwords do arquivo adicional stopwordsGithub.txt
    with open(f'{path}stopwordsGithub.txt', 'r', encoding='utf-8') as file:
        stopwordAdicional = file.readlines()
    stopwordAdicional = [word.strip() for word in stopwordAdicional]
    
    # Adicionar as stopwords adicionais à lista de stopwords
    stop_words.update(stopwordAdicional)

    # Remover pontuações
    pontuacao = set(string.punctuation)
    ruido = stop_words.union(pontuacao)

    # Remover "não" da lista de stopwords a serem removidas pois nesse contexto, ela é necessária
    ruido.discard("não") 
    palavras = texto.split()
    palavras_filtradas = [palavra for palavra in palavras if palavra not in ruido and len(palavra) > 1]
    textoLimpo = ' '.join(palavras_filtradas)
    
    # Substituir "não" por "nao" a fim de obter um vocabulário mais padronizado
    textoLimpo = textoLimpo.replace('não', 'nao')
    
    return textoLimpo

# Função para pré-processamento do texto - Etapa 3
def preprocessamento_etapa3(texto):
    # Aplicar stemming
    ps = PorterStemmer()
    palavras = word_tokenize(texto)
    palavras_stemmed = [ps.stem(palavra) for palavra in palavras]
    textoStemmed = ' '.join(palavras_stemmed)

    return textoStemmed


# Aplicar a função de pré-processamento de acordo com cada etapa (1, 2 e 3)
dados['ETAPA1'] = dados['Comentario'].apply(preprocessamento_etapa1)
dados['ETAPA2'] = dados['ETAPA1'].apply(preprocessamento_etapa2)
dados['ETAPA3'] = dados['ETAPA2'].apply(preprocessamento_etapa3)

# Identificar linhas que contêm a string "!gif" na coluna "ETAPA3"
linhas_com_gif = dados['Comentario'].str.contains(r'!\[gif\]', case=False)
# Remover as linhas identificadas
dfFinal= dados[~linhas_com_gif]

# Salvar os resultados em uma nova planilha
dfFinal.to_excel(f'{path}comentarioPreprocessado.xlsx', index=False)
