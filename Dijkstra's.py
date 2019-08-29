def drive_finder(o,d,ot,DGo,cutoffs,cutoffs_label):
    # find path
    i=0
    l,p={},{}
    df_pathi=pd.DataFrame()
    l[i],p[i]=nx.single_source_dijkstra(DGo,o, cutoff=cutoffs[i]-ot*60, weight=cutoffs_label[i])
    if d not in p[i].keys():
        DG=DGo.copy()
        while d not in p[i].keys():
            if i>=len(cutoffs)-1:
                return (df_pathi,-1)
            else:
                DG.remove_edges_from([(u,v) for u,v,e in DG.edges(data=True) if (v in p[i].keys()) and (u in p[i].keys())])
                df = pd.DataFrame()
                df['d'] = l[i].keys()
                df['l'] = l[i].values()
                i+=1
                for ind, row in df.iterrows():
                    DG.add_weighted_edges_from([('o'+str(i),row['d'],row['l'])],weight=cutoffs_label[i])
                l[i],p[i]=nx.single_source_dijkstra(DG,'o'+str(i), cutoff=cutoffs[i]-ot*60, weight=cutoffs_label[i])
    total_time=l[i][d]
    # output results
    di=d
    seq=0
    for ii in np.arange(i,-1,-1):
        _start=1
        if ii==0:
            _start=0
        for ind in np.arange(len(p[ii][di])-1,_start,-1):
            node_b=p[ii][di][ind]
            node_a=p[ii][di][ind-1]
            duration=DGo[node_a][node_b][cutoffs_label[ii]]/60.0
            dist=DGo[node_a][node_b]['dist']
            route=DGo[node_a][node_b]['name']
            seq+=1
            dfi=pd.DataFrame({'A':[node_a],'B':[node_b],'mode':['drive'],'time':[duration],'dist':[dist],'route':[route],'option':['drive'],'sequence':[seq]})
            df_pathi=dfi.append(df_pathi)
        try:
            di=p[ii][di][1]
        except:
            break
    df_pathi['sequence']=df_pathi['sequence'].max()+2-df_pathi['sequence']
    return (df_pathi.sort_values('sequence',ascending=1),total_time)