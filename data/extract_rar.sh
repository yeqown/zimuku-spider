#!/usr/bin/sh

files=`ls ./rar`

for filename in $files;
do
    unrar e "./rar/$filename";
done
echo "extract all rar files done"

mv "./rar/*.srt" "./srt/"
echo "mv all srt files into ./srt/ done"

rm "./rar/*.rar"
echo "rm all rar files in ./rar/ done"
