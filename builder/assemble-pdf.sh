#!/bin/bash
# Build SttL hymnal from pdfs

set -e # exit on any error without printing "Created SttL.pdf"

# Set Java's path to the pdf tool library
export CLASSPATH="$PWD/Multivalent.jar"

pushd ../Psalms/pdf >/dev/null

psalmlist=(
    psalm001_*.pdf psalm001b_*.pdf psalm00[2-9]_*.pdf \
    psalm01[0-5]_*.pdf psalm016_*.pdf psalm016b_*.pdf psalm01[7-9]_*.pdf psalm019b_*.pdf \
    psalm02[0-2]_*.pdf psalm022b_*.pdf psalm022c_*.pdf psalm02[3-5]_*.pdf psalm025b_*.pdf psalm02[6-9]_*.pdf \
    psalm03[0-9]_*.pdf \
    psalm04[0-2]_*.pdf psalm042b_*.pdf psalm043b_*.pdf psalm04[4-7]_*.pdf psalm047b_*.pdf psalm04[8-9]_*.pdf \
    psalm05[0-1]_*.pdf psalm051b*.pdf psalm05[2-9]_*.pdf \
    psalm06[0-3]_*.pdf psalm063b_*.pdf psalm06[4-5]_*.pdf psalm065b_*.pdf psalm06[6-8]_*.pdf psalm068?_*.pdf psalm069_*.pdf psalm069b_*.pdf \
    psalm07[0-2]*.pdf  psalm073_*.pdf psalm073b_*.pdf psalm07[4-8]_*.pdf psalm078b_*.pdf psalm079_*.pdf \
    psalm08[0-1]_*.pdf psalm081b_*.pdf psalm08[2-6]_*.pdf psalm086b_*.pdf psalm087_*.pdf psalm087b_*.pdf psalm08[8-9]*.pdf \
    psalm09[0-5]_*.pdf psalm095b_*.pdf psalm09[6-8]_*.pdf psalm098b_*.pdf psalm099_*.pdf \
    psalm100_*.pdf psalm100b_*.pdf psalm10[1-3]_*.pdf psalm103b_*.pdf psalm10[4-5]_*.pdf psalm105b_*.pdf psalm10[6-9]_*.pdf \
    psalm11[0-6]_*.pdf psalm116b_*.pdf psalm11[7-8]_*.pdf psalm118b_*.pdf psalm119v0[0-2]?_*.pdf psalm119v025b_*.pdf psalm119v0[3-9]?_*.pdf psalm119v1*.pdf \
    psalm12[0-9]_*.pdf \
    psalm13[0-3]_*.pdf psalm133b_*.pdf psalm13[4-7]_*.pdf psalm137b_*.pdf psalm13[8-9]_*.pdf psalm139b_*.pdf \
    psalm14[0-5]_*.pdf psalm145b_*.pdf psalm14[6-9]_*.pdf psalm149b_*.pdf psalm150_*.pdf psalm150b_*.pdf \
)
#psalms=($(psalm_list | grep -v '\.np\.pdf$'))
psalms=()
for i in "${psalmlist[@]}"; do
    if [[ "$i" != *".np.pdf" ]]; then
        psalms+=("$i")
    fi
done

# Create Psalms.pdf to contain all psalms within one sub-section of the pdf outline
cp SubtitlePsalms.pdf Psalms.pdf
java tool.pdf.Merge -append -samedoc Psalms.pdf blankpage.pdf
java tool.pdf.Compress -nooutline -inplace -quiet Psalms.pdf  # remove outline from pdf
java tool.pdf.Merge -append Psalms.pdf "${psalms[@]}"
java tool.pdf.Merge -append -samedoc Psalms.pdf blankpage.pdf

# Create Hymns.pdf to contain all psalms within one sub-section of the pdf outline
cp SubtitleHymn.pdf Hymns.pdf
java tool.pdf.Merge -append Hymns.pdf ../../Hymns/pdf/Hymn*.pdf

# Create other files that will be merged into pdf, named by the name that will be used in the contents list
cp SttLbackpages1.pdf Indexes.pdf
cp SttLbackpages2.pdf FirstLines.pdf

#The following 3 lines create individual pdf contents entries for each section of the frontmatter
#~ cp Titlepage.pdf Title.pdf
#~ java tool.pdf.Merge -append Title.pdf Copyright.pdf Contents.pdf Prayer.pdf Creeds.pdf Preface.pdf Statement.pdf
#~ mv Title.pdf SttL.pdf

#The following line instead merges the frontmatter with the contents list already existing in the SttLfrontpages pdf
#Copy SttLfrontpages.pdf to Frontmatter.pdf because that is what the first element in the contents list will be called.
cp SttLfrontpages.pdf Frontmatter.pdf

java tool.pdf.Merge -append Frontmatter.pdf \
    Psalms.pdf \
    Hymns.pdf \
    FormsandConfessions.pdf \
    Indexes.pdf \
    ../../Hymns/pdf/Guitar.pdf \
    FirstLines.pdf
mv Frontmatter.pdf SttL.pdf
java tool.pdf.Compress -inplace SttL.pdf

#rm Psalms.pdf Hymns.pdf Indexes.pdf FirstLines.pdf

popd
mv ../Psalms/pdf/SttL.pdf .

echo "Created SttL.pdf"
