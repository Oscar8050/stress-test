#!/bin/bash

NUM_WORKERS=32  # 設置你想啟動的工作節點數量

for i in $(seq 1 $NUM_WORKERS)
do
  locust -f locustfile.py --worker &
done

wait