#!/usr/bin/env python3
import re, sys
import cheat

def main(pattern, bench, in_file="scrabble.txt", out_file="out.txt"):
	# filter file
	words = filter_file(pattern, bench, in_file)
	# check filtered words for letter count
	words = check_filtered(pattern, bench, words)
	# write to file
	with open(out_file, "w") as f:
		for word in words:
			f.write(word + "\n")

def create_regex(pattern, bench):
	# replaces wildcards with appropriate character class
	pattern = pattern.replace(".", "[" + bench + "]")

	# makes sure that the word is not a section of another word by anchoring it
	pattern = "^" + pattern + "$"

	return re.compile(pattern, re.MULTILINE|re.IGNORECASE)

def filter_file(pattern, bench, in_file):
	# creates a regex
	search = create_regex(pattern, bench)

	# reads the file and gets all the valid words
	with open(in_file) as f:
		words = search.findall(f.read().lower())

	return words

def check_filtered(pattern, bench, words):
	# find locations of . in pattern and build a word mask from that data
	# adapted from Salvador Dali at https://stackoverflow.com/a/32794963
	mask = [pos for pos, char in enumerate(pattern) if char == "."]

	valid_words = []
	for word in words:
		letters = {}
		# count letters not masked
		for c in mask:
			if word[c] in letters:
				letters[word[c]] += 1
			else:
				letters[word[c]] = 1
		# if the count does not violate the bench, append to a new list
		valid = True
		for letter, count in letters.items():
			if count > bench.count(letter):
				valid = False
		if valid:
			valid_words.append(word)
	return valid_words

if __name__ == "__main__":
	# Checks to make sure that the proper format is supplied
	args = sys.argv
	if len(args) != 5:
		print("Usage: ./find_words.py <pattern> <bench> <in_file> <out_file>")
		sys.exit()

	main(args[1], args[2], args[3], args[4])
