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

## Características Utilizadas e Convenção de Nota

A biblioteca Essentia, por padrão, adota a convenção de que as notas com acidente se darão pelo sustenino, ou seja,
em seus resultados de extração, nunca haverá um bemol, mas sustenidos em cada saída.

Por exemplo, sabe-se que Lá Sustenido é, muitas vezes, chamado também de Si Bemol, ao utilizar a biblioteca essentia, a saída sempre conterá o acidente em formato de sustenido. Se a afinação do arquivo em que se está executando a analise for Si bemol, no arquivo de saída aparecerá Lá Sustenido.

Para a análise, neste trabalho foram utilizadas as seguintes caracteristicas extraídas das músicas:

- intensidade média (average_loudness)
- batidas por minuto (bpm)
- intensidade das batidas (beats_loudness):
	- média (mean)
	- mediana (median)
	- variancia (var)
	- intensidade mínima (min)
	- intensidade máxima (max)
- danceabilidade (danceability)
- taxa de alteração de acordes por intervalo (chords_changes_rate)
- intervalo de acordes (chords_number_rate)
- taxa de acordes (chords_number_rate)
- força da métrica da afinação (key_strength)
- nota ou afinação (key_key)
- escala da nota da afinação (chords_scale)
- escala dos acordes (chords_scale)

## Extração

Ao definir-se tanto arquivo de perfil quanto características utilizadas, executou-se um programa escrito na linguagem python para extrair as informações do arquivo em lotes, chamado de "extractor.py". Este programa recebe como parâmetro o caminho absoluto no sistema operacional onde os arquivos listados por diretório (conforme citado acima) estão e sua saída para cada arquivo é a seguinte:


```
Extracting 'essentia_streaming_extractor_music' From: '/media/emerson/Dados/nn-musics/indie/01 Is This It.mp3'

Process step: Read metadata
Process step: Compute md5 audio hash and codec
Process step: Replay gain
Process step: Compute audio features
Process step: Compute aggregation
All done
```

Ao final da extração, os resultados foram os seguintes:

```
emerson@vdell-eos:~/projects/tcc$ tree results/ --filelimit=20
results/
├── eletronic [21 entries]
├── grunge [21 entries]
├── hard-rock [21 entries]
├── hip-hop [21 entries]
├── indie [21 entries]
├── metal [21 entries]
├── new-metal [21 entries]
├── pop [21 entries]
├── pop-rock [21 entries]
├── progressive-metal [21 entries]
├── punk [21 entries]
└── ska [21 entries]
```

Entrando na pasta cujo genero é "indie", temos os seguintes arquivos:

```
emerson@vdell-eos:~/projects/tcc$ tree results/indie/
results/indie/
├── 01259a33f7d1ff1cb23ee4db3eabf901.json
├── 014af205c51e9035799f0203f87b9fd7.json
├── 05abf2332e5437f78314f3d922dd6b08.json
├── 0a61bcd4429b9ccc2a3fc27f0a6010d4.json
├── 0e1b96f08b2253bda459b89b4887edf0.json
├── 11a2bc1bf4eacc0d447bd83f0dbab5e5.json
├── 13985b04438ce2bbb042355b77ae829b.json
├── 301bbbdf469826135197865678424eae.json
├── 3261c593e75ca375ed213cc1d34f22c3.json
├── 50137bad97362e033519d36b6cde8e11.json
├── 5925e1dc6118387f3dfe53730158cd7b.json
├── 5e13fbbb7b84b86a76ea72c3f2278fa1.json
├── 7a68c172a8743253fbaf042ae7ae4b67.json
├── 7c64c8127fc476e7cec6ea6867c50e8a.json
├── 9d85e185fe17a2b47ba355662e2a7d8b.json
├── af3585a7e1d126dbecd3cb8d88639a77.json
├── b6a671635b0df3d60356cf82e72dfe86.json
├── d104c091bd2453e8c4f266750c5c196b.json
├── eb4e83ee973e5008922c4c47838afb94.json
├── f067200e68986be6d8abde9ce5d4d639.json
└── f59dde1c4dd658993a6c693f1eb80652.json
```


## Rede Neural Para Classificação de Gênero

### Definição da Rede Neural

Neste trabalho, a abordagem de inteligencia artificial utilizada foi, como descrito nos textos acima, mutil nível de perceptron com backpropagation. Conforme mencionado, redes neurais são um sistema de aprendizagem supervisionada, o que significa que haverá interação com os resultados e avaliação dos mesmos.

Para implementação, utilizou-se a biblioteca pybrain, que permite a criação, treinamento e usdo de redes neurais com backpropagation e multi nivel de perceptrons

Os elementos desse tipo de rede neural são:

- Conjunto de Treinamento Supervisionado
- Agente Treinador (BackpropTrainer)
- Rede Neural em si
	- Quantidade de neuronios
	- Quantidade de camadas
	- Quantidade de saídas esperadas
- Dados de teste

### Normalização de Entradas e Saídas

Antes de iniciar o processo de treinamento e classificação, é necessário definir o pré-processamento dos dados de entrada e saída esperada da rede.

Para este fim, os dados foram normalizados, conforme descrito abaixo.

#### Normalização de Gênero

Para cada gênero, foi atribuido um código numérico, conforme descrito a seguir:

```
GENRE_CODES = {
    "eletronic"         : 1,
    "grunge"            : 2,
    "hard-rock"         : 3,
    "hip-hop"           : 4,
    "indie"             : 5,
    "metal"             : 6,
    "new-metal"         : 7,
    "pop"               : 8,
    "pop-rock"          : 9,
    "progressive-metal" : 10,
    "punk"              : 11,
    "ska"               : 12
}
```

### Saída Esperada

A saída esperada da rede neural é um array (lista) com as probabilidades da música de pertinência em cada gênero.
É importante salientar que por mais que a entrada da música no conjunto de treinamento possa estar categorizada como um gênero, bandas distintas de gêneros diferentes podem ter músicas parecidas com métricias similares.

# ATUALIZAR SCRIPT PRA ACEITAR ENTRADA .mp3

### Primeira Tentativa - MFCC

Após a extração e os arquivos estarem disponíveis em um diretório no sistema operacional, construiu-se um novo programa em python que simula uma rede neural. Este programa lê os arquivos no formato .json extraidos pela biblioteca essentia e, após carregar cada um deles na memória, executa o seguinte procedimento:

```
seja conjuntoTreinamento ct uma lista

para cada arquivo a na pasta p
	identifique os atributos necessários para montagem do conjunto de treinamento an
		ct receba an
```

Após criar o conjunto de treinamento,


### Redes Neurais e Classificação

----

O objetivo deste trabalho é classificar um arquivo de áudio baseado em suas características, extraidas conforme os processos acima descritos mostram. Todavia, a primeira tentativa executada envolvia uma abordagem totalmente diferente, que consistia no mesmo processo de extração e classificação, porém utilizando as métricas MFCC ao invés das características acima citadas.

Todavia, após










## Trabalhos futuros:

Montagem automática dos conjuntos de testes separados em gêneros, baseados nas ID3 tags dos arquivos.
Uma vez que o acervo pessoal de músicas contém todas as ID3 tags em cada arquivo e nelas estão condidos seus gêneros, é possível montar o conjunto de testes automáticamente, desde que as informações do arquivo sejam previamente extraidas.

Treinamento e Classificão usando MFCCs e outroas tags presentes no arquivo final de extração.