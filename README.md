# Yuksava

WIUT CV loyihasi: mahalliy video tahlili, jonli kompyuter/USB kamera, hodisa annotatsiyasi va 4 haqiqiy sample parchasi.

| Jamoa a’zosi | Vazifasi | Email |
|---|---|---|
| Marufov Ozodbek | Captain | marufovozodbek64@gmail.com |
| Muharramxon Alixonova | UI/UX designer | alixonovamuharramxon45@gmail.com |
| Abdubannopova Oydinoy | Data analytics, researcher | o3939043@gmail.com |

## GitHub’ga yuklash

1. ZIPni oching. GitHub’da `yuksava` nomli yangi repository yarating.
2. `Add file → Upload files` orqali Yuksava_GitHub papkasi **ichidagi fayl va papkalarni** repository ildiziga tashlang. ZIPning o‘zini yuklamang. `app.py`, `README.md`, `Dockerfile` ildizda tursin.
3. `Commit changes` bosing. Agar 100 fayldan ortiq bo‘lsa ikki bo‘lib yuklang. Mac’da yashirin `.github`, `.gitignore`, `.dockerignore` ni ko‘rsatish uchun Command+Shift+. bosing. GitHub Desktop butun papkani ham nashr qila oladi.
4. Repository manzilini `configs/project.json` dagi `repository` maydoniga yozing.

Model `weights/yolox_s.part01` va `part02` ko‘rinishida qo‘shilgan: har fayl brauzerning 25 MiB chegarasidan kichik. O‘rnatishda ular SHA256 tekshiruvi bilan birlashtiriladi. Bu modelni qayta o‘qitmaydi va inference uchun internet kerak emas.
GitHub qoidasi: https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github

## Kompyuterda ishga tushirish

Mac: `start.command`; Windows: `start.bat`. Yoki Python 3.10+ bilan:

```sh
pip install -r requirements.txt
python weights/download.py
python scripts/start.py
```

Manzil: http://127.0.0.1:8765 . Dastlabki ishga tushishda 4 real parcha va oldindan hisoblangan natijalari avtomatik tiklanadi. Yangi yuklangan video haqiqiy modelda qayta tahlil qilinadi.

## Internetda ishlatish

GitHub Pages Python tahlil serverini bajarmaydi. Butun repositoryni Docker/Python qo‘llovchi serverga joylashtiring. Dockerfile modelni yig‘adi, `PORT` o‘zgaruvchisini qabul qiladi; HTTPSni hosting xizmati beradi.

```sh
docker build -t yuksava .
docker run --rm -p 8765:8765 -v yuksava-data:/data -e YUKSAVA_DATA_DIR=/data yuksava
```

Docker bo‘lmasa serverda `pip install -r requirements.txt`, `python weights/download.py`, so‘ng `python scripts/serve.py` ishlatiladi. Health manzili: `/api/health`. Bitta worker ishlating. Doimiy ma’lumot uchun `YUKSAVA_DATA_DIR` ni disk/volume manziliga belgilang. Aniq hosting tarifida tezlik/RAM sinovi hali yo‘q; Docker bu kompyuterda o‘rnatilmagani uchun container sinovi bajarilmagan.

Docker public rejimida jamoa tahriri yopiq; `configs/project.json` ni GitHub’da o‘zgartirib qayta deploy qiling. Mahalliy rejimda forma saqlaydi; o‘zgarishlar `.local/project.json` da turadi va restartdan keyin qoladi. Hosting mavjud ma’lumotini saqlash uchun doimiy disk zarur.

## Tekshiruv va haqiqiy chegaralar

```sh
pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python run_submission.py --videos samples/excerpts --out predictions_excerpts.json
python evaluate.py --pred predictions_excerpts.json --validate-only
```

19 birlik testi va rasmiy format tekshiruvi mahalliy bajarildi. GitHub Actions CI fayli qo‘shildi; GitHub’da hali ishga tushirilmagan. 4 real videoning faqat dastlabki 10.01 s parchalari tahlil qilingan. Avtomatik qamrov 6 dastlabki qoida; 8 detektor, to‘liq videolar, T4 va hidden-test aniqligi hali tayyor emas. Part B nol baseline. Bu paket barcha 14 sinfni ishonchli aniqlaydi degan da’vo yo‘q. Tafsilotlar: [texnik hisobot](docs/TECHNICAL_REPORT_UZ.md).
