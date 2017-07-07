#!/usr/bin/env bash
TEST_FILE=TestFile

echo "Generating test file";
python generator.py 100 1000 $TEST_FILE;
echo "Sorting in memory";
python sorter_in_memory.py $TEST_FILE;
echo "External sorting with chunk size 10";
python sorter.py $TEST_FILE 10;
echo "Dfff";
diff "$TEST_FILE.sorted" "$TEST_FILE.sorted-inmemory";


echo "Sorting in memory REVERSED";
python sorter_in_memory.py $TEST_FILE true;
echo "External sorting with chunk size 10 REVERSED";
python sorter.py $TEST_FILE 10 true;
echo "Dfff";
diff "$TEST_FILE.sorted" "$TEST_FILE.sorted-inmemory";

