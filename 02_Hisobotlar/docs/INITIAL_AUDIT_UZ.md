# WIUT Hackathon 2026: resurs, talab va starter-kit auditi

Tekshiruv: 24-sentabr 2026. Bu hisobot birinchi amaliy bosqich natijasi; tayyor deteksiya modeli yoki yakuniy submission emas. Asl biriktirilgan fayllar o‘zgartirilmadi. ZIPdan chiqarilgan rasmiy fayllar ham o‘zgartirilmadi. Nazorat summasi (SHA-256) faylning aynan saqlanganini tekshiradi.

Vazifa sodda qilib: bitta yo‘l kamerasining videosida hodisa qachon boshlanganini, qachon tugaganini va turini topish. Part A majburiy. Part B esa faqat hozirgacha ko‘rilgan kadrlardan kelgusi 5 soniyadagi avariya xavfini baholash; ixtiyoriy. Kod bilan birga public sayt, haqiqiy upload demo va qisqa texnik hisobot ham talab qilinadi.

## 1. Resurslar va dastlabki talablar

| Resurs | Tekshirilgan holat | Nima uchun ishlatiladi |
|---|---|---|
| wiut_cv_scripts.zip | 20 968 bayt; 7 mazmunli fayl, .DS_Store va __MACOSX yozuvlari | Interfeys, harness (ishga tushiruvchi skript), metrika va format |
| WIUT Hackathon _ CV Track Elimination Task.pdf | 256 742 bayt; 11 sahifa to‘liq matni o‘qildi, sahifalar render qilindi, event jadvali vizual tekshirildi | Rasmiy talablar va vaqt chegaralari |
| Videos.pdf | 40 326 bayt; 1 sahifa; 4 noyob Drive havolasi | Videolarga kirish |
| Pasted text.txt | 21 097 bayt; qo‘shimcha reja matni o‘qildi | Kontekst; tashkilotchi qoidasi sifatida olinmadi |
| examples/ground_truth.json, predictions.json | Format misollari; 2 xayoliy sample nomi, GTda 8, predictionda 9 hodisa | Skript ishlashini sinash; haqiqiy videolarning annotatsiyasi emas |
| Mahalliy muhit | macOS 27.0 arm64, Python 3.14.5, 10 mantiqiy CPU; RAM tekshiruvi tizim tomonidan cheklangan | Faqat mahalliy interfeys sinovi; T4 o‘lchovi emas |

| Talab/toifa | Manba | Chiqadigan natija va qabul mezoni | Hozirgi holat |
|---|---|---|---|
| Majburiy: Part A | PDF 1, 5 | solution.py; haqiqiy videodan qonuniy segmentlar, 14 rasmiy label doirasi | Faqat bo‘sh baseline ishladi; 0/14 sinf detektori bor |
| Majburiy: rasmiy skriptlarni o‘zgartirmaslik | PDF 7, 10 | ZIPdagi baytlar bilan bir xil SHA-256 | Bajarildi |
| Majburiy: repository, weights, src, README, requirements yoki Dockerfile, predictions_samples.json | PDF 7–8 | Toza muhitda 2 buyruq ishlashi; sample natijalari takrorlanishi | Hali yakuniy paket yo‘q |
| Majburiy: public sayt va ishlaydigan .mp4 upload | PDF 8–9 | Haqiqiy model natijasi, timeline, playback/kliplar; jarayon va limitlar; hakamlik davomida onlayn | Hali yo‘q |
| Majburiy: barcha samplelar EDA va vizualizatsiyasi | PDF 8–9 | Haqiqiy o‘lchovlar, obyektlar, izlar, zichlik, hodisalar va xatolar | Videolar mahalliy yo‘q |
| Majburiy: qisqa hisobot, jamoa va havolalar | PDF 1, 8–9 | Usul, ishlagan/ishlamagan qismlar; a’zolar hissasi; repo/weights/predictions havolalari | Ushbu audit tayyor; loyiha hisoboti hali emas |
| Majburiy: offline, ≤5 GB weights, ≤3× davomiylik | PDF 7 | Internetsiz to‘liq run, hajm va vaqt dalillari | Sintetik baseline vaqt limiti ichida; model/T4 testi yo‘q |
| Majburiy: determinism, litsenziya, manbalar | PDF 7–10 | Seedlar, qayta run, ochiq weights, dataset litsenziyasi, attribution | Baseline ikki run bir xil; model hali tanlanmagan |
| Ixtiyoriy: Part B | PDF 2 | Causal RiskEstimator, har kadrda 0–1 | Standart nol klass saqlandi va tekshirildi |
| Ixtiyoriy | PDF 7, 9 | Notebook, ablation, interaktiv grafik, event orqali video vaqtiga o‘tish, qo‘shimcha dashboard | Keyingi bosqich |
| Tavsiya | PDF 10–11 | O‘z annotatsiyalari, detector+tracker, vaqt chegaralarini tahlil qilish, erta runtime sinovi | Rejaga kiritildi |
| Bizning muhandislik tanlovi | Ushbu audit | configs/, annotations/, tests/, docs/, web/; aniq versiyalarni alohida yozish | Rasmiy majburiy kataloglar deb ko‘rsatilmaydi |

