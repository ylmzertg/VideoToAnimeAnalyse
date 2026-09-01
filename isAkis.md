# Codex ve GitHub Remote Çalışma Akışı

Son güncelleme: 2026-09-01  
Proje: `ylmzertg/VideoToAnimeAnalyse`  
Ana dal: `main`

Bu belge, VideoToAnimeAnalyse projesinin Codex Cloud üzerinden GitHub'a bağlanması, yeni bir çalışma ortamının hazırlanması ve geliştirmelerin güvenli biçimde GitHub'a aktarılması için kalıcı operasyon rehberidir.

## 1. Bilgi ve talimat hiyerarşisi

Yeni bir Codex oturumu eski sohbetleri otomatik olarak bilmez. Çalışmaya başlamadan önce aşağıdaki dosyalar bu sırayla okunmalıdır:

1. `AGENTS.md` — zorunlu çalışma ve test kuralları.
2. `docs/analyse.md` — kalıcı ürün kararlarının ana kaynağı.
3. `docs/architecture.md` — sistem katmanları ve bağımlılık yönleri.
4. `docs/integration-contract.md` — FootballAnalysisAI ile veri alışverişi sözleşmesi.
5. `README.md` — kurulum, komutlar ve mevcut özellikler.
6. `isAkis.md` — Codex/GitHub bağlantısı ve günlük geliştirme süreci.

Bir belgede çelişki görülürse ürün hedefleri için `docs/analyse.md`, kodlama ve doğrulama kuralları için `AGENTS.md` esas alınır. Belirsizlik çözülmeden kalıcı mimari karar değiştirilmemelidir.

## 2. Codex Cloud ile GitHub'ı ilk kez bağlama

