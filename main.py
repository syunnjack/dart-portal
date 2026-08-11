import datetime
import json
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Dart Portal API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- データモデル ----------


class Pro(BaseModel):
    id: int
    name: str
    league: str
    gender: str
    popularity_score: float
    bio: str
    tags: List[str] = Field(default_factory=list)
    gear_ids: List[int] = Field(default_factory=list)
    media_appearances: List[dict] = Field(default_factory=list)
    followers: dict = Field(default_factory=dict)
    upcoming_events_count: int = 0


class Event(BaseModel):
    id: int
    title: str
    pro_id: int
    area: str
    date: datetime.date
    ticket_aff: bool
    ticket_url: Optional[str] = None
    source_url: Optional[str] = None


class Shop(BaseModel):
    id: int
    name: str
    chain: str
    prefecture: str
    city: str
    address: str
    lat: float
    lng: float
    official_url: str
    event_page_url: Optional[str] = None
    scraper_key: Optional[str] = None


class Gear(BaseModel):
    id: int
    name: str
    category: str
    brand: str
    pro_id: int
    price: int
    image_url: Optional[str] = None
    affiliate_links: dict = Field(default_factory=dict)
    is_signature_model: bool = False


class Fan(BaseModel):
    area: str
    favorite_pro_ids: List[int]
    budget: int


class Item(BaseModel):
    id: int
    name: str
    pro_id: int
    price: int
    url: str


class Offer(BaseModel):
    event: Event
    bundle: List[Item]
    total: int
    score: float


class RecommendationBundle(BaseModel):
    pro_id: int
    pro_name: str
    items: List[Item]
    total_price: int
    affiliate_total_commission_est: int


class RecommendationResponse(BaseModel):
    events: List[Event]
    gear_bundles: List[RecommendationBundle]
    featured_media: List[dict]
    score: float


class ProDetailResponse(BaseModel):
    pro: Pro
    upcoming_events: List[Event]
    related_gear: List[Gear]


class EventDetailResponse(BaseModel):
    event: Event
    pro: Optional[Pro]
    shop: Optional[Shop]
    related_gear: List[Gear]

class ShopDetailResponse(BaseModel):
    shop: Shop
    related_events: List[Event]


# ---------- データセット ----------

PROS_DB = [
    Pro(
        id=101,
        name="寺下智香",
        league="JAPAN",
        gender="female",
        popularity_score=92.8,
        bio="来店イベントと物販でファン人気の高いトッププロ。",
        tags=["人気女子プロ", "イベント強い", "JAPAN"],
        gear_ids=[1, 2],
        media_appearances=[
            {
                "title": "ダーツ専門誌インタビュー",
                "media_type": "magazine",
                "url": "https://example.com/media/terashita",
                "published_at": "2026-07-15",
            }
        ],
        followers={"x": 42000, "instagram": 68000},
    ),
    Pro(
        id=205,
        name="寺村文孝",
        league="PERFECT",
        gender="male",
        popularity_score=84.4,
        bio="大会実績と店舗イベントの両方で支持を集めるベテラン。",
        tags=["ベテラン", "PERFECT", "チャレンジマッチ"],
        gear_ids=[3],
        media_appearances=[
            {
                "title": "大会レポート",
                "media_type": "web",
                "url": "https://example.com/media/teramura",
                "published_at": "2026-06-20",
            }
        ],
        followers={"x": 18000, "instagram": 9500},
    ),
    Pro(
        id=309,
        name="姫路麗",
        league="JAPAN",
        gender="female",
        popularity_score=90.2,
        bio="関西圏のイベントで根強い集客力を持つ人気プロ。",
        tags=["関西", "人気女子プロ", "物販"],
        gear_ids=[4],
        media_appearances=[
            {
                "title": "SNSライブ配信",
                "media_type": "web",
                "url": "https://example.com/media/himeji",
                "published_at": "2026-08-01",
            }
        ],
        followers={"x": 51000, "instagram": 74500},
    ),
]

