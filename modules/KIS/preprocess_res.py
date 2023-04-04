def save_price_info(res, stock_info):
    if res["rt_cd"] == "0":
        stock_code = res["output1"]["stck_shrn_iscd"]
        for j in range(len(res["output2"])):
            try:
                Date = res["output2"][j]["stck_bsop_date"]
                Close = res["output2"][j]["stck_clpr"]
                Open  = res["output2"][j]["stck_oprc"]
                High = res["output2"][j]["stck_hgpr"]
                Low = res["output2"][j]["stck_lwpr"]
                Volume = res["output2"][j]["acml_vol"]
                Amount = res["output2"][j]["acml_tr_pbmn"]
                Change = res["output2"][j]["prdy_vrss"]

                stock_info.loc[len(stock_info)] = [stock_code, Date, Open, High, Low, Close, Volume, Amount, Change]
            except:
                pass
            
    else:
        print(f"Error: {res['rt_cd']}, {res['msg_cd']}", {res['msg1']})
    
    return stock_info