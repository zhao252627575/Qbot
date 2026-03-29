# Qbot 项目使用说明文档

## 📋 项目概述

**Qbot** 是一个 AI 智能量化投研平台，支持从数据获取、策略开发、回测验证、模拟交易到实盘交易的全流程闭环。

```
🤖 Qbot = 智能交易策略 + 回测系统 + 自动化量化交易 + 可视化分析工具
```

---

## 🗂️ 项目目录结构

```
Qbot/
├── main.py                    # 程序入口：启动 GUI 主界面
├── qbot_main.py              # 多因子融合实时监控交易脚本
├── monitoring.py             # 后台监控程序（K线形态检测）
├── qbot/                     # 核心模块
│   ├── gui/                  # 图形用户界面
│   ├── engine/               # 交易引擎
│   ├── strategies/           # 策略库
│   ├── data/                 # 数据处理
│   ├── plugins/              # 插件
│   └── common/               # 公共工具
├── pytrader/                 # Python 交易模块
├── pyfunds/                  # 基金策略模块
├── pyfutures/                # 期货策略模块
├── utils/                    # 工具函数
├── web/                      # Web 界面
├── tests/                    # 测试代码
└── docs/                     # 文档
```

---

## 🔧 核心模块详解

### 1. 入口文件

#### `main.py`
**功能**：程序主入口，启动 GUI 界面

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import wx
from qbot.gui.mainframe import MainFrame

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title="AI智能量化投研平台")
    frame.Show()
    app.MainLoop()
```

**作用**：
- 初始化 wxPython 应用
- 加载主窗口 `MainFrame`
- 启动 GUI 事件循环

---

#### `qbot_main.py`
**功能**：多因子融合实时监控交易

**核心功能**：
| 函数 | 说明 |
|------|------|
| `send_signal_sounds(type)` | 播放买卖提示音 |
| `send_signal_message_screen()` | 屏幕弹窗通知 |
| `cal_fusion_result()` | 多因子信号融合计算 |
| `get_weights_distribution()` | 计算权重分布 |

**交易策略**：
- **BIAS 策略**：乖离率上穿/下穿信号
- **MACD 策略**：均线交叉信号
- **KDJ 策略**：K线上穿/下穿D线
- **RSI 策略**：超买(>80)/超卖(<20)信号
- **BOLL 策略**：价格突破布林带上下轨
- **LSTM 策略**：深度学习预测价格

---

#### `monitoring.py`
**功能**：后台监控程序，定时检测 K 线形态

**核心函数**：
| 函数 | 说明 |
|------|------|
| `test(codes, method)` | 检测 K 线形态 |
| `getPosition(codes)` | 获取股票形态位置 |
| `getRecentData()` | 获取 60 分钟 K 线数据 |
| `report()` | 发送邮件预警 |
| `run(codes, s)` | 定时运行监控任务 |

**检测的形态**：
- 上吊线 (CDLHANGINGMAN)
- 黄昏星 (CDLEVENINGDOJISTAR)
- 看跌吞没 (CDLENGULFING)
- 乌云盖顶 (CDLDARKCLOUDCOVER)
- 高位孕线 (CDLHARAMI)
- 三只乌鸦 (CDLIDENTICAL3CROWS)
- 下降三法 (CDLRISEFALL3METHODS)

---

### 2. GUI 模块 (`qbot/gui/`)

#### `mainframe.py`
**功能**：主窗口框架

**核心类**：`MainFrame`

**主要功能**：
- 初始化菜单栏（设置、工具、帮助）
- 初始化状态栏（显示版本、时间）
- 创建主标签页：
  - Qbot 投研智库
  - ChatGPT 策略编写
  - AI 选股/选基
  - 基金投资策略分析
  - 可视化股票/基金回测系统
  - 在线交易(实盘/虚拟盘)

---

#### `panels/` - 面板模块

| 文件 | 功能说明 |
|------|----------|
| `panel_backtest.py` | 回测面板：设置回测参数、选择策略、运行回测 |
| `panel_sim_trade.py` | 模拟交易面板：虚拟盘交易配置 |
| `panel_real_trade.py` | 实盘交易面板：真实交易接口配置 |
| `panel_trade.py` | 交易面板容器 |
| `panel_zhiku.py` | 智库面板：研报展示、投研资讯 |
| `panel_results.py` | 结果展示面板 |

---

#### `widgets/` - 自定义组件

| 文件 | 功能说明 |
|------|----------|
| `widget_matplotlib.py` | Matplotlib 图表组件 |
| `widget_web.py` | 内嵌 Web 浏览器组件 |

---

### 3. 交易引擎 (`qbot/engine/`)

#### `backtest/` - 回测引擎

| 文件 | 功能说明 |
|------|----------|
| `backtest_base.py` | 回测基类 |
| `backtest_main.py` | 回测主程序 |
| `macd_bt.py` | MACD 策略回测示例 |
| `rsrs.py` | RSRS 阻力支撑相对强度回测 |
| `bitcoin_bt_example.py` | 比特币回测示例 |
| `live_trade_binance.py` | 币安实盘交易示例 |

---

#### `trade/` - 交易执行

##### 交易引擎架构：
```
trade/
├── trade_engine.py       # 交易引擎主类
├── trade_real.py         # 实盘交易
├── trade_sim.py          # 模拟交易
├── easytrader/           # 股票自动交易 (同花顺等)
│   ├── api.py           # API 接口
│   ├── clienttrader.py  # 客户端交易
│   └── utils/           # 工具函数
├── engine_apis/          # 各市场交易接口
│   ├── stocks/          # 股票接口
│   ├── futures/         # 期货接口
│   └── btc/             # 数字货币接口
└── trading/             # 交易策略实现
    ├── bitcoin-arbitrage/  # 比特币套利
    ├── emt_api/           # 东方财富 API
    └── thsauto/           # 同花顺自动交易
