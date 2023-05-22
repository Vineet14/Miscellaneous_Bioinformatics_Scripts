#!/usr/bin/python3

# Filters the bam file for the overhangs across the junctions
# Does not consider if there are multiple exons within the mate pairs

#Author Vineet Sharma

# Dated: May, 24, 2019

import pysam
import sys
import optparse

class FilterOverhangs():

    def __init__(self, infile, outfile, jn_overhang):

        self.infile = infile
        self.outfile = outfile
        self.jn_overhang = int(jn_overhang)
        self.samfile = pysam.AlignmentFile(infile, "rb")
        self.writefile = pysam.AlignmentFile(outfile, "wb", template=self.samfile)

    def filter_samfile(self):

        for read in self.samfile.fetch():
            if read.cigartuples[0][0] == 0 and read.cigartuples[-1][0] == 0:
                if read.cigartuples[0][1] >= self.jn_overhang and read.cigartuples[-1][1] >= self.jn_overhang:
                    self.writefile.write(read)
        self.writefile.close()
        self.samfile.close()

if __name__=="__main__":
    
    help_text = """python3 filtering_bam_by_overhang_length.py <input_bam> <output_bam> <minimum_length_of_overhang>"""
    parser = optparse.OptionParser(usage=help_text)
    (options, args) = parser.parse_args()
    data = FilterOverhangs(sys.argv[1], sys.argv[2], sys.argv[3])
    data.filter_samfile()

