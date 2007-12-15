list="101 102 103 103b 104 105 105b 106 107 108 109 110 111 112 113 114 115 116 116b 117 118v001 118v015 118b"
for i in $list; do
  f=`ls "psalm$i\_*.sib"`
  echo "$f.proofed"
  if [ "$f" == "" ]; then
    echo "Error: No file '$f'"
  else
    touch "$f.proofed"
    svn add "$f.proofed"
  fi
done
