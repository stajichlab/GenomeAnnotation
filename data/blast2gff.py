#!/usr/bin/python
#
# Convert a blastn outfmt=6 file to GFF3 format, taking some static values on the command line.
# Sets Note=source so it shows up on GBrowse searches.

import sys
import argparse

parser = argparse.ArgumentParser(description="Convert a blastn outfmt 6 file to GFF3 format, taking source, feature and assembly on the command line. Sets Note=source to enable GBrowse searches.")
parser.add_argument("--min-bit-score", type=int, default=0, help="minimum bit score of records to be included in GFF3 output")
parser.add_argument("--min-perc-identity", type=float, default=0.0, help="minimum percent identity of records to be included in GFF3 output")
parser.add_argument("filename", help="blast file")
parser.add_argument("source", help="GFF source")
parser.add_argument("feature", help="GFF feature")
parser.add_argument("assembly", help="assembly_name")

args = parser.parse_args()

print "##gff-version 3"

f = open(args.filename, 'rU')
    
for line in f:
    chunks = line.split('\t')
    if len(chunks)>=11:
        # BLAST fields
        queryLabel = chunks[0].rstrip()
        targetLabel = chunks[1].rstrip()
        percIdentity = float(chunks[2].rstrip())
	alignLength = int(chunks[3].rstrip())
	numMismatches = int(chunks[4].rstrip());
	numGaps = int(chunks[5].rstrip());
	queryStart = int(chunks[6].rstrip());
	queryEnd = int(chunks[7].rstrip());
	targetStart = int(chunks[8].rstrip());
	targetEnd = int(chunks[9].rstrip());
	eValue = float(chunks[10].rstrip());
	bitScore = int(round(float(chunks[11].rstrip()))); # round to int, which is usually is
        # optional filter criteria
        bitScoreOK = bitScore >= args.min_bit_score
        percIdentityOK = percIdentity >= args.min_perc_identity
        if bitScoreOK and percIdentityOK:
            # GFF fields
            seqid = targetLabel
            name = queryLabel
            if targetStart<targetEnd:
                start = targetStart
                end = targetEnd
                strand = '+'
            else:
                start = targetEnd
                end = targetStart
                strand = '-'
            score = bitScore
            # build attributes
            attributes = "Name="+name+";"
            attributes += "assembly_name="+args.assembly+";"
            attributes += "Note="+args.source+";";
            # BLAST stuff
            attributes += "perc_identity="+str(percIdentity)+";"
            attributes += "align_length="+str(alignLength)+";"
            attributes += "num_mismatches="+str(numMismatches)+";"
            attributes += "num_gaps="+str(numGaps)+";"
            attributes += "evalue="+str(eValue)+";"
            # write out the GFF record
            print seqid+'\t'+args.source+'\t'+args.feature+'\t'+str(start)+'\t'+str(end)+'\t'+str(bitScore)+'\t'+strand+'\t'+'.'+'\t'+attributes

f.close()
