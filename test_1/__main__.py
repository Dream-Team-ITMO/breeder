from test_1.testing.work_n_fun.fun import *
import test_1.testing.work_n_fun.work

try:
    print(open('.SELF/README.md').read())
except (IOError, OSError):
    print("Rats, no README")

print(Fun())
print(test_1.testing.work_n_fun.work.Work())
