import yfinance as yf
import pandas as pd
import datetime
import json
import time

def calculate_rsi(data, periods=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def run_screener():
    print("Starting advanced swing setup screener...")
    
    # רשימה מורחבת של מניות מסקטורים שונים
    tickers = [
        'AAPL', 'MSFT', 'NVDA', 'META', 'AMZN', 'AVAV', 'CVE', 'NET', 
        'ET', 'NOC', 'PHM', 'SMCI', 'WDC', 'NBIS', 'JPM', 'V', 'WMT', 'NFLX', 'AMD'
    ]
    
    results = []
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            info = stock.info
            
            if hist.empty or len(hist) < 150:
                continue
                
            market_cap = info.get('marketCap', 0)
            price = hist['Close'].iloc[-1]
            volume = hist['Volume'].rolling(window=90).mean().iloc[-1]
            
            # סינון בסיסי לנזילות ושווי שוק
            if market_cap < 1e9 or price < 5 or volume < 400000:
                continue
                
            # חישוב ממוצעים ו-RSI
            hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
            hist['SMA_150'] = hist['Close'].rolling(window=150).mean()
            hist['RSI_14'] = calculate_rsi(hist)
            
            # MACD חישוב
            hist['EMA_12'] = hist['Close'].ewm(span=12, adjust=False).mean()
            hist['EMA_26'] = hist['Close'].ewm(span=26, adjust=False).mean()
            hist['MACD'] = hist['EMA_12'] - hist['EMA_26']
            hist['Signal'] = hist['MACD'].ewm(span=9, adjust=False).mean()
            
            # Bollinger Bands חישוב
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            hist['STD_20'] = hist['Close'].rolling(window=20).std()
            hist['Upper_BB'] = hist['SMA_20'] + (hist['STD_20'] * 2)
            hist['Lower_BB'] = hist['SMA_20'] - (hist['STD_20'] * 2)
            hist['Bandwidth'] = (hist['Upper_BB'] - hist['Lower_BB']) / hist['SMA_20']
            
            # שליפת הנתונים הנוכחיים
            sma_50 = hist['SMA_50'].iloc[-1]
            sma_150 = hist['SMA_150'].iloc[-1]
            rsi = hist['RSI_14'].iloc[-1]
            macd = hist['MACD'].iloc[-1]
            signal = hist['Signal'].iloc[-1]
            macd_prev = hist['MACD'].iloc[-2]
            signal_prev = hist['Signal'].iloc[-2]
            
            # זיהוי תנאים מיוחדים (Squeeze, MACD Crossover)
            current_bandwidth = hist['Bandwidth'].iloc[-1]
            min_bandwidth_120d = hist['Bandwidth'].rolling(window=120).min().iloc[-1]
            is_squeeze = bool(current_bandwidth <= (min_bandwidth_120d * 1.2))
            macd_bullish = bool(macd > signal and macd_prev <= signal_prev)
            
            # תבניות נרות יפניים ביומיים האחרונים
            open_0, close_0, high_0, low_0 = hist['Open'].iloc[-1], hist['Close'].iloc[-1], hist['High'].iloc[-1], hist['Low'].iloc[-1]
            open_1, close_1 = hist['Open'].iloc[-2], hist['Close'].iloc[-2]
            
            # בולען שורי
            is_engulfing = bool(close_1 < open_1 and close_0 > open_0 and open_0 < close_1 and close_0 > open_1)
            # פטיש
            body = abs(close_0 - open_0)
            lower_shadow = min(open_0, close_0) - low_0
            upper_shadow = high_0 - max(open_0, close_0)
            is_hammer = bool(lower_shadow > (2 * body) and upper_shadow < (0.5 * body) and body > 0)
            
            has_pattern = is_engulfing or is_hammer
            pattern_name = "בולען שורי" if is_engulfing else ("פטיש" if is_hammer else "אין")
            
            # זיהוי פולבאק (מחיר בקרבה של 2.5% לממוצע 50 או 150)
            pullback_50 = bool(abs(low_0 - sma_50) / sma_50 < 0.025)
            pullback_150 = bool(abs(low_0 - sma_150) / sma_150 < 0.025)
            is_pullback = pullback_50 or pullback_150
            
            # סינון סופי: רק מניות במבנה מגמה עולה (מחיר > 150, ממוצע 50 > 150)
            if price > sma_150 and sma_50 > sma_150 and 40 <= rsi <= 75:
                
                # מנוע בניית הסטאפ וההמלצות (Scoring System)
                score = 0
                if is_squeeze: score += 1
                if macd_bullish: score += 1
                if has_pattern: score += 1
                if is_pullback: score += 1
                
                recommendation = "מעקב (חסר טריגר)"
                if score >= 2: recommendation = "הכנה לכניסה (סטאפ מתהווה)"
                if score >= 3: recommendation = "קנייה חזקה - סטאפ בשל"
                if is_squeeze and has_pattern: recommendation = "פריצה קרובה - כיווץ + נר היפוך"
                if is_pullback and has_pattern: recommendation = "כניסה בפולבאק - תמיכה + נר היפוך"

                results.append({
                    "ticker": ticker,
                    "price": round(price, 2),
                    "rsi": round(rsi, 2),
                    "sma_50": round(sma_50, 2),
                    "sma_150": round(sma_150, 2),
                    "sector": info.get('sector', 'Unknown'),
                    "in_squeeze": is_squeeze,
                    "macd_bullish": macd_bullish,
                    "pattern": pattern_name,
                    "is_pullback": is_pullback,
                    "recommendation": recommendation,
                    "score": score
                })
                
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            
    # סידור התוצאות מהציון הגבוה לנמוך (הסטאפים הטובים ביותר למעלה)
    results = sorted(results, key=lambda x: x['score'], reverse=True)
            
    output_data = {
        "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_results": len(results),
        "stocks": results
    }
    
    with open('screener_results_v2.json', 'w') as f:
        json.dump(output_data, f, indent=4)
        
    print(f"Completed. Found {len(results)} active setups.")

if __name__ == '__main__':
    run_screener()
