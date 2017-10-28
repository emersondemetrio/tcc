# Como funciona

## Escolha de gêneros:

Escolheu-se diversos arquivos de músicas cujo gênero é previamente conhecido.
Os gêneros podem ser definidos de diferentes maneiras:

- Votação
- Conhecimento prévio
- Pesquisa (crawler)

### Meta Tags e ID3 Tags

Artigos que falam sobre id3 tags/ meta tags

### Identificação Prévia de Gênero

Para este trabalho, optou-se por utilizar conhecimento prévio, através das ID3 tags presentes nos arquivos para definir qual era seu gênero no momento anterior a montagem do conjunto de testes.

Os generos escolhidos foram:

- eletronic
- grunge
- hard-rock
- hip-hop
- indie
- metal
- new-metal
- pop
- pop-rock
- progressive-metal
- punk
- ska

A opção por cada um dos gêneros deu-se pela escolha pessoal do autor, devido ao número de arquivos para cada gênero e por considerar a especificação dos gêneros escolhida a mais distinta entre si possivel.

Após definidos os gêneros, o passo seguinte foi, para cada gênero, escolher bandas distintas para cada gênero, conforme tabela tal.

### Extração da informação presente nos arquivos

As tags presentes nos arquivos são consideradas em MIR como "meta-informação", ou seja, informação sobre a informação presente no arquivo, todavia, para extração das caracterísitcas físicas do sinal sonoro presente em cada arquivo, foi necessário o uso da biblioteca essentia associado a um programa escrito na linguagem python que é capaz de varrer diretórios em busca de arquivos no formato mp3, associar o arquivo ao seu gênero, baseado na pasta onde está inserido, montar uma string com o caminho final do arquivo de informação extraido e executar o script de extração da biblioteca essentia.

O caminho final para o arquivo de informações extraido se deu por um hash md5 simples do caminho inicial do arquivo, para fins de simplificação.

O formato de saída, a quantidade de samplers usado e outras diversas caracteristicas do arquivo final de extração podem ser definidos como parametro de entrada nos scripts da biblioteca essentia, bastando criar-se um arquivo no formato yml chamado comumente de profile.

O arquivo profile.yml utilizado para extração neste trabalho foi o seguinte:

```
startTime: 0
endTime: 60
outputFrames: 0
outputFormat: json
requireMbid: false
indent: 4

lowlevel:
    frameSize: 2048
    hopSize: 1024
    zeroPadding: 0
    windowType: blackmanharris62
    silentFrames: noise
    stats: ["mean", "var", "median", "min", "max", "dmean", "dmean2", "dvar", "dvar2"]

average_loudness:
    frameSize: 88200
    hopSize: 44100
    windowType: hann
    silentFrames: noise

rhythm:
    method: degara
    minTempo: 40
    maxTempo: 208
    stats: ["mean", "var", "median", "min", "max", "dmean", "dmean2", "dvar", "dvar2"]

tonal:
    frameSize: 4096
    hopSize: 2048
    zeroPadding: 0
    windowType: blackmanharris62
    silentFrames: noise
    stats: ["mean", "var", "median", "min", "max", "dmean", "dmean2", "dvar", "dvar2"]
```

Das diversas características presentes no arquivo, as informações mais interessantes são a quantidade de samplers usada para extração, que é definida pelo tempo total em segundos desde o início da música (ou de um determinado tempo previamente especificado) até um determinado tempo final especificado.

Neste projeto, optou-se por utilizar 60 segundos de cada música para fins de extração, uma vez que ao observar as características dos arquivos de entrada, percebeu-se que os primeiros 15 segundos de cada música são normalmente sua introdução, seguida por verso e refrão.
Assim sendo, utiizar 60 segundos para cada música é suficiente para extrair com certo grau de confiança as informações usadas posteriormente como entrada para a rede neural classificadora.

O layout final dos arquivos de informação musical extraida foi como na figura abaixo:

results/genero/md5-caminho-arquivo.json



















## Trabalhos futuros:

Montagem automática dos conjuntos de testes separados em gêneros, baseados nas ID3 tags dos arquivos.
Uma vez que o acervo pessoal de músicas contém todas as ID3 tags em cada arquivo e nelas estão condidos seus gêneros, é possível montar o conjunto de testes automáticamente, desde que as informações do arquivo sejam previamente extraidas.

Treinamento e Classificão usando MFCCs e outroas tags presentes no arquivo final de extração.