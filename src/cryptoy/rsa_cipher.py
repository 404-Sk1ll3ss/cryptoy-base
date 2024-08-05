from math import gcd

from cryptoy.utils import draw_random_prime,int_to_str,modular_inverse,pow_mod,str_to_int


def keygen() -> dict:
	e = 65537
	p = draw_random_prime()
	q = draw_random_prime()
	d = modular_inverse(e, (p - 1) * (q - 1))
	return { "public_key": (e, p * q), "private_key": d }


def encrypt(msg: str, public_key: tuple) -> int:
	num = str_to_int(msg)
	if (num >= public_key[1]):
		raise RuntimeError("num >= public_key[1]")
	e = public_key[0]
	N = public_key[1]
	return pow_mod(num, e, N)


def decrypt(msg: int, key: dict) -> str:
	d = key["private_key"]
	N = key["public_key"][1]
	return int_to_str(pow_mod(msg, d, N))
