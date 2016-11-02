var crypto = require('./crypto.js')

var input = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
var key = "ICE"

var encrypted = crypto.xorWithRepeatedKey(Buffer.from(input, "utf8"), key)
console.log(encrypted.toString("hex"))