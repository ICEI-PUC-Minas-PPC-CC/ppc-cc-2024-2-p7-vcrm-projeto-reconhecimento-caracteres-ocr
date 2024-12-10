# Reconhecimento de Caracteres OCR

`PPC-CC: PUC Poços de Caldas - Ciência da Computação`
`Disciplina: Visão Computacional e Realidade Misturada`
`2024 - Semestre 2`

## Integrantes

- Leonardo Vilas Boas Mendes
- Vinicius Machioni

## Professor

- Prof. M. Sc. Will Machado 

# Documentação

## 1º Passo: Instalação do Python

### Requisitos
- Sistema Operacional compatível: Windows, macOS ou Linux.
- Permissões de administrador para instalar softwares.

### Passo a Passo
1. Acesse o site oficial do Python
- https://www.python.org/

2. Baixe o instalador
- Na página inicial, clique em *Downloads*
- Selecione o instalador para o seu sistema operacional.

3. Execute o Instalador:
   ### Windows
- Clique duas vezes no arquivo baixado.
- Na janela de instalação:
    - Marque a opção Add Python to PATH.
    - Clique em Install Now.
- Aguarde até que a instalação seja concluída e clique em Close.

  ### Linux
- No linux, o python vem instalado. Verifique digitando:
   ```python3 --version```
4. Verifique a instalação:
  ```python --version``` ou ```python3 --version```

## 2º Passo: Instalação do Poppler
Poppler é uma biblioteca usada para manipulação de arquivos PDF. É essencial para conversão de PDFs em imagens ou extração de texto em projetos Python que usam ferramentas como pdf2image.

1. Instalação no Windows:
- Baixe o Poppler para Windows em:  https://github.com/oschwartz10612/poppler-windows/releases/.
- Extraia o conteúdo do arquivo baixado para uma pasta de sua escolha (por exemplo, ```C:\poppler```).
- Adicione o caminho da pasta ```bin``` ao PATH do sistema:
    - Clique com o botão direito em Este Computador > Propriedades > Configurações Avançadas do Sistema.
    - Clique em Variáveis de Ambiente.
    - Na variável Path, adicione o caminho completo da pasta ```C:\poppler\bin```.

2. Instalação no Linux:
- Use o gerenciador de pacotes da sua distribuição para instalar o Poppler:
- Debian/Ubuntu:
  ```sudo apt update``` e 
  ```sudo apt install poppler-utils```

3. Verificando a instalação:
- Abra o terminal.
- Digite:
  ```pdfinfo --version```

## 3º Passo: Faça o clone do repositório
- Abra o terminal do git e digite: `https://github.com/ICEI-PUC-Minas-PPC-CC/ppc-cc-2024-2-p7-vcrm-projeto-reconhecimento-caracteres-ocr`

## 4º Passo: Instalação das bibliotecas
- Abra o terminal do VS Code e digite: `pip install -r requirements.txt`

## 5º Passo: Rode a Aplicação
- No terminal, rode o comando para habilitar a API (Importante: Deixe rodando): `python ocr_api.py`
- Abra uma nova janela do terminal, para rodar a interface gráfica: `python app.py`

Seguindo os passos acima, a aplicação deverá rodar normalmente.
