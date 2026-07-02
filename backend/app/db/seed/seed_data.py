"""Run with: python -m app.db.seed.seed_data"""
import asyncio
import uuid

from sqlalchemy import select, text

from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.models import Guide, Hotel, Region, Spot, User
from app.core.security.password import hash_password

REGIONS = [
    {"name_ar": "الرياض", "name_en": "Riyadh", "latitude": 24.7136, "longitude": 46.6753},
    {"name_ar": "مكة المكرمة", "name_en": "Makkah", "latitude": 21.3891, "longitude": 39.8579},
    {"name_ar": "المدينة المنورة", "name_en": "Madinah", "latitude": 24.5247, "longitude": 39.5692},
    {"name_ar": "المنطقة الشرقية", "name_en": "Eastern Province", "latitude": 26.4207, "longitude": 50.0888},
    {"name_ar": "عسير", "name_en": "Asir", "latitude": 18.2164, "longitude": 42.5053},
    {"name_ar": "تبوك", "name_en": "Tabuk", "latitude": 28.3998, "longitude": 36.5716},
    {"name_ar": "حائل", "name_en": "Hail", "latitude": 27.5114, "longitude": 41.7208},
    {"name_ar": "القصيم", "name_en": "Qassim", "latitude": 26.3268, "longitude": 43.9751},
    {"name_ar": "جازان", "name_en": "Jazan", "latitude": 16.8892, "longitude": 42.5611},
    {"name_ar": "نجران", "name_en": "Najran", "latitude": 17.4922, "longitude": 44.1277},
    {"name_ar": "الباحة", "name_en": "Al-Bahah", "latitude": 20.0129, "longitude": 41.4677},
    {"name_ar": "الجوف", "name_en": "Al-Jouf", "latitude": 29.7865, "longitude": 39.9926},
    {"name_ar": "الحدود الشمالية", "name_en": "Northern Borders", "latitude": 30.9843, "longitude": 41.1184},
]

SPOTS = [
    {
        "region_en": "Riyadh", "spot_type": "desert",
        "name_ar": "كثبان الثمامة", "name_en": "Thumamah Dunes",
        "description_ar": "كثبان رملية حمراء هادئة على أطراف الرياض، مثالية للتخييم ومشاهدة النجوم.",
        "description_en": "Quiet red sand dunes on the edge of Riyadh, perfect for camping and stargazing.",
        "latitude": 25.1, "longitude": 46.5, "access_difficulty": "medium",
        "best_season": "Winter", "walking_distance_km": 1.5, "visit_duration_hours": 4,
        "requires_4x4": True, "has_phone_signal": True, "ai_quality_score": 0.9,
    },
    {
        "region_en": "Asir", "spot_type": "nature",
        "name_ar": "غابات رجال ألمع", "name_en": "Rijal Almaa Forests",
        "description_ar": "غابات جبلية خضراء كثيفة تطل على قرية رجال ألمع التراثية.",
        "description_en": "Dense green mountain forests overlooking the heritage village of Rijal Almaa.",
        "latitude": 18.2, "longitude": 42.4, "access_difficulty": "hard",
        "best_season": "Summer", "walking_distance_km": 3.0, "visit_duration_hours": 5,
        "requires_4x4": True, "has_phone_signal": False, "ai_quality_score": 0.95,
    },
    {
        "region_en": "Al-Jouf", "spot_type": "archaeological",
        "name_ar": "آثار دومة الجندل", "name_en": "Dumat Al-Jandal Ruins",
        "description_ar": "مدينة أثرية قديمة تضم قلعة مارد وقصور من الطين تعود لآلاف السنين.",
        "description_en": "An ancient archaeological city featuring Marid Castle and mudbrick palaces dating back millennia.",
        "latitude": 29.8, "longitude": 39.9, "access_difficulty": "easy",
        "best_season": "Winter", "walking_distance_km": 1.0, "visit_duration_hours": 2,
        "requires_4x4": False, "has_phone_signal": True, "ai_quality_score": 0.88,
    },
    {
        "region_en": "Eastern Province", "spot_type": "coastal",
        "name_ar": "شاطئ نصف القمر", "name_en": "Half Moon Bay",
        "description_ar": "شاطئ منحني هادئ بمياه فيروزية صافية بعيداً عن الزحام.",
        "description_en": "A quiet crescent-shaped beach with clear turquoise water, away from the crowds.",
        "latitude": 26.1, "longitude": 50.0, "access_difficulty": "easy",
        "best_season": "Autumn", "walking_distance_km": 0.5, "visit_duration_hours": 3,
        "requires_4x4": False, "has_phone_signal": True, "ai_quality_score": 0.85,
    },
    {
        "region_en": "Hail", "spot_type": "desert",
        "name_ar": "جبال أجا", "name_en": "Aja Mountains",
        "description_ar": "سلسلة جبلية جرانيتية تحمل نقوشاً صخرية قديمة ومسارات تسلق طبيعية.",
        "description_en": "A granite mountain range carrying ancient rock carvings and natural climbing trails.",
        "latitude": 27.6, "longitude": 41.6, "access_difficulty": "hard",
        "best_season": "Winter", "walking_distance_km": 2.5, "visit_duration_hours": 4,
        "requires_4x4": True, "has_phone_signal": False, "ai_quality_score": 0.92,
    },
    {
        "region_en": "Makkah", "spot_type": "village",
        "name_ar": "قرية الأسدية التراثية", "name_en": "Al-Asdiyah Heritage Village",
        "description_ar": "قرية جبلية مبنية بالحجر الطيني، تحافظ على طابع العمارة الحجازية القديمة.",
        "description_en": "A stone-built mountain village preserving the character of old Hejazi architecture.",
        "latitude": 21.5, "longitude": 40.2, "access_difficulty": "medium",
        "best_season": "Spring", "walking_distance_km": 1.2, "visit_duration_hours": 2.5,
        "requires_4x4": False, "has_phone_signal": True, "ai_quality_score": 0.87,
    },
]

