import string
import random


def get_rand_str(str_size=10):
	allowed_chars = string.ascii_letters + string.punctuation
	return ''.join(random.choice(allowed_chars) for x in range(str_size))
