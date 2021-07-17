#!/usr/bin/env groovy
def cli = new CliBuilder(usage:'obo-2-adoc')
cli.f(longOpt:'file', args:1, argName:'file', 'The obo file to convert.')
def options = cli.parse(args)

if (!options || options.h) {
    cli.usage()
    exit(1)
}
if( !new File(options.f).exists() ) {
  println "File does not exist"
} else {
  println "Reading from ${options.f}"
  dataList = new File(options.f).text.split( '\n\n' ).inject( [] ) { list, block ->
    list << block.split( '\n' ).inject( [:].withDefault{[]} ) { map, line ->
      def (key,value) = line.split( ': ', 2).collect { it.trim().replaceAll("\\|","\\\\|") }
      map[key] << value 
      map
    }
  }
}

def basename = options.f.take(options.f.lastIndexOf('.'))
def outFile = new File(basename+".adoc")
println "Writing to ${outFile.name}"
outFile.withWriter { out ->
  dataList.eachWithIndex { it, index ->
    if(index==0) {
	out.println "= ${basename} Ontology "
	out.println ":doctype: article"
	out.println ":sectnums:"
	out.println ":toc: left"
	out.println ""
	out.println "[#header]"
	out.println "== Document Metadata"
	out.println ".Metadata"
	out.println "[cols=\"2*\"]"
	out.println "|==="
    } else if(index==1) {
	out.println "[#definitions-and-terms]"
	out.println "== Definitions and Terms"	
    } else {
	out.println "[#${it["id"][0]}]"
	out.println "=== ${it["id"][0]} ${it["name"][0]}" 
    }
    it.each { k, v ->
    
      if(k.equals("[Typedef]")) {
        out.println ".Typedef ${it["id"]}"
	out.println "[cols=\"2*\"]"
        out.println "|==="
      } else if(k.equals("[Term]")) {
        out.println ".Term ${it["id"]}"
	out.println "[cols=\"2*\"]"
        out.println "|==="
      } else {
        v.each { value ->
          if(k.equals("is_a")) {
            if(value.contains("!")) {
	      def refId = value.split("!", 2)
	      out.println "| $k | <<${refId[0].trim()}>> ! ${refId[1].trim()} "
            } else {
	      out.println "| $k | <<${value.trim()}>> "
            }
	  } else if(k.equals("relationship")) {
            if(value.contains("!")) {
	      def term = value.split("!")
	      def refId = term[0].split(" ")
	      out.println "| $k | ${refId[0]} <<${refId[1]}>> ! ${term[1]} "
            } else if(value.contains(" ")) {
	      def term = value.split(" ")
	      out.println "| $k | ${term[0]} <<${term[1]}>> "
            }
	  } else {
	    out.println "| $k | $value "
	  }
        }
      }
    }
    out.println "|==="
    out.println ""
  }
}