GUIDE_USERS = [
    {
        "email": "guide.sara@athar.sa", "full_name": "Sara Al-Qahtani", "full_name_ar": "سارة القحطاني",
        "region_en": "Asir", "bio_ar": "مرشدة سياحية معتمدة متخصصة في جبال عسير ومسارات التسلق.",
        "bio_en": "Certified guide specializing in the Asir mountains and hiking trails.",
        "specializations": ["hiking", "nature"], "languages": ["ar", "en"],
        "daily_rate": 450.0, "rating": 4.8, "review_count": 32, "years_experience": 6,
    },
    {
        "email": "guide.omar@athar.sa", "full_name": "Omar Al-Rashid", "full_name_ar": "عمر الراشد",
        "region_en": "Al-Jouf", "bio_ar": "خبير في تاريخ وآثار منطقة الجوف ودومة الجندل.",
        "bio_en": "Expert in the history and archaeology of Al-Jouf and Dumat Al-Jandal.",
        "specializations": ["archaeological", "history"], "languages": ["ar", "en"],
        "daily_rate": 400.0, "rating": 4.6, "review_count": 21, "years_experience": 9,
    },
    {
        "email": "guide.lama@athar.sa", "full_name": "Lama Al-Otaibi", "full_name_ar": "لمى العتيبي",
        "region_en": "Riyadh", "bio_ar": "مرشدة صحراوية متخصصة في رحلات الكثبان الرملية والتخييم.",
        "bio_en": "Desert guide specializing in dune trips and camping expeditions.",
        "specializations": ["desert", "camping"], "languages": ["ar", "en"],
        "daily_rate": 350.0, "rating": 4.9, "review_count": 45, "years_experience": 4,
    },
]

HOTELS = [
    {
        "region_en": "Riyadh", "name_ar": "فندق الدرعية التراثي", "name_en": "Diriyah Heritage Hotel",
        "latitude": 24.73, "longitude": 46.57, "stars": 5, "price_per_night": 850.0,
        "rating": 4.7, "contact_phone": "+966112345678",
    },
    {
        "region_en": "Asir", "name_ar": "نزل أبها الجبلي", "name_en": "Abha Mountain Lodge",
        "latitude": 18.22, "longitude": 42.51, "stars": 4, "price_per_night": 420.0,
        "rating": 4.5, "contact_phone": "+966172345678",
    },
    {
        "region_en": "Eastern Province", "name_ar": "منتجع نصف القمر", "name_en": "Half Moon Bay Resort",
        "latitude": 26.12, "longitude": 50.02, "stars": 5, "price_per_night": 950.0,
        "rating": 4.8, "contact_phone": "+966132345678",
    },
]


