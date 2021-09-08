#!/usr/bin/python
################################################################################
# Vrutha Sahayi - An application that helps one to find/check the "vrutham"
# (metrics) of a given Malayalam poem.
#
# Authors:	Sanjeev Kozhisseri <sanjvkoz@yahoo.com>
#			Sushen V Kumar <sushku@yahoo.com>
#
# Vrutha Sahayi is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Vrutha Sahayi is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Vrutha Sahayi; if not, write to the
#				 Free Software Foundation, Inc.,
#				 51 Franklin St, Fifth Floor,
#				 Boston, MA  02110-1301 USA
################################################################################
from syllable import *
from utils import *

def findCharType(sylChars):
	sylCharCount = len(sylChars)
	#print ("findCharType", sylCharCount)
	if (sylCharCount == 1):
		if sylChars[0] in ['\u0d06', '\u0d08', '\u0d0a', '\u0d0f', '\u0d10', '\u0d13', '\u0d14']:
			return 'sg'	# Independent vowels (AA, II, UU, EE, AI, AU)
		elif sylChars[0] in ['\u0d7a', '\u0d7b']:
			return 'nch'	# n chillu
		elif sylChars[0] in ['\u0d7c', '\u0d7d', '\u0d7e', '\u0d7f']:
			return 'rlch'	# rl chillu
		else:
			return 'sl'
	elif (sylCharCount == 2):
		if '\u0d4d' in sylChars:
			# special case for chillu
			for oneChar in sylChars:
				if oneChar in ['\u0d23', '\u0d28']:
					return 'nch'
				if oneChar in ['\u0d30', '\u0d31', '\u0d32', '\u0d33']:
					return 'rlch'
				if (oneChar >= '\u0d15' and oneChar <= '\u0d39'):
					return 'hc'			# Half consonant
			return 'sl'					# Will not come here
		for oneChar in sylChars:
			if oneChar in ['\u0d3e', '\u0d40', '\u0d42', '\u0d47', '\u0d48', '\u0d4b', '\u0d4c', '\u0d57', '\u0d02', '\u0d03']:
				return 'sg' # Dependent vowels (AA, II, UU, EE, AI, OO, AU), ANUSVARA, VISARGA
			if oneChar in ['\u0d7a', '\u0d7b', '\u0d7c', '\u0d7d', '\u0d7e', '\u0d7f']:
				return 'sg' # vowel followed by chillu
		return 'sl'
	elif (sylCharCount == 3):
		if '\u0d4d' in sylChars:
			if '\u0d41' in sylChars:
				return 'sl'
			elif '\u200d' in sylChars:
				for oneChar in sylChars:
					if oneChar in ['\u0d23', '\u0d28']:
						return 'nch'
					if oneChar in ['\u0d30', '\u0d31', '\u0d32', '\u0d33']:
						return 'rlch'
			elif '\u200c' in sylChars:
				for oneChar in sylChars:
					if (oneChar >= '\u0d15' and oneChar <= '\u0d39'):
						return 'hc'			# Half consonant
				return 'sl'
			else:
				return 'kl'
		for oneChar in sylChars:
			if oneChar == '\u0d46':
				for anotherChar in sylChars:
					if anotherChar in ['\u0d3e']:
						return 'sl'
					else:
						return 'sg'
			elif oneChar == '\u0d47':
				return 'sg'
			if oneChar in ['\u0d7a', '\u0d7b', '\u0d7c', '\u0d7d', '\u0d7e', '\u0d7f']:
				return 'sg' 
		return 'sg'
	else:											# If sylCharCount is 4 or more
		if sylChars[0] in ['\u0d23', '\u0d28', '\u0d30',  '\u0d31', '\u0d32', '\u0d33'] and sylChars[1] == '\u0d4d' and sylChars[2] == '\u200d':
			return 'ccc'							# Chillu before consonant combo. Extra special case
		if '\u0d46' in sylChars:					# Dependent vowel sign E
			if '\u0d3e' in sylChars:				# Dependent vowel sign AA
				return 'kl'							# Case: KO
			elif '\u0d57' in sylChars:				# Dependent vowel sign AU
				return 'kg'							# Case: KAU
		for oneChar in sylChars:
			if oneChar in ['\u0d3e', '\u0d40', '\u0d42', '\u0d47', '\u0d48', '\u0d4b', '\u0d4c', '\u0d02', '\u0d03']:
				return 'kg'
			if oneChar in ['\u0d7a', '\u0d7b', '\u0d7c', '\u0d7d', '\u0d7e', '\u0d7f']:
				return 'kg' 
		return 'kl'

