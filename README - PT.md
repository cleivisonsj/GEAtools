# GEATools

Esta ferramenta tem o objetivo de aprimorar os resultados obtidos com o programa NDpredict na associação de progenitores/descendentes de galáxias em diferentes redshifts usando a sequência vermelha.

## Pré-requisitos

Antes de usar a ferramenta é recomendável a criação de um ambiente de programação com Python 3.x.x e o R 3.x.x.

É necessário ter os seguintes pacotes instalados no ambiente:
- rpy2
- numpy 
- matplotlib 
- h5py 
- pandas 
- scipy 
- xlsxwriter

Com o Anaconda podem ser instalados com o comando abaixo:
```
conda install -c conda-forge rpy2 numpy matplotlib h5py pandas scipy xlsxwriter
```
Na mesma pasta que foi baixado os arquivos da ferramenta deve conter as bibliotecas NDpredict (https://github.com/sawellons/NDpredict) e o illustris_python (https://github.com/illustristng/illustris_python). Essa última é necessária ser for trabalhar com os dados baixados da simulação Illustris. É importante verificar o funcionamento das bibliotecas seguindo o passo a passo descrito nas páginas do github.

No arquivo config.py, dentro da pasta GEATools, é necessário definir os parâmetros abaixo:
- R_HOME => Caminho da pasta raiz do R
- R_USER => Caminho da pasta raiz do pacote rpy2
- simulation_name => Nome da simulação do Illustris selecionada

Após isso, a ferramenta está pronta para o uso.

## Baixando dados do Illustris

A ferramenta desenvolvida foi testada com os dados da simulação Illustris, e possui scripts que auxiliam na obtenção dos dados disponíveis.

Na pasta Complementary Scripts, com o script down_files.py é possível baixar os dados das simulações do Illustris.

Também nesta pasta, temos o script get_subhalo_descendant_tree.py, necessário para baixar as árvores de descendência dos subhalos que forem ser analisados, em um formato compatível com o programa. O resultado de execução desse script gera a pasta Auxiliary Data, na qual o conteúdo deve ser colocado na mesma pasta presente na raiz do programa.

## Funcionalidades

O script analysis.py ilustra o funcionamento básico da aplicação.

O primeiro passo é importar a biblioteca fazendo:
```
import GEAtools as geat
```

Após, é necessário definir o snapshot/redshift a serem analisados em z0 e zf e o id do subhalo em z0 que será o progenitor/descendente escolhido. No script isso é definido em:
```
snap_num_z0 = 50
snap_num_zf = 53
start_subhalo_z0 = 21 
```

Assim, é obtido o resultado com o NDpredict, fazendo:
```
prog_subhalo_id = start_subhalo_z0
true_desc_subhalo_id = subhalo_descendant_tree[snap_num_zf]
z0 = redshifts[snap_num_z0]
zf = redshifts[snap_num_zf]
M0 = geat.get_subhalo_mass_star(snap_num_z0, prog_subhalo_id)
sample = geat.get_sample(snap_num_zf, 0)
probs_ndp = geat.calc_prob_ndp(sample, z0, zf, M0)
```

E o resultado usando a sequência vermelha:
```
probs_rg = geat.calc_prob_rg(sample, zf)
geat.adjust_probs_scale(probs_rg)
```

Com o resultado obtido com o NDpredict e o RG, pode-se escolher o método de combinação e os valores dos pesos, b1 e b2, para combinar os resultados com o objetivo de melhoria das probabilidades obtidas com o NDpredict. Isso é feito no script em:
```
method = 'kk'
kk = []

b1=0.75
b2=0.25
probs_comb = geat.calc_comb(method, probs_ndp, probs_rg, b1, b2)
```

No script isso também é feito para os outros métodos de combinação disponíveis e pesos.

Ao final da execução do script são gerados gráficos e tabelas com os resultados, essas informações ficam salvas na pasta Results, que é criada ao fim da execução.
