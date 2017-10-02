'''
Created on Aug 29, 2017

@author: dgrewal
'''
import argparse
import pyBigWig as pybw


class readToMap(object):
    def __init__(self, infile, outfile, maxhits):
        self.input = infile
        self.output = outfile
        self.maxhits = maxhits

    def main(self):
        output = pybw.open(self.output,"w")     
        last_chrom = None
        expected_pos = 0
        
        values = []
        
        
        print 'fixedStep chrom=Y start=1 step=1'
        
        with open(self.input) as infile:
            for line in infile:
                    
                line = line.strip()
            
                if line == "":
                    continue
            
                pos, _,_,_,_,_,hits = line.split()
                chrom, pos = pos.split(":")
                
                hits = float(hits)
                pos = int(pos)
                
                
                
                if last_chrom and not chrom == last_chrom:    
                    output.addHeader([chrom, len(values)])
                    output.addEntries(chrom, xrange(len(values)), values)
                    last_chrom = chrom
                    expected_pos = 0
                
                while not pos==expected_pos:
                    values.append(0.0)
                    expected_pos += 1
            
                hits +=1
                value = 0.0;
                if hits <= self.maxhits: 
                    value = 1.0 / hits;
            
            
                values.append(value)
                expected_pos+=1
                
            output.addHeader([(chrom, len(values))])
            output.addEntries(chrom, 1, values=values, span=1, step=1)
            output.close()
    
def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('--max_hits',
                        type=int,
                        default=4)

    args = parser.parse_args()
    
    return args

if __name__ == "__main__":
    args = parse_args()

    readToMap(args.input, args.output, args.max_hits).main()