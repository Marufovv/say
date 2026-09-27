# Yuksava: topshirish holati

Repository tuzilishi: solution.py, run_submission.py, evaluate.py, requirements.txt, README.md, src, weights, samples, docs ildizda. Asl 01–06 papkalar saqlanadi; GitHub Pages ulardagi saqlangan natijalarni ochadi. Rasmiy skriptlar o‘zgartirilmaydi. Model yig‘ilganda SHA256 tekshiriladi.

## Bajarilgan yoki tekshirishga tayyor
- Uch jamoa a’zosi, vazifalari va email kontaktlari saqlangan.
- Haqiqiy video upload va tahlil qiladigan Python dasturi bor; Dockerfile uni serverda ishga tushiradi.
- 14 event ta’rifi va qo‘lda tekshirish oynasi; 6 dastlabki avtomatik qoida. Nizom CLASSES ro‘yxatini qisqartirishga ruxsat beradi. Part B ixtiyoriy nol baseline.
- Bir sinf segmentlari birlashtiriladi; vaqtlar video chegarasida.
- 4 ta 10.01 soniyali haqiqiy parcha va ularning EDA/natijalari mavjud.
- GitHub Actions birlik testlari va o‘zgarmagan harness/validatorni bajaradi. CI muvaffaqiyati hidden-test aniqligi degani emas.

## Hali yakunlanmagan majburiy ishlar
1. To‘liq 4 original sample videosining EDA, vizualizatsiya va predictions_samples.json natijasi. Parcha natijasini shu nom bilan yashirish mumkin emas.
2. Internetdan yangi video yuklab tahlil qilinadigan public Python/Docker server va butun hakamlik davrida ishlashi. GitHub Pages bunga yetmaydi.
3. T4 sinfi 16 GB GPU / 8 CPU / 32 GB RAM sharoitida A+B ≤3× va xotira o‘lchovi.
4. Yakuniy commit/tagni topshirishda qayd etish va jamoa portfolio havolalarini to‘ldirish.

## Aniqlashtirish va model chegaralari
- samples/camera.md berilmagan; signal va huquqiy taqiqlar uydirilmaydi.
- 8 sinf uchun avtomatik detektor yo‘q. Mavjud 6 qoida ham evristik, sifatini belgilangan ground truth bilan tekshirish kerak.
- Haqiqiy hidden-test F1 yoki tanlov balli o‘lchanmagan. To‘liq nizomga mos tayyor topshirish deb e’lon qilinmaydi.

## Hosting
GitHub repo → Docker/Python Web Service. Root Directory bo‘sh, Dockerfile Path `./Dockerfile`, health `/api/health`. Server `PORT` ni o‘qiydi. Doimiy disk uchun `YUKSAVA_DATA_DIR` sozlanadi. GitHub Pages `index.html` ko‘rish rejimini saqlaydi. Docker build mahalliy Docker bo‘lmasa sinalmagan; hostingdagi log tekshirilishi kerak.
