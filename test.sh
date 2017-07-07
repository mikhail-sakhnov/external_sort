#!/usr/bin/env zsh
if [ "$#" -ne 1 ]; then
    echo "Usage: test.sh <filepath>"
    exit;
fi

echo "Sorting in memory";
python sorter_in_memory.py $1;
echo "External sorting with chunk size 10";
python sorter.py $1 10;
echo "Dfff";
diff "$1.sorted" "$1.sorted-inmemory";


echo "Sorting in memory REVERSED";
python sorter_in_memory.py $1 true;
echo "External sorting with chunk size 10 REVERSED";
python sorter.py $1 10 true;
echo "Dfff";
diff "$1.sorted" "$1.sorted-inmemory";

