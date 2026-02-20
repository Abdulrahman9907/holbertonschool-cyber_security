#!/bin/bash
sha256sum "$1" | awk -v fname="$1" -v hash="$2" '{if ($1==hash) print fname ": OK"}'
