#!/bin/bash
sha256sum "$1" | awk -v h="$2" -v f="$1" '{if ($1==h) print f": OK"; else print f": FAILED"}'
