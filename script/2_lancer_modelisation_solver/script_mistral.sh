#### 4 benchmarck possibles 
#1: graph orienté benchmark1 
#2: graph non orienté benchmark1
#3: graph orienté benchmark2 dit B
#4: graph non orienté benchmark2 dit B


 
#echo "Dowload Mistral"

#if [ ! -d ../../Mistral-2.0 ];then 
#	cd ../..
#	git clone https://github.com/ehebrard/Mistral-2.0/
#	cd Mistral-2.0/
#	make
#	echo "====> ignore flatzinc(on va pas l'utiliser), ok compilation"
#	echo ""
#fi

#1: graph orienté benchmark1 
echo "#1: graph orienté benchmark1"
if [ ! -d ../../BENCHMARKdata_arc ];then
	mkdir BENCHMARKdata_arc
fi;

echo "generating xml models with json files"


#for jsonfile in ../../fichiers_json/Subisomorphism_/*.json; do
#	echo $jsonfile
#	python3 Subisomorphism.py -data=$jsonfile
#	echo ""
#done;
mv *.xml ../../BENCHMARKdata_arc/

echo "===== running solver on generated xml files ==="

log=../../résultat/BENCHMARK_arcoutput.txt #save all output into a file 
printf "BENCHMARK RESULTS\n" > $log
for xmlfile in ../../BENCHMARKdata_arc/*.xml; do
	echo $xmlfile >> $log
	echo $xmlfile
	../../Mistral-2.0/bin/MistralXCSP --print_sta $xmlfile >> $log
	#Mistral-2.0/bin/MistralXCSP $xmlfile
done;
echo "all xml files processed ! :) bye"
echo " ****************** "


#2: graph non orienté benchmark1
echo "#2: graph non orienté benchmark1"
if [ ! -d ../../BENCHMARKdata ];then
	mkdir BENCHMARKdata
fi;

echo "generating xml models with json files"

#for jsonfile in ../../fichiers_json/Subisomorphism_/*.json; do
#	echo $jsonfile
#	python3 Subisomorphism.py -data=$jsonfile
#	echo ""
#done;

mv *.xml ../../BENCHMARKdata/
echo "===== running solver on generated xml files ==="

log=../../résultat/BENCHMARK_output.txt #save all output into a file 
printf "BENCHMARK RESULTS\n" > $log
for xmlfile in ../../BENCHMARKdata/*.xml; do
	echo $xmlfile >> $log
	echo $xmlfile
	../../Mistral-2.0/bin/MistralXCSP --print_sta $xmlfile >> $log
	#Mistral-2.0/bin/MistralXCSP $xmlfile
done;
echo "all xml files processed ! :) bye"
echo " ****************** "

#3: graph orienté benchmark2 dit B
echo "#3: graph orienté benchmark2 dit B"

if [ ! -d ../../BENCHMARKdata_arcB ];then
	mkdir BENCHMARKdata_arcB
fi;

echo "generating xml models with json files"

#for jsonfile in ../../fichiers_json/SubisomorphismB_/*.json; do
#	echo $jsonfile
#	python3 Subisomorphism.py -data=$jsonfile
#	echo ""
#done;
mv *.xml ../../BENCHMARKdata_arcB/
echo "===== running solver on generated xml files ==="

log=../../résultat/BENCHMARKoutput_arcB.txt #save all output into a file 
printf "BENCHMARK RESULTS\n" > $log
for xmlfile in ../../BENCHMARKdata_arcB/*.xml; do
	echo $xmlfile >> $log
	echo $xmlfile
	../../Mistral-2.0/bin/MistralXCSP --print_sta $xmlfile >> $log
	#Mistral-2.0/bin/MistralXCSP $xmlfile
done;
echo "all xml files processed ! :) bye"
echo " ****************** "

#4: graph non orienté benchmark2 dit B
echo"#4: graph non orienté benchmark2 dit B"

if [ ! -d ../../BENCHMARKdataB ];then
	mkdir BENCHMARKdataB
fi;

echo "generating xml models with json files"

#for jsonfile in ../../fichiers_json/Subisomorphism_/*.json; do
#	echo $jsonfile
#	python3 Subisomorphism.py -data=$jsonfile
#	echo ""
#done;

mv *.xml ../../BENCHMARKdataB/
echo "===== running solver on generated xml files ==="

log=../../résultat/BENCHMARKoutputB.txt #save all output into a file 
printf "BENCHMARK RESULTS\n" > $log
for xmlfile in ../../BENCHMARKdataB/*.xml; do
	echo $xmlfile >> $log
	echo $xmlfile
	../../Mistral-2.0/bin/MistralXCSP --print_sta $xmlfile >> $log
	#Mistral-2.0/bin/MistralXCSP $xmlfile
done;
echo "all xml files processed ! :) bye"
echo " ****************** "
