#! /usr/bin/env python
# -*- encoding: utf-8 -*-

import datetime
import os
import json

import matplotlib.pyplot as plt
import numpy as np
import wx
from functools import partial

from qbot.gui.common.SysFile import Base_File_Oper
from qbot.common.logging.logger import LOGGER as logger

# 全局临时存储（程序关闭后丢失）
_temp_storage = {
    "tushare_api_key": None,
    "mysql_config": None,
    "csv_path": None
}

# 防止递归标志
_processing_tushare = False

QBOT_TOP_PATH = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
)


def MessageDialog(info):
    # 提示对话框
    # info:提示内容
    back_info = ""
    dlg_mesg = wx.MessageDialog(None, info, "温馨提示", wx.YES_NO | wx.ICON_INFORMATION)
    if dlg_mesg.ShowModal() == wx.ID_YES:
        back_info = "点击Yes"
    else:
        back_info = "点击No"
    dlg_mesg.Destroy()
    return back_info


def ChoiceDialog(info, choice):

    dlg_mesg = wx.SingleChoiceDialog(None, info, "单选提示", choice)
    dlg_mesg.SetSelection(0)  # default selection

    if dlg_mesg.ShowModal() == wx.ID_OK:
        select = dlg_mesg.GetStringSelection()
    else:
        select = None
    dlg_mesg.Destroy()
    return select

class WebDialog(wx.Dialog):  # user-defined

    load_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "/data/"

    def __init__(
        self, parent, title="Web显示", file_name="treemap_base.html", size=(1200, 900)
    ):

        wx.Dialog.__init__(
            self, parent, -1, title, size=size, style=wx.DEFAULT_FRAME_STYLE
        )

        self.browser = wx.html2.WebView.New(self, -1, size=size)
        with open(self.load_path + file_name, "r") as f:
            html_cont = f.read()
        self.browser.SetPage(html_cont, "")
        self.browser.Show()

class InputsDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title)
 
        self.panel = wx.Panel(self)
 
        self.text1 = wx.TextCtrl(self.panel, pos=(20, 20))
        self.text2 = wx.TextCtrl(self.panel, pos=(20, 60), style=wx.TE_PASSWORD)
 
        self.ok_button = wx.Button(self.panel, wx.ID_OK, "OK", pos=(20, 100))
        self.cancel_button = wx.Button(self.panel, wx.ID_CANCEL, "Cancel", pos=(120, 100))
 
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.ok_button)
 
        self.Fit()
 
    def OnOk(self, event):
        user = self.text1.GetValue()
        password = self.text2.GetValue()
        logger.info(f"User: {user}, Password: {password}")
        self.EndModal(wx.ID_OK)


class InputDialogTwoParameters(wx.Dialog):
    def __init__(self, parent, id, title, input_name1="用户名:", input_name2="密码:"):
        wx.Dialog.__init__(self, parent, id, title)
 
        self.panel = wx.Panel(self)
 
        mainBoxSizer = wx.BoxSizer(wx.VERTICAL)

        # 输入参数1
        textSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.textLabel1 = wx.StaticText(
            self.panel, 0, label=input_name1, pos=(40, 25)
        )
        # textFont = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        # textLabel1.SetFont(textFont)
        textSizer1.Add(self.textLabel1)
        textSizer1.Add((10, 10))
        self.text_ctrl1 = wx.TextCtrl(self.panel, pos=(120, 20))
        textSizer1.Add(self.text_ctrl1)

        # 输入参数2
        textSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.textLabel2 = wx.StaticText(
            self.panel, 0, label=input_name2, pos=(40, 70)
        )
        # textFont = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.BOLD)
        # textLabel1.SetFont(textFont)
        textSizer2.Add(self.textLabel2)
        # textSizer2.Add((10, 10))
        self.text_ctrl2 = wx.TextCtrl(self.panel, pos=(120, 60))
        textSizer2.Add(self.text_ctrl2)
 
        mainBoxSizer.Add(textSizer1, 
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
        mainBoxSizer.Add(textSizer2, 
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )
 
        # 创建确认和取消按钮
        self.button_cancel = wx.Button(self.panel, wx.ID_CANCEL, "Cancel", pos=(40, 100))
        self.button_ok = wx.Button(self.panel, wx.ID_OK, "OK", pos=(140, 100))
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.button_ok)
 
        # 设置对话框的大小
        self.SetSize((300, 200))
        self.Centre()
    
    def OnOk(self, event):
        user = self.text_ctrl1.GetValue()
        password = self.text_ctrl1.GetValue()
        logger.info(f"User: {user}, Password: {password}")
        self.EndModal(wx.ID_OK)


class UserDialog(wx.Dialog):  # user-defined
    def __init__(
        self, parent, title="自定义提示信息", label="自定义日志", size=(1024, 768)
    ):
        wx.Dialog.__init__(
            self, parent, -1, title, size=size, style=wx.DEFAULT_FRAME_STYLE
        )

        self.log_tx_input = wx.TextCtrl(
            self, -1, "", size=(600, 400), style=wx.TE_MULTILINE | wx.TE_READONLY
        )  # 多行|只读
        self.log_tx_input.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.ok_btn = wx.Button(self, wx.ID_OK, "确认")
        self.ok_btn.SetDefault()

        self.dialog_info_box = wx.StaticBox(self, -1, label)
        self.dialog_info_sizer = wx.StaticBoxSizer(self.dialog_info_box, wx.VERTICAL)
        self.dialog_info_sizer.Add(
            self.log_tx_input,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=10,
        )
        self.dialog_info_sizer.Add(self.ok_btn, proportion=0, flag=wx.ALIGN_CENTER)
        self.SetSizer(self.dialog_info_sizer)

        self.disp_loginfo()

    def disp_loginfo(self):
        self.log_tx_input.Clear()
        self.log_tx_input.AppendText(Base_File_Oper.read_log_trade())