1. [Codex Cloud](https://chatgpt.com/codex) açılır ve proje sahibinin ChatGPT hesabıyla oturum açılır.
2. Codex ayarlarından **Environments** bölümü açılır ve **Create environment** seçilir.
3. GitHub bağlantısı henüz kurulmadıysa **Connect GitHub** seçilir.
4. GitHub yetkilendirme ekranında `ylmzertg` hesabı seçilir.
5. Mümkünse **Only select repositories** seçeneği kullanılır.
6. Yalnızca `ylmzertg/VideoToAnimeAnalyse` reposuna erişim verilir.
7. Yetkilendirme tamamlandıktan sonra Codex'e dönülür.

GitHub parolası, Personal Access Token, SSH özel anahtarı veya başka bir gizli bilgi sohbete ya da repo dosyalarına yazılmaz. GitHub erişimi yalnızca GitHub'ın yetkilendirme ekranından verilir.

## 3. VideoToAnimeAnalyse ortamını oluşturma

Yeni environment için aşağıdaki değerler kullanılır:

| Ayar | Değer |
|---|---|
| Environment adı | `VideoToAnimeAnalyse` |
| Repository | `ylmzertg/VideoToAnimeAnalyse` |
| Başlangıç/base dalı | `main` |
| Python | 3.10 veya üzeri; CI uyumu için tercihen 3.12 |
| Setup komutu | `python -m pip install -e .` |
| Test komutu | `python -m unittest discover -s tests -v` |

Setup script:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Bu kilometre taşında GPU, model ağırlığı veya ücretli servis anahtarı gerekli değildir. `ffprobe` yalnızca gerçek klipten metadata çıkaran `probe` komutu kullanılacaksa gerekir.

## 4. İlk Codex görevi

Environment oluşturulduktan sonra `VideoToAnimeAnalyse` ortamı seçilir ve ilk mesaj olarak şu başlangıç talimatı kullanılabilir:

```text
Önce AGENTS.md, docs/analyse.md, docs/architecture.md,
docs/integration-contract.md, README.md ve isAkis.md dosyalarını tamamen oku.
Mevcut kodu değiştirmeden önce testleri çalıştır ve projenin mevcut durumunu doğrula.
Ardından istenen görevi kalıcı ürün kararlarına ve mimari sınırlara uygun biçimde uygula.
```

Codex ortamı seçilen dalı veya commit'i izole bir konteynere alır, setup scriptini çalıştırır ve ardından görev üzerinde çalışır. Bu nedenle her yeni görevde doğru environment ve base dalının seçildiği kontrol edilmelidir.

## 5. Günlük geliştirme akışı

Her geliştirme için aşağıdaki sıra izlenir:

1. GitHub'daki `main` dalının güncel olduğu doğrulanır.
2. Codex'te `VideoToAnimeAnalyse` environment'ı ve `main` base dalı seçilir.
3. Görev tek ve doğrulanabilir bir sonuç şeklinde tarif edilir.
4. Codex önce ilgili dokümanları ve mevcut testleri inceler.
5. Değişiklik yalnızca görev kapsamındaki dosyalara uygulanır.
6. Yeni davranış için test eklenir veya mevcut testler güncellenir.
7. Tüm testler çalıştırılır:

   ```bash
   python -m unittest discover -s tests -v
   ```

8. Codex'in sunduğu özet ve diff incelenir.
9. Değişiklik ayrı bir dal ve pull request üzerinden GitHub'a gönderilir; doğrudan `main` güncellemesi özellikle istenmedikçe tercih edilmez.
10. Pull request birleştirildikten sonra `main` HEAD'i ve GitHub Actions sonucu doğrulanır.
11. Kilometre taşı veya kalıcı karar değiştiyse `docs/analyse.md`, mimari değiştiyse `docs/architecture.md` aynı çalışma içinde güncellenir.

## 6. Görev tamamlama kontrol listesi

Bir iş tamamlandı sayılmadan önce şunlar doğrulanmalıdır:

- İstenen davranış uygulanmış olmalı.
- Projenin spor bağımsız çekirdeği korunmalı.
- FootballAnalysisAI ile doğrudan Python bağımlılığı oluşturulmamalı.
- GPU gerektirmeyen temel yol çalışmaya devam etmeli.
- Kaynak maç videosu, üretilmiş video, model ağırlığı, kimlik bilgisi veya telifli karakter varlığı commit edilmemeli.
- İlgili testler eklenmiş veya güncellenmiş olmalı.
- `python -m unittest discover -s tests -v` başarılı olmalı.
- Değişen kalıcı kararlar dokümantasyona yansıtılmalı.
- Uzak commit/PR ve GitHub Actions sonucu kontrol edilmeli.

## 7. Repo Codex'te görünmüyorsa

1. GitHub'da **Settings → Applications** açılır.
2. **Installed GitHub Apps** veya yetkilendirilmiş uygulamalar bölümünde Codex/OpenAI bağlantısı bulunur.
3. **Configure** seçilir.
4. `VideoToAnimeAnalyse` reposunun erişim listesinde bulunduğu kontrol edilir.
5. Codex **Settings → Environments** sayfası yenilenir.

Repo hâlâ görünmüyorsa şunlar kontrol edilir:

- Codex ve GitHub'da doğru hesapla oturum açılmış olması.
- Kullanıcının repoda gerekli erişim yetkisine sahip olması.
- Workspace yöneticisinin Codex Cloud veya GitHub bağlantısını engellememiş olması.
- Repo erişiminin yalnızca başka bir GitHub organizasyonuna verilmemiş olması.

## 8. Environment kurulumu başarısız olursa

Önce Python sürümü kontrol edilir:

```bash
python --version
```

Ardından kurulum ve testler yeniden çalıştırılır:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

Eski environment önbelleği sorun çıkarıyorsa Codex environment sayfasındaki **Reset cache** işlemi kullanılır. İnternet erişimi setup aşamasında paket kurulumu için kullanılabilir; agent aşamasındaki internet erişimi varsayılan olarak kapalı olabilir.

## 9. Yerel bilgisayarda çalışma alternatifi

Codex Cloud yerine Windows bilgisayarda yerel çalışılacaksa repo önce klonlanır:

```powershell
git clone https://github.com/ylmzertg/VideoToAnimeAnalyse.git
cd VideoToAnimeAnalyse
git switch main
git pull --ff-only origin main
```

Remote bağlantısı şu komutla doğrulanır:

```powershell
git remote -v
```

Beklenen remote:

```text
origin  https://github.com/ylmzertg/VideoToAnimeAnalyse.git (fetch)
origin  https://github.com/ylmzertg/VideoToAnimeAnalyse.git (push)
```

Yerel Codex/CLI doğrudan bu klasörde çalıştırılır. Bu kullanımda GitHub bağlantısını Codex değil, klasördeki Git `origin` remote'u ve bilgisayarın güvenli GitHub oturumu yönetir.

## 10. Resmî kaynaklar

- [Codex Cloud kurulumu](https://learn.chatgpt.com/docs/cloud)
- [Codex Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environment)
- [Codex ile GitHub pull request inceleme](https://learn.chatgpt.com/docs/third-party/github)

Codex arayüzü zamanla değişebileceğinden menü adları farklı görünürse resmî OpenAI dokümantasyonu kontrol edilir ve bu belge güncellenir.