### Yetishmayotgan resurslar va aniqlashtirishlar

| Nima | Tasdiqlangan dalil / savol | Ta’siri |
|---|---|---|
| samples/camera.md | ZIPning barcha yozuvlari va berilgan 4 attachment ichida yo‘q. sample/camera.md ham yo‘q. Rasmiy nom PDF 4da **samples/camera.md** | Yo‘lak, ruxsat etilgan burilish, svetofor va chiziq konfiguratsiyasi tasdiqlanmagan |
| Haqiqiy .mp4 fayllar | ZIPda yo‘q; Drive sahifalari mavjud; yuklab olish yakunlanmagan | Haqiqiy baseline, davomiylik/fps/o‘lcham, EDA va CV sifati tekshirilmagan |
| Rasmiy sample label | PDFga ko‘ra berilmaydi | O‘zimiz belgilash va inson tekshiruvi kerak; kamchilik deb tashkilotchiga yuklanmaydi |
| Model weights/src | Boshlang‘ich ZIPda yo‘q | Jamoa yaratadigan qism; starter buzilgan degani emas |
| Deadline | [Rasmiy sayt](https://hackathon.wiut.uz/) 27 Sep 2026 deydi; soat va vaqt zonasi yo‘q | 72 soat bor deb kafolatlab bo‘lmaydi; aniq cutoff tashkilotchidan kerak |
| Amaldagi hardware | PDFda T4-class; bosh sahifada GPU yangilanishi topilmadi, yopiq hackathon kanali tekshirilmagan | Yangilangan rasmiy e’lon bo‘lsa olish zarur |
| Jamoa/server/hosting | Tajriba, mavjud GPU, budjet va portfolio ma’lum emas | Reja uch kishilik taxminiy rol taqsimotiga asoslanadi |
| Qoidalar chekka holati | 4-bo‘limdagi farqlar va event ta’riflaridagi noaniqliklar | Skriptni o‘zgartirmay tashkilotchi aniqligi kerak |

Rasmiy bosh sahifaning final pitch mezonlari CV elimination formulasiga almashtirilmaydi. Sahifada final baholashi haqida alohida FAQ mavjud.

## 2. Videolarning 4 havolasi

| Havola | Brauzerda tasdiqlangan nom | Tekshiruv va cheklov |
|---|---|---|
| [1](https://drive.google.com/file/d/1kR9jODA2Wotw4gwkvpRKdqFADNJNc1nS/view?usp=drive_link) | C3896.MP4 | Drive sahifasi ochildi; avval preview xatosi, keyin player yuklanishi. Download sahifasi **5,8G** ko‘rsatdi, hajm sabab virus tekshiruvi yo‘q; qo‘shimcha tasdiq so‘radi |
| [2](https://drive.google.com/file/d/1hp8DYeqtYHSwfM6qAo9FPSRHlpMFrIN_/view?usp=drive_link) | C3897.MP4 | Sahifa ochildi; preview “videoni yuklab bo‘lmadi” xatosini ko‘rsatdi |
| [3](https://drive.google.com/file/d/10cHEReCWzO3u-Vk1CnNgHAx6egGy5MwJ/view?usp=drive_link) | C3902.MP4 | Sahifa, download tugmasi va player yuklanishi ko‘rindi; ijro/metadata tasdiqlanmadi |
| [4](https://drive.google.com/file/d/1aJ-QsAZVYJtLKHiRvKKeBq1D3GWNobRd/view?usp=drive_link) | C3905.MP4 | Sahifa, download tugmasi va player yuklanishi ko‘rindi; ijro/metadata tasdiqlanmadi |

Oddiy web o‘qish vositasi to‘rttalasini ham ocha olmadi; brauzer esa fayl sahifalarini ochdi. Demak “havolalar ishlamaydi” yoki “fayllar private” degan xulosa chiqarilmaydi. Buyruq qatori orqali birinchi Drive download so‘rovida DNS xatosi bo‘ldi. Nomlar brauzerdan olingan; metadata taxmin qilinmagan. FPS, kadrlar soni, davomiylik, o‘lcham va hodisalar to‘rtta haqiqiy videoning birortasida o‘lchanmagan. PDFdagi “odatda 25 fps, bir necha daqiqa” iborasi real metadata o‘rniga yozilmaydi. Birinchi faylning 5,8G hajmi Drive interfeysi ko‘rsatgan yaxlitlangan qiymat, aniq bayt soni emas.

## 3. 48–72 soatlik real reja

Bu muddat ichida 14 sinfga yuqori aniqlik kafolatlanmaydi. Maqsad — qoidaga mos, qayta ishlaydigan submission va ishonchli kichikroq deteksiya qamrovi. Resurslar ochilmasa, majburiy EDA/sample natijalari tugamaydi. Vaqt kamligi majburiy talabni bekor qilmaydi.

Uch kishi: **A — CV/Part A**, **B — annotatsiya/baholash/tezlik va vaqt qolsa Part B**, **C — sayt/backend/demo/hujjat**. Bu rollar tajribaga ko‘ra almashadi. Backend aynan bir xil solution interfeysini chaqiradi; 6-soatgacha JSON va ish holatlari kelishiladi. Rol taqsimoti taklif, a’zolar tayinlangan degani emas.

| Oyna / rol | Ish, kirish va bog‘liqlik | Natija / qabul mezoni | Xavf va vaqt yetmasa oqibat |
|---|---|---|---|
| 0–4 soat / A+B | ZIP/PDF audit, video va camera.md, deadline/server | Hashlar, ishlaydigan baseline, resurs reyestri | Auditning mahalliy qismi bajarildi; video/camera kechiksa keyingi ishlar cheklanadi |
| 2–10 / B, A yordamida | Haqiqiy videolar ochilgach metadata, kadrlar, sahna EDA; vaqt bloklarini ajratish | 4 video jadvali; camera tasdig‘iga bog‘langan ROI/yo‘nalishlar; tuning va holdout bo‘laklari | 5,8G kabi hajmlar yuklash/dekodlashni cho‘zadi; tekshirilmagan parametrlar majburiy aniqlanmagan deb qoladi |
| 4–18 / A | Ochiq weights va litsenziyani tekshirish, yengil detector+tracker integratsiyasi | Bitta hodisaning video → segment → JSON yo‘li ishlaydi; iz uzilishi ko‘riladi | Noldan katta model o‘qitish rejalashtirilmaydi; tracking xatosi bo‘lsa qamrov torayadi |
| 4–24 / B | PDF qoidalari bilan qo‘lda annotatsiya; bahsli epizodlarga ikkinchi tekshiruv | my_labels.json va belgilash qaydlari; inson tekshirgan/AI taklif ajratilgan | Barcha kadrni ko‘rishga vaqt yetmasa tekshirilgan bo‘laklar aniq yoziladi; to‘liq GT deyilmaydi |
| 4–18 / C | Repo va haqiqiy Python inference backend; dastlab baseline bilan ulash | Upload → navbat/progress → natija; hajm/davomiylik limiti; xatolar | Bo‘sh baseline “deteksiya ishlaydi” deb namoyish qilinmaydi; bu faqat integratsiya |
| 18–36 / A+B | Sahna dalili bor sinflarni qo‘shish; masalan to‘xtash/piyoda/yo‘nalish faqat dalil yetganda | Sinflar bo‘yicha qo‘llab-quvvatlash, FP/FN, chegaralar va holdout F1 | Kamera hujjatisiz “illegal”/signal sinflari tasdiqlanmaydi; 14/14 degan da’vo yo‘q |
| 18–40 / C | Barcha sample vizualizatsiyalari, EDA, team/report/linklar, haqiqiy modelga ulash | Har sampleda playback+timeline; telefon ko‘rinishi; haqiqiy upload sinovi | Dataset ochilmasa bu majburiy bo‘lim tugamaydi; bezakdan oldin funksiyalar |
| 32–44 / B | Part A barqaror bo‘lsa sababiy Part B prototipi; aks holda nol klass | Prefix-causality/reset testi, risk va alarm bahosi; real dalil | Optional qismni tashlash mumkin; accident bor testda 18/100 maksimal ulush boy beriladi |
| 40–48 / hamma | Toza muhit, offline, rasmiy skript hash, runtime/memory/weights, sayt test | 48-soatlik topshirishga tayyor holat yoki ochiq kamchiliklar ro‘yxati | Sayt, samplelar yoki inference ishlamasa submission to‘liq emas; muhit tuzatishdan keyin ishlamasa model 0 |
| 48–60 / A+B | Faqat eng katta o‘lchangan xatolar; chegaralar, sampling va xotira | O‘zgarishdan oldin/keyin bir xil holdoutda o‘lchov | 72 soat qolmasa yangi sinflar o‘rniga barqarorlik |
| 60–68 / hamma | Regression, yangi muhit/T4 sinovi, hujjat va demo | Qayta run bir xil; vaqtga zaxira; barcha sample natijasi | Mahalliy Mac natijasi T4 dalili emas; T4 bo‘lmasa cheklov ochiq yoziladi |
| 68–72 / jamoa sardori | Public repo/site, teg/commit, yakuniy ko‘rik va topshirish | Aniq commit, URLlar, saqlangan submission dalili | Faqat aniq deadline imkon bersa; oxirgi 4 soat bufer bo‘lsin |

Uyqu/tanaffuslarni almashtirib tashkil qilish va yuklash vaqti uchun zaxira zarur. Jadval kalendar oynalaridir, har odam uchun 72 soat uzluksiz ish emas. 48-soatda ishlaydigan versiya muzlatiladi; keyingi vaqt kafolatlanmagan.

### Keyingi to‘liqroq reja (taxminan 2–4 hafta)

| Muddat / rol | Kirish va ish | Natija / qabul mezoni | Bog‘liqlik, xavf, kechikish oqibati |
|---|---|---|---|
| 1–3 kun / B+A | camera.md, 4 video, rasmiy javoblar; annotatsiyani ikki kishilik kelishtirish | Har label uchun kelishilgan yo‘riqnoma; bahsli epizodlar ro‘yxati | Noaniq GT sifatni buzadi; avval dalil va chegarani tuzatish |
| 3–7 kun / A | Litsenziyasi tekshirilgan public data va weights; tracking/scene konfiguratsiyasi | Sinflar bo‘yicha qamrov, tashqi ma’lumot manifesti, holdout natijalari | Shu kameradan qo‘shimcha footage yig‘ilmaydi; rare class yetishmasa qamrov cheklangan |
| 5–12 kun / A+B | Accident/near-miss kliplari, occlusion va temporal chegara tahlili | Tekshirilgan klassifikator/rule taqqoslash, xato galereyasi | Box overlap kontakt isboti emas; transfer natijasi kafolatlanmaydi |
| 8–15 kun / B | Sababiy izlar va risk; vaqt bo‘yicha ajratilgan label | Kalibrlash, AP/alarm/TTA, kelajakdan ma’lumot sizmasligi testi | 4 sample statistik ishonch uchun kam; katta generalizatsiya da’vosi yo‘q |
| 12–18 kun / A+C | T4, uzun/yuqori aniqlikdagi video, offline muhit | Vaqt/xotira profili; sampling/batching ablation; deploy artefakt | Python risk ro‘yxati katta xotira olishi mumkin; throughput tekshiriladi |
| 15–21+ kun / C+B | Barqaror backend, o‘lchangan natijalar | To‘liq EDA, barcha sample, access/progress/error UX, reproduksiya va release | Hosting ishlamasa demo balli yo‘q; yangi feature release sifatini buzmasin |

Bu reja boshlang‘ich deadline o‘rnini bosmaydi va deadline’dan keyingi commitlar elimination’da hisoblanishini anglatmaydi.

## 4. PDF va starter-kit taqqoslanishi

### Interfeys va hardware

`solution.py` ildizda `CLASSES`, `detect_events(video_path) -> list[list]`, `RiskEstimator.reset(meta)`, `step(frame,t_sec) -> float` ni beradi. 14 ID PDF, solution va evaluate’da bir xil. `reset`ga video_id/fps/width/height/n_frames beriladi; `step` har kadrda BGR uint8 (H,W,3) oladi. Part A ko‘p marta o‘qishi mumkin; Part B video ochmaydi va kelajakdan hisoblangan Part A natijasini olmaydi. Bu sababiylik kod auditiga ham muhtoj: harness bir modulni yuklaydi, holat almashishini avtomatik taqiqlamaydi.

Rasmiy cheklovlar: Python ≥3.10; 1×NVIDIA T4-class 16 GB VRAM, 8 CPU, 32 GB RAM; weights jami ≤5 GB; Part A+B ≤3×video davomiyligi; inference internetsiz. weights/download.sh oldindan internet bilan bir marta ishlashi mumkin. Hosted model inference API taqiqlangan. Kod/sayt/hisobotni AI yordamida yozish mumkin. Ochiq weights, dataset litsenziyalari, attribution, seedlar va bir xil bashoratlar talab qilinadi. Qo‘shimcha shu-kamera video yig‘ish taqiqlangan. Jamoa 3 kishi, bitta submission, deadline’dagi tagged commit.

| Masala | PDF/README bayoni | Kodning haqiqiy xatti-harakati va ta’sir |
|---|---|---|
| Xatoda bo‘sh natija | PDF 6: detect_events yoki step crash bo‘lsa video empty | run_submission.py 173–196: A xatosida B ishlashda davom etadi; B xatosida A saqlanadi. Ikki alohida test tasdiqladi. Skript o‘zgartirilmadi |
| Meta/import xatosi | Umumiy crash bayoni | solution import 146 va video_meta 166 per-video try tashqarisida; buzilgan fayl ochilmasa butun jarayon to‘xtashi mumkin. Statik audit; korrupt-video test bajarilmadi |
| End video davomiyligidan katta | PDF: end≤duration; README noto‘g‘ri vaqtlar dropped | clean_events 91da end duration’ga jim kesiladi, logga yozilmaydi; evaluate 98da GT bo‘lsa +0.5 s tolerant. GTsiz yuqori chegara tekshirilmaydi. Test tasdiqladi; yechim qat’iy PDF chegarasini saqlashi kerak |
| Same-class overlap | FAQ: bir segmentda qamrab olish kerak | Harness 96–104 birlashtirmaydi, keyingi segmentni tashlaydi. Bu zid qoida emas: birlashtirish solution mas’uliyati. Test tasdiqladi |
| “Har doim valid” clean_events | run_submission.py 76 izohi | 95da 3 xona yaxlitlash juda qisqa segmentni [0,0] qilishi mumkin; qayta s<e tekshiruvi yo‘q. [0.0001,0.0002] bilan test tasdiqladi. Buni umumiy 0.5 s haqiqiy hodisalarni olib tashlash qoidasi bilan “tuzatish” kerak emas |
| Near-miss ignore ustuvorligi | PDF 6: accident ichidagi va near_miss [s−5,e] kadrlari ignored | evaluate 224–233: avval accident ichini ignore, keyin accident oldi positive, keyin near-miss ignore. Kesishganda positive yutadi. t=8, accident [10,12], near_miss [9,11] → 1. Tashkilotchidan aniqlik kerak |
| Doimiy risk=1 har doim 0 | PDF 6 shunday umumlashtiradi | AP=0, ammo t=0 alarm 10 s oynadagi accidentga mos tushishi mumkin. Sun’iy s=5 holatda Score_B=0.5 chiqdi. Audit counterexample; metrikadan foydalanib ball oshirish usuli sifatida qo‘llanilmaydi |
| Accident yo‘q holat | PDF asosiy formulasida fallback ochiq yozilmagan | evaluate 278–281,344–350 va README94–95: B=None, M=A. Test tasdiqladi |
| Ortiqcha video ignored | evaluate validator 124–125 va report 361–362 | Part A 176–179 sinflarni barcha predictionsdan yig‘adi; GTda yo‘q video yangi label olib kirsa macro denominator o‘zgaradi. Testda A 1→0.5. Faqat talab qilingan videolarni chiqarish kerak |
| Vaqt limiti | 3× wall-clock | t0 video metadata va modul importidan keyin; A majburan interrupt qilinmaydi, tugagach limit tekshiriladi. B har 100 kadrda deadline tekshiradi; yakunda vaqt 0.1 sga yaxlitlangan holda solishtiriladi. Import/model yuklashning rasmiy hisobga olinishi aniqlashtirilsin |
| Xotira/weights/GPU/offline | PDF hardware limitlari | Skript bu chegaralarni avtomatik cheklamaydi; tashqi muhit va jamoa tekshiruvi kerak |
| Risk formatining to‘liqligi | Har kadrda bitta risk | evaluate timestamps non-decreasing/range ni tekshiradi, ammo har kadr soni, to‘liq qamrov, duration va barcha finite timestamp shartlarini to‘liq tekshirmaydi. VALID faqat cheklangan format testi |
| “ONLY solution.py” | README8 va solution sarlavhasi | solution.py9–10 va PDF7 yordamchi src/ni ruxsat etadi; ma’nosi interfeysni shu faylda saqlash, hamma kodni bitta faylga tiqish emas |
| Dependency versiyalari | numpy≥1.24, opencv-python-headless≥4.8 | Yuqori chegara/lock yo‘q. Ushbu muhitda yangi versiyalar o‘rnatildi; reproducibility uchun keyingi loyiha muhitining aniq versiyalari saqlanishi tavsiya |
| Postprocessing tavsiyasi | README103: sub-second blip; solution62–63: <0.5s/gap<1s | Bular tavsiya, event ta’rifini o‘zgartiradigan rasmiy minimum emas. Qisqa haqiqiy eventlarni ko‘r-ko‘rona o‘chirmaslik kerak |
| Part A riskdan foydalanishi | PDF11: A B riskini ishlatishi mumkin | Harness avval A, keyin B chaqiradi; tayyor B curve A’ga uzatilmaydi. A kerak bo‘lsa o‘zi alohida causal pass qiladi; Bga future cache uzatilmaydi |

### Scoring: aniq qoida

Part A: sinf va temporal IoU (vaqt kesmalarining kesishmasi/birlashmasi) 0.3/0.5/0.7 uchun bir videodagi juftlar IoU kamayish tartibida birga-bir greedy moslanadi. TP/FP/FN videolar bo‘yicha yig‘iladi; har sinfning uch F1 o‘rtachasi, keyin sinflar o‘rtachasi olinadi. Teng IoU juftlar kodda tuple indekslari bilan reverse tartibga tushadi. Sinflar GT yoki predictionda paydo bo‘lganlar; noto‘g‘ri yangi rasmiy class prediction ham denominatorni oshiradi. Micro va class-agnostic diagnostika, asosiy score emas. Har ikkisi bo‘sh bo‘lsa A=0.

Part B: H=5 s, W=10 s, theta=0.5, merge gap qat’iy <2 s. Accident [s,e] uchlari bilan ignore; accident oldi [s−5,s) positive; near_miss [s−5,e] ignore, lekin koddagi ustuvorlik yuqorida qayd etilgan. AP bir xil score qiymatlarini bir guruh sifatida hisoblaydi. Normallashtirilgan AP=max(0,(AP_raw−r)/(1−r)); r=1 bo‘lsa kod 0 oladi. Random score cheklangan kichik namunada tasodifan musbat AP berishi mumkin, “har doim aynan 0” kafolati yo‘q.

Alarm — score≥0.5 davomli qatori; oxirgi yuqori kadr bilan keyingi yuqori qator start orasidagi farq <2 s bo‘lsa birlashadi. Avval qatorlar birlashadi, so‘ng start ignored bo‘lsa butun alarm olib tashlanadi. Accidentlar vaqt tartibida; [s−10,s) oynadagi eng erta foydalanilmagan alarm moslanadi. Moslanmagan accident TTA=0. mTTA barcha accidentlar bo‘yicha o‘rtacha. B=0.4AP+0.4F1_alarm+0.2min(1,mTTA/10). PDFda min yozilmagan, lekin 10 s matching oynasi uni odatiy valid holatda ortiqcha himoya qiladi.

M=0.7A+0.3B; accident umuman yo‘q bo‘lsa kodda M=A. Elimination=0.6M+0.25Website+0.15Code. Accident mavjud holatda 100 balldagi ulushlar: A42, B18, sayt25, kod15. Bni tashlash majburiy talabni buzmaydi, ammo uning ulushini bermaydi; A/sayt/kod mukammal bo‘lgandagina nazariy maksimal 82. Bu prognoz ball emas.

Sayt rubrikasi: demo30%, barcha sample vizualizatsiyasi20%, EDA15%, usul/hisobot15%, team/portfolio10%, UX/extras10%. Kod: submitted run40%, reproducibility25%, structure20%, engineering15%. evaluate.py sayt/kod/Elimination yakunini hisoblamaydi; faqat model qismini chiqaradi.

## 5. 14 sinf uchun belgilash yo‘riqnomasi

Quyidagi start/endlar PDF 2–4-jadvalining o‘zbekcha mazmunidir. Kodda label va qisqa izohlar bor, vaqt semantikasini tekshiradigan detektor yo‘q. **Barcha 14 sinf: hozir amalga oshirilmagan, haqiqiy video sifati sinalmagan.** Jadvaldagi yondashuvlar keyingi implementatsiya taklifi.

| Label va ta’rif | Boshlanish | Tugash | Kerakli dalil / usul va cheklov |
|---|---|---|---|
| accident: yo‘l ishtirokchilari o‘zaro yoki qo‘zg‘almas obyektga urilishi | Kontakt ko‘ringan birinchi kadr | Barcha ishtirokchilar harakatdan to‘xtaydi yoki kadrdan chiqadi | Kontakt va keyingi harakatning temporal klipi; bbox overlapning o‘zi isbot emas |
| near_miss: kontaktsiz qochish uchun keskin tormoz/burilish | Qochish harakati boshlanishi | Ishtirokchilar bir-biridan xoli bo‘ladi | Izlar, keskin o‘zgarish, kontaktsizlik; odatiy burilishdan farqlash |
| red_light: o‘z signalida qizil payt stop-chiziqdan o‘tish | Transport old qismi chiziqni kesadi | Chorrahadan yoki kadrdan chiqadi | Signal holati, transport yo‘lagi, stop-chiziq va intersection; signal ko‘rinmasa dalilsiz label yo‘q |
| wrong_way: yo‘lak oqimiga qarshi, shu jumladan qarama-qarshi yo‘lakda yurish | Qarama-qarshi yo‘lakka kiradi | To‘g‘ri yo‘lakka qaytadi yoki kadrdan chiqadi | Tasdiqlangan lane/direction va iz; video boshi ichkarida bo‘lsa annotatsiya konvensiyasi aniqlashtiriladi |
| illegal_u_turn: belgi/chiziq taqiqlagan qayrilish | Burila boshlaydi | Burilishni tugatadi | Taqiq dalili va trajectory; 180° burilishning o‘zi noqonuniylik isboti emas |
| stopped_vehicle: qatnovda ≥10s qimirlamaslik, signal navbati emas | Transport to‘xtagan payt (10sdan keyin emas) | Qayta yuradi yoki olib tashlanadi | Barqaror iz, ≥10s tasdiq, queue exclusion; kamera tebranishi/occlusion hisobga olinadi |
| jaywalking: crossing tashqarisidagi qatnovda piyoda | Yo‘lga qadam qo‘yadi | Yo‘ldan chiqadi | Piyoda va road/crossing poligonlari; oyoq nuqtasi/occlusion ehtiyotkorligi |
| failure_to_yield: crossingdagi yoki unga qadam qo‘yayotgan piyodaga qaramay o‘tish | Transport crossingga kiradi | Transport crossingdan chiqadi | Piyoda+transport birgalikdagi vaqt va zona; solution qisqa izohida “stepping onto” tushib qolgan, PDF to‘liq ta’rif olinadi |
| illegal_turn: noto‘g‘ri yo‘lakdan yoki taqiqlangan yo‘nalishga burilish | Burilish boshlanadi | Burilish tugaydi | Ruxsat etilgan lane→turn xaritasi; faqat tasdiqlangan sahna konfiguratsiyasi |
| solid_line_crossing: uzluksiz chiziq orqali manevr | G‘ildirak chiziqni kesadi | Transport yangi yo‘lakka to‘liq o‘tadi | Chiziq va g‘ildirak/transport geometriyasi; oddiy markaz nuqta chegarani siljitadi |
| stop_line: qizilda chiziqdan o‘tib, chorrahaga kirmay to‘xtash | Transport to‘xtaydi | Signal yashilga o‘tadi | Signal + stop chiziq + intersection; end “qayta yurdi” deb almashtirilmaydi |
| congestion: yo‘nalishdagi barcha yo‘laklarda to‘xtash/juda sekin yurish | Navbat harakati to‘xtaydi | Navbat tarqaladi | Barcha lane occupancy va harakat; crawl ta’rifi bilan start “stops” o‘rtasidagi noaniqlik so‘raladi |
| road_obstacle: qatnovdagi chiqindi, hayvon, tushgan obyekt | To‘siq paydo bo‘ladi | To‘siq olib tashlanadi | Road ROI va mos detector/background evidence; odam/soya bilan chalkashmasligi |
| fire_smoke: yo‘l yoki transportdagi ko‘rinadigan olov/tutun | PDF aynan “birinchi ko‘rinadigan tutun” deydi | Tutun tarqaladi yoki kadr tugaydi | Temporal tasdiq; bug‘/changdan farqlash. Tutunsiz olov uchun start/end PDFda noaniq, o‘zimiz qoida qo‘shmaymiz |

Umumiy: birinchi kadrdan soniyalar; 0≤start<end≤duration; videodan keyin davom etgan event end=duration. Bir xil sinfda bir vaqtdagi hodisalar eng erta start/eng kech end bilan qamrab olinadi. Turli sinflar overlap qilishi mumkin. Speeding yo‘q. Piksel masofa kalibrlanmagan metr/tezlik sifatida aytilmaydi. Video boshida allaqachon davom etayotgan event, qisqa occlusion, queue “clears”, tutunsiz olov kabi holatlar bo‘yicha annotator konvensiyasini tashkilotchidan so‘rash kerak.

## 6. Bajarilgan amaliy bosqich va test dalillari

ZIP yo‘llari absolute/traversal/symlink bo‘yicha tekshirilib, `work/starter/`ga chiqarildi. Mazmunli fayllar: solution.py, run_submission.py, evaluate.py, requirements.txt, README.md, examples/ground_truth.json, examples/predictions.json. 20 ZIP yozuvi jami: 2 katalog, 18 fayl (7 mazmunli + 11 metadata). `starter_manifest.json` har bir faylning bayti/SHA-256 va unchanged tekshiruvini beradi. src/, weights/, notebooks/, samples/, predictions_samples.json yo‘q.

Alohida `work/venv` yaratildi. Boshlang‘ich o‘rnatish tarmoq cheklovi sabab ishlamadi; tarmoq ruxsatidan so‘ng requirements o‘zgarmagan holda muvaffaqiyatli o‘rnatildi: numpy==2.5.3, opencv-python-headless==5.0.0.93 (cv2.__version__ 5.0.0). Bu Mac/arm64/Python3.14.5 tekshiruvi; Linux/Python3.10/T4 uchun kafolat emas. GPU modeli va RAM bu auditda tasdiqlanmadi; NVIDIA ishlatilgani haqida da’vo yo‘q.

| Sinov | Haqiqiy natija | Nimani isbotlamaydi |
|---|---|---|
| Sintetik MP4: 320×240, 25fps, 100 kadr, 4s | Fayl yaratildi/dekodlandi | Bu WIUT sample emas, hodisali test to‘plami emas |
| O‘zgarmagan baseline, 2 marta | Har safar 0 event, 100 risk=0, log errors=[] | Aniqlik, 14 class qamrovi, real avariya yo‘qligi |
| Baseline format | VALID, 0 error, 0 warning | Formatdan tashqari model sifati |
| Bashoratlar determinismi | events/risk obyektlari aynan teng | Kelajakdagi haqiqiy model determinismi |
| Runtime | Birinchi butun subprocess ~0.203s; harness 0.1s aniqlikda 0.0s; budget12s | 0.0 haqiqiy nol vaqt emas; real video/T4 tezligi emas |
| Example JSON format | 2 video, 9 event, VALID, 0 warning | Haqiqiy sample natijasi emas |
| Example JSON metrikasi | A=0.9074, B=0.7600, M=0.8632 | **Bizning modelimizning balli emas**; tayyor format misoli hisoblandi |
| 18 xatti-harakat tekshiruvi | 18/18 kutilgan audit kuzatuvi tasdiqlandi | “18 ta tashkilotchi talabi bajarildi” degani emas; ayrimlari kamchilikni qayta ko‘rsatadi |
| A/B exception sinovi | Alohida vaqtinchalik test modullari bilan boshqa qism saqlanishi isbotlandi | Asl solution.py o‘zgartirilmagan |
| Hash tekshiruvi | Asl fayllar va chiqarilgan kit nazorat qilindi | Keyingi tahrirlardan keyin yana tekshirish kerak |

`tests/checks.json` — 18 tekshiruv; `tests/*.log.json` — stdout/stderr/exit code/vaqt; `tests/baseline1.json` va baseline2 — faqat sintetik prediction; `tests/example_score.json` — misol JSON score. `test_summary.log` qisqa umumiy dalil. Hech biri `predictions_samples.json` deb nomlanmadi.

### Keyingi haqiqiy baseline’ni ishga tushirish

Ishchi kit ichida rasmiy defaultlar bilan:

```sh
python run_submission.py --videos /absolute/path/to/samples --out predictions_samples.json --team TEAM_NAME
python evaluate.py --pred predictions_samples.json --validate-only
python evaluate.py --pred predictions_samples.json --gt my_labels.json --per-video
```

Oxirgi buyruq faqat haqiqiy, tekshirilgan my_labels.json bo‘lganda. `TEAM_NAME` haqiqiy jamoa nomi bilan almashtiriladi. Official rejimda `--no-risk`, `--risk-stride`, `--time-factor` bilan natijani yengillashtirib ko‘rsatmaslik kerak. Har run logidagi errors ham tekshiriladi; exit code 0 hamma video xatosiz degani emas.

Paketdagi README_AUDIT.md lokal qayta bajarish yo‘lini beradi. Hozir yangi detektor yozish, weights yuklash, sayt qurish yoki public nashr qilish bajarilmadi: ular ushbu so‘rovdagi birinchi amaliy bosqichdan keyingi ishlardir.

## 7. Yakuniy holat

| Ish | Holat |
|---|---|
| Uch asosiy manba va qo‘shimcha kontekstni o‘qish | Bajarildi |
| Asllarni saqlash, ishchi nusxa, checksum, ZIP audit | Bajarildi |
| 5 asosiy faylning kodi/mazmunini audit qilish | Bajarildi |
| 14 class start/end, scoring/interface/hardware solishtirish | Bajarildi; noaniqliklar alohida yozildi |
| 4 link mavjudligi va nomlari | Bajarildi |
| camera.md bor-yo‘qligi | Berilgan to‘plamda yo‘qligi tasdiqlandi; tashqi tashkilotchi resurslarining hammasida yo‘q deyilmaydi |
| 48–72 soat va to‘liqroq reja | Bajarildi; cutoff/jamoa/GPU javobiga qarab moslanadi |
| O‘zgarmagan baseline va mavjud mahalliy sinovlar | Bajarildi — sintetik video va example JSONlarda |
| Haqiqiy 4 video metadata/EDA/baseline | Bajarilmadi — fayllar yuklanmagan |
| Haqiqiy aniqlik, T4 runtime, xotira, offline toza Linux testi | Bajarilmadi |
| Detektor, Part B modeli, demo/sayt, yakuniy submission | Keyingi reja; bajarildi deb ko‘rsatilmaydi |
