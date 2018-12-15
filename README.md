# Odyssey Alignment

## Install Dependencies

> python & make required

#### Install Python Packages

```pip install jieba```

#### Install GIZA++

[http://www.statmt.org/moses/giza/GIZA++.html](http://www.statmt.org/moses/giza/GIZA++.html)

**For Mac User**

in giza-pp folder

```make```

Then copy GIZA++, plain2snt.out under *giza++ -v2*, and mkcls under *mkcls* to root directory of Odyssey Alignment Project (in the same directory with run.sh) 

## Generate Alignment results

```python main.py```

This python script will go through each steps and generates final JSON result. During the process, multiply files may be generated. Do not touch any file during the process.

After everything is finished, a couple JSON files will be generated. Each contains an alignment result.

> If you can not complie GIZA++, there is a zip file, contains all aligned data

## View with Web Interface

Run a HTTP server on port **8000** in Odyssey Alignment Project directory (in same directory with all alignment JSON data).

You can use python SimpleHTTPServer or nodejs http-server. (CORS might be a problem for some browser)

**Run with Python SimpleHTTPServer**

```python -m SimpleHTTPServer 8000```

**Run with nodejs http-server**

> You must have nodejs & npm installed

```npm install -g http-server```

```http-server -p 8000 --cors```

under directory *www*, open ```index.html``` with browser.