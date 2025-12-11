import re
import pandas as pd

def is_english_card(card_name, set_name=None, description=None):
    """
    Determine if card is English version
    """
    japanese_indicators = [
        '日本', 'japanese', 'jpn', 'jp', 'プロモ',
        'japan exclusive', 'japanese language'
    ]

    korean_indicators = ['korean', 'kor', '한국', 'korea']

    other_language_indicators = [
        'german', 'french', 'italian', 'spanish',
        'portuguese', 'chinese', 'thai'
    ]

    text_to_check = f"{card_name} {set_name or ''} {description or ''}".lower()

    all_indicators = japanese_indicators + korean_indicators + other_language_indicators

    for indicator in all_indicators:
        if indicator in text_to_check:
            return False

    return True

def normalize_card_name(card_name):
    """
    Normalize card name for matching
    """
    # Convert to lowercase
    name = card_name.lower()

    # Remove special characters but keep spaces
    name = re.sub(r'[^\w\s]', ' ', name)

    # Remove set numbers like "125/198"
    name = re.sub(r'\d+\/\d+', '', name)

    # Remove extra whitespace
    name = ' '.join(name.split())

    return name.strip()

def extract_card_type(card_name):
    """
    Extract card type (ex, VMAX, V, etc.)
    """
    name_lower = card_name.lower()

    if ' ex' in name_lower or '-ex' in name_lower:
        return 'ex'
    elif 'vmax' in name_lower:
        return 'VMAX'
    elif 'vstar' in name_lower:
        return 'VSTAR'
    elif ' v ' in name_lower or name_lower.endswith(' v'):
        return 'V'
    elif 'gx' in name_lower:
        return 'GX'
    elif ' ex ' in name_lower or name_lower.endswith(' ex'):
        return 'EX'
    else:
        return 'Regular'

def clean_price(price_str):
    """
    Clean price string to float
    """
    if isinstance(price_str, (int, float)):
        return float(price_str)

    # Remove currency symbols and commas
    price_str = str(price_str).replace('$', '').replace(',', '').strip()

    try:
        return float(price_str)
    except:
        return None

def filter_english_cards(df):
    """
    Filter dataframe to only English cards
    """
    df['is_english'] = df.apply(
        lambda row: is_english_card(
            row['card_name'],
            row.get('set_name'),
            row.get('description')
        ),
        axis=1
    )

    return df[df['is_english'] == True].copy()