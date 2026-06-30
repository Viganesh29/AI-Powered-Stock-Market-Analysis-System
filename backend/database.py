import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="10qpalzm",
        database="financial_ai"
    )


# =============================
# SAVE SEARCH HISTORY
# =============================
def save_search_history(ticker, asset_type, period):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO search_history (ticker, asset_type, period)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (ticker, asset_type, period))

    conn.commit()
    cursor.close()
    conn.close()


# =============================
# SAVE AI REPORT
# =============================
def save_ai_report(ticker, report):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO ai_reports (ticker, report)
    VALUES (%s, %s)
    """

    cursor.execute(query, (ticker, report))
    conn.commit()

    cursor.close()
    conn.close()


# =============================
# SAVE ASSET COMPARISON
# =============================
def save_asset_comparison(
    asset1,
    asset2,
    return1,
    return2,
    vol1,
    vol2,
    verdict
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO asset_comparisons
    (asset_1, asset_2, return_1, return_2,
     volatility_1, volatility_2, verdict)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (asset1, asset2, return1, return2, vol1, vol2, verdict)
    )

    conn.commit()
    cursor.close()
    conn.close()


# =============================
# SAVE PREDICTION
# =============================
def save_prediction(
    ticker,
    period,
    predicted_price,
    expected_return,
    volatility,
    signal,
    risk,
    confidence
):

    conn = get_connection()
    cursor = conn.cursor()

    # Convert numpy values to Python types
    predicted_price = float(predicted_price)
    expected_return = float(expected_return)
    volatility = float(volatility)

    query = """
    INSERT INTO predictions
    (asset_symbol, prediction_period,
     predicted_price, expected_return,
     volatility, trading_signal,
     risk_level, confidence_level)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            ticker,
            period,
            predicted_price,
            expected_return,
            volatility,
            str(signal),
            str(risk),
            str(confidence)
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

# =============================
# DATABASE ANALYTICS FUNCTIONS
# =============================

def get_most_searched():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT ticker, COUNT(*) as search_count
    FROM search_history
    GROUP BY ticker
    ORDER BY search_count DESC
    LIMIT 10
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def get_most_compared():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT asset_1, asset_2, COUNT(*) as compare_count
    FROM asset_comparisons
    GROUP BY asset_1, asset_2
    ORDER BY compare_count DESC
    LIMIT 10
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


def get_ai_reports():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT ticker, created_at
    FROM ai_reports
    ORDER BY created_at DESC
    LIMIT 20
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
def get_predictions():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT asset_symbol,
           prediction_period,
           predicted_price,
           expected_return,
           trading_signal,
           risk_level,
           confidence_level
    FROM predictions
    ORDER BY id DESC
    LIMIT 20
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result