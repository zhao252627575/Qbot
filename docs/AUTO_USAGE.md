# Qbot Auto 使用说明 (code-based)

生成时间（请根据实际使用更新）

## 模块: `qbot/common/file_utils.py`

- 函数: extract_content, save_strings_as_json, file2dict, list_files_in_directory



## 模块: `qbot/common/utils.py`

- 函数: check_port_in_use



## 模块: `qbot/data/dump_bin.py`

- 类: DumpDataAll, DumpDataFix, DumpDataUpdate



## 模块: `qbot/engine/backtest/bitcoin_bt_example.py`

- 类: CustomPandas, Strategy

- 函数: amberdata, amberdata_ohlcv, amberdata_stf, to_pandas



## 模块: `qbot/engine/backtest/live_trade_binance.py`

- 类: RSIStrategy



## 模块: `qbot/engine/backtest/macd_bt.py`

- 类: MyStrategy



## 模块: `qbot/engine/backtest/rsrs.py`

- 函数: get_payments



## 模块: `qbot/engine/trade/easytrader/easytrader/api.py`

- 函数: use, follower

  - `use`: 用于生成特定的券商对象     :param broker:券商名支持 ['yh_client', '银河客户端'] ['ht_client', '华泰客户端']     :param debug: 控制 debug 日志的显示, 默认为 True     :param initial_assets: [雪球参数] 控制雪球初始资金，默认为一百万     :

  - `follower`: 用于生成特定的券商对象     :param platform:平台支持 ['jq', 'joinquant', '聚宽’]     :param initial_assets: [雪球参数] 控制雪球初始资金，默认为一万,         总资金由 initial_assets * 组合当前净值 得出     :param total_assets: [雪



## 模块: `qbot/engine/trade/easytrader/easytrader/clienttrader.py`

- 类: IClientTrader, ClientTrader, BaseLoginClientTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/config/client.py`

- 类: YH, HT, GJ, GF, WK, HTZQ, UNIVERSAL

- 函数: create



## 模块: `qbot/engine/trade/easytrader/easytrader/exceptions.py`

- 类: TradeError, NotLoginError



## 模块: `qbot/engine/trade/easytrader/easytrader/follower.py`

- 类: BaseFollower



## 模块: `qbot/engine/trade/easytrader/easytrader/gf_clienttrader.py`

- 类: GFClientTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/gj_clienttrader.py`

- 类: GJClientTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/grid_strategies.py`

- 类: IGridStrategy, BaseStrategy, Copy, WMCopy, Xls



## 模块: `qbot/engine/trade/easytrader/easytrader/ht_clienttrader.py`

- 类: HTClientTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/htzq_clienttrader.py`

- 类: HTZQClientTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/joinquant_follower.py`

- 类: JoinQuantFollower



## 模块: `qbot/engine/trade/easytrader/easytrader/pop_dialog_handler.py`

- 类: TradePopDialogHandler



## 模块: `qbot/engine/trade/easytrader/easytrader/refresh_strategies.py`

- 类: IRefreshStrategy, Switch, Toolbar



## 模块: `qbot/engine/trade/easytrader/easytrader/remoteclient.py`

- 函数: use



## 模块: `qbot/engine/trade/easytrader/easytrader/ricequant_follower.py`

- 类: RiceQuantFollower



## 模块: `qbot/engine/trade/easytrader/easytrader/server.py`

- 函数: error_handle, post_prepare, get_balance, get_position, get_auto_ipo, get_today_entrusts, get_today_trades, get_cancel_entrusts, post_buy, post_sell, post_cancel_entrust, get_exit, run



## 模块: `qbot/engine/trade/easytrader/easytrader/universal_clienttrader.py`

- 类: UniversalClientTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/utils/captcha.py`

- 函数: captcha_recognize, recognize_verify_code, detect_yh_client_result, input_verify_code_manual, default_verify_code_detect, detect_gf_result, invoke_tesseract_to_recognize

  - `recognize_verify_code`: 识别验证码，返回识别后的字符串，使用 tesseract 实现     :param image_path: 图片路径     :param broker: 券商 ['ht', 'yjb', 'gf', 'yh']     :return recognized: verify code string

  - `detect_yh_client_result`: 封装了tesseract的识别，部署在阿里云上，     服务端源码地址为： https://github.com/shidenggui/yh_verify_code_docker



## 模块: `qbot/engine/trade/easytrader/easytrader/utils/misc.py`

- 函数: parse_cookies_str, file2dict, grep_comma, str2num

  - `parse_cookies_str`: parse cookies str to dict     :param cookies: cookies str     :type cookies: str     :return: cookie dict     :rtype: dict



## 模块: `qbot/engine/trade/easytrader/easytrader/utils/perf.py`

- 函数: perf_clock



## 模块: `qbot/engine/trade/easytrader/easytrader/utils/stock.py`

- 函数: get_stock_type, get_30_date, get_today_ipo_data

  - `get_stock_type`: 判断股票ID对应的证券市场     匹配规则     ['50', '51', '60', '90', '110'] 为 sh     ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz     ['5', '6', '9'] 开头的为 sh， 其余为 sz     :para

  - `get_30_date`: 获得用于查询的默认日期, 今天的日期, 以及30天前的日期     用于查询的日期格式通常为 20160211     :return:

  - `get_today_ipo_data`: 查询今天可以申购的新股信息     :return: 今日可申购新股列表 apply_code申购代码 price发行价格



## 模块: `qbot/engine/trade/easytrader/easytrader/webtrader.py`

- 类: WebTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/wk_clienttrader.py`

- 类: WKClientTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/xq_follower.py`

- 类: XueQiuFollower



## 模块: `qbot/engine/trade/easytrader/easytrader/xqtrader.py`

- 类: XueQiuTrader



## 模块: `qbot/engine/trade/easytrader/easytrader/yh_clienttrader.py`

- 类: YHClientTrader



## 模块: `qbot/engine/trade/easytrader/tests/test_easytrader.py`

- 类: TestYhClientTrader, TestHTClientTrader, TestHTZQClientTrader



## 模块: `qbot/engine/trade/easytrader/tests/test_xq_follower.py`

- 类: TestXueQiuTrader, TestXqFollower



## 模块: `qbot/engine/trade/easytrader/tests/test_xqtrader.py`

- 类: TestXueQiuTrader



## 模块: `qbot/engine/trade/engine_apis/btc/btc_trade_engine_test.py`

- 函数: fetch_ohlcv, calculate_macd, check_trade_signals, cctx_main, okx_main, main



## 模块: `qbot/engine/trade/engine_apis/stocks/gmtrade_example.py`

- 函数: on_execution_report, on_order_status, on_trade_data_connected, on_trade_data_disconnected, on_account_status



## 模块: `qbot/engine/trade/engine_apis/stocks/stock_engine.py`

- 函数: on_execution_report, on_order_status, on_trade_data_connected, on_trade_data_disconnected, on_account_status



## 模块: `qbot/engine/trade/trader/panel/apps.py`

- 类: PanelConfig



## 模块: `qbot/engine/trade/trader/panel/const.py`

- 类: ContractType, ExchangeType, SectionType, SortType, AddressType, OperatorType, DirectionType, CombOffsetFlag, OffsetFlag, OrderStatus, OrderSubmitStatus, SignalType, PriorityType



## 模块: `qbot/engine/trade/trader/panel/models.py`

- 类: Autonumber, Address, Broker, Performance, Strategy, Param, Instrument, Signal, MainBar, DailyBar, Order, Trade

- 函数: to_df

  - `to_df`: :param queryset: django.db.models.query.QuerySet     :param index_col: str or list of str, optional, default: None     :param parse_dates: list or dict, default: None     :return: 



## 模块: `qbot/engine/trade/trader/test/test_api.py`

- 类: APITest



## 模块: `qbot/engine/trade/trader/trader/main.py`

- 类: RedislHandler



## 模块: `qbot/engine/trade/trader/trader/strategy/__init__.py`

- 类: BaseModule



## 模块: `qbot/engine/trade/trader/trader/strategy/brother2.py`

- 类: TradeStrategy



## 模块: `qbot/engine/trade/trader/trader/utils/__init__.py`

- 函数: str_to_number, price_round, get_next_id, get_expire_date, store_main_bar, handle_rollover, calc_main_inst, create_main, create_main_all, is_auction_time, calc_sma, calc_corr, nCr, find_best_score, calc_history_signal, calc_his_all, calc_his_up_limit, calc_his_down_limit, load_kt_data

  - `price_round`: 根据最小精度取整，例如对于IF最小精度是0.2，那么 1.3 -> 1.2, 1.5 -> 1.4     :param x: Decimal 待取整的数     :param base: Decimal 最小精度     :return: float 取整结果



## 模块: `qbot/engine/trade/trader/trader/utils/func_container.py`

- 类: CallbackFunctionContainer

- 函数: RegisterCallback



## 模块: `qbot/engine/trade/trader/trader/utils/my_logger.py`

- 函数: get_my_logger



## 模块: `qbot/engine/trade/trader/trader/utils/tick.py`

- 类: TickBar



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/arbitrage.py`

- 函数: main



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/arbitrer.py`

- 类: Arbitrer



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/fiatconverter.py`

- 类: XmlHandler



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/detailedlogger.py`

- 类: DetailedLogger



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/emailer.py`

- 类: Emailer

- 函数: send_email



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/historydumper.py`

- 类: HistoryDumper



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/logger.py`

- 类: Logger



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/observer.py`

- 类: Observer



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/specializedtraderbot.py`

- 类: SpecializedTraderBot



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/traderbot.py`

- 类: TraderBot



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/traderbotsim.py`

- 类: MockMarket, TraderBotSim



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/observers/xmppmessager.py`

- 类: MyXMPPClient, XmppMessager



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/private_markets/bitstampusd.py`

- 类: PrivateBitstampUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/private_markets/market.py`

- 类: TradeException



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/private_markets/paymium.py`

- 类: PrivatePaymium



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_binance.py`

- 类: Binance



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_bitfinex.py`

- 类: Bitfinex



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_bitflyer.py`

- 类: BitFlyer



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_bitstamp.py`

- 类: Bitstamp



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_btcc.py`

- 类: BTCC



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_cex.py`

- 类: CEX



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_gdax.py`

- 类: GDAX



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_gemini.py`

- 类: Gemini



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_kraken.py`

- 类: Kraken



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/_okcoin.py`

- 类: OKCoin



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/binanceusd.py`

- 类: BinanceUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/bitfinexeur.py`

- 类: BitfinexEUR



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/bitfinexusd.py`

- 类: BitfinexUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/bitflyereur.py`

- 类: BitFlyerEUR



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/bitflyerusd.py`

- 类: BitFlyerUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/bitstampeur.py`

- 类: BitstampEUR



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/bitstampusd.py`

- 类: BitstampUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/btcccny.py`

- 类: BTCCCNY



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/cexeur.py`

- 类: CEXEUR



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/cexusd.py`

- 类: CEXUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/gdaxeur.py`

- 类: GDAXEUR



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/gdaxusd.py`

- 类: GDAXUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/geminiusd.py`

- 类: GeminiUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/krakeneur.py`

- 类: KrakenEUR



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/krakenusd.py`

- 类: KrakenUSD



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/market.py`

- 类: Market



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/okcoincny.py`

- 类: OKCoinCNY



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/public_markets/paymiumeur.py`

- 类: PaymiumEUR



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/test/arbitrage_speed_test.py`

- 类: TestObserver

- 函数: main



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/test/arbitrage_test.py`

- 类: TestArbitrage



## 模块: `qbot/engine/trade/trading/bitcoin-arbitrage/arbitrage/utils.py`

- 函数: log_exception



## 模块: `qbot/engine/trade/trading/emt_api/EmQuantAPI.py`

- 类: c_safe_union, stEQChar, stEQCharArray, stEQVarient, stEQVarientArray, stEQData, stEQLoginInfo, stEQMessage, stEQCtrData, stOrderInfo

- 函数: DemoCallback, chqDemoCallback, cstCallBack, cnqdemoCallBack

  - `DemoCallback`: DemoCallback 是csq订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata     :param quantdata:cls.EmQuantData     :return:

  - `chqDemoCallback`: chqDemoCallback 是chq订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata     :param quantdata:cls.EmQuantData     :return:

  - `cstCallBack`: cstCallBack 是日内跳价服务提供的回调函数模板



## 模块: `qbot/engine/trade/trading/emt_api/demo.py`

- 函数: mainCallback, startCallback, csqCallback, cstCallBack, cnqCallback

  - `mainCallback`: mainCallback 是主回调函数，可捕捉如下错误     在start函数第三个参数位传入，该函数只有一个为c.EmQuantData类型的参数quantdata     :param quantdata:c.EmQuantData     :return:

  - `csqCallback`: csqCallback 是csq订阅时提供的回调函数模板。该函数只有一个为c.EmQuantData类型的参数quantdata     :param quantdata:c.EmQuantData     :return:



## 模块: `qbot/engine/trade/trading/emt_api/example/highgrowth/DemoStrategy_HighGrowth.py`

- 函数: pick, transfer



## 模块: `qbot/engine/trade/trading/emt_api/example/ma_strategy/DemoStrategy_MA.py`

- 函数: trade, ma



## 模块: `qbot/engine/trade/trading/emt_api/installEmQuantAPI.py`

- 函数: installEmQuantAPI



## 模块: `qbot/engine/trade/trading/thsauto/server.py`

- 函数: run_client, interval_call, get_balance, get_position, get_active_orders, get_filled_orders, sell, buy, buy_kc, sell_kc, cancel, kill_client, restart_client, test



## 模块: `qbot/engine/trade/trading/thsauto/thsauto.py`

- 函数: get_clipboard_data, hot_key, set_text, get_text, parse_table



## 模块: `qbot/gui/elements/def_dialog.py`

- 类: WebDialog, InputsDialog, InputDialogTwoParameters, UserDialog, ParamsConfigDialog

- 函数: MessageDialog, ChoiceDialog



## 模块: `qbot/gui/elements/def_grid.py`

- 类: GridTable



## 模块: `qbot/gui/elements/def_treelist.py`

- 类: CollegeTreeListCtrl



## 模块: `qbot/gui/gui_utils.py`

- 函数: _pydate2wxdate, _wxdate2pydate



## 模块: `qbot/gui/mainframe.py`

- 类: MainFrame



## 模块: `qbot/gui/panels/panel_backtest.py`

- 类: PanelBacktest

- 函数: OnBkt



## 模块: `qbot/gui/panels/panel_real_trade.py`

- 类: RealTradePanel



## 模块: `qbot/gui/panels/panel_results.py`

- 类: ResultsPanel



## 模块: `qbot/gui/panels/panel_sim_trade.py`

- 类: SimTradePanel



## 模块: `qbot/gui/panels/panel_trade.py`

- 类: TradePanel



## 模块: `qbot/gui/panels/panel_zhiku.py`

- 类: QbotHomePanel, YanbaoPanel, NotebookPanel, ZhikuPanel



## 模块: `qbot/gui/widgets/widget_matplotlib.py`

- 类: MatplotlibPanel



## 模块: `qbot/gui/widgets/widget_web.py`

- 类: WebPanel



## 模块: `qbot/plugins/auto_monitor.py`

- 函数: show_notification, show_notification_2, get_data, check_strategy, check



## 模块: `qbot/plugins/dagster/dagster_taskgraph.py`

- 函数: load_bondlist, update_factor_chg, update_factor_close, task_graph, merge_datas, cb_task_job



## 模块: `qbot/plugins/quantstats/quantstats/__init__.py`

- 函数: extend_pandas

  - `extend_pandas`: Extends pandas by exposing methods to be used like:     df.sharpe(), df.best('day'), ...



## 模块: `qbot/plugins/quantstats/quantstats/_plotting/core.py`

- 函数: _get_colors, plot_returns_bars, plot_timeseries, plot_histogram, plot_rolling_stats, plot_rolling_beta, plot_longest_drawdowns, plot_distribution, plot_table, format_cur_axis, format_pct_axis



## 模块: `qbot/plugins/quantstats/quantstats/_plotting/wrappers.py`

- 函数: to_plotly, snapshot, earnings, returns, log_returns, daily_returns, yearly_returns, distribution, histogram, drawdown, drawdowns_periods, rolling_beta, rolling_volatility, rolling_sharpe, rolling_sortino, monthly_heatmap, monthly_returns



## 模块: `qbot/plugins/quantstats/quantstats/reports.py`

- 函数: _get_trading_periods, _match_dates, html, full, basic, metrics, plots, _calc_dd, _html_table, _download_html, _open_html, _embed_figure



## 模块: `qbot/plugins/quantstats/quantstats/stats.py`

- 函数: pct_rank, compsum, comp, distribution, expected_return, geometric_mean, ghpr, outliers, remove_outliers, best, worst, consecutive_wins, consecutive_losses, exposure, win_rate, avg_return, avg_win, avg_loss, volatility, rolling_volatility, implied_volatility, autocorr_penalty, sharpe, smart_sharpe, rolling_sharpe, sortino, smart_sortino, rolling_sortino, adjusted_sortino, probabilistic_ratio

  - `pct_rank`: Rank prices by window

  - `compsum`: Calculates rolling compounded returns

  - `comp`: Calculates total compounded returns



## 模块: `qbot/plugins/quantstats/quantstats/utils.py`

- 函数: _mtd, _qtd, _ytd, _pandas_date, _pandas_current_month, multi_shift, to_returns, to_prices, log_returns, to_log_returns, exponential_stdev, rebase, group_returns, aggregate_returns, to_excess_returns, _prepare_prices, _prepare_returns, download_returns, _prepare_benchmark, _round_to_closest, _file_stream, _in_notebook, _count_consecutive, _score_str, make_index, make_portfolio, _flatten_dataframe



## 模块: `qbot/qbot.py`

- 函数: get_data



## 模块: `qbot/strategies/adx_strategy.py`

- 函数: adx_strategy



## 模块: `qbot/strategies/arbr_strategy.py`

- 函数: get_code, get_data, arbr, plot_arbr



## 模块: `qbot/strategies/bigger_than_ema_bt.py`

- 类: BiggerThanEmaStrategy

- 函数: get_data



## 模块: `qbot/strategies/boll_strategy_bt.py`

- 类: BollStrategy



## 模块: `qbot/strategies/get_stack_data.py`

- 函数: get_from_tushare, get_from_tushare_pro, get_from_akshare, get_from_baostock



## 模块: `qbot/strategies/k_lines.py`

- 函数: paint_dayk, main



## 模块: `qbot/strategies/klines_bt.py`

- 类: KlinesStrategy

- 函数: get_k_data



## 模块: `qbot/strategies/lstm_strategy_bt.py`

- 类: LSTMPredict

- 函数: get_data



## 模块: `qbot/strategies/multi_strategy_bt.py`

- 类: MultiStrategy

- 函数: get_data



## 模块: `qbot/strategies/rl_strategy_bt.py`

- 类: RLStrategy

- 函数: get_data



## 模块: `qbot/strategies/sma_cross_strategy_bt.py`

- 类: SmaCross

- 函数: get_data



## 模块: `qbot/strategies/ssa_strategy_bt.py`

- 类: ssa_index_ind, MyStrategy



## 模块: `qbot/strategies/undervalued_stock_picking_strategy.py`

- 函数: initialize, trade, check_stocks, dapan_stoploss, dp_stoploss



## 模块: `qbot/strategies/util.py`

- 函数: computeMACD, calculateEMA, calculateMACD



## 模块: `qbot_main.py`

- 函数: send_signal_sounds, send_signal_message_screen, cal_fusion_result, get_weights_distribution



## 模块: `utils/common/AShareDailyData.py`

- 函数: auto_update, run_parent, run_child

  - `run_child`: 子线程下载数据     :return:



## 模块: `utils/common/BaseService.py`

- 类: BaseService, HistorySet



## 模块: `utils/common/TuShare.py`

- 函数: to_ts_symbol, to_split_ts_codes

  - `to_ts_symbol`: 转换合约代码为tushare查询代码



## 模块: `utils/configure/ util.py`

- 函数: notify, read_web_headers_cookies, send_message_via_wechat, rsa_encrypt, rsa_decrypt, market_status, _format_addr, send_from_aliyun, send_sms, jsonp2json, js2json, bond_filter, get_holding_list, mongo_convert_df, get_jsl_code, fmt_date, calendar



## 模块: `utils/configure/settings.py`

- 类: DBSelector

- 函数: get_config_data, config_dict, get_tushare_pro



## 模块: `utils/larkbot.py`

- 函数: main



## 模块: `utils/push_local_sigal.py`

- 函数: send_signal_sounds, send_signal_message_screen



## 模块: `utils/send_email.py`

- 函数: send_email



## 模块: `utils/sendemail_stargazers.py`

- 函数: close_github_issues



## 模块: `utils/wxbot.py`

- 函数: print_others, reply_my_friend, auto_accept_friends



## 模块: `utils/yesterday_zt_monitor.py`

- 类: PlotYesterdayZT

- 函数: main



## 快速启动

```bash
cd d:\file\python\Qbot
pip install -r dev/requirements.txt
python main.py
```
