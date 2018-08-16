# SimpleDBpediaQA

This repo contains data from the following paper:

- Michael Azmy, Peng Shi, Ihab Ilyas, and Jimmy Lin. [Farewell Freebase: Migrating the SimpleQuestions Dataset to DBpedia](http://aclweb.org/anthology/C18-1178). Proceedings of the 27th International Conference on Computational Linguistics (COLING 2018), pages 2093-2103, August 2018, Santa Fe, New Mexico.

## Get started

To generate entity labels (IO scheme), you need to install the Python *fuzzywuzzy* library:

```
pip install fuzzywuzzy
```

and then run:

```
cd script
python reverse_linking.py
```

The script generates `train.txt`, `valid.txt`, and `test.txt` in the `V1/` folder and you're good to go!