SHOPS_DB = [
    Shop(
        id=1,
        name="自遊空間 神戸店",
        chain="自遊空間",
        prefecture="兵庫県",
        city="神戸市中央区",
        address="兵庫県神戸市中央区三宮町1-1-1",
        lat=34.6901,
        lng=135.1955,
        official_url="https://example.com/shop/kobe",
        event_page_url="https://example.com/shop/kobe/events",
        scraper_key="jiyu-kobe",
    ),
    Shop(
        id=2,
        name="BAGUS 新宿店",
        chain="BAGUS",
        prefecture="東京都",
        city="新宿区",
        address="東京都新宿区新宿3-1-1",
        lat=35.6917,
        lng=139.7036,
        official_url="https://example.com/shop/shinjuku",
        event_page_url="https://example.com/shop/shinjuku/events",
        scraper_key="bagus-shinjuku",
    ),
    Shop(
        id=3,
        name="ダーツバー BLUE 大阪梅田",
        chain="ダーツバー",
        prefecture="大阪府",
        city="大阪市北区",
        address="大阪府大阪市北区梅田2-2-2",
        lat=34.7025,
        lng=135.4959,
        official_url="https://example.com/shop/osaka",
        event_page_url="https://example.com/shop/osaka/events",
        scraper_key="blue-umeda",
    ),
]

GEAR_DB = [
    Gear(
        id=1,
        name="プロモデルバレル",
        category="barrel",
        brand="PORTAL",
        pro_id=101,
        price=12000,
        image_url="https://example.com/gear/barrel.png",
        affiliate_links={
            "amazon": "https://example.com/aff/amazon/barrel",
            "rakuten": "https://example.com/aff/rakuten/barrel",
        },
        is_signature_model=True,
    ),
    Gear(
        id=2,
        name="フライトセット",
        category="flight",
        brand="PORTAL",
        pro_id=101,
        price=2000,
        image_url="https://example.com/gear/flight.png",
        affiliate_links={
            "amazon": "https://example.com/aff/amazon/flight",
        },
    ),
    Gear(
        id=3,
        name="シグネチャーケース",
        category="case",
        brand="PORTAL",
        pro_id=205,
        price=6500,
        image_url="https://example.com/gear/case.png",
        affiliate_links={
            "amazon": "https://example.com/aff/amazon/case",
        },
    ),
    Gear(
        id=4,
        name="応援タオル",
        category="goods",
        brand="PORTAL",
        pro_id=309,
        price=3000,
        image_url="https://example.com/gear/towel.png",
        affiliate_links={
            "amazon": "https://example.com/aff/amazon/towel",
        },
    ),
]

ITEMS_DB = [
    Item(id=1, name="プロモデルバレル", pro_id=101, price=12000, url="https://aff.example.com/barrel"),
    Item(id=2, name="フライトセット", pro_id=101, price=2000, url="https://aff.example.com/flight"),
    Item(id=3, name="応援タオル", pro_id=101, price=3000, url="https://aff.example.com/towel"),
    Item(id=4, name="シグネチャーケース", pro_id=205, price=6500, url="https://aff.example.com/case"),
    Item(id=5, name="ベーシックシャフト", pro_id=309, price=1800, url="https://aff.example.com/shaft"),
]


# ---------- データ読み込み ----------


def load_events_db() -> List[Event]:
    events_path = Path(__file__).with_name("events.json")
    if not events_path.exists():
        return []

    raw = json.loads(events_path.read_text(encoding="utf-8"))
    events: List[Event] = []
    for index, entry in enumerate(raw, start=1):
        events.append(
            Event(
                id=index,
                title=entry["title"],
                pro_id=101,
                area=entry["area"],
                date=datetime.date.fromisoformat(entry["date"]),
                ticket_aff=entry["ticket_aff"],
                ticket_url=entry.get("ticket_url"),
                source_url=entry.get("detail_url"),
            )
        )

    return events


def get_events_db() -> List[Event]:
    return load_events_db()


# ---------- ロジック ----------


def get_pro_by_id(pro_id: int) -> Optional[Pro]:
    return next((pro for pro in PROS_DB if pro.id == pro_id), None)


