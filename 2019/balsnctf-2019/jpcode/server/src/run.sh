#!/bin/bash
# 
exec 2>/dev/null
cd /home/jpcode
timeout 30 python /home/jpcode/chal.py
