from fastapi import FastAPI, Query, Header, HTTPException
from fastapi.responses import JSONResponse
import requests
import re
import os
from typing import Optional

app = FastAPI(title="TRAUMA Phone Lookup API", version="1.0.0")

# Fixed API key requested by the owner.
# You can later override it with the TRAUMA_API_KEY environment variable.
API_KEY = os.getenv("TRAUMA_API_KEY", "TRAUMA")

AUTH_URL = "https://number.mcinem.com/api/v1/auth/device"
SEARCH_URL = "https://number.mcinem.com/api/v1/numbers/search"
CALLER_URL = "https://caller-uegx.vercel.app/api/search"

COUNTRY_CODES = {
    "1": "NANP",
    "7": "روسيا/كازاخستان",
    "20": "مصر",
    "27": "جنوب أفريقيا",
    "30": "اليونان",
    "31": "هولندا",
    "32": "بلجيكا",
    "33": "فرنسا",
    "34": "إسبانيا",
    "36": "المجر",
    "39": "إيطاليا",
    "40": "رومانيا",
    "41": "سويسرا",
    "43": "النمسا",
    "44": "المملكة المتحدة",
    "45": "الدنمارك",
    "46": "السويد",
    "47": "النرويج",
    "48": "بولندا",
    "49": "ألمانيا",
    "51": "بيرو",
    "52": "المكسيك",
    "53": "كوبا",
    "54": "الأرجنتين",
    "55": "البرازيل",
    "56": "تشيلي",
    "57": "كولومبيا",
    "58": "فنزويلا",
    "60": "ماليزيا",
    "61": "أستراليا",
    "62": "إندونيسيا",
    "63": "الفلبين",
    "64": "نيوزيلندا",
    "65": "سنغافورة",
    "66": "تايلاند",
    "81": "اليابان",
    "82": "كوريا الجنوبية",
    "84": "فيتنام",
    "86": "الصين",
    "90": "تركيا",
    "91": "الهند",
    "92": "باكستان",
    "93": "أفغانستان",
    "94": "سريلانكا",
    "95": "ميانمار",
    "98": "إيران",
    "211": "جنوب السودان",
    "212": "المغرب",
    "213": "الجزائر",
    "216": "تونس",
    "218": "ليبيا",
    "220": "غامبيا",
    "221": "السنغال",
    "222": "موريتانيا",
    "223": "مالي",
    "224": "غينيا",
    "225": "ساحل العاج",
    "226": "بوركينا فاسو",
    "227": "النيجر",
    "228": "توغو",
    "229": "بنين",
    "230": "موريشيوس",
    "231": "ليبيريا",
    "232": "سيراليون",
    "233": "غانا",
    "234": "نيجيريا",
    "235": "تشاد",
    "236": "أفريقيا الوسطى",
    "237": "الكاميرون",
    "238": "الرأس الأخضر",
    "239": "ساو تومي وبرينسيب",
    "240": "غينيا الاستوائية",
    "241": "الغابون",
    "242": "الكونغو",
    "243": "الكونغو الديمقراطية",
    "244": "أنغولا",
    "245": "غينيا بيساو",
    "246": "إقليم المحيط الهندي البريطاني",
    "247": "سانت هيلينا",
    "248": "سيشل",
    "249": "السودان",
    "250": "رواندا",
    "251": "إثيوبيا",
    "252": "الصومال",
    "253": "جيبوتي",
    "254": "كينيا",
    "255": "تنزانيا",
    "256": "أوغندا",
    "257": "بوروندي",
    "258": "موزمبيق",
    "260": "زامبيا",
    "261": "مدغشقر",
    "262": "ريونيون/مايوت",
    "263": "زيمبابوي",
    "264": "ناميبيا",
    "265": "ملاوي",
    "266": "ليسوتو",
    "267": "بوتسوانا",
    "268": "إسواتيني",
    "269": "جزر القمر",
    "290": "سانت هيلينا",
    "291": "إريتريا",
    "297": "أروبا",
    "298": "جزر فارو",
    "299": "غرينلاند",
    "350": "جبل طارق",
    "351": "البرتغال",
    "352": "لوكسمبورغ",
    "353": "أيرلندا",
    "354": "آيسلندا",
    "355": "ألبانيا",
    "356": "مالطا",
    "357": "قبرص",
    "358": "فنلندا",
    "359": "بلغاريا",
    "370": "ليتوانيا",
    "371": "لاتفيا",
    "372": "إستونيا",
    "373": "مولدوفا",
    "374": "أرمينيا",
    "375": "بيلاروس",
    "376": "أندورا",
    "377": "موناكو",
    "378": "سان مارينو",
    "379": "الفاتيكان",
    "380": "أوكرانيا",
    "381": "صربيا",
    "382": "الجبل الأسود",
    "383": "كوسوفو",
    "385": "كرواتيا",
    "386": "سلوفينيا",
    "387": "البوسنة والهرسك",
    "389": "مقدونيا الشمالية",
    "500": "جزر فوكلاند",
    "501": "بليز",
    "502": "غواتيمالا",
    "503": "السلفادور",
    "504": "هندوراس",
    "505": "نيكاراغوا",
    "506": "كوستاريكا",
    "507": "بنما",
    "508": "سان بيير وميكلون",
    "509": "هايتي",
    "590": "غوادلوب/سان مارتان",
    "591": "بوليفيا",
    "592": "غيانا",
    "593": "الإكوادور",
    "594": "غويانا الفرنسية",
    "595": "باراغواي",
    "596": "مارتينيك",
    "597": "سورينام",
    "598": "أوروغواي",
    "599": "كوراساو/الكاريبي الهولندي",
    "670": "تيمور الشرقية",
    "672": "أقاليم أسترالية",
    "673": "بروناي",
    "674": "ناورو",
    "675": "بابوا غينيا الجديدة",
    "676": "تونغا",
    "677": "جزر سليمان",
    "678": "فانواتو",
    "679": "فيجي",
    "680": "بالاو",
    "681": "واليس وفوتونا",
    "682": "جزر كوك",
    "683": "نييوي",
    "685": "ساموا",
    "686": "كيريباتي",
    "687": "كاليدونيا الجديدة",
    "688": "توفالو",
    "689": "بولينيزيا الفرنسية",
    "690": "توكلاو",
    "691": "ميكرونيزيا",
    "692": "جزر مارشال",
    "850": "كوريا الشمالية",
    "852": "هونغ كونغ",
    "853": "ماكاو",
    "855": "كمبوديا",
    "856": "لاوس",
    "880": "بنغلاديش",
    "886": "تايوان",
    "960": "المالديف",
    "961": "لبنان",
    "962": "الأردن",
    "963": "سوريا",
    "964": "العراق",
    "965": "الكويت",
    "966": "السعودية",
    "967": "اليمن",
    "968": "عُمان",
    "970": "فلسطين",
    "971": "الإمارات",
    "972": "إسرائيل",
    "973": "البحرين",
    "974": "قطر",
    "975": "بوتان",
    "976": "منغوليا",
    "977": "نيبال",
    "992": "طاجيكستان",
    "993": "تركمانستان",
    "994": "أذربيجان",
    "995": "جورجيا",
    "996": "قيرغيزستان",
    "998": "أوزبكستان",
    "1242": "جزر البهاما",
    "1246": "بربادوس",
    "1264": "أنغويلا",
    "1268": "أنتيغوا وبربودا",
    "1284": "جزر العذراء البريطانية",
    "1340": "جزر العذراء الأمريكية",
    "1345": "جزر كايمان",
    "1441": "برمودا",
    "1473": "غرينادا",
    "1649": "جزر تركس وكايكوس",
    "1658": "جامايكا",
    "1664": "مونتسرات",
    "1670": "جزر ماريانا الشمالية",
    "1671": "غوام",
    "1684": "ساموا الأمريكية",
    "1721": "سينت مارتن",
    "1758": "سانت لوسيا",
    "1767": "دومينيكا",
    "1784": "سانت فنسنت والغرينادين",
    "1787": "بورتوريكو",
    "1809": "جمهورية الدومينيكان",
    "1829": "جمهورية الدومينيكان",
    "1849": "جمهورية الدومينيكان",
    "1868": "ترينيداد وتوباغو",
    "1869": "سانت كيتس ونيفيس",
    "1876": "جامايكا"
}
COUNTRY_CODE_LIST = sorted(COUNTRY_CODES.keys(), key=len, reverse=True)