def get_shop_by_id(shop_id: int) -> Optional[Shop]:
    return next((shop for shop in SHOPS_DB if shop.id == shop_id), None)


def get_gear_by_pro_id(pro_id: int) -> List[Gear]:
    return [gear for gear in GEAR_DB if gear.pro_id == pro_id]


def calc_score(fan: Fan, ev: Event, items: List[Item]) -> float:
    score = 0.0

    if ev.pro_id in fan.favorite_pro_ids:
        score += 50.0

    days = (ev.date - datetime.date.today()).days
    if 0 <= days <= 14:
        score += float(20 - days)

    total = sum(item.price for item in items)
    if fan.budget > 0:
        ratio = total / fan.budget
        if 0.7 <= ratio <= 1.1:
            score += 30.0
        elif 0.4 <= ratio < 0.7:
            score += 10.0

    if ev.ticket_aff:
        score += 15.0

    return score


def build_item_bundle(fan: Fan, pro_id: int) -> tuple[list[Item], int]:
    pro_items = [item for item in ITEMS_DB if item.pro_id == pro_id]
    pro_items.sort(key=lambda item: item.price, reverse=True)

    bundle: List[Item] = []
    total = 0

    for item in pro_items:
        if total + item.price <= int(fan.budget * 1.1):
            bundle.append(item)
            total += item.price

    return bundle, total


def generate_offers(fan: Fan) -> List[Offer]:
    offers: List[Offer] = []

    for ev in get_events_db():
        if ev.area != fan.area:
            continue

        if ev.pro_id not in fan.favorite_pro_ids:
            continue

        bundle, total = build_item_bundle(fan, ev.pro_id)
        if not bundle:
            continue

        offers.append(
            Offer(
                event=ev,
                bundle=bundle,
                total=total,
                score=calc_score(fan, ev, bundle),
            )
        )

    offers.sort(key=lambda offer: offer.score, reverse=True)
    return offers


def generate_recommendations(fan: Fan) -> RecommendationResponse:
    events = [
        ev
        for ev in get_events_db()
        if ev.area == fan.area and ev.pro_id in fan.favorite_pro_ids
    ]
    events.sort(key=lambda event: event.date)

    bundles: List[RecommendationBundle] = []
    featured_media: List[dict] = []
    scores: List[float] = []

    for event in events:
        bundle, total = build_item_bundle(fan, event.pro_id)
        if not bundle:
            continue

        pro = get_pro_by_id(event.pro_id)
        bundles.append(
            RecommendationBundle(
                pro_id=event.pro_id,
                pro_name=pro.name if pro else f"Pro {event.pro_id}",
                items=bundle,
                total_price=total,
                affiliate_total_commission_est=int(total * 0.05),
            )
        )

        if pro:
            featured_media.extend(pro.media_appearances)

        scores.append(calc_score(fan, event, bundle))

    return RecommendationResponse(
        events=events,
        gear_bundles=bundles,
        featured_media=featured_media[:5],
        score=round(sum(scores) / len(scores), 1) if scores else 0.0,
    )


# ---------- エンドポイント ----------


@app.get("/")
def index():
    events = get_events_db()
    return {
        "name": app.title,
        "description": "ダーツプロ・イベント・店舗・ギアを横断検索できる総合ポータルの MVP API です。",
        "routes": [
            "/health",
            "/pros",
            "/events",
            "/shops",
            "/gear",
            "/recommendations",
            "/offers",
        ],
        "counts": {
            "pros": len(PROS_DB),
            "events": len(events),
            "shops": len(SHOPS_DB),
            "gear": len(GEAR_DB),
        },
    }


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.datetime.now(datetime.UTC).isoformat()}


@app.get("/pros", response_model=List[Pro])
def list_pros(
    sort: str = Query("popularity", pattern="^(popularity|events)$"),
    limit: int = Query(20, ge=1, le=100),
):
    events = get_events_db()
    pro_map = {pro.id: pro.model_copy() for pro in PROS_DB}

    for pro in pro_map.values():
        pro.upcoming_events_count = sum(
            1 for event in events if event.pro_id == pro.id and event.date >= datetime.date.today()
        )

    pros = list(pro_map.values())
    if sort == "events":
        pros.sort(key=lambda pro: (pro.upcoming_events_count, pro.popularity_score), reverse=True)
    else:
        pros.sort(key=lambda pro: (pro.popularity_score, pro.upcoming_events_count), reverse=True)

    return pros[:limit]


