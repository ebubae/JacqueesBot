wget https://zenodo.org/record/1290750/files/IRMAS-TrainingData.zip?download=1
mv IRMAS-TrainingData.zip\?download\=1 irmas_training.zip
unzip irmas_training.zip

wget https://zenodo.org/record/1290750/files/IRMAS-TestingData-Part1.zip?download=1
mv IRMAS-TestingData-Part1.zip\?download\=1 irmas_testing1.zip
unzip irmas_testing1.zip

wget https://zenodo.org/record/1290750/files/IRMAS-TestingData-Part2.zip?download=1
mv IRMAS-TestingData-Part2.zip\?download\=1 irmas_testing2.zip
unzip irmas_testing2.zip

wget https://zenodo.org/record/1290750/files/IRMAS-TestingData-Part3.zip?download=1
mv IRMAS-TestingData-Part3.zip\?download\=1 irmas_testing3.zip
unzip irmas_testing3.zip

rm irmas*.zip
