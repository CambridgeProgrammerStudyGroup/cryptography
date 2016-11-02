module.exports = {
	xorWithChar: xorWithChar,
	decryptXor: decryptXor,
	xorWithRepeatedKey: xorWithRepeatedKey,
	decryptXorWithRepeatedKey: decryptXorWithRepeatedKey
}

function range(start, end) {
	return [...Array(end+1).keys()].slice(start)
}

function xorWithChar (buffer, charCode) {
	var result = Buffer.alloc(buffer.length)
	for (var entry of buffer.entries()) {
		result[entry[0]] = entry[1] ^ charCode
	}
	return result
}

function xorWithRepeatedKey (buffer, key) {
	var result = Buffer.alloc(buffer.length)
	for (var entry of buffer.entries()) {
		result[entry[0]] = entry[1] ^ key.charCodeAt(entry[0] % key.length)
	}
	return result
}

function code(string) {
	return string.charCodeAt(0)
}

function codes(string) {
	return range(0, string.length-1).map(i => string.charCodeAt(i))
}

var lowerCaseCodes = range(code("a"), code("z"))
var upperCaseCodes = range(code("A"), code("Z"))
var whitespaceCodes = [code(" ")]
var punctuationCodes = codes(".,:;-'\"")

var allLetterCodes = upperCaseCodes.concat(lowerCaseCodes)
var allLetterAndWhiteSpaceCodes = allLetterCodes.concat(whitespaceCodes)
var allTextCodes = allLetterAndWhiteSpaceCodes.concat(punctuationCodes)

function countInSet(buffer, codesSet) {
	var count = 0
	for (var code of buffer) {
		if (codesSet.has(code)) {
			count++
		}
	}
	return count
}

function decryptXor(input) {
	var allowedSet = new Set(allTextCodes)
	var scores = allTextCodes.map(function(code) {
		var xored = xorWithChar(input, code)
		var score = countInSet(xored, allowedSet)
		return { 'code': code, 'decrypted': xored, 'score': score }
	})
	scores.sort((x,y) => y['score'] - x['score'])
	return scores
}

function popCount(x) {
	var count;
    for (count=0; x; count++)
        x &= x-1;
    return count;
}

function hammingDistanceStrings(str1, str2) {
	return hammingDistance(Buffer.from(str1, "utf8"), Buffer.from(str2, "utf8"))
}

function hammingDistance(buffer1, buffer2) {
	if (buffer1.length != buffer2.length) {
		return
	}
	
	var distance = 0;
	for (var i = 0; i < buffer1.length; i++) {
		var xor = buffer1[i] ^ buffer2[i]
		distance += popCount(xor)
	}
	return distance
}

function keySizeLikelyhood(cipher, keysize) {
	var slice1 = cipher.slice(0, keysize)
	var slice2 = cipher.slice(keysize, keysize * 2)
	return hammingDistance(slice1, slice2) / keysize
}

function decryptXorWithRepeatedKey(cipher, maxKeyLength) {
	var sorted = range(2, maxKeyLength).map(function(keysize) {
		return { 'keysize': keysize, 'likelyhood': keySizeLikelyhood(cipher, keysize) }
	})
	sorted.sort((x,y) => x['likelyhood'] - y['likelyhood'])

	var scores = sorted.map(x => x['keysize']).map(keysize => {

		var blocks = []
		var blockSize = Math.ceil(cipher.length/keysize)
		for (var offset = 0; offset < cipher.length; offset += blockSize) {
			blocks.push(Buffer.alloc(Math.min(blockSize, cipher.length - offset), ""))
		}
		for (var i = 0; i < cipher.length; i++) {
			blocks[i % keysize][Math.trunc(i / keysize)] = cipher[i]
		}

		var key = ""
		var keySizeScore = 0
		for (var block of blocks) {
			var scores = decryptXor(block)
			var entry = scores[0]

			keySizeScore += entry['score']
			key += String.fromCharCode(entry['code'])
		}

		return { key: key, score: keySizeScore/cipher.length }
	})
	scores.sort((x,y) => y['score'] - x['score'])
	return scores
}