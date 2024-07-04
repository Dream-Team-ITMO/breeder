# breeder

![Snakey](snakey.png)

This is a quick-and-dirty tool for combining multiple .py files into a single script, making it easier to distribute/deploy/encode/encrypt Python scripts along with their dependencies.

Usage examples:
1. Combine all .py files in a directory `my_module/` into `my_module/breeded.py` without compression and encoding:
```sh
python3 breeder.py my_module/
```
2. Combine all .py files in a directory `my_module/` into `./out.py` with compression and encoding:
```sh
python3 breeder.py --compress --out out.py my_module/
```

Full usage help message:
```
usage: TheBreeder [-h] [--compress] [--out OUT] directory

Tool for breeding Python projects

positional arguments:
  directory   Directory with project to breed

options:
  -h, --help  show this help message and exit
  --compress  Compress and base64 the source code
  --out OUT   Output file (default is "directory/breeded.py")
```

---

Studcamp Yandex x ITMO 2024
