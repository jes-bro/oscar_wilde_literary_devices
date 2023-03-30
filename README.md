# oscar_wilde_literary_devices

oscar_wilde_literary_devices is a repo that performs literary analysis on the work of Oscar Wilde.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install several dependencies, including:
* nltk
* wordcloud
* matplotlib

To install polyglot, another dependency, consult their [documentation](https://polyglot.readthedocs.io/en/latest/Installation.html)

```bash
pip install <"pip dependency">
```

In your terminal, open a python3 intepreter and run:

```bash
import nltk
nltk.download("cmudict")
```
To download the CMU dictionary of phonemes for the alliteration function

## Usage

The oscar_wilde_literary_devices.ipynb file has cells that denote how to use all of our plotting functions. Simply replace the urls in list_of_urls with the ones you care about analyzing to make the functions create plots specific to your data. 

Personally, we used urls from Project Gutenberg that point to text files of Wilde's work. The functions do not have to be specific to Oscar Wilde's work. You can also designate the names of each file in the second element of each tuple in list_of_urls to generate plots with axis labels that correspond to your text.

The utils.py file contains all of the data analysis functions, the plotting.py function contains all plotting functions, and the text_processing.py file contains all data cleaning functions.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.