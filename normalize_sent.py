import sys
from tsm.sentence import Sentence
for line in sys.stdin.readlines():
    line = Sentence.normalize(line)
    sys.stdout.write(f"{line}\n")
