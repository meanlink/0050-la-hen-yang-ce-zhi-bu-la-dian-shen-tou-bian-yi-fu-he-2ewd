from variance_case import calculate

def seed(cx):
    for key,name,variation in [('WB-83','浅褐斜纹外衣袖缝',False),('WB-82','靛青府绸裙边',True),('WB-81','砂色棉衬小样',False)]:
        if not cx.execute("INSERT INTO wax_batches(code,fabric) VALUES (%s,%s) ON CONFLICT DO NOTHING RETURNING code",(key,name)).fetchone():continue
        for i,bench in enumerate('ABC'):
            for seam in (1,2):
                mark=f"{bench}-{seam}"
                cx.execute("INSERT INTO wax_swatches VALUES (%s,%s,%s,%s)",(key,mark,bench,'直纹' if seam==1 else '斜纹'))
                if key=='WB-81' and mark=='C-2':continue
                center=(.2 if seam==2 else .0)
                center+=([.35,.65,1.6][i] if variation else [.9,.7,.5][i])
                for run,delta in [(1,-.10),(2,.10)]:
                    cx.execute("INSERT INTO wax_readings VALUES (%s,%s,%s,%s)",(key,mark,run,round(center+delta,2)))
        if key=='WB-82':
            calculate(cx,key)
