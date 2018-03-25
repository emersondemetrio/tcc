# UFSC / CTC / SIN / INE5660 - Projetos II (TCC)

## Orientador: Elder Santos

## Coordenador TCC: Renato Cislaghi

## Aluno: Emerson Demetrio

## Tema: "Técnicas de IA e similaridade aplicadas ao reconhecimento de padrões musicais"

### Projeto

Um sistema interativo capaz de descrever qual é o gênero (rock, blues, pop) de um arquivo de áudio,
valendo-se de uma base de treino e um acervo faixas de áudio.

### Funcionamento

1 - Extração de Informação

Necessariamente, deve haver um diretório no sistema operacional que contenha arquivos .mp3.
O caminho para este diretório será o primeiro parametro para a operação de extração de informação musical (MIR).
O segundo parametro será o caminho para um diretório de saída.

Exemplo:

```cd mir```

```python self-extractor.py -i /home/user/musics -o /home/user/output```

2 - Database Populate

Depois de extrair as informações, o sistema poderá armazenar os atributos de interesse num banco de dados.


