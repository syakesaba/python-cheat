Python-Cheat
===============
Linux cheating tool using python-ptrace.  

** Only work searching, reading, writing. yet.

Depends
===============
* [python-ptrace](https://pypi.python.org/pypi/python-ptrace "Ptrace library for python") - The best debugging tool.
* Optional: [distorm3](http://code.google.com/p/distorm/ "Distorm3 - DisAssembler") - The best disassembler for X86
* Optional: [Capstone](http://www.capstone-engine.org/ "") - ARM compatible disassembler

How to use
======

```sh
apt-get install gcc python-dev
pip install python-ptrace

git clone https://github.com/syakesaba/python-cheat.git
cd python-cheat
sudo python -m cheat.run <pid>
```
