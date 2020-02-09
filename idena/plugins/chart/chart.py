import io
import threading
import pandas as pd
import plotly.io as pio
import plotly.graph_objs as go
import idena.emoji as emo

from io import BytesIO
from pandas import DataFrame
from telegram import ParseMode
from pycoingecko import CoinGeckoAPI
from idena.plugin import IdenaPlugin


class Chart(IdenaPlugin):

    CG_ID = "idena"
    BASE = "btc"

    @IdenaPlugin.threaded
    @IdenaPlugin.send_typing
    def execute(self, bot, update, args):
        if args:
            if len(args) > 1:
                update.message.reply_text(
                    text=self.get_usage(),
                    parse_mode=ParseMode.MARKDOWN)
                return
            if not args[0].isnumeric():
                update.message.reply_text(
                    text=f"{emo.ERROR} The provided argument has to be a number (days)",
                    parse_mode=ParseMode.MARKDOWN)
                return
            time_frame = int(args[0])  # Days
        else:
            time_frame = 3  # Days

        try:
            info = CoinGeckoAPI().get_coin_by_id(self.CG_ID)
            market = CoinGeckoAPI().get_coin_market_chart_by_id(self.CG_ID, self.BASE, time_frame)
        except Exception as e:
            return self.notify(e)

        # Volume
        df_volume = DataFrame(market["total_volumes"], columns=["DateTime", "Volume"])
        df_volume["DateTime"] = pd.to_datetime(df_volume["DateTime"], unit="ms")
        volume = go.Scatter(
            x=df_volume.get("DateTime"),
            y=df_volume.get("Volume"),
            name="Volume"
        )

        # Price
        df_price = DataFrame(market["prices"], columns=["DateTime", "Price"])
        df_price["DateTime"] = pd.to_datetime(df_price["DateTime"], unit="ms")
        price = go.Scatter(
            x=df_price.get("DateTime"),
            y=df_price.get("Price"),
            yaxis="y2",
            name="Price",
            line=dict(
                color="rgb(22, 96, 167)",
                width=2
            )
        )

        margin_l = 140
        tickformat = "0.8f"

        max_value = df_price["Price"].max()
        if max_value > 0.9:
            if max_value > 999:
                margin_l = 90
                tickformat = "0,.0f"
            else:
                margin_l = 95
                tickformat = "0.2f"

        layout = go.Layout(
            images=[dict(
                source=info["image"]["large"],
                opacity=0.8,
                xref="paper", yref="paper",
                x=1.05, y=1,
                sizex=0.2, sizey=0.2,
                xanchor="right", yanchor="bottom"
            )],
            paper_bgcolor='rgb(233,233,233)',
            plot_bgcolor='rgb(233,233,233)',
            autosize=False,
            width=800,
            height=600,
            margin=go.layout.Margin(
                l=margin_l,
                r=50,
                b=85,
                t=100,
                pad=4
            ),
            yaxis=dict(
                domain=[0, 0.20]
            ),
            yaxis2=dict(
                domain=[0.25, 1],
                tickprefix="",
                ticksuffix=""
            ),
            title=dict(
                text=f"{info['symbol'].upper()} Price & Volume in {self.BASE.upper()}",
                font=dict(
                    size=24
                )
            ),
            legend=dict(
                orientation="h",
                yanchor="top",
                xanchor="center",
                y=1.05,
                x=0.45
            ),
            shapes=[{
                "type": "line",
                "xref": "paper",
                "yref": "y2",
                "x0": 0,
                "x1": 1,
                "y0": market["prices"][len(market["prices"]) - 1][1],
                "y1": market["prices"][len(market["prices"]) - 1][1],
                "line": {
                    "color": "rgb(50, 171, 96)",
                    "width": 1,
                    "dash": "dot"
                }
            }],
        )

        try:
            fig = go.Figure(data=[price, volume], layout=layout)
        except Exception as e:
            return self.notify(e)

        fig["layout"]["yaxis2"].update(tickformat=tickformat)

        update.message.reply_photo(photo=io.BufferedReader(BytesIO(pio.to_image(fig, format="jpeg"))))