@app.get("/pros/{pro_id}", response_model=ProDetailResponse)
def get_pro_detail(pro_id: int):
    pro = get_pro_by_id(pro_id)
    if not pro:
        raise HTTPException(status_code=404, detail="Pro not found")

    events = [event for event in get_events_db() if event.pro_id == pro_id]
    events.sort(key=lambda event: event.date)

    return ProDetailResponse(
        pro=pro,
        upcoming_events=events,
        related_gear=get_gear_by_pro_id(pro_id),
    )


@app.get("/events", response_model=List[Event])
def list_events(
    area: Optional[str] = None,
    pro_id: Optional[int] = None,
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
    limit: int = Query(50, ge=1, le=200),
):
    events = get_events_db()
    filtered: List[Event] = []

    for event in events:
        if area and event.area != area:
            continue
        if pro_id and event.pro_id != pro_id:
            continue
        if date_from and event.date < date_from:
            continue
        if date_to and event.date > date_to:
            continue
        filtered.append(event)

    filtered.sort(key=lambda event: (event.date, event.title))
    return filtered[:limit]


@app.get("/events/{event_id}", response_model=EventDetailResponse)
def get_event_detail(event_id: int):
    event = next((item for item in get_events_db() if item.id == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    pro = get_pro_by_id(event.pro_id)
    related_gear = get_gear_by_pro_id(event.pro_id)

    shop = SHOPS_DB[0] if SHOPS_DB else None
    if event.area == "Tokyo":
        shop = get_shop_by_id(2)
    elif event.area == "Osaka":
        shop = get_shop_by_id(3)
    elif event.area == "Hyogo":
        shop = get_shop_by_id(1)

    return EventDetailResponse(
        event=event,
        pro=pro,
        shop=shop,
        related_gear=related_gear,
    )


@app.get("/shops", response_model=List[Shop])
def list_shops(
    prefecture: Optional[str] = None,
    chain: Optional[str] = None,
):
    shops = SHOPS_DB
    if prefecture:
        shops = [shop for shop in shops if shop.prefecture == prefecture]
    if chain:
        shops = [shop for shop in shops if shop.chain == chain]
    return shops


@app.get("/shops/{shop_id}", response_model=ShopDetailResponse)
def get_shop_detail(shop_id: int):
    shop = get_shop_by_id(shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    area = {
        "兵庫県": "Hyogo",
        "東京都": "Tokyo",
        "大阪府": "Osaka",
    }.get(shop.prefecture)

    related_events = []
    if area:
        related_events = [event for event in get_events_db() if event.area == area]
        related_events.sort(key=lambda event: event.date)

    return ShopDetailResponse(shop=shop, related_events=related_events)


@app.get("/gear", response_model=List[Gear])
def list_gear(
    pro_id: Optional[int] = None,
    category: Optional[str] = None,
    signature_only: bool = False,
):
    gear = GEAR_DB
    if pro_id is not None:
        gear = [item for item in gear if item.pro_id == pro_id]
    if category:
        gear = [item for item in gear if item.category == category]
    if signature_only:
        gear = [item for item in gear if item.is_signature_model]

    gear.sort(key=lambda item: item.price)
    return gear


@app.get("/gear/{gear_id}", response_model=Gear)
def get_gear_detail(gear_id: int):
    gear = next((item for item in GEAR_DB if item.id == gear_id), None)
    if not gear:
        raise HTTPException(status_code=404, detail="Gear not found")
    return gear


@app.post("/recommendations", response_model=RecommendationResponse)
def get_recommendations(fan: Fan):
    return generate_recommendations(fan)


@app.post("/offers", response_model=List[Offer])
def get_offers(fan: Fan):
    return generate_offers(fan)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
