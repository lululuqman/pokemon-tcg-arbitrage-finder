from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    card_name = Column(String, nullable=False, index=True)
    set_name = Column(String, index=True)
    card_number = Column(String)
    rarity = Column(String, index=True)
    card_type = Column(String)  # 'ex', 'VMAX', 'V', etc.

    # Language filtering
    language = Column(String, default='English', index=True)
    is_english_verified = Column(Boolean, default=False)

    # Images
    image_url_small = Column(String)
    image_url_large = Column(String)

    # Normalization
    normalized_name = Column(String, index=True)

    # Pokemon TCG API ID
    pokemon_tcg_id = Column(String, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    prices = relationship("Price", back_populates="card")
    arbitrage_opportunities = relationship("ArbitrageOpportunity", back_populates="card")

class Price(Base):
    __tablename__ = 'prices'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)

    marketplace = Column(String, nullable=False, index=True)  # 'tcgplayer', 'ebay'
    price = Column(Float, nullable=False)
    condition = Column(String, default='NM')  # NM, LP, MP, HP, DMG

    listing_url = Column(String)
    seller_rating = Column(Float)

    # Validation
    is_verified = Column(Boolean, default=False)
    ai_price_check = Column(String)  # 'REASONABLE', 'SUSPICIOUS_HIGH', 'SUSPICIOUS_LOW'

    scraped_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    card = relationship("Card", back_populates="prices")

class ArbitrageOpportunity(Base):
    __tablename__ = 'arbitrage_opportunities'

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('cards.id'), nullable=False)

    buy_marketplace = Column(String, nullable=False)
    buy_price = Column(Float, nullable=False)
    buy_url = Column(String)

    sell_marketplace = Column(String, nullable=False)
    sell_price = Column(Float, nullable=False)

    # Calculations
    raw_profit = Column(Float)
    fees = Column(Float)
    net_profit = Column(Float, index=True)
    profit_percentage = Column(Float, index=True)

    # AI Insights
    ai_score = Column(Float)  # 1-10 rating
    ai_reasoning = Column(String)

    # Status
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime)

    # Relationships
    card = relationship("Card", back_populates="arbitrage_opportunities")