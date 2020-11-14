echo "put this script into your constraintProgramming_learn/"
echo "ok je suis en" $PWD "* * Ici Mistral pour ton xml * *"
 
#read thisxml 

#if [ ! -d ./Mistral-2.0 ];then 
#	git clone https://github.com/ehebrard/Mistral-2.0/
#	cd Mistral-2.0/
#	make
#	echo "====> ignore flatzinc(on va pas l'utiliser), ok compilation"
#	echo ""
#fi
if [ ! -d BENCHMARKdataB ];then
	mkdir BENCHMARKdataB
fi;

echo "running mistral on xml files"

printf "generating xml models"

for jsonfile in SubisomorphismB_/*.json; do
	echo $jsonfile
	python3 Subisomorphism.py -data=$jsonfile
	echo ""
done;
mv *.xml BENCHMARKdataB/
echo "===== running solver on generated xml files ==="

log=BENCHMARKoutputB.txt #save all output into a file 
printf "BENCHMARK RESULTS\n" > $log
for xmlfile in BENCHMARKdataB/*.xml; do
	echo $xmlfile >> $log
	echo $xmlfile
	Mistral-2.0/bin/MistralXCSP --print_sta $xmlfile >> $log
	#Mistral-2.0/bin/MistralXCSP $xmlfile
done;
echo "all xml files processed ! :) bye"
echo " ****************** "

