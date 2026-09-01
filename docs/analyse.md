# VideoToAnimeAnalyse — Kalıcı Ürün Kararları

Son güncelleme: 2026-09-01  
Durum: Foundation V0.1

Bu belge projenin kalıcı karar kaydıdır. Gelecekteki geliştirmeler bu hedefleri sessizce değiştirmemelidir.

## 1. Temel hedef

Proje, gerçek spor yayınındaki seçilmiş önemli anları **referans** olarak kullanır ve aynı olayı özgün, renkli, temiz 2D limited-anime sahnesi olarak yeniden canlandırır.

Ana hedef tam video-to-video stil dönüşümü değildir. Orijinal görüntünün her pikselini korumak yerine şu bilgiler korunur:

- olay sırası ve sonucu,
- sporcu/top/araç hareketlerinin temel zamanlaması,
- takım ve yön bilgisi,
- gerekli saha/pist geometrisi,
- kritik taktik bağlam.

Hareketler dramatik amaçla değiştirilebilir: gerçek dışı sıçrama, aşırı hız, enerji izi, darbe dalgası, ağır çekim ve dramatik yakın planlar kullanılabilir.

## 2. Kullanıcı iş akışı

1. Kullanıcı uzun yayından önemli anları CapCut ile keser.
2. Genellikle toplam 2–3 dakikalık referans görüntü kalır.
3. Sistem bu görüntüyü 2–8 saniyelik olay ve planlara ayırır.
4. Spor adaptörü oyuncu/nesne hareketini ve olayları çözer.
5. Ortak motor anime storyboard, kamera, hareket abartma ve efekt planını üretir.
6. 2D sahne render edilir; ardından telestration, anlatım, ses ve müzik eklenir.

## 3. Üç üretim seviyesi

Her saniye aynı ayrıntıda yeniden üretilmez.

- **Seviye 1 — Açıklama:** sabit veya hafif hareketli saha, pan/zoom, freeze-frame, telestration.
- **Seviye 2 — Normal oyun:** 2D rig/sprite döngüsü, gerçek izlere bağlı temel hareket, top/nesne yörüngesi.
- **Seviye 3 — Kahraman anı:** özel pozlar, yakın plan, abartılı hareket, impact frame, enerji ve kamera efektleri.

Bu seçim 90'lar televizyon animasyonundaki limited-animation ekonomisini modern ve otomatik bir iş akışına taşır.

## 4. Görsel dil

- Varsayılan çıktı: 16:9, 1920×1080, 24 FPS.
- Varsayılan çizim ritmi: 12 FPS; seçili planlarda 8 veya 24 FPS kullanılabilir.
- Güçlü kontur, temiz cel gölgelendirme, okunabilir takım renkleri ve dramatik perspektif.
- Stil özgün olacaktır. Korunan karakterlerin, logoların veya belirli bir serinin bire bir kopyası hedeflenmez.
- Önemli sporcu kimliği gerekirse forma rengi/numarası, saç silueti ve kontrollü karakter referansı ile korunur.

## 5. Çoklu spor mimarisi

Ortak çekirdek spor bağımsızdır. Her spor kendi adaptörüyle eklenir.

İlk sıra:

1. Futbol
2. Basketbol
3. Boks/MMA
4. Voleybol
5. Tenis
6. Motor sporları

Spor adaptörleri nesne türlerini, olay sözlüğünü, saha geometrisini ve anime efekt reçetelerini tanımlar.

## 6. FootballAnalysisAI ilişkisi

- FootballAnalysisAI mevcut futbol analiz ve telestration projesidir; bu repo onun kopyası değildir.
- İki proje arasında doğrudan Python import bağı kurulmayacaktır.
- Entegrasyon, sürümlü JSON referans paketi üzerinden yapılacaktır.
- FootballAnalysisAI oyuncu/top takibi, olay ve kamera verisini dışarı verir.
- VideoToAnimeAnalyse bu veriyi doğrular, storyboard'a ve anime sahnesine dönüştürür.
- Bu ayrım her iki projenin bağımsız test edilmesini ve farklı spor analizörlerinin bağlanmasını sağlar.

## 7. Donanım ve maliyet

- Temel planlama ve 2D render yolu GTX 1050/CPU ortamında çalışabilmelidir.
- Ağır üretken video modelleri çekirdeğin zorunlu bağımlılığı olmayacaktır.
- Bulut veya güçlü GPU kullanan modeller yalnızca opsiyonel karakter/arka plan üreticileri olabilir.
- Tekrar kullanılabilir karakter rigleri, arka planlar ve efektler üretim maliyetini azaltmalıdır.

## 8. İçerik ve lisans güvenliği

- Kaynak spor görüntüsünü kullanma hakkı kullanıcıya aittir.
- Girdi videoları, model ağırlıkları ve korunan karakter varlıkları repoya konmaz.
- Ticari olmayan model lisansları gelir elde edilen içerik hattına eklenmez.
- Her model, ağırlık ve varlığın kod lisansından ayrı kullanım şartları kontrol edilir.

## 9. V0.1 kabul kriterleri

- Sürümlü referans JSON'u doğrulanabilmeli.
- Futbol `shot`, `pass`, `dribble`, `save` olayları storyboard'a dönüşebilmeli.
- Üç üretim seviyesi plan içinde görünmeli.
- HTML storyboard önizlemesi üretilebilmeli.
- Çekirdek kod üçüncü taraf Python paketi ve GPU olmadan test edilebilmeli.

## 10. Sonraki kilometre taşları

- V0.2: otomatik shot/scene bölme ve FootballAnalysisAI export adaptörü.
- V0.3: SVG/Pillow tabanlı 2D animatic renderer.
- V0.4: oyuncu sprite/rig sistemi ve hareket abartma eğrileri.
- V0.5: efekt, kamera, telestration ve ses kompozisyonu.
- V0.6: basketbol adaptörü.
- V1.0: seçilmiş bir futbol anından uçtan uca 16:9 anime analiz videosu.

