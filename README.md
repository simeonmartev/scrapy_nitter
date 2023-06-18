# Scrapy exemplary project to crawl nitter.it

## Instalation 
1. Install python virtual env:
    - https://virtualenvwrapper.readthedocs.io/en/latest/install.html
2. Make virtual env:
    - https://virtualenvwrapper.readthedocs.io/en/latest/install.html#quick-start

```sh
# on linux or mac
mkdir scrapy_nitter
cd scrapy_nitter
mkvirtualenv -a `pwd` --python `which python3.11` `basename "$PWD"`
# the above comand is the same as:
# mkvirtualenv -a /Users/simeonmartev/ws/test/scrapy_nitter  --python /opt/homebrew/bin/python3.11 scrapy_nitter

# activate the envairoment
workon scrapy_nitter
```

3. Installing requirements
```sh
pip install -r requirements.txt
```

4. Run scrapy commands and crawl
```
scrapy list
# > nitter

scrapy crawl nitter
```
