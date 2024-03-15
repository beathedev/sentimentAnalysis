# id: KmPPwGOKxvjERhLJSqs9tw
# secret: 0DUvfHpw9hKDU3TpHLsOeoLm1bDmkw
# name: analisert
import praw
import pandas as pd
from varGlobal import path, client_id, client_secret, user_agent

# Autenticação no Reddit
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


# Lista para armazenar os dados dos comentários
dadosbrutos_comentarios = []

# Postagens que serão utilizadas
post_ids = ['14sfftq', '14rpwgh', '14st1bj','14rt8kr', '17qr5pr', '17rphof', '14vcgkb', '14t4gwl']


# Loop sobre as IDs das postagens
for post_id in post_ids:
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=None)
    
    # Verificar se há comentários de primeira camada
    comentarios_primeira_camada = [comment for comment in submission.comments if comment.parent_id.startswith('t3_')]
    print(f"Post ID: {post_id}, Comentários de Primeira Camada: {len(comentarios_primeira_camada)}")
    
    for comment in comentarios_primeira_camada:
        dadosbrutos_comentarios.append({
            'Post_ID': submission.id,
            'Comentario': comment.body,
            'Subreddit': submission.subreddit.display_name,
            'Pontuação': comment.score,
            'Data da criação': pd.to_datetime(comment.created_utc, unit='s'),
            'Link do comentário': f'https://www.reddit.com{comment.permalink}'
        })


# Converter a lista de dicionários em DataFrame
df_comentarios = pd.DataFrame(dadosbrutos_comentarios)

# Salvar os dados dos comentários em uma planilha no Excel
dadosbrutoscomentarios_excel = f'{path}comentarioBruto.xlsx'

# Salvar o DataFrame em um arquivo Excel
df_comentarios.to_excel(dadosbrutoscomentarios_excel, index=False)

print(f'Comentários salvos em {dadosbrutoscomentarios_excel}')