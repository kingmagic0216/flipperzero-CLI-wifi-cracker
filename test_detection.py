#!/usr/bin/env python3
"""Test tool detection"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import get_tool_command

print("Testing hcxpcapngtool detection...")
cmd = get_tool_command('hcxpcapngtool')
print(f"Result: {cmd}")
print(f"Type: {type(cmd)}")
print(f"Is string: {isinstance(cmd, str)}")
print(f"Equals 'hcxpcapngtool': {cmd == 'hcxpcapngtool'}")
print(f"Is list: {isinstance(cmd, list)}")
if isinstance(cmd, list):
    print(f"List contents: {cmd}")

