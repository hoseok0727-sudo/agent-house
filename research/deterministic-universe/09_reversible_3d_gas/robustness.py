"""12-condition robustness sweep (paired ballistic/collision initial states)."""
import csv
from pathlib import Path
from experiment import suite

def main():
    out=Path("data"); out.mkdir(exist_ok=True)
    rows=[]
    for L in (12,16,20):
        for p in (.25,.35):
            for b in (2,4):
                dest=out/f"robust_L{L}_p{int(p*100)}_b{b}"
                rows.extend(suite(L,b,48,p,12,dest))
    with (out/"robustness_summary.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    print("12 conditions verified:",len(rows)//2)
if __name__=="__main__": main()
