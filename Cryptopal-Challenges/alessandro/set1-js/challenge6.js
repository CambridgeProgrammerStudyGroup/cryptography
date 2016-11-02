var fs = require('fs')
var crypto = require('./crypto.js')

var cipher = Buffer.from(fs.readFileSync("6.txt", "utf8"), "base64")

var scores = crypto.decryptXorWithRepeatedKey(cipher, 40)

var key = scores[0]['key']
console.log(" -- KEY: '" + key + "'")
var decrypted = crypto.xorWithRepeatedKey(cipher, key)
console.log(" -- DECRYPTED TEXT:")
console.log(decrypted.toString())
