# Discombobulator


Sometimes tables contain many different related items. For instance, the following box shows the contents of one cell in a table from [PMID:30057029](https://pubmed.ncbi.nlm.nih.gov/30057029/){:target="_blank"} in a column entitled "dysmorpholoy".


!!! dysmorphology 

    frontal bossing, curled hair, highly arched and sparse eyebrows, long eyelashes, downslanting palpebral fissures, depressed nasal ridge, tented upper lip

While we could create annotations by hand and create one column for each entry in this cell (and all of the other entries in the column), it can be error-prone and time consuming. Therefore, pyphetools has a (currently experimental) feature called "discombobulation", then takes all of the entries in such a cell from each cell in a column, and creates corresponding columns and rows for the standard Excel template file. To do this, we create the following python code.


```python
from pyphetools.creation import Discombobulator, HpoParser
import pandas as pd
parser = HpoParser()
hp_cr = parser.get_hpo_concept_recognizer()
disco = Discombobulator(hpo_cr=hp_cr)
```

This creates a Discombobulator object that can be used for all of the relevant columns of the original supplemental file. Assuming for this example that the original file is called "temp.xslx" and the column of interest is called "face", we would use the following python code.


```python
df = pd.read_excel("temp.xlsx")
df_face = disco.decode(df=df, column="face", assumeExcluded=True)
df_face.head(3)
```

The assumeExcluded argument determines if we call a feature to be absent if it is not mentioned in a certain cell but is mentioned in another cell in the same column. This assumption seems justified for dysmorphology features if the authors state a full examination was conducted.


For now, this function operates one column at a time. We can save the results in an excel file and manually add them to the template file.

```python
df_face.to_excel("temp_face.xlsx")
```

This functionality is currently in an experimental stage and we are exploring ways to make its use easier. We do not recommend using the Decombobualtor unless you are very comfortable with Python and Excel.

There is no need to keep the temporary excel files or python code after creating the main template file.