```

---

### 4. 策略库 (`qbot/strategies/`)

#### 经典技术指标策略

| 策略文件 | 说明 | 类型 |
|----------|------|------|
| `boll_strategy.py` | 布林带策略 | 趋势 |
| `klines_bt.py` | 双均线策略 | 趋势 |
| `aroon_strategy.py` | 阿隆指标策略 | 趋势 |
| `arbr_strategy.py` | 情绪指标 ARBR | 情绪 |
| `adx_strategy.py` | MACD+ADX 组合 | 趋势+强度 |
| `rsi_departure_strategy.py` | RSI 背离策略 | 反转 |
| `stoch_rsi_strategy.py` | 随机 RSI 策略 | 动量 |

#### AI/机器学习策略

| 策略文件 | 说明 | 算法 |
|----------|------|------|
| `lstm_strategy_bt.py` | LSTM 时序预测 | RNN |
| `lgb_strategy.py` | LightGBM 预测 | GBDT |
| `svm_strategy.py` | SVM 预测 | 支持向量机 |
| `rl_strategy_bt.py` | 强化学习策略 | RL |
| `q-learning.py` | Q-Learning 策略 | RL |
| `ssa_strategy_bt.py` | 麻雀优化算法 SSA | 群体智能 |

#### 多因子策略

| 策略文件 | 说明 |
|----------|------|
| `multi_strategy_bt.py` | 多因子组合交易 |
| `multi_factor_strategy.py` | 多因子自动组合策略 |
| `bigger_than_ema.py` | 简单移动均线策略 |
| `undervalued_stock_picking_strategy.py` | 低估值选股策略 |

---

### 5. 数据处理 (`qbot/data/`)

| 文件 | 功能说明 |
|------|----------|
| `dump_bin.py` | 数据导出为二进制格式 |
| `dump_pit.py` | PIT 数据导出 |
| `check_dump_bin.py` | 检查二进制数据 |

---

### 6. PyTrader 模块 (`pytrader/`)

基于 easyquant 的量化交易框架。

#### 核心组件：

| 目录/文件 | 功能说明 |
|-----------|----------|
| `easyquant/` | 量化框架核心 |
| ├── `main_engine.py` | 主引擎 |
| ├── `event_engine.py` | 事件引擎 |
| ├── `quotation.py` | 行情获取 |
| ├── `push_engine/` | 推送引擎 |
| └── `strategy/` | 策略模板 |
| `easyquotation/` | 行情 API 封装 |
| `easytrader/` | 交易 API 封装 |
| `strategies/` | AI 策略实现 |
| `backtest_strategies/` | 回测策略 |
| `analyser/` | 分析工具 |
| `web/` | Web 服务 |

---

### 7. PyFunds 模块 (`pyfunds/`)

基金投资分析与回测模块。

| 目录 | 功能说明 |
|------|----------|
| `backtest/xalpha/` | 基金回测核心库 |
| `strategy/` | 基金策略 |

**xalpha 主要功能**：
- `info.py` - 基金信息获取
- `backtest.py` - 回测引擎
- `trade.py` - 交易记录管理
- `multiple.py` - 多基金组合分析
- `realtime.py` - 实时数据

---

### 8. 工具模块 (`utils/`)

| 文件 | 功能说明 |
|------|----------|
| `larkbot.py` | 飞书机器人通知 |
| `wxbot.py` | 微信机器人通知 |
| `send_email.py` | 邮件发送工具 |
| `train_lstm.py` | LSTM 模型训练 |
| `common/TuShare.py` | Tushare 数据接口 |
| `common/AShareDailyData.py` | A 股日线数据 |
| `yesterday_zt_monitor.py` | 昨日涨停监控 |

---

### 9. 插件 (`qbot/plugins/`)

| 文件/目录 | 功能说明 |
|-----------|----------|
| `quantstats/` | 量化绩效分析库 |
| `auto_monitor.py` | 自动监控程序 |
| `dagster/` | Dagster 工作流编排 |

---

## 🚀 快速开始

### 1. 环境安装

```bash
# 克隆项目
git clone https://github.com/UFund-Me/Qbot --depth 1
cd Qbot

