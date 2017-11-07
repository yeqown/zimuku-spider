#!/usr/bin/sh

files=`ls ./zip`

for filename in $files;
do
    unzip -o -d "./zip" "./zip/$filename";
done

echo "all zip files extract done"

mv "./zip/*.srt" "./srt/"
echo "mv all zip files into ./srt/ done"

rm "./zip/*.zip"
echo "rm all zip files in ./rar/ done"