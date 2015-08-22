Python-Cheat
===============
Linux cheating tool using python-ptrace.  

** Only work searching, reading, writing. yet.

Depends
===============
* [python-ptrace](https://pypi.python.org/pypi/python-ptrace "Ptrace library for python") - The best debugging tool.
* Optional: [distorm3](http://code.google.com/p/distorm/ "Distorm3 - DisAssembler") - The best disassembler for X86
* Optional: [Capstone](http://www.capstone-engine.org/ "") - ARM compatible disassembler SEE: [here](https://gist.github.com/hugsy/9882f26a8a3323c8ee74#file-python-ptrace_capstone-patch, "")

How to use
======

```sh
apt-get install gcc python-dev
pip install python-ptrace

git clone https://github.com/syakesaba/python-cheat.git
cd python-cheat
sudo python -m cheat.run <pid>
```

CANDO
======
* 固定値サーチ

TODO
======
* 変動サーチ(equal, not equal, less than (equal), greater than (equal))
* malloc動的ポインタ追跡（チートコード）
* 関数サーチ（プログラマブルなサーチ）
* Capstone(distorm3はライブラリ入ってたら使えるけど、Capstone対応は)と連携してバイナリのディスアセンブル
* 
