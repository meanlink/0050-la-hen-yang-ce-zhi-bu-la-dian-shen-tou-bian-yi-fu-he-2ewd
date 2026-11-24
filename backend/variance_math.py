from decimal import Decimal
from statistics import mean

def analyze(data):
    all_values=[value for stations in data.values() for seam in stations.values() for value in seam]
    grand=mean(all_values)
    ss_bench=ss_seam=ss_read=Decimal(0)
    for station in data.values():
        bench_avg=mean([value for seam in station.values() for value in seam])
        ss_bench+=4*(bench_avg-grand)**2
        for seam in station.values():
            seam_avg=mean(seam)
            ss_seam+=2*(seam_avg-bench_avg)**2
            ss_read+=sum((value-seam_avg)**2 for value in seam)
    m_b,m_s,m_r=ss_bench/2,ss_seam/3,ss_read/6
    return grand,max(Decimal(0),(m_b-m_s)/4),max(Decimal(0),(m_s-m_r)/2),m_r,           {"bench":float(ss_bench),"seam":float(ss_seam),"repeat":float(ss_read)}
