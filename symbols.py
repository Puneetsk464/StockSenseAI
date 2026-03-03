# symbols.py

MASTER_STOCK_LIST = {
    "Banking": {
        "Large Cap": [
            'HDFCBANK.NS', 'ICICIBANK.NS', 'SBIN.NS', 'AXISBANK.NS',
            'KOTAKBANK.NS', 'INDUSINDBK.NS', 'BANKBARODA.NS', 'PNB.NS',
            'CANBK.NS', 'UNIONBANK.NS', 'INDIANB.NS', 'FEDERALBNK.NS',
            'IDFCFIRSTB.NS'
        ],
        "Mid Cap": [
            'AUBANK.NS', 'YESBANK.NS', 'BANDHANBNK.NS', 'KARURVYSYA.NS',
            'MAHABANK.NS', 'CENTRALBK.NS', 'BANKINDIA.NS', 'UCOBANK.NS',
            'PSB.NS', 'J&KBANK.NS', 'CUB.NS', 'IDBI.NS', 'IOB.NS'
        ],
        "Small Cap": [
            'RBLBANK.NS', 'EQUITASBNK.NS', 'UJJIVANSFB.NS', 'SOUTHBANK.NS',
            'CSBBANK.NS', 'KTKBANK.NS', 'DCBBANK.NS', 'FINOPB.NS',
            'SURYODAY.NS', 'UTKARSHBNK.NS', 'ESAFSFB.NS', 'DHANBANK.NS',
            'SATIN.NS', 'REPCOHOME.NS'
        ]
    },

    "IT": {
        "Large Cap": [
            'TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS',
            'LTIM.NS', 'TECHM.NS'
        ],
        "Mid Cap": [
            'PERSISTENT.NS', 'OFSS.NS', 'LTTS.NS', 'KPITTECH.NS',
            'MPHASIS.NS', 'COFORGE.NS', 'TATAELXSI.NS', 'CYIENT.NS',
            'AFFLE.NS', 'SONATSOFTW.NS', 'BSOFT.NS',
            'ZENSARTECH.NS', 'INTELLECT.NS', 'MASTEK.NS'
        ],
        "Small Cap": [
            'NEWGEN.NS', 'HAPPSTMNDS.NS', 'TANLA.NS', 'ECLERX.NS',
            'SAKSOFT.NS', 'FSL.NS', 'DATAMATICS.NS', 'RATEGAIN.NS',
            'QUICKHEAL.NS', 'RAMCOSYS.NS', '63MOONS.NS', 'EXPLEOSOL.NS',
            'NUCLEUS.NS', 'HGS.NS', 'MOSCHIP.NS', 'CREATIVE.NS'
        ]
    },

    "Auto": {
        "Large Cap": [
            'TATAMOTORS.NS', 'M&M.NS', 'MARUTI.NS', 'BAJAJ-AUTO.NS',
            'TVSMOTOR.NS', 'EICHERMOT.NS', 'HEROMOTOCO.NS',
            'MOTHERSON.NS'  # Fixed: Was SAMVARDHANA.NS
        ],
        "Mid Cap": [
            'BOSCHLTD.NS', 'ASHOKLEY.NS', 'BHARATFORG.NS', 'MRF.NS',
            'SONACOMS.NS', 'UNOMINDA.NS', 'TIINDIA.NS', 'EXIDEIND.NS',
            'APOLLOTYRE.NS', 'BALKRISIND.NS', 'CEATLTD.NS', 'ENDURANCE.NS'
        ],
        "Small Cap": [
            'AMARAJABAT.NS', 'SUPRAJIT.NS', 'JBMA.NS', 'GABRIEL.NS',
            'PRICOL.NS', 'SUBROS.NS', 'LUMAXIND.NS', 'SMLISUZU.NS',
            'FORCEMOT.NS',  # Fixed: Was FORCE.NS
            'OLECTRA.NS', 'CRAFTSMAN.NS', 'RICOAUTO.NS',
            'GNA.NS', 'MUNJALAU.NS', 'FIEMIND.NS'
        ]
    },

    "Pharma": {
        "Large Cap": [
            'SUNPHARMA.NS', 'DIVISLAB.NS', 'CIPLA.NS', 'DRREDDY.NS',
            'TORNTPHARM.NS', 'ZYDUSLIFE.NS', 'MANKIND.NS'
        ],
        "Mid Cap": [
            'LUPIN.NS', 'AUROPHARMA.NS', 'ALKEM.NS', 'ABBOTINDIA.NS',
            'GLENMARK.NS', 'BIOCON.NS', 'LAURUSLABS.NS', 'SYNGENE.NS',
            'IPCALAB.NS', 'NATCOPHARM.NS', 'GRANULES.NS',
            'PFIZER.NS', 'SANOFI.NS', 'AJANTPHARM.NS', 'GLAND.NS'
        ],
        "Small Cap": [
            'ERIS.NS', 'CAPLIPOINT.NS', 'MARKSANS.NS', 'NEULANDLAB.NS',
            'SUVENPHAR.NS', 'HIKAL.NS', 'SEQUENT.NS', 'MOREPENLAB.NS',
            'WOCKPHARMA.NS', 
            'STAR.NS',        # Fixed: Was STRIDESPHAR.NS
            'FDC.NS',
            'ORCHIDPHAR.NS', 'SHILPAMED.NS', 'RPGLIFE.NS',
            'GUJTHEMIS.NS', 'SMSPHARMA.NS'
        ]
    },

    "FMCG": {
        "Large Cap": [
            'ITC.NS', 'HINDUNILVR.NS', 'VBL.NS', 'TATACONSUM.NS',
            'NESTLEIND.NS', 'BRITANNIA.NS', 'GODREJCP.NS', 'DABUR.NS'
        ],
        "Mid Cap": [
            'COLPAL.NS', 'MARICO.NS', 'UNITDSPR.NS', 'PGHH.NS',
            'JUBLFOOD.NS', 'UBL.NS', 'EMAMILTD.NS', 'BIKAJI.NS',
            'MANYAVAR.NS', 'DEVYANI.NS', 'WESTLIFE.NS',
            'HATSUN.NS', 'KANSAINER.NS', 'BATAINDIA.NS', 'WHIRLPOOL.NS'
        ],
        "Small Cap": [
            'RADICO.NS', 'ZYDUSWELL.NS', 
            'BECTORFOOD.NS',  # Fixed: Was MRSBECTORS.NS
            'JYOTHYLAB.NS',
            'VADILALIND.NS', 'HERITGFOOD.NS', 'BAJAJCON.NS', 'HNDFDS.NS',
            'BALRAMCHIN.NS', 'DODLA.NS', 'GOKULAGRO.NS', 'ADFFOODS.NS',
            'DIAMONDYD.NS',   # Fixed: Was PRATAAP.NS
            'TASTYBITE.NS', 'GILLETTE.NS'
        ]
    },

    "Energy": {
        "Large Cap": [
            'RELIANCE.NS', 'NTPC.NS', 'ONGC.NS', 'POWERGRID.NS',
            'TATAPOWER.NS', 'ADANIGREEN.NS', 'COALINDIA.NS', 'IOC.NS',
            'BPCL.NS', 'ADANIPOWER.NS', 'GAIL.NS', 'ADANIENT.NS'
        ],
        "Mid Cap": [
            'JSWENERGY.NS', 'SUZLON.NS', 'NHPC.NS', 'SJVN.NS',
            'TORNTPOWER.NS', 'OIL.NS', 'PETRONET.NS', 'IGL.NS',
            'CESC.NS', 'MGL.NS', 'ATGL.NS', 'INOXWIND.NS', 'CASTROLIND.NS'
        ],
        "Small Cap": [
            'KPIGREEN.NS', 
            'WAAREERTL.NS',   # Fixed: Was WAAREE.NS
            'GENSOL.NS', 'JPPOWER.NS',
            'BORORENEW.NS', 'CHENNPETRO.NS', 'MRPL.NS', 
            'GREENPOWER.NS',  # Fixed: Was ORIENTGRN.NS
            'CONFIPET.NS', 'DEEPINDS.NS', 'HINDOILEXP.NS', 'GIPCL.NS',
            'PANACEABIO.NS',  # Fixed: Was PANACEA.NS
            'URJA.NS', 'BFUTILITIE.NS'
        ]
    },

    "Metal": {
        "Large Cap": [
            'TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'VEDL.NS',
            'JINDALSTEL.NS', 'HINDZINC.NS', 'NMDC.NS'
        ],
        "Mid Cap": [
            'SAIL.NS', 'NATIONALUM.NS', 'APLAPOLLO.NS', 'JSL.NS',
            'RATNAMANI.NS', 'WELCORP.NS', 'JINDALSAW.NS',
            'HINDCOPPER.NS', 
            'SHYAMMETL.NS'    # Fixed: Was SHYAMMET.NS
        ],
        "Small Cap": [
            'GPIL.NS',        # Fixed: Was GODAWARI.NS
            'USHAMART.NS', 'GRAVITA.NS', 'JAIBALAJI.NS',
            'GALLANTT.NS', 'SARDAEN.NS', 'IMFA.NS', 'MOIL.NS',
            'SANDUMA.NS',     # Fixed: Was SANDUR.NS
            'KIOCL.NS', 'SALASAR.NS', 'LLOYDSME.NS',
            'MANINDS.NS', 'GOODLUCK.NS'
        ]
    },

    "Realty": {
        "Large Cap": [
            'DLF.NS', 'LODHA.NS', 'GODREJPROP.NS', 'PRESTIGE.NS',
            'OBEROIRLTY.NS', 'PHOENIXLTD.NS'
        ],
        "Mid Cap": [
            'BRIGADE.NS', 'SOBHA.NS', 'MAHLIFE.NS', 'NBCC.NS',
            'SIGNATURE.NS', 'SWANENERGY.NS', 'ANANTRAJ.NS'
        ],
        "Small Cap": [
            'SUNTECK.NS', 'IBREALEST.NS', 'DBREALTY.NS', 'PURVA.NS',
            'KOLTEPATIL.NS', 'OMAXE.NS', 
            'HEMIPROP.NS',    # Fixed: Was HEMISPHERE.NS
            'AJMERA.NS',
            'ARIHANTSUP.NS', 'ARVSMART.NS', 'NESCO.NS', 'MARATHON.NS',
            'RUSTOMJEE.NS',   # Fixed: Was KEYSTONE.NS
            'ASHIANA.NS'
        ]
    }
}