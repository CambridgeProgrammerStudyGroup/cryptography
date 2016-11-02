var crypto = require('./crypto.js')

var input = Buffer.from("1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736", "hex")
console.log(input.toString())

var scores = crypto.decryptXor(input)
var entry = scores[0]
console.log(String.fromCharCode(entry['code']) + ": " + entry['decrypted'].toString() + ": " + entry['score'])