def getMatraArray(uniPadyam):
	strippedPadyam = changeNewLineToPipe(uniPadyam)
	charCount = len(strippedPadyam)
	prev = 0
	sylCount = 0
	lineSylCount = 0
	prevType = ' '
	glArray = []
	sylArray = []
	while (prev < charCount):
		if not isMal(strippedPadyam[prev]):
			prev = prev + 1
			continue
		if (strippedPadyam[prev] == '|'):							# If end of a line
			lineSylCount = 0
			glArray.append('|')										# Append '|' in glArray to mark end of line
			sylArray.append((-1,-1))								# Append (-1,-1) in sylArray to mark end of line
			prevPrevType = prevType
			prevType = '|'
			prev = prev + 1
			sylCount = sylCount + 1
			continue
		syllable = findSyllable(strippedPadyam, prev, charCount)
		sylList = strippedPadyam[prev:syllable]
		charType = findCharType(sylList)
		#print("strippedPadyam", strippedPadyam)
		#print("sylList", sylList)
		#print("charType", charType)
		if (charType == 'sl'):
			glArray.append('v')
			sylArray.append((prev,syllable-1))
		elif (charType == 'sg'):
			glArray.append('-')
			sylArray.append((prev,syllable-1))
		elif (charType == 'kl'):
			if (sylCount > 0):
				if (lineSylCount > 0):
					glArray[sylCount - 1] = '-'
			glArray.append('v')
			sylArray.append((prev,syllable-1))
		elif (charType == 'kg'):
			if (sylCount > 0):
				if (lineSylCount > 0):
					glArray[sylCount - 1] = '-'
			glArray.append('-')
			sylArray.append((prev,syllable-1))
		elif (charType == 'nch'):						# Type nch (Chillu n, N)
			if (sylCount > 0) and (lineSylCount > 0):
				glArray[sylCount - 1] = '-'
				sylArray[sylCount -1] = sylArray[sylCount -1][0], syllable - 1
				sylCount = sylCount - 1
		elif (charType == 'rlch'):						# Type rlch (Chillu r, R, l, L)
			if (sylCount > 0) and (lineSylCount > 0):
				if glArray[sylCount - 1] != '-':
					glArray[sylCount - 1] = 'c'
				sylArray[sylCount -1] = sylArray[sylCount -1][0], syllable - 1
				sylCount = sylCount - 1
		elif (charType == 'hc'):						# Half consonant
			if (sylCount > 0) and (lineSylCount > 0):
				glArray[sylCount - 1] = '-'
				sylArray[sylCount -1] = sylArray[sylCount -1][0], syllable - 1
				sylCount = sylCount - 1
		else:											# Chillu before consonant combo. Extra special case
			if (sylCount > 0) and (lineSylCount > 0):
				if glArray[sylCount - 1] != '-':
					glArray[sylCount - 1] = 'c'
				sylArray[sylCount -1] = sylArray[sylCount -1][0], sylArray[sylCount -1][1] + 3
				sylCount = sylCount - 1
				syllable = prev + 3
		prev = syllable
		prevPrevType = prevType
		prevType = charType
		lineSylCount = lineSylCount + 1
		sylCount = sylCount + 1
	return glArray, sylArray