# 安装依赖
pip install -r requirements.txt
# 或
pip install -r dev/requirements.txt

# 设置 Python 路径
export PYTHONPATH=${PYTHONPATH}:$(pwd)
```

### 2. 启动方式

#### 方式一：GUI 界面（推荐）
```bash
python main.py
# Mac 用户使用
pythonw main.py
```

#### 方式二：命令行实时监控
```bash
python qbot_main.py
```

#### 方式三：后台监控
```bash
python monitoring.py
# 或后台运行
nohup python qbot/plugins/auto_monitor.py > monitoring.log &
```

---

## 📊 主要功能使用

### 1. 策略回测

**步骤**：
1. 打开 GUI，切换到"可视化股票/基金回测系统"标签
2. 选择股票代码（如 399006.SZ）
3. 选择基准指数（如 000300.SH）
4. 选择交易策略（如 RSI、MACD、BOLL 等）
5. 点击运行回测

**代码示例**：
```python
from pytrader.easyquant.quotation import use_quotation
from pytrader.backtest_strategies.RSI import RSIStrategy

quotation = use_quotation("jqdata")
trade_days = quotation.get_all_trade_days()
bars = quotation.get_bars("002230", 500, end_dt="2021-12-24")

strategy = RSIStrategy("002230", bars, days=500)
strategy.process()
strategy.show_plt()
```

---

### 2. 实盘交易

**支持的交易平台**：
- 同花顺客户端
- 东方财富
- 华泰证券
- 国泰君安
- 币安/火币/OKEX（数字货币）

**代码示例**：
```python
import easytrader

# 初始化交易对象
user = easytrader.use('ths')  # 同花顺
user.connect('交易客户端路径')

# 查询资金和持仓
balance = user.balance
positions = user.position

# 买入/卖出
user.buy('000001', price=10.0, amount=100)
user.sell('000001', price=11.0, amount=100)
```

---

### 3. 多因子融合交易

修改 `qbot_main.py` 配置文件：

```python
# 设置股票池
stocks_pool = [
    {"code": "sz000063", "name": "中兴通讯", "min_threshold": "26", "max_threshold": "38"},
    {"code": "sh000016", "name": "上证50"},
]

