from .fun import Fun
from testing.config.duck import duck

class Work(object):
  def __str__(self):
    print(duck())
    return "I am boring!"
