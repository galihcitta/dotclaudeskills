# UI Copy Patterns

Extract and structure user-facing text into bilingual tables (Indonesian + English).

## Contents
- [Extraction Rules](#extraction-rules)
- [Standard Table Formats](#standard-table-formats)
- [Example: Full Extraction](#example-full-extraction)
- [Best Practices](#best-practices)

## Why Structure UI Copy Separately

1. **Clarity** — Keeps business logic clean, UI text in one place
2. **Translation** — Easy to review/update translations
3. **Consistency** — Reusable error messages across features
4. **Handoff** — Clear for frontend implementation

---

## Extraction Rules

1. Scan PRD for all user-facing text (buttons, messages, labels, errors)
2. Group by screen/component
3. Create unique keys for each string
4. Separate success messages, error messages, and UI labels

---

## Standard Table Formats

### Screen/Component Labels
```markdown
### [Screen Name]
| Key | Indonesian | English |
|-----|------------|---------|
| title | Verifikasi Nomor HP | Phone Number Verification |
| description | Anda perlu melakukan... | You need to verify... |
| button_primary | Verifikasi via Whatsapp | Verify via WhatsApp |
| button_secondary | Batalkan | Cancel |
```

### Success Messages
```markdown
### Success Messages
| Key | Indonesian | English |
|-----|------------|---------|
| verification_success | Nomor HP Anda berhasil diverifikasi | Your phone number has been verified |
| pin_created | PIN berhasil dibuat | PIN created successfully |
```

### Error Messages
Map to error codes for consistency:

```markdown
### Error Messages
| Code | Indonesian | English |
|------|------------|---------|
| PHONE_MISMATCH | Nomor HP WhatsApp Anda berbeda dengan nomor HP yang mendapatkan voucher | The WhatsApp phone number does not match the one that received the voucher |
| SESSION_EXPIRED | Sesi verifikasi telah berakhir. Silakan coba lagi | Verification session has expired. Please try again |
| PIN_INVALID | PIN yang Anda masukkan salah | The PIN you entered is incorrect |
| ACCOUNT_LOCKED | Akun terkunci selama 30 menit | Account locked for 30 minutes |
| GENERIC_ERROR | Terjadi kesalahan. Silakan coba lagi | An error occurred. Please try again |
```

### System Messages (WhatsApp/SMS)
```markdown
### WhatsApp Messages
| Key | Indonesian | English |
|-----|------------|---------|
| wa_verification_prompt | Kirim pesan ini tanpa mengubah isi pesan untuk proses verifikasi... | Send this message without changing its content for verification... |
| wa_success | Nomor HP Anda berhasil diverifikasi. Klik tombol dibawah ini... | Your phone number has been verified. Click the button below... |
| wa_mismatch | Nomor HP WhatsApp Anda berbeda dengan... | The WhatsApp phone number you provided does not match... |
| wa_error | Kami tidak dapat menyelesaikan permintaan Anda... | We couldn't complete your request... |
```

---

## Example: Full Extraction

**From raw PRD:**
```
Text:
ID: 
Verifikasi Nomor HP
Anda perlu melakukan verifikasi nomor HP melalui Whatsapp...
Button: Verifikasi via Whatsapp

EN:
Phone Number Verification
You need to verify your phone number via WhatsApp...
Button: Verify via Whatsapp
```

**Structured output:**
```markdown
## UI Copy (Bilingual)

### Verification Screen
| Key | Indonesian | English |
|-----|------------|---------|
| title | Verifikasi Nomor HP | Phone Number Verification |
| description | Anda perlu melakukan verifikasi nomor HP melalui Whatsapp untuk mengakses voucher ini. Pastikan Anda memiliki aplikasi Whatsapp dan nomor HP whatsapp yang Anda gunakan sama nomor HP yang menerima voucher link ini. | You need to verify your phone number via WhatsApp to access your voucher. Please ensure that you have the WhatsApp app installed and that the phone number used for WhatsApp matches the phone number that received the voucher link. |
| button_verify | Verifikasi via Whatsapp | Verify via WhatsApp |

### WhatsApp Chatbot
| Key | Indonesian | English |
|-----|------------|---------|
| prompt | Kirim pesan ini tanpa mengubah isi pesan untuk proses verifikasi. Pastikan Anda menggunakan akun WhatsApp yang memiliki nomor HP yang sama dengan nomor HP yang menerima voucher link tersebut. [masking eGift code xxxxxxxxxxxxxxxxx] | Send this message without changing its content for verification. Ensure you are using the WhatsApp account with the same phone number that received the voucher link. [masking eGift code xxxxxxxxxxxxxxxxx] |
| success | Nomor HP Anda berhasil diverifikasi. Klik tombol dibawah ini untuk mengakses voucher Anda. Tombol hanya berlaku selama 10 menit. | Your phone number has been successfully verified. Click the button below to access your voucher. The button is valid for 10 minutes. |

### Error Messages
| Code | Indonesian | English |
|------|------------|---------|
| PHONE_MISMATCH | Nomor HP WhatsApp Anda berbeda dengan nomor HP yang mendapatkan voucher link tersebut. Silakan menggunakan akun WhatsApp dengan nomor HP yang sama dengan nomor HP yang mendapatkan voucher link tersebut. | The WhatsApp phone number you provided does not match the one that received the voucher link. Please use the WhatsApp account associated with the phone number that received the voucher link. |
| SYSTEM_ERROR | Kami tidak dapat menyelesaikan permintaan Anda. Kendala ada pada kami, bukan pada Anda. Silakan copy pesan sebelumnya dan kirim kembali. | We couldn't complete your request. It's us, not you. Please copy the previous message and resend it. |
| UNEXPECTED_MESSAGE | Pesan yang Anda kirimkan tidak sesuai. WhatsApp ini hanya untuk verifikasi nomor HP untuk mengakses voucher link Anda. Untuk pertanyaan lain, mohon hubungi kami melalui https://wa.me/6281315007070 | The message you sent is unexpected. This WhatsApp is only for phone number verification to access your voucher link. For other questions, please contact us through https://wa.me/6281315007070 |
```

---

## Best Practices

1. **Use descriptive keys** — `button_verify` not `btn1`
2. **Keep translations parallel** — Same meaning, localized phrasing
3. **Group by context** — Screen, component, or feature area
4. **Error codes match API** — `PHONE_MISMATCH` in API = same in UI
5. **Include placeholders** — Note dynamic values: `{minutes}`, `{phone}`
6. **Flag long strings** — Mark if text might overflow UI containers

```markdown
| Key | Indonesian | English | Notes |
|-----|------------|---------|-------|
| description | [long text] | [long text] | ⚠️ May need truncation on mobile |
```
