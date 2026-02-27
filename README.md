# NRCLex

(C) 2019 Mark M. Bailey, PhD

## About
NRCLex measures emotional affect from text. Affect dictionary contains approximately 27,000 words and is based on the National Research Council Canada (NRC) affect lexicon and NLTK WordNet synonym sets.

Lexicon source is (C) 2016 National Research Council Canada (NRC) and this package is **for research purposes only**. Source: http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm As per the terms of use of the NRC Emotion Lexicon, if you use the lexicon or any derivative from it, cite this paper: Crowdsourcing a Word-Emotion Association Lexicon, Saif Mohammad and Peter Turney, Computational Intelligence, 29 (3), 436-465, 2013.

NLTK data is (C) 2019, NLTK Project. Source: [NLTK](https://www.nltk.org/). Reference: Bird, Steven, Edward Loper and Ewan Klein (2009), Natural Language Processing with Python. O’Reilly Media Inc.

## Installation
`pip install NRCLex`

## Affects
Emotional affects measured include:

* fear
* anger
* anticipation
* trust
* surprise
* positive
* negative
* sadness
* disgust
* joy

## Sample Usage

`from nrclex import NRCLex`

Instantiate NRCLex object. By default this loads the bundled lexicon packaged with the library:

`text_object = NRCLex()`

You can pass your raw text to this method (for best results, text should be unicode):

`text_object.load_raw_text(text: str)`

You can pass already tokenized text as a list of tokens. This usage does not require TextBlob tokenization:

`text_object.load_token_list(list_of_tokens: list)`

Return words list:

`text_object.words`

Return sentences list:

`text_object.sentences`

Return affect list:

`text_object.affect_list`

Return affect dictionary:

`text_object.affect_dict`

Return raw emotional counts:

`text_object.raw_emotion_scores`

Return highest emotions:

`text_object.top_emotions`

Return affect frequencies:

`text_object.affect_frequencies`