# 设置权重
default_weights = {
    "BIAS": 0.1, 
    "KDJ": 0.2, 
    "RSI": 0.15, 
    "BOLL": 0.25, 
    "MACD": 0.2, 
    "LSTM": 0.1
}

# 设置本金和佣金
broker_config = [{
    "setcash": 100000,    # 本金
    "ballance": 100000,   # 余额
    "stake": 100,         # 每次交易股数
    "commission": 0.0005  # 佣金万五
}]
```

---

### 4. 添加自定义策略

**步骤**：
1. 在 `qbot/strategies/` 创建策略文件
2. 继承策略基类
3. 实现 `init()` 和 `next()` 方法

**模板**：
```python
from pytrader.easyquant.strategy.strategyTemplate import StrategyTemplate

class MyStrategy(StrategyTemplate):
    def init(self):
        # 初始化指标
        self.sma = self.calculate_sma(self.code, 20)
    
    def next(self):
        # 交易逻辑
        if self.price > self.sma:
            self.buy(self.code, self.price, 100)
        elif self.price < self.sma:
            self.sell(self.code, self.price, 100)
```

---

## 📈 策略分类

### 按交易对象
| 类型 | 说明 | 路径 |
|------|------|------|
| 股票策略 | A 股、港股等 | `qbot/strategies/` |
| 基金策略 | 场外基金、ETF | `pyfunds/strategy/` |
| 期货策略 | 商品期货、股指期货 | `pyfutures/` |
| 数字货币 | BTC、ETH 等 | `qbot/engine/trade/engine_apis/btc/` |

### 按策略类型
| 类型 | 说明 | 代表策略 |
|------|------|----------|
| 趋势跟踪 | 跟随趋势 | 双均线、布林带、阿隆指标 |
| 均值回归 | 回归均值 | BOLL 均值回归 |
| 动量策略 | 追涨杀跌 | RSI、KDJ、MACD |
| 多因子 | 多指标组合 | 多因子选股、Alpha 对冲 |
| AI 策略 | 机器学习 | LSTM、LightGBM、强化学习 |

---

## 🔌 数据接口

| 数据源 | 用途 | 配置位置 |
|--------|------|----------|
| Tushare | A 股数据 | `utils/common/TuShare.py` |
| AkShare | 免费 A 股数据 | 策略文件中直接使用 |
| efinance | 东方财富数据 | `monitoring.py` |
| 掘金量化 | 仿真交易 | `pytrader/easyquant/` |
| 币安 API | 数字货币 | `qbot/engine/trade/engine_apis/btc/` |

---

## ⚙️ 配置说明

### `qbot/common/config.py`
全局配置文件，包含：
- 数据路径配置
- 日志级别设置
- 交易参数默认值

### `qbot/gui/config.py`
GUI 配置文件，包含：
- 界面主题
- 默认股票列表
- 窗口布局参数

---

## 🛠️ 开发规范

### 添加新策略
1. 在 `qbot/strategies/` 创建 Python 文件
2. 遵循命名规范：`{strategy_name}_strategy.py`
3. 实现策略类，继承基类
4. 在 GUI 中注册策略

### 添加新数据源
1. 在 `qbot/data/` 或 `pytrader/easyquotation/` 添加数据获取类
2. 实现统一的数据接口
3. 更新配置

---

## ⚠️ 注意事项

1. **风险提示**：交易策略仅供学习研究，实盘交易风险自负
2. **Python 版本**：仅在 Python 3.8、3.9 下测试通过
3. **依赖安装**：部分依赖可能需要额外安装（如 wxPython、TA-Lib）
4. **交易权限**：实盘交易需要开通券商量化接口权限

---

## 📚 相关文档

- [安装指南](docs/Install_guide.md)
- [策略原理文档](docs/02-经典策略/)
- [常见问题](https://ufund-me.github.io/Qbot/#/04-常见问题/FQA)
- [在线文档](https://ufund-me.github.io/Qbot/#/)

---

**维护者**: Charmve  
**联系方式**: Yida_Zhang2 (微信)  
**开源协议**: CC BY-NC-SA 4.0