class PostgreSQLConfigDialog(wx.Dialog):
    """PostgreSQL配置对话框"""
    
    def __init__(self, parent, id, title="PostgreSQL配置"):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 350))
        
        self.panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 表单字段
        fields = [
            ("host", "服务器地址:", "localhost"),
            ("port", "端口:", "5432"),
            ("database", "数据库:", ""),
            ("user", "用户名:", "postgres"),
            ("password", "密码:", ""),
            ("table", "表名:", "stock_data"),
        ]
        
        self.inputs = {}
        for field_id, label, default in fields:
            row_sizer = wx.BoxSizer(wx.HORIZONTAL)
            lbl = wx.StaticText(self.panel, label=label, size=(80, -1))
            if field_id == "password":
                txt = wx.TextCtrl(self.panel, value=default, style=wx.TE_PASSWORD, size=(250, -1))
            else:
                txt = wx.TextCtrl(self.panel, value=default, size=(250, -1))
            row_sizer.Add(lbl, 0, wx.ALL | wx.CENTER, 5)
            row_sizer.Add(txt, 0, wx.ALL, 5)
            main_sizer.Add(row_sizer, 0, wx.EXPAND | wx.ALL, 2)
            self.inputs[field_id] = txt
        
        # 按钮
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ok_btn = wx.Button(self.panel, wx.ID_OK, "确定")
        self.cancel_btn = wx.Button(self.panel, wx.ID_CANCEL, "取消")
        btn_sizer.Add(self.ok_btn, 0, wx.ALL, 5)
        btn_sizer.Add(self.cancel_btn, 0, wx.ALL, 5)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        self.panel.SetSizer(main_sizer)
        self.Centre()
    
    def get_config(self):
        """获取配置字典"""
        return {
            "host": self.inputs["host"].GetValue().strip(),
            "port": self.inputs["port"].GetValue().strip(),
            "database": self.inputs["database"].GetValue().strip(),
            "user": self.inputs["user"].GetValue().strip(),
            "password": self.inputs["password"].GetValue(),
            "table": self.inputs["table"].GetValue().strip(),
        }


