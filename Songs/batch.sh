list="006 028 034 038"
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
