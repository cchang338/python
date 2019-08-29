def buildDrivingNetwork(df_links,ARRIVAL_STRATEGY): #ann 03282018
    print('** build driving network **')
    df_link_grids=pd.read_csv('data_node_link/stmFilled/Link_Grids_Nodes_ValidSpeed_stm_2020_ML_0809.csv')
    df_link_grids=df_link_grids[df_link_grids['A_B'].isin(df_links['A_B'])]
    df_link_grids['new']=-1
    for ind, row in df_link_grids.iterrows():
        for col in df_link_grids.columns.values.tolist():
            if col[-5:]=='ttime':
                dist=row[col[:-5]+'dist']
                ttime=row[col[:-5]+'ttime']
                speed=row[col[:-5]+'speed']
                ttime_new=dist/5280.0/speed
                if ttime_new>ttime:
                    df_link_grids.set_value(ind,col[:-5]+'ttime',ttime_new)
                    df_link_grids.set_value(ind,'new',1)
    


    #all_ttimes = ['063000_ttime', '073000_ttime', '083000_ttime', '093000_ttime', '064500_ttime', '074500_ttime', '084500_ttime', '094500_ttime', '070000_ttime', '080000_ttime', '090000_ttime', '100000_ttime', '071500_ttime', '081500_ttime', '091500_ttime']
    all_ttimes = ['080000_ttime','081500_ttime','083000_ttime','084500_ttime','090000_ttime','091500_ttime','093000_ttime', '094500_ttime']
    # note: this is an error, should not *60 -> already fixed
    for col in all_ttimes:
        df_link_grids.loc[df_link_grids[col].isnull(),col]=df_link_grids.loc[df_link_grids[col].isnull(),'DISTANCE']/df_link_grids.loc[df_link_grids[col].isnull(),'SPEEDLIMIT']
    
    DGo=nx.DiGraph()
    # weight is in minutes
    for ind, row2 in df_link_grids.iterrows():
        i=-1
        for col in all_ttimes:
            i+=1
            edgeLabel = col.split('_')[0]
            if ARRIVAL_STRATEGY==1: #ann 03282018
                DGo.add_weighted_edges_from(
                        [(str(row2['A']),str(row2['B']),float(row2[col])*60.0)],weight=edgeLabel, dist=row2['DISTANCE'],name=row2['NAME'])
            else:
                DGo.add_weighted_edges_from([(str(row2['B']),str(row2['A']),float(row2[col])*60.0)],weight=edgeLabel, dist=row2['DISTANCE'],name=row2['NAME'])
    return DGo