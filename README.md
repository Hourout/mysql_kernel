# Mysql_kernel

![PyPI version](https://img.shields.io/pypi/pyversions/mysql_kernel.svg)
![Github license](https://img.shields.io/github/license/Hourout/mysql_kernel.svg)
[![PyPI](https://img.shields.io/pypi/v/mysql_kernel.svg)](https://pypi.python.org/pypi/mysql_kernel)
![PyPI format](https://img.shields.io/pypi/format/mysql_kernel.svg)
![contributors](https://img.shields.io/github/contributors/Hourout/mysql_kernel)
![downloads](https://img.shields.io/pypi/dm/mysql_kernel.svg)

Mysql Kernel for Jupyter

[中文介绍](document/chinese.md)

## Installation

#### step1:
```
pip install mysql_kernel
```

To get the newest one from this repo (note that we are in the alpha stage, so there may be frequent updates), type:

```
pip install git+git://github.com/Hourout/mysql_kernel.git
```

#### step2:
Add kernel to your jupyter:

```
python -m mysql_kernel.install
```

ALL DONE! 🎉🎉🎉

## Uninstall

#### step1:

View and remove mysql kernel
```
jupyter kernelspec list
jupyter kernelspec remove mysql
```

#### step2:
uninstall mysql kernel:

```
pip uninstall mysql-kernel
```

ALL DONE! 🎉🎉🎉


## Using

```
jupyter notebook
```
<img src="image/mysql1.png" width = "700" height = "300" />

### step1: you should set mysql host and port
```
mysql://user:password@host:port

or

mysql://host:port
```

### step2: write your mysql code

![](image/mysql2.png)

## Quote 
kernel logo

<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fk.kakaocdn.net%2Fdn%2FyZrl5%2FbtqwEwV2HHb%2Fd8u9PLWcIxXLJ8BkqvV881%2Fimg.jpg" width = "32" height = "32" />

- https://jeongw00.tistory.com/203
