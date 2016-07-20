cat en/* | sed -e 's/<p>//g' -e 's/<h>//g' -e 's/[-@ \.",):;(#0-9]//g' -e "s/'//g" | tr [a-z] [A-Z] | tr -d '\n' > corpus_en.txt