class ParamsConfigDialog(wx.Dialog):
    def __init__(
        self, parent=None, title="参数配置", displaySize=(1440, 1120)
    ):
        displaySize_shrink = int(0.7 * displaySize[0]), int(0.6 * displaySize[1])
        wx.Dialog.__init__(
            self, parent, -1, title, size=displaySize_shrink, style=wx.DEFAULT_FRAME_STYLE
        )

        # 加载配置文件
        self.firm_para = Base_File_Oper.load_sys_para("firm_para.json")
        self.back_para = Base_File_Oper.load_sys_para("back_para.json")
        self.sys_para = Base_File_Oper.load_sys_para("sys_para.json")
        self.trade_plat_para = Base_File_Oper.load_sys_para("trade_plat_para.json")
        self.btc_trade_plat_para = Base_File_Oper.load_sys_para(
            "btc_trade_plat_para.json"
        )

        # 创建系统参数配置面板
        self.SysPanel = wx.Panel(self, -1)

        sys_input_box = wx.StaticBox(self.SysPanel, -1, "系统选项")
        sys_input_sizer = wx.StaticBoxSizer(sys_input_box, wx.VERTICAL)

        # 初始化操作系统类别
        self.sel_operate_val = ["macos", "windows", "linux_86"]

        self.sel_operate_cmbo = wx.ComboBox(
            self.SysPanel,
            -1,
            self.sys_para["operate_sys"],
            choices=self.sel_operate_val,
            style=wx.CB_SIMPLE | wx.CB_DROPDOWN | wx.CB_READONLY,
        )  # 选择操作系统
        sel_operate_text = wx.StaticText(self.SysPanel, -1, "当前操作系统")
        sel_operate_text.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))

        # 界面尺寸大小提示
        disp_size_text = wx.StaticText(
            self.SysPanel,
            -1,
            "显示器屏幕尺寸：\n长:{};宽:{}".format(displaySize[0], displaySize[1]),
        )
        disp_size_text.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL))

        sys_input_sizer.Add(
            sel_operate_text, proportion=0, flag=wx.EXPAND | wx.ALL, border=2
        )
        sys_input_sizer.Add(self.sel_operate_cmbo, 0, wx.EXPAND | wx.ALL | wx.CENTER, 2)
        sys_input_sizer.Add(disp_size_text, 0, wx.EXPAND | wx.ALL | wx.CENTER, 2)

        # 初始化数据存储方式
        data_store_list = ["本地csv", "postgresql"]
        self.data_store_box = wx.RadioBox(
            self.SysPanel,
            -1,
            label="数据存储",
            choices=data_store_list,
            majorDimension=2,
            style=wx.RA_SPECIFY_COLS,
        )
        # 绑定选择事件
        self.data_store_box.Bind(wx.EVT_RADIOBOX, self._ev_on_data_store_change)
        # 初始化存储变量
        self.data_store_val = self.data_store_box.GetStringSelection()
        # 加载已保存的配置
        self.data_store_config = self.sys_para.get("data_store_config", {})

        # 初始化数据源 - 调整顺序，将离线csv放在第一位作为安全默认值
        data_src_list = ["离线csv", "tushare", "新浪爬虫", "baostock"]
        self.data_src_box = wx.RadioBox(
            self.SysPanel,
            -1,
            label="数据源",
            choices=data_src_list,
            majorDimension=2,
            style=wx.RA_SPECIFY_ROWS,
        )
        # 绑定选择事件
        self.data_src_box.Bind(wx.EVT_RADIOBOX, self._ev_on_data_src_change)
        # 默认选中离线csv（安全默认值），不默认选tushare
        self.data_src_box.SetSelection(0)  # "离线csv"现在是第1个选项，索引为0
        self.data_src_Val = self.data_src_box.GetStringSelection()
        
        self.hbox_btt = wx.BoxSizer(wx.HORIZONTAL)

        # 保存按钮
        self.save_but = wx.Button(self.SysPanel, -1, "保存参数")
        self.save_but.Bind(wx.EVT_BUTTON, self._ev_save_para)  # 绑定按钮事件

        # 取消按钮
        self.cancel_but = wx.Button(self.SysPanel, -1, "取消")
        self.cancel_but.Bind(wx.EVT_BUTTON, self.OnClose)  # 绑定按钮事件
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.hbox_btt.Add(self.save_but, border=2, flag=wx.EXPAND | wx.ALL)
        self.hbox_btt.AddSpacer(20)
        self.hbox_btt.Add(self.cancel_but, border=2, flag=wx.EXPAND | wx.ALL)

        vboxnetA = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        vboxnetA.Add(
            sys_input_sizer, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=10
        )  # proportion参数控制容器尺寸比例
        vboxnetA.Add(
            self.data_store_box, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=10
        )
        vboxnetA.Add(
            self.data_src_box, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=10
        )
        vboxnetA.AddSpacer(30)
        vboxnetA.Add(
            self.hbox_btt, proportion=0, flag=wx.EXPAND | wx.BOTTOM, border=10
        )
        self.SysPanel.SetSizer(vboxnetA)

        # 创建显示参数配置面板
        self.CtrlPanel = wx.Panel(self, -1)

        # 创建FlexGridSizer布局网格
        # rows 定义GridSizer行数
        # cols 定义GridSizer列数
        # vgap 定义垂直方向上行间距
        # hgap 定义水平方向上列间距
        self.FlexGridSizer = wx.FlexGridSizer(rows=4, cols=4, vgap=10, hgap=10)

        self.trade_plat_ind = {
            "国信证券": ["", 201],
            "兴业证券": ["", 202],
            "国金证券": ["", 203],
            "国投证券（原安信）": ["", 204],
            "华泰证券": ["", 205],
            "银河证券": ["", 206],
            "财通证券": ["", 207],
            "海通证券": ["", 208],
            "国联证券": ["", 209],
            "通达信": ["", 210],
            "东方财富": ["", 211],
            "同花顺": ["", 212],
        }

        self.btc_trade_plat_ind = {
            "欧易OKX": ["", 201],
            "币安Binance": ["", 202],
            "火币Huobi": ["", 203],
            "CoinBase": ["", 204],
            "BitGet": ["", 205],
            "Bybit": ["", 206],
        }

        # 界面参数配置
        self.sys_ind = {
            "多子图MPL的单幅X大小": ["mpl_fig_x", 201],
            "多子图MPL的单幅Y大小": ["mpl_fig_y", 202],
            "多子图WEB的单幅X大小": ["web_size_x", 203],
            "多子图WEB的单幅Y大小": ["web_size_y", 204],
            "多子图MPL与左边框距离": ["mpl_fig_left", 205],
            "多子图MPL与右边框距离": ["mpl_fig_right", 206],
            "多子图MPL与上边框距离": ["mpl_fig_top", 207],
            "多子图MPL与下边框距离": ["mpl_fig_bottom", 208],
        }

        self.firm_mpl = {
            "行情MPL与左边框距离": ["left", 301],
            "行情MPL与右边框距离": ["right", 302],
            "行情MPL与上边框距离": ["top", 303],
            "行情MPL与下边框距离": ["bottom", 304],
        }

        self.back_mpl = {
            "回测MPL与左边框距离": ["left", 401],
            "回测MPL与右边框距离": ["right", 401],
            "回测MPL与上边框距离": ["top", 401],
            "回测MPL与下边框距离": ["bottom", 401],
        }

        self.TradePlatFlexGridSizer = wx.FlexGridSizer(rows=4, cols=4, vgap=10, hgap=10)
        trade_plat_box = wx.StaticBox(self.CtrlPanel, -1, "证券交易平台配置")
        trade_plat_sizer = wx.StaticBoxSizer(trade_plat_box, wx.HORIZONTAL)
        tradePlatLabelFont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)
        tradePlatAdsFont = wx.Font(
            8, wx.FONTFAMILY_ROMAN, wx.NORMAL, wx.NORMAL, underline=False
        )
        for k, v in self.trade_plat_ind.items():
            self.trade_plat_box = wx.StaticBox(self.CtrlPanel, -1, k)
            self.plat_ind_sizer = wx.StaticBoxSizer(self.trade_plat_box, wx.VERTICAL)

            # lable and logo
            self.hbox_sizer = wx.BoxSizer(wx.HORIZONTAL)

            bitmap = wx.Bitmap(self.trade_plat_para[k]["icon"])
            image = bitmap.ConvertToImage()
            image = image.Rescale(24, 24)
            bitmap = wx.Bitmap(image)
            static_bitmap = wx.StaticBitmap(self.CtrlPanel, wx.ID_ANY, bitmap)
            self.hbox_sizer.Add(static_bitmap, 0, wx.ALL | wx.CENTER, 5)

            self.plat_label_text = wx.StaticText(
                self.CtrlPanel,
                v[1],
                str(self.trade_plat_para[k]["labels"][0])
                + "  "
                + str(self.trade_plat_para[k]["labels"][1]),
                style=wx.TE_PROCESS_ENTER,
            )
            self.plat_label_text.SetFont(tradePlatLabelFont)
            self.plat_label_text.SetForegroundColour("red")
            self.hbox_sizer.Add(self.plat_label_text, 0, wx.ALL | wx.CENTER, 5)

            self.plat_ads_text = wx.StaticText(
                self.CtrlPanel,
                v[1],
                str(self.trade_plat_para[k]["ads"][0])
                + "  "
                + str(self.trade_plat_para[k]["ads"][1]),
                style=wx.TE_PROCESS_ENTER,
            )
            self.plat_ads_text.SetFont(tradePlatAdsFont)
            self.btn_open_account = wx.Button(self.CtrlPanel, label="立即开户")
            self.Bind(
                wx.EVT_BUTTON,
                partial(self.OnClickOpenAccunt, trade_plat=k),
                self.btn_open_account,
            )

            if k in ["国金证券", "华泰证券", "银河证券", "财通证券", "银河证券", "海通证券"]:
                self.btn_open_account.SetBackgroundColour("red")
                self.btn_open_account.SetForegroundColour("white")

            self.plat_ind_sizer.Add(
                self.hbox_sizer,
                proportion=0,
                flag=wx.EXPAND | wx.ALL | wx.CENTER,
                border=2,
            )
            self.plat_ind_sizer.Add(
                self.plat_ads_text,
                proportion=0,
                flag=wx.EXPAND | wx.ALL | wx.CENTER,
                border=2,
            )
            self.plat_ind_sizer.Add(
                self.btn_open_account,
                proportion=0,
                flag=wx.EXPAND | wx.ALL | wx.CENTER,
                border=2,
            )
            # 加入Sizer中
            self.TradePlatFlexGridSizer.Add(
                self.plat_ind_sizer, proportion=1, border=1, flag=wx.ALL | wx.EXPAND
            )
        trade_plat_sizer.Add(
            self.TradePlatFlexGridSizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        # 虚拟货币交易平台配置
        self.BtcTradePlatFlexGridSizer = wx.FlexGridSizer(
            rows=1, cols=6, vgap=10, hgap=10
        )
        btc_trade_plat_box = wx.StaticBox(self.CtrlPanel, -1, "虚拟货币交易平台配置")
        btc_trade_plat_sizer = wx.StaticBoxSizer(btc_trade_plat_box, wx.HORIZONTAL)
        btcTradePlatLabelFont = wx.Font(
            8, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False
        )
        btcTradePlatAdsFont = wx.Font(
            8, wx.FONTFAMILY_ROMAN, wx.NORMAL, wx.NORMAL, underline=False
        )
        for k, v in self.btc_trade_plat_ind.items():
            self.trade_plat_box1 = wx.StaticBox(self.CtrlPanel, -1, k)
            self.btc_plat_ind_vbox_sizer = wx.StaticBoxSizer(
                self.trade_plat_box1, wx.VERTICAL
            )

            # lable and logo
            self.hbox_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

            bitmap = wx.Bitmap(self.btc_trade_plat_para[k]["icon"])
            image = bitmap.ConvertToImage()
            image = image.Rescale(24, 24)
            bitmap = wx.Bitmap(image)
            static_bitmap = wx.StaticBitmap(self.CtrlPanel, wx.ID_ANY, bitmap)
            self.hbox_sizer2.Add(static_bitmap, 0, wx.ALL | wx.CENTER, 5)

            self.btc_plat_label_text = wx.StaticText(
                self.CtrlPanel,
                v[1],
                str(self.btc_trade_plat_para[k]["labels"][0])
                + "  "
                + str(self.btc_trade_plat_para[k]["labels"][1]),
                style=wx.TE_PROCESS_ENTER,
            )
            self.btc_plat_label_text.SetFont(btcTradePlatLabelFont)
            self.btc_plat_label_text.SetForegroundColour("red")
            self.hbox_sizer2.Add(self.btc_plat_label_text, 0, wx.ALL | wx.CENTER, 5)

            self.btc_plat_ads_text = wx.StaticText(
                self.CtrlPanel,
                v[1],
                str(self.btc_trade_plat_para[k]["ads"][0])
                + "  "
                + str(self.btc_trade_plat_para[k]["ads"][1]),
                style=wx.TE_PROCESS_ENTER,
            )
            self.btc_plat_ads_text.SetFont(btcTradePlatAdsFont)
            self.btn_open_btc_account = wx.Button(self.CtrlPanel, label="立即开户")
            self.Bind(
                wx.EVT_BUTTON,
                partial(self.OnClickOpenBtcAccunt, trade_plat=k),
                self.btn_open_btc_account,
            )

            if k in ["欧易OKX", "CoinBase", "BitGet"]:
                self.btn_open_btc_account.SetBackgroundColour("red")
                self.btn_open_btc_account.SetForegroundColour("white")

            self.btc_plat_ind_vbox_sizer.Add(
                self.hbox_sizer2,
                proportion=0,
                flag=wx.EXPAND | wx.ALL | wx.CENTER,
                border=2,
            )
            self.btc_plat_ind_vbox_sizer.Add(
                self.btc_plat_ads_text,
                proportion=0,
                flag=wx.EXPAND | wx.ALL | wx.CENTER,
                border=2,
            )
            self.btc_plat_ind_vbox_sizer.Add(
                self.btn_open_btc_account,
                proportion=0,
                flag=wx.EXPAND | wx.ALL | wx.CENTER,
                border=2,
            )
            # 加入Sizer中
            self.BtcTradePlatFlexGridSizer.Add(
                self.btc_plat_ind_vbox_sizer, proportion=1, border=1, flag=wx.ALL | wx.EXPAND
            )
        btc_trade_plat_sizer.Add(
            self.BtcTradePlatFlexGridSizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        kdata_plot_box = wx.StaticBox(self.CtrlPanel, -1, "行情可视化参数")
        kdata_plot_sizer = wx.StaticBoxSizer(kdata_plot_box, wx.HORIZONTAL)
        for k, v in self.sys_ind.items():
            self.sys_ind_box = wx.StaticBox(self.CtrlPanel, -1, k)
            self.sys_ind_sizer = wx.StaticBoxSizer(self.sys_ind_box, wx.VERTICAL)
            self.sys_ind_input = wx.TextCtrl(
                self.CtrlPanel,
                v[1],
                str(self.sys_para["multi-panels"][v[0]]),
                style=wx.TE_PROCESS_ENTER,
            )
            self.sys_ind_input.Bind(wx.EVT_TEXT_ENTER, self._ev_enter_stcode)
            self.sys_ind_sizer.Add(
                self.sys_ind_input,
                proportion=0,
                flag=wx.EXPAND | wx.ALL | wx.CENTER,
                border=2,
            )
            # 加入Sizer中
            self.FlexGridSizer.Add(
                self.sys_ind_sizer, proportion=1, border=1, flag=wx.ALL | wx.EXPAND
            )
        kdata_plot_sizer.Add(
            self.FlexGridSizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=2,
        )

        vboxnetB = wx.BoxSizer(wx.VERTICAL)  # 纵向box
        vboxnetB.Add(
            trade_plat_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=10,
        )  # proportion参数控制容器尺寸比例
        vboxnetB.Add(
            btc_trade_plat_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=10,
        )
        vboxnetB.Add(
            kdata_plot_sizer,
            proportion=0,
            flag=wx.EXPAND | wx.ALL | wx.CENTER,
            border=10,
        )  # proportion参数控制容器尺寸比例

        # for k, v in self.firm_mpl.items():
        #     self.firm_mpl_box = wx.StaticBox(self.CtrlPanel, -1, k)
        #     self.firm_mpl_sizer = wx.StaticBoxSizer(self.firm_mpl_box, wx.VERTICAL)
        #     self.firm_mpl_input = wx.TextCtrl(
        #         self.CtrlPanel,
        #         v[1],
        #         str(self.firm_para["layout_dict"][v[0]]),
        #         style=wx.TE_PROCESS_ENTER,
        #     )
        #     self.firm_mpl_input.Bind(wx.EVT_TEXT_ENTER, self._ev_enter_stcode)
        #     self.firm_mpl_sizer.Add(
        #         self.firm_mpl_input,
        #         proportion=0,
        #         flag=wx.EXPAND | wx.ALL | wx.CENTER,
        #         border=2,
        #     )
        #     # 加入Sizer中
        #     self.FlexGridSizer.Add(
        #         self.firm_mpl_sizer, proportion=1, border=1, flag=wx.ALL | wx.EXPAND
        #     )

        # for k, v in self.back_mpl.items():
        #     self.back_mpl_box = wx.StaticBox(self.CtrlPanel, -1, k)
        #     self.back_mpl_sizer = wx.StaticBoxSizer(self.back_mpl_box, wx.VERTICAL)
        #     self.back_mpl_input = wx.TextCtrl(
        #         self.CtrlPanel,
        #         v[1],
        #         str(self.back_para["layout_dict"][v[0]]),
        #         style=wx.TE_PROCESS_ENTER,
        #     )
        #     self.back_mpl_input.Bind(wx.EVT_TEXT_ENTER, self._ev_enter_stcode)
        #     self.back_mpl_sizer.Add(
        #         self.back_mpl_input,
        #         proportion=0,
        #         flag=wx.EXPAND | wx.ALL | wx.CENTER,
        #         border=2,
        #     )
        #     # 加入Sizer中
        #     self.FlexGridSizer.Add(
        #         self.back_mpl_sizer, proportion=1, border=1, flag=wx.ALL | wx.EXPAND
        #     )

        # self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)

        # self.CtrlPanel.SetSizer(self.FlexGridSizer)
        self.CtrlPanel.SetSizer(vboxnetB)

        self.HBoxPanel = wx.BoxSizer(wx.HORIZONTAL)
        self.HBoxPanel.Add(
            self.SysPanel, proportion=2, border=2, flag=wx.EXPAND | wx.ALL
        )
        self.HBoxPanel.Add(
            self.CtrlPanel, proportion=10, border=2, flag=wx.EXPAND | wx.ALL
        )
        self.SetSizer(self.HBoxPanel)
        # 注意：不再默认选中tushare，所以不需要初始化检查

    def OnClickOpenAccunt(self, event, trade_plat):
        back_info = ""
        current_license = self.trade_plat_para[trade_plat]['license']
        if current_license is not None and current_license:
            back_info = MessageDialog(f"当前{trade_plat}交易接口授权码为: {current_license}，是否要更新?")
        else:
            back_info = MessageDialog(f"微信联系Yida_Zhang2 获取自动化实盘交易接口后，填写参数：")

        if back_info == "点击No":
            return 0
        
        dialog = wx.TextEntryDialog(None, "Enter Parameter", "交易接口授权License")
        if dialog.ShowModal() == wx.ID_OK:
            parameter = dialog.GetValue()
            logger.info(f"The License is: {parameter}")

            self.trade_plat_para[trade_plat]["license"] = parameter

            Base_File_Oper.save_sys_para("trade_plat_para.json", self.trade_plat_para)
            # MessageDialog("存储完成！点击界面顶部的菜单栏->主菜单->返回")
        
        dialog.Destroy()
        self.Close()
    
    def OnClickOpenBtcAccunt(self, event, trade_plat):
        select_mode = ChoiceDialog(
            "请选择填写key对应的交易模式",
            [
                "模拟交易",
                "实盘交易",
            ],
        )
        dlg = InputDialogTwoParameters(
            None, -1, select_mode+" - "+trade_plat, input_name1="apikey:", input_name2="secretkey:"
        )
        if dlg.ShowModal() == wx.ID_OK:
            apikey = dlg.text_ctrl1.GetValue()
            secretkey = dlg.text_ctrl2.GetValue()
            logger.info(f"apikey: {apikey}, secretkey: {secretkey}")

            current_uid = "123456"
            if select_mode == "实盘交易":
                current_uid = self.btc_trade_plat_para[trade_plat]["api_key"][
                    "real_trade"
                ]["uid"]
                self.btc_trade_plat_para[trade_plat]["api_key"]["real_trade"][
                    "apikey"
                ] = apikey
                self.btc_trade_plat_para[trade_plat]["api_key"]["real_trade"][
                    "secretkey"
                ] = secretkey
            elif select_mode == "模拟交易":
                current_uid = self.btc_trade_plat_para[trade_plat]["api_key"][
                    "sim_trade"
                ]["uid"]
                self.btc_trade_plat_para[trade_plat]["api_key"]["sim_trade"][
                    "apikey"
                ] = apikey
                self.btc_trade_plat_para[trade_plat]["api_key"]["sim_trade"][
                    "secretkey"
                ] = secretkey

            back_info = ""
            if (
                current_uid is not None
                and current_uid
                and current_uid != ""
            ):
                back_info = MessageDialog(
                    f"当前{trade_plat}[{select_mode}]交易接口用户ID为: {current_uid}，是否要更新?"
                )
            else:
                back_info = MessageDialog(
                    f"微信联系Yida_Zhang2 或者自行获取{trade_plat}账户uid后，填写参数."
                )
            if back_info == "点击Yes":
                dialog = wx.TextEntryDialog(
                    None,
                    "Enter Parameter",
                    f"{trade_plat}[{select_mode}]交易接口用户ID",
                )
                if dialog.ShowModal() == wx.ID_OK:
                    uid = dialog.GetValue()
                    logger.info(f"The uid is: {uid}")

                    if select_mode == "实盘交易":
                        self.btc_trade_plat_para[trade_plat]["api_key"]["real_trade"][
                            "uid"
                        ] = uid
                    elif select_mode == "模拟交易":
                        self.btc_trade_plat_para[trade_plat]["api_key"]["sim_trade"][
                            "uid"
                        ] = uid

                    Base_File_Oper.save_sys_para(
                        "btc_trade_plat_para.json", self.btc_trade_plat_para
                    )
                dialog.Destroy()

            Base_File_Oper.save_sys_para(
                "btc_trade_plat_para.json", self.btc_trade_plat_para
            )
        dlg.Destroy()
        self.Close()
    
    def OnClose(self, event):
        self.Close()
        event.Skip()
 
    def OnCloseWindow(self, event):
        logger.info("Dialog is closing...")
        # 在这里执行关闭前需要的操作
        self.Destroy()
        event.Skip()

    def _ev_switch_menu(self, event):
        pass

    def _ev_on_data_store_change(self, event):
        """数据存储方式改变事件"""
        selection = self.data_store_box.GetStringSelection()
        
        if selection == "本地csv":
            # 弹出目录选择对话框
            dlg = wx.DirDialog(self, "选择CSV数据存储目录", 
                              style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            if dlg.ShowModal() == wx.ID_OK:
                selected_path = dlg.GetPath()
                self.data_store_config["type"] = "csv"
                self.data_store_config["path"] = selected_path
                # 临时存储
                _temp_storage["csv_path"] = selected_path
                logger.info(f"CSV存储路径已设置: {selected_path}")
                wx.MessageBox(f"CSV存储路径已设置:\n{selected_path}", "提示", wx.OK | wx.ICON_INFORMATION)
            dlg.Destroy()
            
        elif selection == "postgresql":
            # 使用CallAfter延迟弹出对话框，避免事件处理中的重入问题
            wx.CallAfter(self._show_pg_config_dialog)

    def _show_pg_config_dialog(self):
        """显示PostgreSQL配置对话框"""
        try:
            pg_dlg = PostgreSQLConfigDialog(self, -1, "PostgreSQL数据库配置")
            result = pg_dlg.ShowModal()
            if result == wx.ID_OK:
                config = pg_dlg.get_config()
                pg_dlg.Destroy()
                # 异步测试连接
                self._test_pg_connection_with_busy(config)
            else:
                pg_dlg.Destroy()
        except Exception as e:
            logger.error(f"显示PostgreSQL配置对话框失败: {e}")
            wx.MessageBox(f"打开配置对话框失败: {str(e)}", "错误", wx.OK | wx.ICON_ERROR)

    def _test_pg_connection_with_busy(self, config):
        """带进度提示的PostgreSQL连接测试"""
        # 创建进度对话框
        self._pg_progress = wx.ProgressDialog(
            "连接测试",
            "正在连接PostgreSQL数据库，请稍候...",
            maximum=100,
            parent=self,
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
        )
        self._pg_progress.Update(0)
        
        # 使用定时器来执行连接测试，避免阻塞
        def do_test():
            try:
                success, error_msg = self._test_postgresql_connection(config)
                wx.CallAfter(self._on_pg_test_complete, success, config, error_msg)
            except Exception as e:
                logger.error(f"PostgreSQL连接测试异常: {e}")
                wx.CallAfter(self._on_pg_test_complete, False, config, str(e))
        
        import threading
        thread = threading.Thread(target=do_test, daemon=True)
        thread.start()

    def _on_pg_test_complete(self, success, config, error_msg=None):
        """PostgreSQL连接测试完成回调"""
        if hasattr(self, '_pg_progress') and self._pg_progress:
            self._pg_progress.Update(100)
            self._pg_progress.Destroy()
            self._pg_progress = None
        
        if success:
            self.data_store_config["type"] = "postgresql"
            self.data_store_config["config"] = config
            # 临时存储密码，其他存入配置
            _temp_storage["postgresql_config"] = config
            logger.info(f"PostgreSQL配置已设置: {config['host']}/{config['database']}")
            wx.MessageBox("PostgreSQL连接成功!\n查询测试通过。", "提示", wx.OK | wx.ICON_INFORMATION)
        else:
            if error_msg:
                wx.MessageBox(f"PostgreSQL连接失败:\n{error_msg}", "错误", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("PostgreSQL连接失败，请检查配置!\n\n请确认:\n1. 数据库服务已启动\n2. 网络连接正常\n3. 用户名密码正确\n4. 数据库和表名存在", "错误", wx.OK | wx.ICON_ERROR)

    def _ev_on_data_src_change(self, event):
        """数据源选择改变事件"""
        global _processing_tushare
        
        # 防止递归调用
        if _processing_tushare:
            logger.info("正在处理tushare，跳过递归调用")
            return
        
        try:
            selection = self.data_src_box.GetStringSelection()
            logger.info(f"数据源选择改变: {selection}")
            self.data_src_Val = selection
            
            if selection == "tushare":
                logger.info("检测到tushare选择，准备显示API Key输入对话框")
                _processing_tushare = True
                self._show_tushare_dialog()
            else:
                # 切换到非tushare时，清除API key
                _temp_storage["tushare_api_key"] = None
                # 删除临时token文件
                temp_token_file = os.path.join(QBOT_TOP_PATH, "qbot", "common", "configs", "temp_tushare_token.txt")
                try:
                    if os.path.exists(temp_token_file):
                        os.remove(temp_token_file)
                        logger.info("Tushare API Key 临时文件已删除（切换数据源时）")
                except Exception as e:
                    logger.warning(f"删除临时token文件失败: {e}")
        except Exception as e:
            logger.error(f"数据源选择改变事件处理异常: {e}")
            import traceback
            logger.error(traceback.format_exc())
            _processing_tushare = False
            wx.MessageBox(f"处理数据源选择事件时出错:\n{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
    
    def _show_tushare_dialog(self):
        """显示Tushare API Key输入对话框"""
        global _processing_tushare
        
        logger.info("显示Tushare API Key输入对话框")
        
        try:
            # 检查是否已经设置过
            if _temp_storage.get("tushare_api_key"):
                logger.info("API Key已设置，询问是否重新输入")
                dlg = wx.MessageDialog(self, 
                    "Tushare API Key 已设置，是否重新输入?", 
                    "确认", 
                    wx.YES_NO | wx.ICON_QUESTION)
                result = dlg.ShowModal()
                dlg.Destroy()
                if result != wx.ID_YES:
                    logger.info("用户选择不重新输入")
                    _processing_tushare = False
                    return
            
            dlg = wx.TextEntryDialog(self, "请输入Tushare API Key:", "Tushare登录")
            dlg.SetValue(_temp_storage.get("tushare_api_key") or "")
            
            result = dlg.ShowModal()
            logger.info(f"对话框返回结果: {result}")
            
            if result == wx.ID_OK:
                api_key = dlg.GetValue().strip()
                logger.info(f"用户输入API Key长度: {len(api_key)}")
                if api_key:
                    _temp_storage["tushare_api_key"] = api_key
                    temp_token_file = os.path.join(QBOT_TOP_PATH, "qbot", "common", "configs", "temp_tushare_token.txt")
                    try:
                        with open(temp_token_file, "w", encoding="utf-8") as f:
                            f.write(api_key)
                        logger.info("Tushare API Key 已保存到临时文件")
                    except Exception as e:
                        logger.warning(f"保存临时token失败: {e}")
                    wx.MessageBox("Tushare API Key 已设置!\n注意：程序关闭后需重新输入。", "提示", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("API Key 不能为空!", "警告", wx.OK | wx.ICON_WARNING)
                    self.data_src_box.SetSelection(0)
                    self.data_src_Val = "离线csv"
            else:
                logger.info("用户取消输入，切换回离线csv")
                self.data_src_box.SetSelection(0)
                self.data_src_Val = "离线csv"
            
            dlg.Destroy()
        except Exception as e:
            logger.error(f"显示Tushare对话框时发生异常: {e}")
            import traceback
            logger.error(traceback.format_exc())
            wx.MessageBox(f"显示API Key输入框时出错:\n{str(e)}", "错误", wx.OK | wx.ICON_ERROR)
        finally:
            _processing_tushare = False

    def _test_postgresql_connection(self, config):
        """测试PostgreSQL连接并执行查询，返回 (success: bool, error_msg: str)"""
        import socket
        
        # 先测试网络连通性
        try:
            port = int(config.get('port', 5432))
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)  # 3秒超时
            result = sock.connect_ex((config['host'], port))
            sock.close()
            if result != 0:
                return False, f"无法连接到 {config['host']}:{port}，请检查网络或防火墙设置"
        except Exception as e:
            logger.warning(f"网络连通性测试失败: {e}")
            # 继续尝试数据库连接，不因此中断
        
        try:
            import psycopg2
            # 连接数据库，使用较短的超时
            conn = psycopg2.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                dbname=config['database'],
                port=int(config.get('port', 5432)),
                connect_timeout=5,  # 连接超时5秒
                options='-c statement_timeout=5000'  # 查询超时5秒
            )
            
            # 执行查询 - 使用schema.table格式更安全
            with conn.cursor() as cursor:
                table = config['table']
                # 检查表是否存在
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (table,))
                table_exists = cursor.fetchone()[0]
                
                if not table_exists:
                    logger.warning(f"表 '{table}' 不存在，但连接成功")
                else:
                    # 尝试查询表结构 - 使用 库.表 格式
                    database = config['database']
                    cursor.execute(f"SELECT * FROM {database}.{table} LIMIT 1")
                    result = cursor.fetchone()
                    logger.info(f"PostgreSQL查询成功，表: {database}.{table}")
            
            conn.close()
            return True, None
        except ImportError:
            logger.error("未安装psycopg2，请执行: pip install psycopg2-binary")
            return False, "未安装psycopg2模块!\n请执行: pip install psycopg2-binary"
        except psycopg2.OperationalError as e:
            error_msg = str(e)
            logger.error(f"PostgreSQL连接失败: {error_msg}")
            # 提供更友好的错误提示
            if "Connection refused" in error_msg:
                return False, f"连接被拒绝:\n数据库服务器 {config['host']}:{config.get('port', 5432)} 未启动或拒绝连接。\n请检查:\n1. PostgreSQL服务是否已启动\n2. 防火墙是否允许连接\n3. pg_hba.conf 配置是否正确"
            elif "password authentication" in error_msg:
                return False, "用户名或密码错误，请检查后重试。"
            elif "database" in error_msg and "does not exist" in error_msg:
                return False, f"数据库 '{config['database']}' 不存在，请先创建数据库。"
            elif "timeout" in error_msg.lower():
                return False, "连接超时:\n无法在指定时间内连接到数据库服务器。\n请检查:\n1. 网络连接是否正常\n2. 服务器地址和端口是否正确\n3. 服务器是否可访问"
            else:
                return False, f"连接错误: {error_msg}"
        except Exception as e:
            logger.error(f"PostgreSQL连接失败: {str(e)}")
            return False, f"连接异常: {str(e)}"

    def _ev_save_para(self, event):

        self.sys_para["operate_sys"] = self.sel_operate_cmbo.GetStringSelection()
        # 保存数据存储配置
        if hasattr(self, 'data_store_config') and self.data_store_config:
            self.sys_para["data_store_config"] = self.data_store_config
        # 保存数据源配置（不含敏感信息）
        self.sys_para["data_source"] = self.data_src_box.GetStringSelection()
        
        Base_File_Oper.save_sys_para("sys_para.json", self.sys_para)
        MessageDialog("存储完成！")
        self.Close()

    def _ev_enter_stcode(self, event):

        if event.GetId() < 300:
            # 系统级显示
            for k, v in self.sys_ind.items():
                if v[1] == event.GetId():
                    self.sys_para["multi-panels"][v[0]] = int(event.GetString())
                    break
            Base_File_Oper.save_sys_para("sys_para.json", self.sys_para)

        elif event.GetId() < 400:
            # 行情MPL
            for k, v in self.firm_mpl.items():
                if v[1] == event.GetId():
                    self.firm_para["layout_dict"][v[0]] = float(event.GetString())
                    break
            Base_File_Oper.save_sys_para("firm_para.json", self.firm_para)

        else:
            # 回测MPL
            for k, v in self.back_mpl.items():
                if v[1] == event.GetId():
                    self.back_para["layout_dict"][v[0]] = float(event.GetString())
                    break
            Base_File_Oper.save_sys_para("back_para.json", self.back_para)

