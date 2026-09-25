# Yuksava — texnik hisobot (25.09.2026)

Yuksava mahalliy MP4 va kompyuter/USB kamera uchun ishlaydigan dastur. Asl ZIP va PDF o‘zgartirilmagan. Rasmiy run_submission.py va evaluate.py aynan saqlangan.

## Amalga oshirilgan

- Siz bergan 7 rang, Yuksava nomi, tahlil paytida cyan radar va telefon ko‘rinishi.
- MP4 yuklash (8 GB gacha), fon tahlili, bekor qilish, video, obyekt qutilari/izlari, hodisa vaqt chizig‘i, zichlik xaritasi va JSON.
- Kamera tanlash, HD/Full HD, yoqish/o‘chirish va haqiqiy mahalliy modelda kadr tahlili. Kamera kadrlari saqlanmaydi. RTSP va jismoniy PTZ boshqaruvi amalga oshirilmagan.
- 14 sinfning PDFdagi boshlanish/tugash jadvali, kadrma-kadr qo‘lda annotatsiya, ground_truth eksporti, o‘zgarmagan evaluate.py bilan haqiqiy hisoblash. To‘liq ko‘rik tasdiqlanmaguncha ball chiqarilmaydi.
- Jamoaning 3 a’zosi, rollari, portfoliolari va public havolalari uchun saqlanadigan forma.
- SIFT/RANSAC kamera mosligi: noma’lum rakursda qoidalar o‘chiriladi. Road/crossing/trotuar-orolcha zonalarini video bo‘yicha saqlash.

## Haqiqiy videolardagi sinov

Videos.pdf dagi barcha 4 havoladan haqiqiy kadrlar olindi. Original video: 3840×2160, 29.970 fps. Asl fayllar juda katta: C3896 — 6,241,380,481 bayt; C3897 va C3902 har biri 5,838,719,827 bayt; C3905 — 2,348,992,759 bayt. To‘liq yuklash tugamadi; foydalanuvchining tez yakunlash so‘roviga binoan 4 ta boshlang‘ich parcha bilan tekshirildi. Parchalar 1280×720 H.264 ga aylantirilgan; 300 kadr = 10.01 soniya. Quyidagi sonlar to‘liq videolarga yoki T4 ga tegishli emas.

| Haqiqiy parcha | Davomiylik | Taxminiy iz ID | Model vaqti | Vaqt nisbati | Qoida nomzodi |
|---|---:|---:|---:|---:|---:|
| C3896_first10s.mp4 | 10.01 s | 70 | 3.585 s | 0.358× | 2 |
| C3897_first10s.mp4 | 10.01 s | 51 | 3.645 s | 0.364× | 1 |
| C3902_first10s.mp4 | 10.01 s | 69 | 3.568 s | 0.356× | 1 |
| C3905_first10s.mp4 | 10.01 s | 70 | 3.629 s | 0.363× | 1 |

Izlar takroriy sanash va uzilish xatolariga ega; bu aniq avtomobil/odam soni emas. Hosil qilingan jaywalking segmentlari tekshirilmagan taxminlar. Ular tasdiqlangan qoidabuzarlik emas. Ground truth yo‘q, shu sabab haqiqiy F1/accuracy yoki hidden-test balli berilmaydi.

## Nizomga moslik va qolgan ish

| Talab | Hozirgi holat |
|---|---|
| solution.py / detect_events / CLASSES / soniyalarda segment | Mavjud; rasmiy harness bilan tekshiriladi |
| Bir sinfning ustma-ust vaqtlarini birlashtirish / video oxiri | Implementatsiya va birlik testlari bor |
| Part B causal | Nol baseline, fayl/future/Part A keshini o‘qimaydi; nizomda ixtiyoriy |
| 14 class | 14 ta ta’rif va qo‘lda annotatsiya bor. 6 ta dastlabki avtomatik qoida; 8 ta avtomatik detektor yo‘q. PDF sinflarni qisqartirishga ruxsat beradi |
| Haqiqiy model/offline | YOLOX-S OpenCV Zoo, 35.9 MB; mahalliy CPU DNN |
| Kamera tavsifi | samples/camera.md asl resurslarda yo‘q. Visual geometriya rasmiy tavsif o‘rnini bosmaydi |
| Signal, chiziq va taqiqlangan burilishlar | Rasmiy tavsif/model yo‘qligi sabab tasdiqlanmagan; uydirma buzilish chiqarilmaydi |
| T4/16 GB, 8CPU, 32GB, 3× | Og‘irlik hajmi mos; T4 tezlik va xotira sinovi bajarilmagan |
| Barcha to‘liq sample EDA/predictions_samples.json | Hali yo‘q; faqat 4 ta 10.01 s parcha EDA va predictions_excerpts_official.json bor |
| Public repo, revision, 3 a’zo, portfolio, public sayt | Forma va ishga tushirish fayllari bor; haqiqiy ma’lumot/hosting berilmagan, public nashr qilinmagan |

Bu cheklovlar sabab loyiha 100% tayyor tanlov topshirig‘i deb ko‘rsatilmaydi. Avtomatik 6 qoida ham evristik: stopped_vehicle navbatlardan tashqarida ≥10s, jaywalking crossing tashqarisida, wrong_way tasdiqlangan yo‘nalishga qarshi, failure_to_yield crossing birga bandligi, congestion barcha belgilangan yo‘laklar, road_obstacle faqat ayrim hayvonlar. Har biri PDFdagi to‘liq semantikaga taxminiy yaqinlashuv; wheel/contact/signal/intent dalillarini model bermaydi.

## Keyingi amaliy qadamlar

1. 0–12 soat: to‘liq 4 videoni olish, checksum, barcha sample EDA va pred; rasmiy kamera tavsifini olish.
2. 12–36 soat: mustaqil qo‘lda annotatsiya, xatolarni ko‘rish, 6 qoidaning chegaralarini tuzatish; zarur signal/turn modellari va qonuniy geometriya.
3. 36–48 soat: rasmiy harness, T4 3×/RAM sinovi, toza o‘rnatish, public repo/weights/hosting va 3 a’zo ma’lumotlari.
4. 48–72 soat: vaqt bo‘lsa Part B modeli, holdout tekshiruvi, barcha sample vizualizatsiyasi va final qayta sinov.

Keyingi to‘liqroq ish: ko‘proq qo‘lda belgilangan ruxsat etilgan ma’lumot bilan temporal modelni o‘qitish, iz uzilishi va perspektivani tuzatish, contact/near_miss/fire_smoke uchun alohida ochiq model, probabilistik Part B va kalibrlash. Natijalar faqat o‘lchangandan keyin hisobotga kiritiladi.

## Yakuniy tekshiruv dalili

18 birlik testi o‘tdi. O‘zgarmagan rasmiy harness 4 real parcha uchun 5 taxminiy segment va har biriga 300 risk namunasi berdi; evaluate.py 0 xato, 0 ogohlantirish bilan VALID dedi. Formatning to‘g‘riligi aniqlik balli emas. Haqiqiy JPEG kadr uchun kamera API 21 obyekt qaytardi. HTTP orqali barcha real parcha natijalari, moslash, 14 sinf jadvali, PDF va hisobot ochildi. Brauzerni avtomatik ishga tushirish muhitda SIGABRT bilan to‘xtadi; vizual UI va fizik kamera sinovi o‘tdi deb da’vo qilinmaydi.
