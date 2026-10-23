# JSON-Web-Token
# JWT autentimise API

## Projekti kirjeldus

Selles projektis on loodud Pythonil põhinev REST API, mis kasutab Flaski ja PyJWT teeke JWT-põhiseks autentimiseks ning rollipõhiseks ligipääsu kontrollimiseks.

Rakenduses on kolm lõpp-punkti: `/login`, `/profiil` ja `/admin`.

## Kasutatud tehnoloogiad

- Python
- Flask
- PyJWT
- JWT (JSON Web Token)
- HS256 algoritm
- Postman API testimiseks

## Funktsionaalsus

### 1. POST `/login`

Kontrollib kasutajanime ja parooli.

Õigete andmete korral tagastab JWT tokeni, mis sisaldab järgmisi välju:

- `sub` – kasutaja nimi
- `role` – kasutaja roll
- `iat` – tokeni väljastamise aeg
- `exp` – tokeni aegumisaeg

Token kehtib 5 minutit.

Vale kasutajanime või parooli korral tagastatakse HTTP `401 Unauthorized`.

### 2. GET `/profiil`

Kontrollib JWT tokeni kehtivust ja tagastab tokeni andmed.

- Kehtiv token: `200 OK`
- Puuduv, vigane või aegunud token: `401 Unauthorized`

Token tuleb saata päringu päises:

`Authorization: Bearer YOUR_TOKEN`

### 3. GET `/admin`

Kontrollib, kas tokenis oleva kasutaja roll on `admin`.

- Administraatori roll: `200 OK`
- Kehtiv token, kuid ebapiisavad õigused: `403 Forbidden`
- Puuduv või vigane token: `401 Unauthorized`

## Testkasutajad

| Kasutajanimi | Parool | Roll |
|---|---|---|
| `student` | `student123` | `student` |
| `admin` | `admin123` | `admin` |

Need kasutajad on mõeldud ainult õppeprojekti testimiseks.

## Paigaldamine

### 1. Repositooriumi kloonimine

```bash
git clone https://github.com/melon3000/JSON-Web-Token
cd jwt-project
```

Asenda `https://github.com/melon3000/JSON-Web-Token` enda GitHubi repositooriumi aadressiga.

### 2. Sõltuvuste paigaldamine

```bash
pip install -r requirements.txt
```

Kui `requirements.txt` faili pole, saab teegid paigaldada käsuga:

```bash
pip install Flask PyJWT
```

## Keskkonnamuutuja seadistamine

Salavõti loetakse keskkonnamuutujast `JWT_SECRET`. Seda ei salvestata otse lähtekoodi.

**Windows PowerShell:**

```powershell
$env:JWT_SECRET = "asenda-tugeva-salajase-votmega"
```

**Linux / macOS:**

```bash
export JWT_SECRET="asenda-tugeva-salajase-votmega"
```

## Rakenduse käivitamine

Käivita projekti kaustas käsk:

```bash
python app.py
```

Vaikimisi on API aadressil:

`http://127.0.0.1:5000`

## API testimine Postmaniga

### Sisselogimine

- Meetod: `POST`
- URL: `http://127.0.0.1:5000/login`
- Body → raw → JSON

```json
{
  "username": "student",
  "password": "student123"
}
```

Eduka päringu korral tagastatakse JWT token.

### Profiili päring

- Meetod: `GET`
- URL: `http://127.0.0.1:5000/profiil`
- Authorization → Bearer Token

Sisesta sisselogimisel saadud token.

### Administraatori päring

- Meetod: `GET`
- URL: `http://127.0.0.1:5000/admin`
- Authorization → Bearer Token

Administraatori tokeniga peab päring õnnestuma. `student` rolliga tokeniga peab vastus olema `403 Forbidden`.

## Turvalisus

- Salavõti loetakse keskkonnamuutujast.
- Server lubab ainult HS256 algoritmi.
- Token kehtib 5 minutit.
- Puuduva või vigase tokeni korral tagastatakse `401`.
- Ebapiisavate õiguste korral tagastatakse `403`.

**Märkus:** kasutajate paroolid on selles õppeprojektis lihtsuse huvides koodis näidisandmetena. Päris rakenduses tuleks paroole turvaliselt räsida.

## Testide tulemused

API-d testiti Postmaniga. Testjuhtumite oodatavad ja tegelikud HTTP staatuskoodid, tulemused ning ekraanipildid on dokumenteeritud Notioni andmebaasis `JWT testjuhud`.
