<div align="center">

<a href="https://payam-resan.com">
  <img src=".github/assets/logo.svg" width="64" height="64" alt="پیام رسان">
</a>

<h1>مرجع وب‌سرویس پنل پیامکی پیام رسان</h1>

توصیف ماشین‌خوان رابط برنامه‌نویسی <a href="https://payam-resan.com"><b>پنل پیامکی پیام رسان</b></a><br>
منبع واحدی که مستندات، نمونه‌کدها و سرور MCP از آن مشتق می‌شوند

[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-0a7cbd)](specs/v3/openapi.yaml)
[![API](https://img.shields.io/badge/API-V3%20%2B%20V4-777bb4)](https://payam-resan.com)
[![Lint](https://img.shields.io/badge/redocly-clean-2ea44f)](redocly.yaml)
[![License](https://img.shields.io/badge/license-MIT-6e7781)](LICENSE)

<b>فارسی</b> · <a href="README.en.md">English</a>

</div>

---

این مخزن توصیف رسمی و ماشین‌خوان وب‌سرویس است. راهنمای خواندنی در
سایت [`docs.payam-resan.com`](https://docs.payam-resan.com)، نمونه‌کدهای هر زبان و
سرور MCP همگی از همین فایل‌ها مشتق می‌شوند، تا همه‌جا یک جواب واحد به یک پرسش
داده شود.

اگر دنبال راهنمای خواندنی برای انسان هستید، به
سایت [`docs.payam-resan.com`](https://docs.payam-resan.com) بروید. اینجا خودِ توصیف
است، برای ابزارها و تولیدکننده‌های کد.

## چیدمان

```
specs/
├── v3/
│   ├── openapi.yaml
│   └── codes/
│       ├── error-codes.yaml
│       ├── status-codes.yaml
│       ├── template-status.yaml
│       └── http-status.yaml
└── v4/
    ├── openapi.yaml
    └── codes/
sources/
scripts/
├── validate.py
├── sync_swagger.py
├── validate_swagger.py
└── validate_readmes.py
```

نسخه یک پوشه است، نه یک شاخه و نه یک تگ. نسخه‌های قدیمی‌تر سرویس همچنان فعال‌اند
و باید در کنار نسخه جاری خوانده شوند، پس هر نسخه پوشه خودش را دارد و افزودن یک
نسخه تازه هیچ فایلی را در پوشه‌های موجود تغییر نمی‌دهد.
توصیف V3 شامل ۱۳ عملیات منتشرشده در ۱۱ مسیر و V4 شامل ۲۶ عملیات در ۲۴ مسیر
است. تعریف ۲۵ عملیات پیشین sandbox نسخه ۴ در
[نسخه تاریخی](sources/v4/previous-sandbox.json) و فهرست آن‌ها در توصیف V4
نگه داشته شده است؛ این عملیات در Swagger عمومی نیستند و دوباره آزموده نشده‌اند.
قرارداد درخواست و پاسخ هر نسخه مستقلاً با منبع منتشرشده تطبیق داده شده است.
برای توضیح‌های خالی، خلاصه منتشرشده با علامت‌گذاری صریح استفاده می‌شود.
گزارش کامل، ابهام‌های منبع و نتیجه بررسی‌ها در
فایل [`PUBLISHED-SWAGGER-CHANGES.md`](PUBLISHED-SWAGGER-CHANGES.md) آمده است.

نشانی‌های آزمایشی با تأیید نگهدارنده عبارت‌اند از
نشانی `https://www.payam-resan.com/api/V3SandBox` برای نسخه ۳ و
نشانی `https://www.payam-resan.com/uapi/v4SandBox` برای نسخه ۴. سند Swagger هنوز نشانی
قدیمی دارد؛ اصلاح نشانی جدا از نسخه دست‌نخورده منبع ثبت شده است. طبق Swagger،
متد `SendMultiple` نسخه ۴ در محیط آزمایشی وجود ندارد. هیچ عملیات آزمایشی آزموده نشده است.

## آنچه فعلاً از V4 می‌دانیم

سند Swagger عمومی V4 ارسال پیامک تکی و گروهی، پیام‌های قالبی، OTP پیامکی و صوتی،
استعلام وضعیت و اعتبار، صندوق ورودی، دفترچه تلفن و مدیریت کمپین را توصیف می‌کند.
در V4 بیشتر عملیات‌ها با `POST` و کلید در بدنهٔ JSON تعریف شده‌اند؛ دو متد
ارسال قالب `GET` هم دارند که کلید را در query می‌گیرند. برای محافظت از کلید،
در صورت امکان از `POST` استفاده کنید. متد `GetToken` فهرست قالب‌ها را
می‌دهد و توکن ورود نمی‌سازد. نسبت به `TokenList` نسخه ۳، نام فیلدها camelCase
شده، فیلد `VoiceTemplate` حذف شده و وضعیت قالب ۴ جدا شده است. مقایسه دقیق در
گزارش تطبیق آمده است.

سند Swagger برای عملیات‌های V4 پاسخ‌های `200`، `429` و `default` ثبت می‌کند. این
مقادیر و شکل‌های پاسخ، ادعاهای مستندشده در Swagger هستند و رفتار runtime را
مستقلاً اثبات نمی‌کنند. توصیف V3 نیز اکنون همین کدهای HTTP را ثبت می‌کند؛ خطای
ارتباط یا سرور ممکن است پاکت پاسخ معمول را نداشته باشد.

## آنچه باید درباره پاسخ‌های V3 بدانید

سه اعلان منتشرشده V3 که در هر ادغامی تعیین‌کننده‌اند:

<div dir="rtl">

| رفتار | یعنی چه |
|---|---|
| پاسخ‌های منتشرشده `200` و `429` و `default` هستند | دریافت `200` کافی نیست؛ فیلد `Success` را بخوانید. خطاهای HTTP ممکن است شکل دیگری داشته باشند |
| فیلد `ErrorCode` فقط در شکست معنا دارد | تا `Success` برابر `false` نباشد، خواندنش بی‌معناست |
| کلید در خود درخواست است | در `GET` پارامتر query و در `POST` یک فیلد بدنه، نه یک هدر |

</div>

توصیف V3 شامل ۱۳ عملیات در ۱۱ مسیر است؛ متد تازه `SendTokenSingleConcatParam`
با GET و POST ارائه می‌شود. هدر اختیاری `source-app` برای ثبت نام برنامه است،
نه احراز هویت. متد `TokenList` با درخواست JSON شامل `ApiKey`، فهرست
قالب‌ها را با فیلدهای `Key`، `TextTemplate`، `VoiceTemplate` و `Status` برمی‌گرداند.

جزئیات کامل هر سه اعلان V3 در بخش `info` از
توصیف [`openapi.yaml`](specs/v3/openapi.yaml) آمده است.

## چرا جدول‌های کد V3 جدا از spec

مقادیر `ErrorCode` و `StatusCode` در V3 در دو جا لازم‌اند: به‌عنوان `enum` در
اسکیمای پاسخ، و به‌عنوان جدولِ «این عدد یعنی چه» که مستندات، نمونه‌کدها و سرور MCP نشان
می‌دهند. یکی‌شان بدون دیگری کافی نیست، و نگه داشتن متن فارسی داخل `description`
یک enum عملاً غیرقابل مصرف است.

پس عددهای V3 در spec می‌مانند، متن‌ها در `specs/v3/codes/`، و
برنامه [`scripts/validate.py`](scripts/validate.py) شکست می‌خورد اگر این دو از هم
واگرا شوند.

## پوشش جدول‌های کد V3 و V4

<div dir="rtl">

| جدول | محتوا |
|---|---|
| جدول [خطاهای نسخه ۳](specs/v3/codes/error-codes.yaml) | ۲۰ کد خطا، همراه راهکارهای پیشین و دسته `retry` |
| جدول [تحویل نسخه ۳](specs/v3/codes/status-codes.yaml) | ۲۲ وضعیت پیامک، همراه دسته `disposition` پیشین |
| جدول [قالب‌های نسخه ۳](specs/v3/codes/template-status.yaml) | ۳ وضعیت تأیید قالب |
| جدول [پاسخ‌های HTTP نسخه ۳](specs/v3/codes/http-status.yaml) | پاسخ‌های هر ۱۳ عملیات، جدا از کد خطا و تحویل |
| جدول [پاسخ‌های HTTP نسخه ۴](specs/v4/codes/http-status.yaml) | پاسخ‌های هر ۲۶ عملیات؛ کدهای `200` و `429` و پاسخ `default` |
| جدول [خطاهای نسخه ۴](specs/v4/codes/error-codes.yaml) | ۲۴ کد خطا با متن و نام منتشرشده |
| جدول [تحویل نسخه ۴](specs/v4/codes/status-codes.yaml) | ۲۲ وضعیت پیامک از `0` تا `21` |
| جدول [قالب‌های نسخه ۴](specs/v4/codes/template-status.yaml) | چهار وضعیت، شامل رد قطعی با کد `4` |
| جدول [پیشرفت کمپین](specs/v4/codes/campaign-status.yaml) | شش وضعیت از `0` تا `5` |
| جدول [فیلتر کمپین](specs/v4/codes/campaign-filter-status.yaml) | سه مقدار از `1` تا `3` |
| جدول [گیرندگان کمپین](specs/v4/codes/campaign-recipient-status.yaml) | تعداد ۳۲ وضعیت مستقل از وضعیت تحویل پیامک |

</div>

متن جدول‌ها با Swagger ذخیره‌شده تطبیق داده شده است. راهکارها و مشاهده‌های
پیشین تیم سرویس با سابقه خود نگه داشته شده‌اند؛ در این مرحله با سرویس زنده
دوباره سنجیده نشده‌اند.

دسته `retry` می‌گوید تکرار درخواست فایده دارد یا نه، و `disposition` می‌گوید
حلقه استعلام وضعیت کِی باید بایستد. هر دو برای این‌اند که برنامه بدون حدس زدن
تصمیم بگیرد.

کد HTTP با کد خطای API و وضعیت تحویل یکسان نیست. پاسخ `default` نیز عدد HTTP
نیست؛ شکل خطاهای دیگری را پوشش می‌دهد که سند جداگانه نام نبرده است. نام هدر
زمان تلاش بعدی در پاسخ `429` منتشر نشده است. در جدول‌های V4، سیاست‌های منتشرنشده
با مقدار `null` و توضیح صریح نگه داشته شده‌اند؛ از نسخه ۳ کپی نشده‌اند.
ردیف‌های بررسی‌شده فقط با Swagger، تأیید مستقل سرویس ندارند و هشدار باقی می‌مانند.

## دو نکته که در کد لازم می‌شود

<div dir="rtl">

| نکته | جزئیات |
|---|---|
| نام فیلد فرستنده در `GetInbox` نسخه ۳ | `Form` است، نه `From`. عیناً همین‌طور مستند شده تا کد شما با پاسخ واقعی بخواند |
| وضعیت قالب نسخه ۳ | سند Swagger سه مقدار دارد؛ تفاوت‌های پیشین پنل به‌عنوان شاهد تاریخی در جدول نگه داشته شده است |

</div>

## اعتبارسنجی

دو بررسی مستقل، و هر دو باید سبز باشند.

**بررسی اول: سازگاری spec با جدول کدها**؛ تنها وابستگی `PyYAML` است.

```bash
# بررسی و گزارش
python3 scripts/validate.py
# فهرست شکاف‌ها
python3 scripts/validate.py --gaps
# حالت سخت‌گیرانه؛ هشدار هم شکست حساب می‌شود
python3 scripts/validate.py --strict
```

**بررسی دوم: اعتبار خود OpenAPI**؛ با Docker، بدون نصب چیزی.

```bash
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml specs/v4/openapi.yaml
```

امکان اجرای همین فرمان با Podman نیز هست. پس از دریافت تصویر، از
فرمان `podman run --rm --pull=never --network=none` را با همان مسیر و آرگومان‌ها اجرا کنید.

برای بررسی تطبیق با منبع و همه مثال‌های صریح، PyYAML و jsonschema لازم است:

```bash
python3 scripts/sync_swagger.py v3 --check
python3 scripts/sync_swagger.py v4 --check
python3 scripts/validate_swagger.py v3 v4
python3 scripts/validate_readmes.py
```

سه مثال پاسخ موفق کمپین V4 در Swagger زمان بدون منطقه زمانی دارند و با
قالب `date-time` سازگار نیستند. اصل مثال‌ها در `x-invalid-source-examples` و منبع
ذخیره‌شده باقی است؛ زمان حدسی به‌عنوان مثال معتبر ارائه نشده است.

قواعد خاموش‌شده و دلیلشان در [`redocly.yaml`](redocly.yaml) است.

## مصرف‌کننده‌ها

<div dir="rtl">

| مصرف‌کننده | چه می‌گیرد |
|---|---|
| سایت `docs.payam-resan.com` | صفحات مرجع API و جدول کدها |
| مخزن‌های نمونه‌کد هر زبان | امضای متدها و نام فیلدها |
| سرور MCP | تعریف ابزارها |

</div>

## مستندات و پشتیبانی

راهنمای کامل وب‌سرویس در [docs.payam-resan.com](https://docs.payam-resan.com)
است.

سؤال یا خطایی هست؟ [issue باز کنید](https://github.com/Mojeshahr/sms-webservice-spec/issues)
یا با [پشتیبانی](https://payam-resan.com) تماس بگیرید.

## مجوز

منتشرشده با مجوز MIT. متن کامل در [`LICENSE`](LICENSE).

<br>
<div align="center">
  <sub>
    <img src=".github/assets/logo.svg" width="16" height="16" alt="" align="top">
    &nbsp;<b>پنل پیامکی پیام رسان - موج شهر</b>&nbsp;
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset=".github/assets/mojeshahr-dark.svg">
      <img src=".github/assets/mojeshahr-light.svg" width="16" height="16" alt="" align="top">
    </picture>
  </sub>
  <br>
  <sub>
    <a href="https://payam-resan.com">payam-resan.com</a>
    &nbsp;·&nbsp;
    <a href="https://mojeshahr.ir">mojeshahr.ir</a>
  </sub>
</div>
