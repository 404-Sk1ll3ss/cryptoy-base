from math import gcd

from cryptoy.utils import str_to_unicodes, unicodes_to_str

def compute_permutation(a: int, b: int, n: int) -> list[int]:
	return [(a * i + b) % n for i in range (0, n)]

def compute_inverse_permutation(a: int, b: int, n: int) -> list[int]:
	permutation = compute_permutation(a, b, n)
	inv_permutation = [0]*n
	for i in range(0, n):
		inv_permutation[permutation[i]] = i
	return inv_permutation

def encrypt(msg: str, a: int, b: int) -> str:
	unicodes =  str_to_unicodes(msg)
	all_permutation = compute_permutation(a, b, 1114112)
	permutation = [all_permutation[i] for i in unicodes]
	return unicodes_to_str(permutation)

def encrypt_optimized(msg: str, a: int, b: int) -> str:
	unicodes =  str_to_unicodes(msg)
	permutation = [(a * i + b) % 1114112 for i in unicodes]
	return unicodes_to_str(permutation)


def decrypt(msg: str, a: int, b: int) -> str:
	unicodes =  str_to_unicodes(msg)
	all_inv_permutation = compute_inverse_permutation(a, b, 1114112)
	inv_permutation = [all_inv_permutation[y] for y in unicodes]
	return unicodes_to_str(inv_permutation)


def decrypt_optimized(msg: str, a_inverse: int, b: int) -> str:
	unicodes =  str_to_unicodes(msg)
	inv_permutation = [(a_inverse*(y - b)) % 1114112 for y in unicodes]
	return unicodes_to_str(inv_permutation)


def compute_affine_keys(n: int) -> list[int]:
	return [i for i in range(0, n) if gcd(i, n) == 1]


def compute_affine_key_inverse(a: int, affine_keys: list, n: int) -> int:
	for item in affine_keys:
		if(a * item % n == 1):
			return item
	raise RuntimeError(f"{a} has no inverse")


def attack() -> tuple[str, tuple[int, int]]:
	s = "࠾ੵΚઐ௯ஹઐૡΚૡೢఊஞ௯\u0c5bૡీੵΚ៚Κஞїᣍફ௯ஞૡΚր\u05ecՊՊΚஞૡΚՊեԯՊ؇ԯրՊրր"
	for item in compute_affine_keys(58):
		decrypted = decrypt(s, item, 58)
		if ("bombe" in decrypted):
			return (decrypted, (item, 58))
	raise RuntimeError("Failed to attack")


def attack_optimized() -> tuple[str, tuple[int, int]]:
	s = (
		"જഏ൮ൈ\u0c51ܲ೩\u0c51൛൛అ౷\u0c51ܲഢൈᘝఫᘝా\u0c51\u0cfc൮ܲఅܲᘝ൮ᘝܲాᘝఫಊಝ"
		"\u0c64\u0c64ൈᘝࠖܲೖఅܲఘഏ೩ఘ\u0c51ܲ\u0c51൛൮ܲఅ\u0cfc\u0cfcඁೖᘝ\u0c51"
	)
	key_list = compute_affine_keys(1114112)
	for count, value in enumerate(key_list):
		print("a:", count, "/", len(key_list))
		try:
			value_1 = compute_affine_key_inverse(value, key_list, 1114112)
		except:
			continue
		for index in range(1, 10001):
			decrypted = decrypt_optimized(s, value_1, index)
			if ("bombe" in decrypted):
				return (decrypted, (value, index))
	raise RuntimeError("Failed to attack")
