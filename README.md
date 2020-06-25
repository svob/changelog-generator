### Changelog generator
Generates readme file from yaml source files to prevent merge conflicts.

Inspired by [GitLab's solution](https://about.gitlab.com/blog/2018/07/03/solving-gitlabs-changelog-conflict-crisis/)

#### Usage
Install required dependencies globally or in virtual environment
```
$ python -m pip install -r requirements.txt 
```

```
$ python main.py -h
usage: main.py [-h] [-d] [-o] [--dry-run] [--version]

Generate changelog

optional arguments:
  -h, --help      show this help message and exit
  -d              input directory
  -o , --output   output directory
  --dry-run       doesn't write or comit anything, just print to output
  --version, -v   show program's version number and exit
```

To generate readme from provided test data run

```commandline
python main.py -d ./test_data/changelog/
```
