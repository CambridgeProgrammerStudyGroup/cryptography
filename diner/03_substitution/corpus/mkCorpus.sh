cat en/* | sed -e 's/<p>//g' -e 's/<h>//g' -e 's/[^a-zA-Z]//g' | tr [a-z] [A-Z] | tr -d '\n' > corpus_en.txt
