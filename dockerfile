# Usa uma imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependência para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
COPY . .

# Expõe a porta usada pelo Uvicorn
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
