#!/usr/bin/env python

import random
import string

punctuation = '!#$%&()*+,-./:;<=>?@^_{|}~'
choices = string.ascii_letters + string.digits + punctuation
selected = [random.SystemRandom().choice(choices) for _ in range(50)]
generated_key = ''.join(selected)
print(generated_key)
