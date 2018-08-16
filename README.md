# SimpleDBpediaQA
This repo contains the data for the following paper:
- Michael Azmy, Peng Shi, Ihab Ilyas, and Jimmy Lin. [Farewell Freebase: Migrating the SimpleQuestions Dataset to DBpedia](http://aclweb.org/anthology/C18-1178). Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018), August 2018, Santa Fe, New Mexico.

## Get started

To generate entity labels (IO scheme), you need to install *fuzzywuzzy* lib.

```
pip install fuzzywuzzy
```

and then run

```
cd script
python reverse_linking.py
```

and *train.txt/valid.txt/test.txt* will be generated in *V1* fold and you are ready to go.



 
