from symbols import MASTER_STOCK_LIST


def build_stock_universe():

    universe = []

    for sector, caps in MASTER_STOCK_LIST.items():

        for cap_category, stocks in caps.items():

            for symbol in stocks:

                universe.append({
                    "symbol": symbol,
                    "sector": sector,
                    "market_cap": cap_category
                })

    return universe


def get_symbol_list():

    universe = build_stock_universe()

    return [stock["symbol"] for stock in universe]