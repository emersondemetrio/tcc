Distinct Supergenre

5312	rock
2445	alternative
1791	other
1167	progressive
1077	indie
910		folk
808		metal
753		pop
675		punk
466		blues
270		classic
253		grunge
228		electronic
209		jazz
205		new wave
204		funk
203		hardcore
80		chamber
55		gothic
42		hip hop

- Criar table de teste
-- Pegar 30% de cada supergenre [ OK ]
-- inserir na tabela de teste [ OK ]
-- suply to test no weka

################
RANDOM FOREST: USE TRAINNING SET!
weka.classifiers.trees.RandomForest -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1

--> estudar mfcc-> mean (superficialmente)
--> Estudar parametros principais dos algoritmos (superficial)

http://www.practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/

1o teste:
MFCC + genero --> (nn, rf, j48)

2o teste:
dados q tenho + MFCC + genero --> (nn, rf, j48)

PARA NN

Variar momentum e learningRate de .25 em .25

Outro: Se der tempo: Testar o genero "outro", se nao, nao usar.

Em relação a quantidade de generos: Testar o q for possivel
