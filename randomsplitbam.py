#! /usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import pysam
import random
from signal import signal, SIGPIPE, SIG_DFL

# Handle broken pipes:
signal(SIGPIPE, SIG_DFL) 

version = '1.1 (2017-05-16)'

parser = argparse.ArgumentParser(description="Randomly split BAM file into two. Input BAM file must be sorted by read name.")
parser.add_argument('-v', '--version', action='version', version='%(prog)s {0}'.format(version))
parser.add_argument('-d', '--directory', dest='directory', required=True, help='directory of inout BAM file')
parser.add_argument('-i', '--input', dest='filename', required=True,  help='Input BAM file')
parser.add_argument('-f', '--fraction', dest='fraction', required=True, help='fraction of reads to write to one of the output BAM files - the remainder will be written to another BAM file')
args = parser.parse_args()

input = pysam.AlignmentFile(args.directory + '/' + args.filename, "rb")
output1=pysam.AlignmentFile(args.directory + '/output1_' + args.fraction + '_' + args.filename, "wb", template=input)
output2=pysam.AlignmentFile(args.directory + '/output2_' + str(1- float(args.fraction)) + '_' + args.filename, "wb", template=input)

written1={}
written2={}

for read in input.fetch():
    if read.query_name not in written1:
        if read.query_name not in written2:
            if random.random() > float(args.fraction):
                output2.write(read)
                written2[read.query_name]=''
            else:
                output1.write(read)
                written1[read.query_name]=''
        else:
            output2.write(read)
            del written2[read.query_name]
    else:
        output1.write(read)
        del written1[read.query_name]