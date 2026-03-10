#!/bin/bash
whois $1 | awk '/^(Registrant|Admin|Tech) /{if(/Ext:/) {print $0","} else {n=index($0,": "); field=substr($0,1,n-1); val=substr($0,n+2); if(/Street/) val=val" "; print field","val}}' > $1.csv
