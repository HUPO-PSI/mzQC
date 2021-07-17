#!/bin/bash
#if [ -f "psi-ms.obo" ]; then
#  echo "psi-ms.obo file exists, please remove or backup before running this script!"
#  exit 1
#fi
mkdir -p target
cd target/
rm -r *.obo *.obo.adoc *.obo.adoc.html
while IFS='' read -r line || [[ -n "$line" ]]; do
    wget -v $line 
    rc=$?
    if [ $rc -ne 0 ]; then
      echo "Download exited with error code $rc" >&2
      exit $rc
    fi
done < "../ontology-urls.ini"
echo "Transforming obo to asciidoc"
for i in *.obo; do
  ../obo-2-adoc.groovy -f "$i" 
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "Transformation exited with error code $rc" >&2
    exit $rc
  fi
done
cat <<END_HTML > index.html
<html>
        <head></head>
        <body>
                <h1>HTML Versions of selected Ontologies (from obo files)</h1>
		<ul>
END_HTML
for i in *.adoc; do
  echo "Rendering asciidoc as html"
  asciidoctor -b html5 -o "$i.html" "$i"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "Rendering exited with error code $rc" >&2
    exit $rc
  fi
  cat <<END_HTML >> index.html
  <li><a href="$i.html">$i</a></li>
END_HTML
#echo "Rendering asciidoc as pdf"
#asciidoctor-pdf "$i"
#rc=$?
#if [ $rc -ne 0 ]; then
#  echo "Rendering exited with error code $rc" >&2
#  exit $rc
#fi
done
cat <<END_HTML >> index.html
</ul>
</body>
</html>
END_HTML
echo "Done!"
cd ../
