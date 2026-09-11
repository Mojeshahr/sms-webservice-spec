<div align="center">

<a href="https://payam-resan.com">
  <img src=".github/assets/logo.svg" width="64" height="64" alt="پیام رسان">
</a>

<h1>مرجع وب‌سرویس پنل پیامکی پیام رسان</h1>

توصیف ماشین‌خوان رابط برنامه‌نویسی <a href="https://payam-resan.com"><b>پنل پیامکی پیام رسان</b></a><br>
منبع واحدی که مستندات، نمونه‌کدها و سرور MCP از آن مشتق می‌شوند

[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-0a7cbd)](specs/v3/openapi.yaml)
[![API](https://img.shields.io/badge/API-V3-777bb4)](https://payam-resan.com)
[![Lint](https://img.shields.io/badge/redocly-clean-2ea44f)](redocly.yaml)
[![License](https://img.shields.io/badge/license-MIT-6e7781)](LICENSE)

<b>فارسی</b> · <a href="README.en.md">English</a>

</div>

---

این مخزن توصیف رسمی و ماشین‌خوان وب‌سرویس است. مستندات
[`docs.payam-resan.com`](https://docs.payam-resan.com)، نمونه‌کدهای هر زبان و
سرور MCP همگی از همین فایل‌ها مشتق می‌شوند، تا همه‌جا یک جواب واحد به یک پرسش
داده شود.

اگر دنبال راهنمای خواندنی برای انسان هستید، به
[`docs.payam-resan.com`](https://docs.payam-resan.com) بروید. اینجا خودِ توصیف
است، برای ابزارها و تولیدکننده‌های کد.

## چیدمان

```
specs/
└── v3/
    ├── openapi.yaml              توصیف OpenAPI 3.1
    └── codes/
        ├── error-codes.yaml      مقادیر ErrorCode
        ├── status-codes.yaml     مقادیر StatusCode
        └── template-status.yaml  وضعیت تأیید قالب
scripts/
└── validate.py                   spec در برابر جدول‌ها
```

نسخه یک پوشه است، نه یک شاخه و نه یک تگ. نسخه‌های قدیمی‌تر سرویس همچنان فعال‌اند
و باید در کنار نسخه جاری خوانده شوند، پس هر نسخه پوشه خودش را دارد و افزودن یک
نسخه تازه هیچ فایلی را در پوشه‌های موجود تغییر نمی‌دهد.

## آنچه باید درباره پاسخ‌ها بدانید

سه رفتار سرویس که در هر ادغامی تعیین‌کننده‌اند:

<div dir="rtl">

| رفتار | یعنی چه |
|---|---|
| همه پاسخ‌ها `200` هستند | موفقیت از فیلد `Success` خوانده می‌شود، نه از کد وضعیت HTTP |
| `ErrorCode` فقط در شکست معنا دارد | تا `Success` برابر `false` نباشد، خواندنش بی‌معناست |
| کلید در خود درخواست است | در `GET` پارامتر query و در `POST` یک فیلد بدنه، نه یک هدر |

</div>

جزئیات کامل هر سه در توصیف `info` فایل [`openapi.yaml`](specs/v3/openapi.yaml)
آمده است.

## چرا کدها جدا از spec

مقادیر `ErrorCode` و `StatusCode` در دو جا لازم‌اند: به‌عنوان `enum` در اسکیمای
پاسخ، و به‌عنوان جدولِ «این عدد یعنی چه» که مستندات، نمونه‌کدها و سرور MCP نشان
می‌دهند. یکی‌شان بدون دیگری کافی نیست، و نگه داشتن متن فارسی داخل `description`
یک enum عملاً غیرقابل مصرف است.

پس عددها در spec می‌مانند، متن‌ها در `codes/`، و
[`scripts/validate.py`](scripts/validate.py) شکست می‌خورد اگر این دو از هم
واگرا شوند.

## پوشش

<div dir="rtl">

| جدول | محتوا |
|---|---|
| [`error-codes.yaml`](specs/v3/codes/error-codes.yaml) | ۲۰ کد خطا، هر کدام با علت، راهکار و دسته `retry` |
| [`status-codes.yaml`](specs/v3/codes/status-codes.yaml) | ۲۲ وضعیت پیامک، از `0` تا `21`، هر کدام با `disposition` |
| [`template-status.yaml`](specs/v3/codes/template-status.yaml) | ۳ وضعیت تأیید قالب |

</div>

دسته `retry` می‌گوید تکرار درخواست فایده دارد یا نه، و `disposition` می‌گوید
حلقه استعلام وضعیت کِی باید بایستد. هر دو برای این‌اند که برنامه بدون حدس زدن
تصمیم بگیرد.

## دو نکته که در کد لازم می‌شود

<div dir="rtl">

| نکته | جزئیات |
|---|---|
| نام فیلد فرستنده در `GetInbox` | `Form` است، نه `From`. عیناً همین‌طور مستند شده تا کد شما با پاسخ واقعی بخواند |
| وضعیت قالب | پنل کاربری چهار حالت نشان می‌دهد و بین دو نوع رد شدن فرق می‌گذارد، ولی API برای هر دو `3` برمی‌گرداند |

</div>

## اعتبارسنجی

دو بررسی مستقل، و هر دو باید سبز باشند.

**۱. سازگاری spec با جدول کدها**؛ تنها وابستگی `PyYAML` است.

```bash
python3 scripts/validate.py            # بررسی و گزارش
python3 scripts/validate.py --gaps     # فقط فهرست شکاف‌ها
python3 scripts/validate.py --strict   # هشدار هم شکست حساب می‌شود
```

**۲. اعتبار خود OpenAPI**؛ با Docker، بدون نصب چیزی.

```bash
docker run --rm -v "$PWD":/spec -w /spec redocly/cli lint specs/v3/openapi.yaml
```

قواعد خاموش‌شده و دلیلشان در [`redocly.yaml`](redocly.yaml) است.

## مصرف‌کننده‌ها

<div dir="rtl">

| مصرف‌کننده | چه می‌گیرد |
|---|---|
| `docs.payam-resan.com` | صفحات مرجع API و جدول کدها |
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
