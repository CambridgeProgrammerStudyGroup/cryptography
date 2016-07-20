var fs = require('fs');
var _ = require('lodash');
var freq_en = require('./frequencies/en')

var cipher = fs.readFileSync('../../01-Substitution/03-substitution/cipher.txt');
var MR_TINY = 1e-10;

function getCharacterFrequency(buffer) {
  var frequencies = {};

  Array.from(buffer.entries())
    .map(function(pair){
      return String.fromCharCode(pair[1]);
    })
    .filter(function(letter){
      return !/\s/.test(letter);
    })
    .forEach(function(letter) {
      if (letter in frequencies) {
        frequencies[letter]++;
      } else {
        frequencies[letter] = 1;
      }
    });

  var pairs = _.toPairs(frequencies);
  var pairsOrdered = _.sortBy(pairs, function(pair) { return pair[1]; });

  return pairsOrdered;
}

function getNGramFrequencies(buffer, n) {
  var frequencies = {};

  var filteredCharacters = Array.from(buffer.entries())
    .map(function(pair){
      return String.fromCharCode(pair[1]);
    })
    .filter(function(letter){
      return !/\s/.test(letter);
    });

  var range = (filteredCharacters.length > n)?_.range(0, filteredCharacters.length - n):[];


  range.forEach(function(index) {
    var slicedStrArr = filteredCharacters.slice(index, index + n);

    var str = slicedStrArr.join("");
    if (str in frequencies) {
      frequencies[str]++;
    } else {
      frequencies[str] = 1;
    }
  });

  var pairs = _.toPairs(frequencies);
  var pairsOrdered = _.sortBy(pairs, function(pair) { return pair[0]; });

  return pairsOrdered;
}

function displayFrequencies(freqs, n) {
  console.log(freqs);
  console.log("Length: " + freqs.length);
  console.log("Max:" + nCk(26, n));
}

function factorial(n) {
   return _.reduce(_.range(1, n+1), _.multiply);
}

function nCk(n, k) {
  return factorial(n)/(factorial(k)*(factorial(n-k)));
}

// Kullback Leibler Divergence (discrete)
function klDivergence(orderedReferenceCounts, orderedUnderTestCounts) {
  var pad_length = orderedReferenceCounts.length-orderedUnderTestCounts.length;
  var padding = Array.apply(null, Array(Math.abs(pad_length))).map(function(){return MR_TINY;});

  if(orderedReferenceCounts.length<orderedUnderTestCounts.length){
    orderedReferenceCounts = padding.concat(orderedReferenceCounts);
  }else{
    orderedUnderTestCounts = padding.concat(orderedUnderTestCounts);
  }
  return _.sum(_.zipWith(orderedReferenceCounts, orderedUnderTestCounts, function(r,t) {
    return r * Math.log(r/t);
  }));
}

function biGramFreq2normalisedCounts(biGramFreq){
  var counts = biGramFreq.map(function(item){return item[1];});
  var total = _.sum(counts);
  return counts.map(function(count){return count/total;});
}

function makeTranslationTable(cipherGrams, englishgrams){
  var l = _.min([cipherGrams.length, englishgrams.length]);
  return _.zip(_.takeRight(cipherGrams, l), _.takeRight(englishgrams, l))
    .reduce(function(acc, countPair){
      var cipherPair = countPair[0];
      var englishPair = countPair[1];
      var mapping = {}
      mapping[cipherPair[0]] = englishPair[0];
      return _.assign(acc, mapping);
    }, {});
}

function table2mapper(table){
  return function(c){
    // var c = String.fromCharCode(c);
    if(c in table){
      return table[c];
    }
    return c;
  }
}

function fitness(translationTable, cipherText, standard){
  // console.log("=== cipher")
  // console.log(cipherText);

  var attempt = _(cipherText).map(table2mapper(translationTable)).value().join('');
  // console.log("=== attempt")
  // console.log(attempt);

  var normalized_counts_attempt = biGramFreq2normalisedCounts(getNGramFrequencies(new Buffer(attempt, 'utf8'), 2));
  // console.log(normalized_counts_attempt)
  return klDivergence(standard.normalised_counts, normalized_counts_attempt);
}

function printWith(table, cipher){
  console.log(_(cipher).map(table2mapper(table)).value().join(''));
}

function main() {
  var oneGram = getNGramFrequencies(cipher, 1);
  var biGram = getNGramFrequencies(cipher, 2);
  var triGram = getNGramFrequencies(cipher, 3);

  var corpusEn = fs.readFileSync('./corpus/en/corpus_en.txt');
  var en_standard= {};

  if(fs.existsSync("en.dat.json")){
    en_standard = JSON.parse(fs.readFileSync("en.dat.json").toString());
  }else{

    en_standard = {
      oneGram : getNGramFrequencies(corpusEn, 1),
      normalised_counts : biGramFreq2normalisedCounts(getNGramFrequencies(corpusEn, 2))
    };
    fs.writeFileSync("en.dat.json", JSON.stringify(en_standard));
  }

  var normalized_counts_cipher = biGramFreq2normalisedCounts(getNGramFrequencies(cipher, 2));
  // console.log(klDivergence(en_standard.normalised_counts, en_standard.normalised_counts));
  // console.log(klDivergence(en_standard.normalised_counts, normalized_counts_cipher));


  var translationTable = makeTranslationTable(oneGram, en_standard.oneGram);
  var noTranslation = makeTranslationTable(en_standard.oneGram, en_standard.oneGram);

  console.log(fitness(noTranslation, corpusEn.toString(), en_standard))
  console.log(fitness(translationTable, cipher.toString(), en_standard))
  console.log(fitness(noTranslation, cipher.toString(), en_standard))

  /* The ordering of the bigram frequencies that we're getting (with getNGramFrequencies) isn't stable.
     We need to find a way to use the map between the frequencies directly,
      without having to worry about the ordering /*
}

main();