def detect_country_code(value: str):
    clean = re.sub(r"\D", "", str(value or ""))
    for code in COUNTRY_CODE_LIST:
        if clean.startswith(code) and len(clean) > len(code):
            return {
                "code": code,
                "phone": clean[len(code):],
                "country": COUNTRY_CODES[code],
                "fullPhone": f"+{clean}",
            }
    return None


def check_key(key: Optional[str]):
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


def create_device():
    response = requests.post(
        AUTH_URL,
        json={
            "app_version": "0.1.4",
            "locale": "en-US",
            "platform": "android",
        },
        headers={
            "User-Agent": "Dalil/0.1.4 (Android)",
            "accept-language": "en",
            "content-type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip",
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    token = data.get("data", {}).get("access_token")
    if not token:
        raise RuntimeError("لم يتم الحصول على Access Token")
    return token


def search_caller_api(code: str, phone: str):
    try:
        response = requests.post(
            CALLER_URL,
            json={"code": code, "phone": phone},
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=15,
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        return [
            item.get("الاسم")
            for item in results
            if isinstance(item, dict)
            and isinstance(item.get("الاسم"), str)
            and item.get("الاسم").strip()
        ]
    except Exception:
        return []


def search_number_api(full_phone: str):
    try:
        access_token = create_device()
        response = requests.post(
            SEARCH_URL,
            json={"phone": full_phone},
            headers={
                "Authorization": f"Bearer {access_token}",
                "User-Agent": "Dalil/0.1.4 (Android)",
                "Accept-Language": "en",
                "Content-Type": "application/json; charset=UTF-8",
                "Accept-Encoding": "gzip",
            },
            timeout=15,
        )
        response.raise_for_status()
        aliases = response.json().get("data", {}).get("aliases", [])
        return [
            name for name in aliases
            if isinstance(name, str) and name.strip()
        ]
    except Exception:
        return []


def lookup_number(number: str):
    detected = detect_country_code(number)
    if not detected:
        raise HTTPException(
            status_code=400,
            detail="لم أستطع تحديد رمز الدولة أو الرقم غير مكتمل."
        )

    names_a = search_caller_api(detected["code"], detected["phone"])
    names_b = search_number_api(detected["fullPhone"])

    unique_names = list(dict.fromkeys(
        name.strip()
        for name in (names_a + names_b)
        if isinstance(name, str) and name.strip()
    ))

    return {
        "success": True,
        "phone": detected["fullPhone"],
        "country_code": detected["code"],
        "country": detected["country"],
        "names": unique_names,
        "count": len(unique_names),
    }


@app.get("/")
def root():
    return {
        "name": "TRAUMA Phone Lookup API",
        "status": "online",
        "usage": "/<phone>?key=TRAUMA",
        "health": "/api/health",
    }


@app.get("/api/health")
def health():
    return {"ok": True, "service": "TRAUMA Phone Lookup API"}


@app.get("/api/lookup")
def lookup(
    number: str = Query(..., min_length=2),
    key: Optional[str] = Query(None),
    x_api_key: Optional[str] = Header(None, alias="x-api-key"),
):
    check_key(key or x_api_key)
    return lookup_number(number)


@app.get("/api/lookup/{number}")
def lookup_path(
    number: str,
    key: Optional[str] = Query(None),
    x_api_key: Optional[str] = Header(None, alias="x-api-key"),
):
    check_key(key or x_api_key)
    return lookup_number(number)
