# id: KmPPwGOKxvjERhLJSqs9tw
# secret: 0DUvfHpw9hKDU3TpHLsOeoLm1bDmkw
# name: analisert

#mais um: https://www.reddit.com/r/investimentos/comments/14vcgkb/sobre_a_reforma_tribut%C3%A1ria_o_qu%C3%AA_ach
# am/
# https://www.reddit.com/r/brasilivre/comments/14t4gwl/apenas_repostas_concisas_sobreapresentem_fatos_e/

#https://www.reddit.com/r/brasil/comments/14rpwgh/partido_republicanos_declara_apoio_%C3%A0_reforma/
#https://www.reddit.com/r/brasil/comments/14st1bj/resumo_da_reforma_tribut%C3%A1ria_aprovada_no_plen%C3%A1rio/
#https://www.reddit.com/r/brasil/comments/14rt8kr/haddad_inclui_proposta_de_reduzir_impostos_dos/

import praw
import pandas as pd
from varGlobal import path

# Autenticação no Reddit
reddit = praw.Reddit(client_id='KmPPwGOKxvjERhLJSqs9tw',
                     client_secret='0DUvfHpw9hKDU3TpHLsOeoLm1bDmkw',
                     user_agent='analisert')

# IDs das postagens que você quer extrair
post_ids = ['14sfftq', '14rpwgh', '14st1bj','14rt8kr', '17qr5pr', '17rphof', '14vcgkb', '14t4gwl']

# Lista para armazenar os dados
dados = []

# Loop sobre as IDs das postagens
for post_id in post_ids:
    submission = reddit.submission(id=post_id)
    dados.append({
        'ID': submission.id,
        'Título': submission.title,
        'Texto': submission.selftext,
        'Subreddit': submission.subreddit.display_name,
        'Pontuação': submission.score,
        'Número de comentários': submission.num_comments,
        'Data da criação': pd.to_datetime(submission.created_utc, unit='s'),
        'Link': submission.url
    })

# Converter a lista de dicionários em DataFrame
df = pd.DataFrame(dados)

# Exibir o DataFrame
print(df)

# Salvar os dados brutos em uma planilha no Excel
postagemBruto = f'{path}postagemBruto.xlsx'

# Salvar o DataFrame em um arquivo Excel
df.to_excel(postagemBruto, index=False)

print(f'Dados salvos em {postagemBruto}')

