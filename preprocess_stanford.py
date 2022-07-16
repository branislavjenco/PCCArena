import argparse 
import glob
from xvfbwrapper import Xvfb    
from utils.pc_utils import calculate_normal

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", help="Glob expression for point cloud files")
    parser.add_argument("-s", help="Source directory")
    parser.add_argument("-o", help="Output directory")
    parser.add_argument("-d", help="Xvfb display")
    args = parser.parse_args()
    g = args.g
    o = args.o
    s = args.s
    d = args.d
    
    files = sorted(glob.glob(g))
    for filename in files:
        print("processing", filename)
        calculate_normal(filename, s, o, 3, d)
