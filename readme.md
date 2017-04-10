# Vera ![lahacks badge](https://img.shields.io/badge/lahacks-rocks-ff69b4.svg)

An artificial intelligence system based on machine learning and linguistic analysis to determine if a given statement is true or false.

Nowadays, information is more accessible than ever. Often, people are surrounded with information from a million different sources, each claiming something or another. Along with these unstable times in our country, we determined that there should be a way to check the validity of a statement.

At LAHacks 2017, we built an artificial intelligence system that uses machine learning from the Microsoft Cognitive Services to help determine whether a given statement is true or false.

Check it out at [verafy.herokuapp.com](verafy.herokuapp.com).

<img width="1680" alt="screen shot 2017-04-02 at 7 22 51 am" src="https://cloud.githubusercontent.com/assets/7104017/24588013/47be8d7e-1775-11e7-995a-03c936cc7bc1.png">

## How it works

We used Microsoft Cognitive Services (MCS) Language Analytics to pick apart the parts of speech in the statement, and break it down in subject, verb, and descriptor (e.g. The sky (subject) is (verb) blue (descriptor)). The statement is subject to several algorithms. 

1. Firstly, we check if MCS Web Language Model can predict one half of the statement from the first half (making it likely to be true). For example, we can predict that “1919” will likely follow the phrase “UCLA was founded in”. 

2. Second, we check whether the negative version of the statement is more or less likely to be predicted by MCS, using Big Huge Thesaurus to find antonyms. With Vera.fy, we were able to validate Donald Trump’s quote that “there has been a tremendous surge of optimism in the business world” using our second method. 

3. Thirdly, we deployed our own API with Wolfram’s Cloud Development Platform to identify the topic of the statement, find descriptors in the same category and compare them with the current descriptor with MCS to see which one is the most plausible. For example, in the phrase, “Boeing is an aerospace company” is a much likely statement than: Boeing is an agricultural company. 

4. Finally, if all else fails, we determine the validity of the statement based on how likely MCS the words in the sentence to follow each other. For example, “Obama hates cheese.“ is just not a very common sentence.

We also account for negation in the statements and for a completely true sentence, not a partially true sentence.
We are still improving the AI, and hope to make it process more complex sentences, and differentiate common myths (e.g. “Obama was not born in America”) from popular truths.

## Technologies Used

Built using Python and Django. Connected with Microsoft Cognitive Services API, Wolfram API, and [Big Huge Thesaurus](https://words.bighugelabs.com/api.php).

Deployed using Heroku.

## Contributors

[Kyle](https://github.com/kdpatters) & [Alex](https://github.com/alexcdot) & [Ankur](https://github.com/ankurpapneja) & [Neeraj](https://github.com/n3a9)