async def _get_or_create_user(session, **kwargs) -> User:
    existing = (await session.execute(select(User).where(User.email == kwargs["email"]))).scalar_one_or_none()
    if existing:
        return existing
    user = User(id=uuid.uuid4(), **kwargs)
    session.add(user)
    await session.flush()
    return user


async def seed():
    async with engine.begin() as conn:
        # Enable pgvector
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Seed regions (skip if already present)
        existing_regions = (await session.execute(select(Region))).scalars().all()
        regions_by_en = {r.name_en: r for r in existing_regions}
        if not existing_regions:
            for r in REGIONS:
                region = Region(
                    id=uuid.uuid4(),
                    name_ar=r["name_ar"],
                    name_en=r["name_en"],
                    latitude=r["latitude"],
                    longitude=r["longitude"],
                )
                session.add(region)
            await session.flush()
            regions_by_en = {r.name_en: r for r in (await session.execute(select(Region))).scalars().all()}

        # Seed admin + ministry users
        await _get_or_create_user(
            session, email="admin@athar.sa", hashed_password=hash_password("Admin@2030!"),
            full_name="Platform Admin", full_name_ar="مدير المنصة", role="admin",
            is_active=True, is_verified=True,
        )
        await _get_or_create_user(
            session, email="ministry@athar.sa", hashed_password=hash_password("Ministry@2030!"),
            full_name="Ministry of Tourism", full_name_ar="وزارة السياحة", role="ministry",
            is_active=True, is_verified=True,
        )

        # Seed approved spots
        existing_spot_names = {
            s for (s,) in (await session.execute(select(Spot.name_en))).all()
        }
        for s in SPOTS:
            if s["name_en"] in existing_spot_names:
                continue
            region = regions_by_en[s["region_en"]]
            spot = Spot(
                id=uuid.uuid4(),
                name_ar=s["name_ar"], name_en=s["name_en"],
                description_ar=s["description_ar"], description_en=s["description_en"],
                region_id=region.id, spot_type=s["spot_type"],
                latitude=s["latitude"], longitude=s["longitude"],
                access_difficulty=s["access_difficulty"], best_season=s["best_season"],
                walking_distance_km=s["walking_distance_km"], visit_duration_hours=s["visit_duration_hours"],
                requires_4x4=s["requires_4x4"], has_phone_signal=s["has_phone_signal"],
                status="approved", ai_quality_score=s["ai_quality_score"],
            )
            session.add(spot)
            region.spot_count += 1

        # Seed guides (each backed by a real 'guide' role user)
        for g in GUIDE_USERS:
            user = await _get_or_create_user(
                session, email=g["email"], hashed_password=hash_password("Guide@2030!"),
                full_name=g["full_name"], full_name_ar=g["full_name_ar"], role="guide",
                is_active=True, is_verified=True,
            )
            existing_guide = (
                await session.execute(select(Guide).where(Guide.user_id == user.id))
            ).scalar_one_or_none()
            if existing_guide:
                continue
            region = regions_by_en[g["region_en"]]
            session.add(Guide(
                id=uuid.uuid4(), user_id=user.id, region_id=region.id,
                bio_ar=g["bio_ar"], bio_en=g["bio_en"],
                specializations=g["specializations"], languages=g["languages"],
                daily_rate=g["daily_rate"], rating=g["rating"], review_count=g["review_count"],
                is_available=True, is_verified=True, years_experience=g["years_experience"],
            ))

        # Seed hotels
        existing_hotel_names = {
            h for (h,) in (await session.execute(select(Hotel.name_en))).all()
        }
        for h in HOTELS:
            if h["name_en"] in existing_hotel_names:
                continue
            region = regions_by_en[h["region_en"]]
            session.add(Hotel(
                id=uuid.uuid4(), region_id=region.id,
                name_ar=h["name_ar"], name_en=h["name_en"],
                latitude=h["latitude"], longitude=h["longitude"],
                stars=h["stars"], price_per_night=h["price_per_night"],
                rating=h["rating"], contact_phone=h["contact_phone"],
            ))

        await session.commit()
        print("✅ Seed data inserted successfully.")
        print("Admin:    admin@athar.sa / Admin@2030!")
        print("Ministry: ministry@athar.sa / Ministry@2030!")
        print("Guides:   guide.sara@athar.sa / guide.omar@athar.sa / guide.lama@athar.sa — Guide@2030!")


if __name__ == "__main__":
    asyncio.run(seed())
