#!/bin/bash
dd if=/dev/urandom bs=1 2>/dev/null | tr -cd '[:alnum:]' | head -c "$1"
