import yfinance as yf
import pandas as pd
import json
import datetime

# רשימת מעקב / מניות לסריקה
TICKERS = ["AAPL", "NVDA", "MSFT", "AMZN", "META", "GOOGL", "TSLA", "AVAV", "CVE", "NET", "ET", "NBIS", "NOC", "PHM", "SMCI", "WDC", "AMD", "PLTR", "UBER", "SHOP"]

results = []

for ticker in TICKERS:
    try:
        data = yf.download(ticker, period="1y", interval="1d", progress=False)
        if len(data) < 150:
            continue
            
        # שיטוח עמודות במידת הצורך
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        close = data['Close']
        high = data['High']
        low = data['Low']
        volume = data['Volume']

        curr_price = float(close.iloc[-1])
        sma50 = float(close.rolling(50).mean().iloc[-1])
        sma150 = float(close.rolling(150).mean().iloc[-1])
        avg_vol = float(volume.rolling(20).mean().iloc[-1])
        curr_vol = float(volume.iloc[-1])

        # חישוב RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = float((100 - (100 / (1 + rs))).iloc[-1])

        # פילטר מגמה בסיסי: מחיר מעל MA150 ו-MA50
        if curr_price > sma150 and curr_price > 5 and avg_vol > 300000:
            recent_high = float(high.iloc[-20:-1].max())
            recent_low = float(low.iloc[-10:-1].min())

            # זיהוי סטאפ
            if curr_price >= recent_high * 0.985:
                setup_type = "Breakout (פריצה)"
                entry_trigger = round(recent_high * 1.002, 2)
                stop_loss = round(min(recent_low, sma50 * 0.99), 2)
            else:
                setup_type = "Pullback (נסיגה לתמיכה)"
                entry_trigger = round(curr_price, 2)
                stop_loss = round(min(sma50 * 0.985, recent_low), 2)

            # חישוב יחידת סיכון (R) ויעדי רווח
            risk_per_share = entry_trigger - stop_loss
            if risk_per_share <= 0:
                risk_per_share = entry_trigger * 0.03
                stop_loss = round(entry_trigger * 0.97, 2)

            tp1 = round(entry_trigger + (risk_per_share * 1.5), 2)  # יחס 1:1.5
            tp2 = round(entry_trigger + (risk_per_share * 2.5), 2)  # יחס 1:2.5
            
            risk_pct = round(((entry_trigger - stop_loss) / entry_trigger) * 100, 2)
            tp1_pct = round(((tp1 - entry_trigger) / entry_trigger) * 100, 2)
            tp2_pct = round(((tp2 - entry_trigger) / entry_trigger) * 100, 2)

            recommendation = f"כניסה: ${entry_trigger} | סטופ: ${stop_loss} (-{risk_pct}%) | יעד 1: ${tp1} (+{tp1_pct}%) | יעד 2: ${tp2} (+{tp2_pct}%)"
            analysis = f"סטאפ מסוג {setup_type}. המניה נסחרת מעל ממוצע 150 יום (${round(sma150,2)}) וממוצע 50 יום (${round(sma50,2)}). RSI ברמה של {round(rsi,1)}."

            results.append({
                "ticker": ticker,
                "price": round(curr_price, 2),
                "setup": setup_type,
                "entry": entry_trigger,
                "stop_loss": stop_loss,
                "tp1": tp1,
                "tp2": tp2,
                "risk_pct": risk_pct,
                "tp1_pct": tp1_pct,
                "tp2_pct": tp2_pct,
                "recommendation": recommendation,
                "analysis": analysis,
                "rsi": round(rsi, 1),
                "volume": int(curr_vol),
                "sma50": round(sma50, 2),
                "sma150": round(sma150, 2)
            })

    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")

# שמירת קובץ התוצאות
output = {
    "last_updated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": results
}

with open("screener_results_v2.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Screener finished. Found {len(results)} stocks.")
