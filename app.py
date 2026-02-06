import streamlit as st
import random
import json
import time
import hashlib
import hmac
import base64
import re

# Sayfa Yapısı
st.set_page_config(page_title="MC MEB Yurt Dışı", page_icon="📚", layout="centered")

# --- VERİLERİ ÖNBELLEĞE ALMA VE YÜKLEME ---
@st.cache_data
def load_questions():
    try:
        with open('mc_soru_bankasi.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

# --- GÖMÜLÜ VERİLER (DOSYA HATALARINI ÖNLEMEK İÇİN) ---
AI_QUESTIONS_DATA = [
    {
        "q": "YAPAY ZEKA (GÜNCEL): 2024 yılında Avrupa Birliği'nin kabul ettiği dünyadaki ilk kapsamlı yapay zeka yasası hangisidir?",
        "a": "AI Act (Yapay Zeka Yasası).",
        "key": "AI Act",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): Anayasa'nın 42. maddesine göre hürriyetlerin kötüye kullanılamayacağı temel ilke nedir?",
        "a": "Eğitim ve Öğrenim Hakkı.",
        "key": "Eğitim Hakkı",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Osmanlı Devleti'nde ilk dış borçlanma hangi savaş sırasında yapılmıştır?",
        "a": "Kırım Savaşı (1853-1856).",
        "key": "Kırım Savaşı",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): Çoklu Zeka Kuramı'na göre 'doğa zekası' yüksek olan bir öğrenci için en uygun öğretim yöntemi nedir?",
        "a": "Gözlem gezileri ve sınıf dışı etkinlikler.",
        "key": "Doğa / Gözlem",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Resmi bir araçta protokol sırasına göre '2 numaralı makam' neresidir?",
        "a": "Makam sahibinin sol arka tarafı.",
        "key": "Sol Arka",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): Türkiye'nin yerli ve milli ilk insanlı savaş uçağının adı nedir?",
        "a": "KAAN.",
        "key": "KAAN",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 1 sayılı Cumhurbaşkanlığı Kararnamesi ile MEB teşkilat yapısında 'Talim ve Terbiye Kurulu'nun statüsü nedir?",
        "a": "Doğrudan Bakana bağlı bir danışma ve karar organıdır.",
        "key": "Bakana Bağlı",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Türkiye'nin NATO'ya üye olduğu yıl hangisidir?",
        "a": "1952.",
        "key": "1952",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): Öğrencinin hazırbulunuşluk düzeyine göre öğretimin zorluk derecesinin ayarlanması hangi ilkedir?",
        "a": "Düzeye Uygunluk (Göre'lik).",
        "key": "Düzeye Uygunluk",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Bayrak Kanunu'na göre Türk Bayrağı yırtık, sökük veya rengi solmuş şekilde asılabilir mi?",
        "a": "Hayır, manevi değeri zedeleyecek şekilde kullanılamaz.",
        "key": "Yasak",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): 2024 Yaz Olimpiyatları hangi şehirde düzenlenmiştir?",
        "a": "Paris.",
        "key": "Paris 2024",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 657 DMK'ya göre 'Müsteşar' unvanı kaldırıldıktan sonra bakanlıkta en üst idari amir kimdir?",
        "a": "Bakan Yardımcısı (İdari olarak en üst memur statüsü değişmiştir, ancak hiyerarşide Bakan'dan sonra gelir).",
        "key": "Bakan Yrd",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Hatay'ın anavatana katılması hangi yıl gerçekleşmiştir?",
        "a": "1939.",
        "key": "1939",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): Bilişsel Çıraklık yönteminde öğretmenin desteğini yavaş yavaş çekmesi sürecine ne denir?",
        "a": "Bilişsel Destek (Scaffolding) / İskele Kurma.",
        "key": "İskele Kurma",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Resmi yemeklerde ev sahibinin (davet sahibinin) eşi masada nereye oturur?",
        "a": "Davet sahibinin tam karşısına.",
        "key": "Tam Karşı",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (GENEL KÜLTÜR): 'Düşünüyorum, öyleyse varım' sözü kime aittir?",
        "a": "Descartes.",
        "key": "Descartes",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 222 Sayılı İlköğretim Kanunu'na göre mecburi ilköğretim çağı hangi yaş grubunu kapsar?",
        "a": "6-14 yaş.",
        "key": "6-14 Yaş",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (TARİH): UNESCO Dünya Mirası Listesi'nde yer alan 'Göbeklitepe' hangi ilimizdedir?",
        "a": "Şanlıurfa.",
        "key": "Şanlıurfa",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): Eğitimde 'Tam Öğrenme Modeli'nin (Bloom) temel varsayımı nedir?",
        "a": "Uygun koşullar sağlanırsa herkes her şeyi öğrenebilir.",
        "key": "Herkes Öğrenir",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Makam odasına girildiğinde oturulacak yer neresidir?",
        "a": "Makam sahibinin işaret ettiği veya masanın önündeki koltuklar.",
        "key": "İşaret Edilen",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 657 DMK - Hediye alma yasağının kapsamını hangi kurul belirler?",
        "a": "Kamu Görevlileri Etik Kurulu.",
        "key": "Etik Kurulu",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): 'Kürk Mantolu Madonna' eserinin yazarı kimdir?",
        "a": "Sabahattin Ali.",
        "key": "Sabahattin Ali",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Mustafa Kemal'e 'Gazilik' unvanı ve 'Mareşallik' rütbesi hangi savaştan sonra verilmiştir?",
        "a": "Sakarya Meydan Muharebesi.",
        "key": "Sakarya",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Resmi yazılarda 'Arz ederim' ifadesi kime karşı kullanılır?",
        "a": "Üst makama veya denk makama (nezaketen) yazarken.",
        "key": "Üst/Denk",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): 'Öğrenilmiş Çaresizlik' kavramı kime aittir?",
        "a": "Seligman.",
        "key": "Seligman",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 1739 Sayılı Kanun'a göre Türk Milli Eğitimi'nin genel amaçlarından biri 'İyi bir ... yetiştirmektir'?",
        "a": "Vatandaş.",
        "key": "Vatandaş",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): 2023 yılında UNESCO Dünya Mirası Listesi'ne giren 'Gordion' antik kenti nerededir?",
        "a": "Ankara (Polatlı).",
        "key": "Ankara",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Osmanlı'da 'Mebusan Meclisi'nin açılmasını sağlayan gelişme?",
        "a": "I. Meşrutiyet'in ilanı (1876).",
        "key": "I. Meşrutiyet",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Kravatın ucu nerede bitmelidir?",
        "a": "Kemer tokasının yarısını kapatacak şekilde.",
        "key": "Kemer Tokası",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): Yurt dışı sürekli görev süresi kural olarak kaç yıldır?",
        "a": "3 Yıl.",
        "key": "3 Yıl",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): Türkiye'nin insanlı ilk uzay misyonunu gerçekleştiren astronot?",
        "a": "Alper Gezeravcı.",
        "key": "Alper Gezeravcı",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): Maslow'un İhtiyaçlar Hiyerarşisi'nde en tabanda ne vardır?",
        "a": "Fizyolojik İhtiyaçlar.",
        "key": "Fizyolojik",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Lozan Barış Antlaşması'nı TBMM adına kim imzalamıştır?",
        "a": "İsmet İnönü.",
        "key": "İsmet İnönü",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 4982 Bilgi Edinme Kanunu'na göre, bilgi edinme istemi reddedilen kişi nereye itiraz eder?",
        "a": "Bilgi Edinme Değerlendirme Kurulu (BEDK).",
        "key": "BEDK",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): Dünyanın 'sıfır noktası' olarak kabul edilen Göbeklitepe hangi dindedir?",
        "a": "Herhangi bir dinle ilişkilendirilmemiştir (Tarih öncesi inanç merkezi).",
        "key": "Tarih Öncesi",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Resmi araçta 'Makam Forsu' ne zaman çekilir?",
        "a": "Makam sahibi araçta iken.",
        "key": "Araçta İken",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): Eğitimde 'Sarmal Programlama' yaklaşımı (Bruner) neyi ifade eder?",
        "a": "Konuların yıllar içinde genişleyerek ve derinleşerek tekrar edilmesi.",
        "key": "Sarmal / Tekrar",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 657 DMK - Memurluktan çekilenler (istifa) kaç ay sonra dönebilir?",
        "a": "6 Ay sonra.",
        "key": "6 Ay",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Mondros Ateşkes Antlaşması'nı Osmanlı adına kim imzalamıştır?",
        "a": "Rauf Orbay.",
        "key": "Rauf Orbay",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): 'Yüzyılın Felaketi' olarak adlandırılan 6 Şubat depremlerinin merkezi olan iller?",
        "a": "Kahramanmaraş (Pazarcık ve Elbistan).",
        "key": "Kahramanmaraş",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Törenlerde İstiklal Marşı okunurken nasıl durulur?",
        "a": "Hazırol duruşunda, cepheye dönerek ve hareket etmeden.",
        "key": "Hazırol",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): 5018 SK - Üst yöneticiler (Bakanlar vb.) bütçe kullanımıyla ilgili kime hesap verir?",
        "a": "Cumhurbaşkanına.",
        "key": "Cumhurbaşkanı",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): 'Gizil Öğrenme' (Tolman) nedir?",
        "a": "Farkında olmadan, amaçsızca gerçekleşen öğrenme.",
        "key": "Gizil / Farkında Olmadan",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (TARİH): Atatürk'ün 'Benim şahsi meselemdir' dediği konu?",
        "a": "Hatay Sorunu.",
        "key": "Hatay",
        "cat": "Tarih"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): Türkiye'nin ilk yerli gözlem uydusu?",
        "a": "RASAT (veya İMECE).",
        "key": "RASAT/İMECE",
        "cat": "Güncel"
    },
    {
        "q": "YAPAY ZEKA (MEVZUAT): Okul Aile Birlikleri hangi yönetmeliğe göre kurulur?",
        "a": "MEB Okul-Aile Birliği Yönetmeliği.",
        "key": "OAB Yönetmeliği",
        "cat": "Mevzuat"
    },
    {
        "q": "YAPAY ZEKA (PEDAGOJİ): 'Balık Kılçığı' (Ishikawa) diyagramı ne için kullanılır?",
        "a": "Neden-Sonuç ilişkilerini belirlemek için.",
        "key": "Neden-Sonuç",
        "cat": "Pedagoji"
    },
    {
        "q": "YAPAY ZEKA (PROTOKOL): Resmi yazılarda imza, ismin neresine atılır?",
        "a": "İsmin üzerine.",
        "key": "İsim Üstü",
        "cat": "Protokol"
    },
    {
        "q": "YAPAY ZEKA (GÜNCEL): İklim değişikliği ile mücadele eden 'Greta Thunberg' hangi ülkedendir?",
        "a": "İsveç.",
        "key": "İsveç",
        "cat": "Güncel"
    }
]

HAP_BILGILER_DATA = [
    "Mustafa Kemal'in askeri eğitim gördüğü şehirler: Manastır (Askerî İdadi) ve İstanbul (Harp Okulu/Akademisi).",
    "Mustafa Kemal'in ataşemiliterlik yaptığı şehir: Sofya.",
    "Mustafa Kemal'e 'Gazi' unvanı ve 'Mareşal' rütbesi verilen savaş: Sakarya Meydan Muharebesi.",
    "I. Dünya Savaşı'nı bitiren ve Bulgaristan ile imzalanan antlaşma: Nöyyi Antlaşması.",
    "Pozantı Kongresi'ni düzenleyen cemiyet: Kilikyalılar Cemiyeti.",
    "Milli Mücadele'de İtalyanların Anadolu'dan tamamen çekildiği savaş: Sakarya Meydan Muharebesi sonu (ve Büyük Taarruz süreci).",
    "Denizcilik alanındaki millileştirme kanunu: Kabotaj Kanunu.",
    "Orta Asya'dan Avrupa'ya göç etmeyen Türk topluluğu: Uygurlar.",
    "Türkiye Selçuklu başkentinin İznik'ten Konya'ya taşınma sebebi: I. Haçlı Seferi.",
    "Miryokefalon Savaşı'nı kazanan sultan: II. Kılıç Arslan.",
    "Kanuni Sultan Süleyman döneminde olmayan gelişme: Kıbrıs'ın Fethi (II. Selim dönemidir).",
    "Osmanlı'nın Avrupa devletler hukukundan yararlanma hakkı kazandığı antlaşma: Paris Antlaşması (1856).",
    "Halifelerin Türk hükümdarlarına gönderdiği hakimiyet sembolü elbise: Hilat.",
    "Sahn-ı Seman Medresesi'ni açan padişah: Fatih Sultan Mehmet.",
    "Şura-yı Devlet'in günümüzdeki karşılığı: Danıştay.",
    "Tevhid-i Tedrisat Kanunu'nun ilgili olduğu alan: Eğitim.",
    "Doğu Roma İmparatorluğu'nu ortadan kaldıran padişah: II. Mehmet (Fatih).",
    "Osmanlı ile Safeviler arasındaki antlaşmalardan biri olmayan: Zitvatorok (Avusturya ile yapılmıştır).",
    "'93 Harbi' olarak bilinen savaş: 1877-1878 Osmanlı-Rus Savaşı.",
    "Türklerde ilk düzenli orduyu kuran: Mete Han.",
    "Nizamülmülk'ün eseri: Siyasetname.",
    "Büyük Selçuklu'da belediye işlerine bakan görevli: Muhtesip.",
    "Osmanlı'da 'Ekber ve Erşed' sistemine geçen padişah: I. Ahmet.",
    "Çocuk Hizmetleri Genel Müdürlüğü'nün temelini oluşturan kurum: Himaye-i Etfal Cemiyeti.",
    "Mustafa Kemal'in 'Müdafaa-i Hukuk Grubu' yerine kurulan grup: Felah-ı Vatan Grubu.",
    "Sakarya Savaşı'nin diplomatik sonuçları: Ankara Antlaşması ve Kars Antlaşması.",
    "Medine Müdafaası kahramanı 'Çöl Kaplanı': Ömer Fahrettin (Türkkan) Paşa.",
    "Preveze Deniz Zaferi'nin kazanıldığı yer (Preveze): Günümüzde Yunanistan sınırlarındadır.",
    "Kutadgu Bilig'in yazarı: Yusuf Has Hacip.",
    "Nizamiye Medreselerini kuran devlet: Büyük Selçuklu Devleti.",
    "Ahilik teşkilatının Osmanlı'daki devamı: Lonca.",
    "Osmanlı'da mali işlerden sorumlu divan üyesi: Defterdar.",
    "İlk Türk devletlerinde hükümdarlık sembolü olmayan: Kalkan (Otağ, Davul, Tuğ, Kılıç semboldür).",
    "Mısır'da kurulan Türk devletlerinden olmayan: Gazneliler ve Osmanlılar (Osmanlı Mısır'ı yönetmiştir ama merkez Mısır değildir; Gazneliler Mısır'da kurulmamıştır).",
    "Kudüs'ü Haçlılardan geri alan komutan: Selahaddin Eyyubi.",
    "Türkiye'nin en kuzey ucu: İnceburun (Sinop).",
    "Endemik 'sığla ağacı'nın görüldüğü yer: Köyceğiz Gölü çevresi.",
    "Pamuk üretiminde öne çıkan il: Şanlıurfa.",
    "Linyit ile çalışan termik santral (Doğalgaz olmayan): Soma (Manisa).",
    "Kelebekler Vadisi Kanyonu hangi ilimizdedir? Muğla.",
    "Yeşilırmak Havzası Gelişim Projesi (YHGP) illerinden biri: Tokat (Amasya, Çorum, Samsun).",
    "Marmara Gölü hangi ilimizdedir? Manisa.",
    "Türkiye'nin gerçek yüzölçümü: Yaklaşık 814.578 km².",
    "Türkiye nüfus özelliği yanlışı: Erkek nüfus kadın nüfustan fazladır (Genelde dengelidir veya çok az fark vardır, ancak sorularda 'Tarım sektöründe istihdam en fazladır' ifadesi genellikle yanlış cevap olarak verilir, çünkü hizmet sektörü öndedir).",
    "Belen Geçidi hangi dağlar üzerindedir? Nur (Amanos) Dağları.",
    "Jeotermal enerjiden elektrik üretilen yerler: Sarayköy (Denizli) ve Germencik (Aydın).",
    "Ege'ye dökülen akarsuların kuzeyden güneye sırası: Bakırçay - Gediz - Küçük Menderes - Büyük Menderes.",
    "Hinterlandı dar olduğu için az gelişen liman şehri: Sinop.",
    "Petrol rafinerisi olmayan il: Adıyaman (Petrol çıkarılır ama rafineri yoktur; Batman, İzmit, Kırıkkale, İzmir'de vardır).",
    "Güney Marmara'da yer alan göl: Ulubat (veya Kuş) Gölü.",
    "Volkanik dağ örneği: Erciyes Dağı.",
    "Kaynağı dışarıda olup Türkiye'den denize dökülen akarsu: Asi Nehri (Kaynağı Lübnan/Suriye, döküldüğü yer Hatay/Türkiye).",
    "Memurun disiplin cezaları: Uyarma, Kınama, Aylıktan Kesme, Kademe İlerlemesinin Durdurulması, Devlet Memurluğundan Çıkarma.",
    "'Görev sırasında amire sözle saygısızlık' cezası: Kınama (Bazı kaynaklarda fiilin ağırlığına göre değişebilir, sınavda şıkka göre Kınama veya Aylıktan Kesme sorulabilir. 657'ye göre 'Saygısız davranmak' Kınama; 'Sözle saygısızlık/hakaret' daha ağır olabilir. Bu soruda cevap şıkkı Kınama olarak işaretlenmiştir).",
    "'Amire hal ve hareketi ile saygısız davranmak': Kınama cezası.",
    "Aylıktan kesme cezasını gerektiren fiil: Hizmet içinde devlet memurunun itibar ve güven duygusunu sarsacak nitelikte davranışlarda bulunmak veya ticari faaliyette bulunmak.",
    "Yurt dışı görevinde hastalık izni süresi: Birer yıllık dönemlerde 90 günü geçerse görev sonlandırılır.",
    "Pasaport Kanunu'na göre diplomatik pasaport harcı: Harç veya resme tabi değildir.",
    "Pasaport sürelerini belirleyen makam: İçişleri Bakanlığı.",
    "TBMM Denetim Yolları: Yazılı Soru, Genel Görüşme, Meclis Araştırması, Meclis Soruşturması. (Gensoru kaldırılmıştır).",
    "Yönetmelik çıkarma yetkisi: Cumhurbaşkanı, Bakanlıklar ve Kamu Tüzel Kişileri.",
    "Normlar Hiyerarşisi (Üstten alta): Anayasa > Kanun (ve Milletlerarası Antlaşmalar) > Cumhurbaşkanlığı Kararnamesi > Yönetmelik.",
    "Sosyal ve Ekonomik Haklar: Eğitim hakkı, Sendika kurma, Ailenin korunması. (Mülkiyet hakkı 'Kişi Hakları' grubundadır) .",
    "Siyasi Haklar: Seçme ve seçilme, Dilekçe hakkı, Vatan hizmeti.",
    "Milletlerarası antlaşmaları onaylama yetkisi: Cumhurbaşkanı.",
    "Yurt dışı görevlendirilecek personel sınavı: Mesleki Yeterlilik Sınavı ve Temsil Yeteneği Sınavı (Mülakat).",
    "Pasaport Türleri: Diplomatik (Siyah), Hususi (Yeşil), Hizmet (Gri), Umuma Mahsus (Bordo). Mavi pasaport artık kullanılmamaktadır.",
    "Mecburi ilköğretim çağı: 6-14 yaş (Ancak 222 sayılı kanuna göre öğretim yılı sonuna kadar bitiremeyenlere en çok 2 yıl daha izin verilir).",
    "Eğitime ara verme (Olağanüstü hal): En az 2 hafta yapılamazsa tatilde telafi edilebilir (izinler kısaltılabilir).",
    "Öğretim İlkeleri: Karmaşık bir konuyu anlaşılır dille anlatmak: Açıklık.",
    "Öğretim İlkeleri: Alışveriş yaparak matematik öğretmek: Yaşama Yakınlık (Hayatilik).",
    "Öğretim İlkeleri: Öğrenci ilgisini çekmeyen materyal kullanımı hatası: Öğrenciye Görelik.",
    "Öğretim Yöntem ve Teknikleri: Sanal ortamda/riskli durumlarda (askeri, pilot, sürücü) eğitim: Benzetim (Simülasyon).",
    "Öğretim Yöntem ve Teknikleri: Üst sınıfın alt sınıfa ders çalıştırması: Tutor (Akran) Destekli Öğretim.",
    "Öğretim Yöntem ve Teknikleri: Fikirlerin saçma/doğru ayrımı yapılmadan listelenmesi: Beyin Fırtınası.",
    "Öğretim Yöntem ve Teknikleri: Bir işi başlatıp diğer grubun devam ettirmesi (şiir, poster vb.): İstasyon.",
    "Öğretim Yöntem ve Teknikleri: Konunun uzmanlarca sunulup sonunda soru alınması (bilimsel): Sempozyum (Bilgi Şöleni).",
    "Öğretim Yöntem ve Teknikleri: Tez-Antitez savunması (Jüri önünde): Münazara.",
    "Öğretim Yöntem ve Teknikleri: Öğrencinin kendi kendine ilke ve genellemelere ulaştığı yol: Buluş Yoluyla Öğretim.",
    "Düşünme Becerileri: Hatalardan ders çıkarma, öz eleştiri: Yansıtıcı Düşünme.",
    "Düşünme Becerileri: Olaylara farklı açılardan bakma (Şapkalar): Altı Şapkalı Düşünme. (Sarı şapka: İyimser/Olumlu).",
    "Düşünme Becerileri: Gerçek/Güvenilir bilgiyi sorgulama: Eleştirel Düşünme.",
    "Çoklu Zekâ: Yalnız yapamama, grupla/sohbetle öğrenme: Sosyal Zekâ.",
    "Çoklu Zekâ: El-göz koordinasyonu, yapma-etme (Berber örneği): Bedensel/Kinestetik Zekâ.",
    "Program Geliştirme: Eğitim programlarını hazırlama/karar organı: Talim ve Terbiye Kurulu Başkanlığı.",
    "Bayrağında hilal olmayan Türk Cumhuriyeti: Kırgızistan (Güneş vardır).",
    "Karabağ Zaferi ateşkes arabulucusu: Rusya.",
    '"Çöpçüler Kralı" filmindeki karakter: Apti.',
    "Uzaya çıkan ilk insan: Yuri Gagarin.",
    "Machu Picchu antik kenti: Peru.",
    "Hollywood (Sinema): ABD.",
    "2020 Tokyo Olimpiyatları'nda Türkiye'nin en çok madalya aldığı branş: Karate.",
    "Türkiye'nin yurt dışı culture tanıtım kurumu (2007): Yunus Emre Enstitüsü.",
    "Mona Lisa tablosunun bulunduğu şehir: Paris (Louvre Müzesi).",
    "Almanya Hükümet Başkanı unvanı: Şansölye.",
    "e-Devlet Kapısı yöneticisi: Cumhurbaşkanlığı Dijital Dönüşüm Ofisi.",
    "Mars keşif aracı (NASA): Perseverance.",
    "ABD'deki 'Türkevi' binası: New York.",
    "Pinokyo'nun ait olduğu edebiyat: İtalya.",
    "Küçük Prens'in adandığı kişi: Yazarın arkadaşı (Leon Werth).",
    "Öldürülen The Beatles üyesi: John Lennon.",
    "Muhammed Ali'nin gitmeyi reddettiği savaş: Vietnam Savaşı.",
    "Grand Slam (Tenis) turnuvası olmayan: İspanya Açık (Avustralya, Fransa, Wimbledon, ABD vardır).",
    "Hem futbol hem basketbol milli olan sporcu: Can Bartu.",
    "Orhun Yazıtları'nın kaidesi: Kaplumbağa.",
    "Looney Tunes karakteri olmayan: Tom ve Jerry (MGM yapımıdır).",
    "24 Kasım Öğretmenler Günü nedeni: Atatürk'e 'Başöğretmen' unvanının verilmesi.",
    "Resim sanatı temsilcileri: Şeker Ahmet Paşa, Osman Hamdi Bey.",
    "Avrupa İnsan Hakları Mahkemesi (AİHM) yargıç sayısı: Taraf devlet sayısı kadardır (Her devletten bir yargıç).",
    "BM Yargı Organı: Uluslararası Adalet Divanı (Lahey).",
    "J.R.R. Tolkien'in eseri: Yüzüklerin Efendisi.",
    "Dönüşüm (Gregor Samsa) yazarı: Franz Kafka.",
    "Türk Lirası uluslararası kodu: TRY.",
    "Dünya Engelliler Günü: 3 Aralık.",
    "Osmanlı'daki ilk borsa: Dersaadet Tahvilat Borsası.",
    "Kobe Bryant'ın efsaneleştiği şehir/takım: Los Angeles (Lakers).",
    "1918-1920 Küresel Salgın: İspanyol Gribi.",
    "TEMA Vakfı kurucusu ('Toprak Dede'): Hayrettin Karaca.",
    "İlk yerli baz istasyonu: Ulak.",
    "2019 Nobel Barış Ödülü: Abiy Ahmed Ali (Etiyopya).",
    "Vatanım Sensin / Filinta / Payitaht Abdülhamid: Tarihî kurgu dizileridir (Payitaht: II. Abdülhamid dönemi)."
]

def load_ai_questions():
    return AI_QUESTIONS_DATA

def load_hap_bilgiler():
    haplar = HAP_BILGILER_DATA
    questions = []
    for bilgi in haplar:
        if ':' in bilgi:
            q, a = bilgi.split(':', 1)
            questions.append({"q": q.strip() + "?", "a": a.strip(), "cat": "Hap Bilgi"})
        else:
            questions.append({"q": bilgi.strip(), "a": "", "cat": "Hap Bilgi"})
    return questions

# --- KULLANICI KODU LİSANS SİSTEMİ ---
SECRET_KEY = b"MUZAFFER_CINAR_2026_MASTER_KEY"

def validate_license(user_code, input_key):
    try:
        user_code = user_code.strip().upper()
        signature = hmac.new(SECRET_KEY, user_code.encode('utf-8'), hashlib.sha256).digest()
        license_key = base64.urlsafe_b64encode(signature).decode('utf-8').upper()
        clean_key = re.sub(r'[^A-Z0-9]', '', license_key)
        return input_key.strip().upper() == clean_key[:6]
    except:
        return False

# --- SESSION STATE BAŞLATMA ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_code' not in st.session_state:
    st.session_state.user_code = ""
if 'mode' not in st.session_state:
    st.session_state.mode = "menu"
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# URL'den otomatik login
query_params = st.query_params
if not st.session_state.authenticated:
    if "user" in query_params and "key" in query_params:
        if validate_license(query_params["user"], query_params["key"]):
            st.session_state.authenticated = True
            st.session_state.user_code = query_params["user"]

# --- PREMİUM LOGO (SVG) ---
LOGO_SVG = """
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="shieldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1976D2;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0D47A1;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FFD54F;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF8F00;stop-opacity:1" />
    </linearGradient>
    <filter id="shadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-opacity="0.3"/>
    </filter>
  </defs>
  
  <!-- Shield Shape -->
  <path d="M100 10 L180 40 L180 100 C180 150 140 180 100 195 C60 180 20 150 20 100 L20 40 Z" 
        fill="url(#shieldGrad)" stroke="url(#goldGrad)" stroke-width="3" filter="url(#shadow)"/>
  
  <!-- Book Icon -->
  <g transform="translate(100, 75)">
    <rect x="-30" y="-20" width="25" height="35" rx="2" fill="white" opacity="0.9"/>
    <rect x="5" y="-20" width="25" height="35" rx="2" fill="white" opacity="0.9"/>
    <line x1="-17" y1="-10" x2="-7" y2="-10" stroke="#0D47A1" stroke-width="2"/>
    <line x1="-17" y1="-2" x2="-7" y2="-2" stroke="#0D47A1" stroke-width="2"/>
    <line x1="-17" y1="6" x2="-12" y2="6" stroke="#0D47A1" stroke-width="2"/>
    <line x1="17" y1="-10" x2="27" y2="-10" stroke="#0D47A1" stroke-width="2"/>
    <line x1="17" y1="-2" x2="27" y2="-2" stroke="#0D47A1" stroke-width="2"/>
    <line x1="17" y1="6" x2="22" y2="6" stroke="#0D47A1" stroke-width="2"/>
  </g>
  
  <!-- Star Accent -->
  <polygon points="100,42 103,50 112,50 105,56 108,64 100,59 92,64 95,56 88,50 97,50" fill="url(#goldGrad)"/>
  
  <!-- Text: MC MEB -->
  <text x="50%" y="140" dominant-baseline="middle" text-anchor="middle" 
        font-family="'Inter', 'Segoe UI', sans-serif" font-weight="700" font-size="22" fill="white"
        style="letter-spacing: 1px;">MC MEB</text>
  
  <!-- Subtitle: Yurt Dışı -->
  <text x="50%" y="162" dominant-baseline="middle" text-anchor="middle" 
        font-family="'Inter', 'Segoe UI', sans-serif" font-weight="500" font-size="12" fill="rgba(255,255,255,0.85)"
        style="letter-spacing: 2px;">YURT DIŞI</text>
</svg>
"""

# Logo'yu Base64'e çevir
logo_b64 = base64.b64encode(LOGO_SVG.encode('utf-8')).decode("utf-8")
logo_html = f'<img src="data:image/svg+xml;base64,{logo_b64}" width="160">'

# CSS STİLLERİ
st.markdown("""
<style>
/* ===== GOOGLE FONTS ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ===== CSS DESIGN TOKENS ===== */
:root {
    --primary: #0D47A1;
    --primary-light: #1976D2;
    --primary-dark: #0A3680;
    --secondary: #00897B;
    --secondary-light: #00ACC1;
    --accent: #FF6F00;
    --accent-light: #FFB300;
    --bg-dark: #0A1628;
    --bg-card: #1A2A40;
    --bg-surface: #243B55;
    --text-primary: #FFFFFF;
    --text-secondary: #B0BEC5;
    --success: #4CAF50;
    --warning: #FFC107;
    --error: #EF5350;
    --border: rgba(255,255,255,0.1);
    --shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ===== MAIN APP BACKGROUND ===== */
.stApp {
    background: linear-gradient(135deg, #0A1628 0%, #0D2137 40%, #1A2A40 80%, #0A1628 100%);
    background-attachment: fixed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ===== HIDE STREAMLIT BRANDING ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== CONTAINER SPACING ===== */
div.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 900px;
}

div[data-testid="stVerticalBlock"] > div {
    gap: 0.75rem !important;
}

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

h1 {
    font-weight: 700 !important;
    font-size: 2.25rem !important;
    letter-spacing: -0.5px;
}

h2 {
    font-weight: 600 !important;
    font-size: 1.75rem !important;
}

h3 {
    font-weight: 600 !important;
    font-size: 1.25rem !important;
    color: rgba(255,255,255,0.95) !important;
}

h4 {
    font-weight: 500 !important;
    font-size: 1rem !important;
    color: var(--text-secondary) !important;
    margin-bottom: 8px !important;
}

p, span, div {
    font-family: 'Inter', sans-serif;
}

/* ===== CARD COMPONENTS ===== */
.login-box, .premium-card {
    background: linear-gradient(145deg, rgba(26, 42, 64, 0.95), rgba(36, 59, 85, 0.9));
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 32px;
    text-align: center;
    color: white;
}

.contact-info {
    background: linear-gradient(145deg, rgba(13, 71, 161, 0.3), rgba(0, 137, 123, 0.2));
    padding: 20px;
    border-radius: 16px;
    margin-top: 24px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ===== INPUT FIELDS ===== */
.stTextInput input {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 12px !important;
    border: 2px solid transparent !important;
    padding: 16px 20px !important;
    font-size: 16px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    text-align: center !important;
    letter-spacing: 1px !important;
    color: #1A2A40 !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(13, 71, 161, 0.2) !important;
}

/* ===== BUTTONS - PRIMARY STYLE ===== */
.stButton button {
    background: linear-gradient(135deg, #0D47A1 0%, #1976D2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 6px 20px rgba(13, 71, 161, 0.35) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    width: 100% !important;
}

.stButton button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 12px 28px rgba(13, 71, 161, 0.45) !important;
    background: linear-gradient(135deg, #1565C0 0%, #1E88E5 100%) !important;
}

.stButton button:active {
    transform: translateY(-1px) !important;
}

/* ===== BUTTONS - CTA/PRIMARY KIND ===== */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #00897B 0%, #00ACC1 100%) !important;
    box-shadow: 0 6px 20px rgba(0, 137, 123, 0.4) !important;
}

div.stButton > button[kind="primary"]:hover {
    box-shadow: 0 12px 28px rgba(0, 137, 123, 0.5) !important;
    background: linear-gradient(135deg, #00796B 0%, #0097A7 100%) !important;
}

/* ===== SIDEBAR STYLING ===== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #0D2137 50%, #1A2A40 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-secondary);
}

section[data-testid="stSidebar"] h3 {
    color: white !important;
    font-size: 14px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ===== ALERTS & INFO BOXES ===== */
.stAlert, div[data-testid="stAlert"] {
    border-radius: 14px !important;
    border-left-width: 4px !important;
    font-family: 'Inter', sans-serif !important;
}

div[data-testid="stAlert"] > div {
    padding: 16px 20px !important;
}

/* ===== PROGRESS BAR ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #0D47A1, #00897B, #00ACC1) !important;
    border-radius: 10px !important;
}

.stProgress > div > div {
    background: rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
}

/* ===== METRICS ===== */
div[data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
    color: white !important;
}

div[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-secondary) !important;
}

/* ===== SELECT BOX ===== */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.95) !important;
    border-radius: 12px !important;
    border: none !important;
}

/* ===== DIVIDERS ===== */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent) !important;
    margin: 20px 0 !important;
}

/* ===== CAPTION TEXT ===== */
.stCaption, div[data-testid="stCaptionContainer"] {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
}

/* ===== RESPONSIVE DESIGN ===== */
@media (max-width: 768px) {
    div.block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    .login-box {
        padding: 20px 16px;
        border-radius: 16px;
    }
    
    h1 {
        font-size: 1.75rem !important;
    }
    
    .stButton button {
        padding: 12px 20px !important;
        font-size: 14px !important;
    }
}

/* ===== ANIMATION FOR SUBTLE POLISH ===== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.stApp > div {
    animation: fadeIn 0.4s ease-out;
}
</style>
""", unsafe_allow_html=True)


# === EKRAN ÇİZİMİ (LOGIN GÖSTERİMİ) ===
if not st.session_state.authenticated:
    if st.session_state.get('show_login', False):
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown(logo_html, unsafe_allow_html=True)
        st.markdown("<h1>MC MEB Yurt Dışı</h1>", unsafe_allow_html=True)
        st.markdown("<h4>Yurt Dışı Öğretmenlik Sınav Hazırlık Platformu</h4>", unsafe_allow_html=True)
        
        st.info("🔐 Devam etmek için lütfen giriş yapın.")
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            user_code_input = st.text_input("Kullanıcı Kodu", placeholder="ÖRNEK: ŞİFRE001", label_visibility="collapsed")
            license_input = st.text_input("Şifre", placeholder="******", type="password", label_visibility="collapsed")
            
            if st.button("GİRİŞ YAP 🚀"):
                if validate_license(user_code_input, license_input):
                    st.session_state.authenticated = True
                    st.session_state.user_code = user_code_input.strip().upper()
                    st.session_state.show_login = False
                    st.session_state.mode = "menu"
                    st.rerun()
                else:
                    st.error("❌ Hatalı şifre!")
            
            if st.button("⬅️ Geri Dön"):
                st.session_state.show_login = False
                st.rerun()

        st.markdown("""
        <div class="contact-info">
            <p>📧 ufomath@gmail.com</p>
            <p style="color: #ddd; font-size: 14px; margin: 5px 0; font-weight: bold; letter-spacing: 0.5px;">LİSANS ANAHTARI TALEP ET</p>
            <hr>
            <a href="https://wa.me/?text=Merhaba%2C%20https%3A%2F%2Fyurtdisimebhazirlik.streamlit.app" target="_blank">
                <button style="background-color: #25D366; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; display: flex; align-items: center; justify-content: center; gap: 5px; margin-bottom: 20px;">
                    <img src="https://cdn-icons-png.flaticon.com/512/1384/1384007.png" width="16" style="filter: brightness(0) invert(1);">
                    WhatsApp ile Paylaş
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    else:
        # Sidebarda giriş butonu
        if st.sidebar.button("🔐 Admin / Lisans Girişi", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()
        
        if "user_code" not in st.session_state:
            st.session_state.user_code = "MİSAFİR"

all_questions = load_questions()
ai_questions = load_ai_questions()
hap_questions = load_hap_bilgiler()
categories = sorted(list(set(q.get("cat", "Genel") for q in all_questions)))

def start_mode(mode, questions):
    st.session_state.mode = mode
    st.session_state.questions = questions.copy()
    random.shuffle(st.session_state.questions)
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.show_answer = False

def go_home():
    st.session_state.mode = "menu"

def next_question(correct):
    if correct:
        st.session_state.score += 1
    st.session_state.index += 1
    st.session_state.show_answer = False
    
    # 20 soru limiti kontrolü (Demo kullanıcıları için)
    if not st.session_state.authenticated and st.session_state.index >= 20:
        st.session_state.mode = "demo_limit"
        return

    if st.session_state.index >= len(st.session_state.questions):
        st.session_state.mode = "result"

if st.session_state.mode == "menu":
    st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'>{logo_html}</div>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; margin-bottom: 20px; margin-top: -10px;'>Yurt Dışı Öğretmenlik Sınav Hazırlık Platformu</h4>", unsafe_allow_html=True)

    # --- DEMO VE GİRİŞ UYARILARI (ANA EKRAN) ---
    if not st.session_state.authenticated:
        st.warning("⚠️ DENEME MODU: Sadece Deneme Sınavında ilk 20 soruya erişiminiz var. 🔐 Lisans alınız!")
        
        if st.button("🔐 ŞİFRE / LİSANS GİRİŞİ YAP", type="primary", use_container_width=True):
             st.session_state.show_login = True
             st.rerun()

    # Compact Divider
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📚 GENEL SINAV\n[Pro 🔒]", use_container_width=True):
            if not st.session_state.authenticated:
                st.error("🔒 Bu modülü kullanmak için lisans gerekli! Lütfen giriş yapınız.")
            else:
                start_mode("exam", all_questions)
                st.rerun()
        if st.button("🤖 AI DESTEKLİ (1000 Soruluk Benzer Sorular)\n[Pro 🔒]", use_container_width=True):
            if not st.session_state.authenticated:
                st.error("🔒 Bu modülü kullanmak için lisans gerekli! Lütfen giriş yapınız.")
            elif ai_questions:
                start_mode("exam", ai_questions)
                st.rerun()
            else:
                st.error("AI soru dosyası bulunamadı!")
    with col2:
        if st.button("⏱️ DENEME SINAVI\n(Demo: ilk 20 soru)", use_container_width=True, type="primary"):
            if not st.session_state.authenticated:
                # Demo: Sadece ilk 20 soruyu gösterir (Asıl kontrol döngüde)
                # Tüm soruları yüklesek de 20. soruda durduracağız.
                # Karışıklık olmasın diye 20 tane sample da alabiliriz ama 
                # kullanıcıya "devamı var" hissi vermek için hepsini yükleyip yarıda kesmek daha etkili olabilir.
                # Ancak performans için 20 tane alalım.
                sample = random.sample(all_questions, min(len(all_questions), 200)) # Biraz fazla al, 20'de kes
                start_mode("exam", sample)
                st.rerun()
            else:
                # Lisanslı: 100 soru
                sample = random.sample(all_questions, min(100, len(all_questions)))
                start_mode("exam", sample)
                st.rerun()
        if st.button("💡 HAP BİLGİ\n[Pro 🔒]", use_container_width=True):
            if not st.session_state.authenticated:
                st.error("🔒 Bu modülü kullanmak için lisans gerekli! Lütfen giriş yapınız.")
            elif hap_questions:
                start_mode("exam", hap_questions)
                st.rerun()
            else:
                st.error("Hap bilgi dosyası bulunamadı!")
    
    # Compact Divider
    st.markdown("<hr style='margin: 10px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
    st.markdown("### 📂 Kategoriye Göre Çalış")
    selected_cat = st.selectbox("Kategori Seçin", ["Tümü"] + categories)
    if st.button("Seçili Kategori ile Başla"):
        if not st.session_state.authenticated:
            st.error("🔒 Bu modülü kullanmak için lisans gerekli! Lütfen giriş yapınız.")
        elif selected_cat == "Tümü":
            start_mode("exam", all_questions)
            st.rerun()
        else:
            filtered = [q for q in all_questions if q.get("cat") == selected_cat]
            start_mode("exam", filtered)
            st.rerun()

    # WHATSAPP SHARE BUTTON - MAIN PAGE FOOTER
    st.markdown("""
    <div style="margin-top: 30px; margin-bottom: 20px;">
        <a href="https://wa.me/?text=Yurt%20dışı%20öğretmenlik%20sınav%20hazırlık%20uygulamasına%20gözatmak%20istermisiniz%20https%3A%2F%2Fyurtdisimebhazirlik.streamlit.app" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 12px 20px; border-radius: 50px; font-weight: bold; cursor: pointer; width: 100%; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                <img src="https://cdn-icons-png.flaticon.com/512/1384/1384007.png" width="20" style="filter: brightness(0) invert(1);">
                Arkadaşına Linki Gönder 🚀
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
            
    # COPYRIGHT FOOTER
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #eee; font-size: 12px; margin-top: 20px;">
        Bu yazılım MEB yurt dışı öğretmenlik sınavlarına hazırlananlara yardımcı ek kaynak olarak hazırlanmıştır.<br>
        Her hakkı saklıdır. © 2026 MC MEB Yurt Dışı
    </div>
    """, unsafe_allow_html=True)
            
    st.sidebar.markdown(logo_html, unsafe_allow_html=True)
    if st.session_state.authenticated:
        st.sidebar.success(f"✅ Hoş geldiniz: {st.session_state.user_code}")
    else:
        st.sidebar.info("👤 Misafir Kullanıcı")
        
    st.sidebar.info(f"📊 Toplam Soru: {len(all_questions)}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📢 Paylaş")
    st.sidebar.markdown("""
    <a href="https://wa.me/?text=Yurt%20dışı%20öğretmenlik%20sınav%20hazırlık%20uygulamasına%20gözatmak%20istermisiniz%20https%3A%2F%2Fyurtdisimebhazirlik.streamlit.app" target="_blank">
        <button style="background-color: #25D366; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; display: flex; align-items: center; justify-content: center; gap: 5px; margin-bottom: 20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/1384/1384007.png" width="16" style="filter: brightness(0) invert(1);">
            WhatsApp ile Paylaş
        </button>
    </a>
    """, unsafe_allow_html=True)
    if st.session_state.authenticated:
        if st.sidebar.button("🚪 ÇIKIŞ YAP", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_code = None
            st.rerun()

elif st.session_state.mode == "exam":
    questions = st.session_state.questions
    idx = st.session_state.index
    
    # GÜVENLİK/LİMİT KONTROLÜ
    # Demo ve index >= 20 ise -> Demo Limit Ekranına at
    if not st.session_state.authenticated and idx >= 20:
        st.session_state.mode = "demo_limit"
        st.rerun()
    
    if idx >= len(questions):
        st.session_state.mode = "result"
        st.rerun()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress((idx + 1) / len(questions))
        st.caption(f"Soru {idx + 1} / {len(questions)}")
        if not st.session_state.authenticated:
            st.info(f"📌 Demo Modu: {20 - idx} soru hakkınız kaldı.")
    with col2:
        if st.button("🏠 Ana Menü"):
            go_home()
            st.rerun()
    q = questions[idx]
    st.markdown(f"### ❓ {q.get('q', 'Soru yok')}")
    if q.get("cat"):
        st.caption(f"📁 {q['cat']}")
    if not st.session_state.show_answer:
        if st.button("👁️ CEVABI GÖR", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
    else:
        st.success(f"✅ **Cevap:** {q.get('a', '-')}")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ BİLDİM", use_container_width=True, type="primary"):
                next_question(True)
                st.rerun()
        with col2:
            if st.button("❌ BİLMEDİM", use_container_width=True):
                next_question(False)
                st.rerun()
    st.sidebar.metric("Doğru", st.session_state.score)
    st.sidebar.metric("Kalan", len(questions) - idx)

elif st.session_state.mode == "demo_limit":
    st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>""", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center;'>{logo_html}</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🔐 LİSANS GEREKLİ</h2>", unsafe_allow_html=True)
    
    st.error("⛔ Ücretsiz Deneme Hakkınız (20 Soru) Doldu!")
    st.markdown("""
    ---
    ### 📌 Tebrikler! 
    İlk 20 soruyu tamamladınız. Devam etmek için **Pro Lisans** sahibi olmanız gerekmektedir.
    
    ### 🎁 Lisans Avantajları:
    ✅ **Sınırsız Soru Çözümü** (Tüm 1000+ Soru)  
    ✅ **Genel Sınav** Modülü  
    ✅ **AI Destekli** Çalışma Modülü  
    ✅ **Hap Bilgiler** ve Çıkmış Sorular  
    ✅ **Kategoriye Göre** Özelleştirilmiş Çalışma  
    ---
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 ŞİFRE / LİSANS GİRİŞİ", type="primary", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()
    with col2:
        if st.button("🏠 ANA MENÜYE DÖN", use_container_width=True):
            go_home()
            st.rerun()
    
    st.markdown("""
    <div class="contact-info">
        <p>📧 ufomath@gmail.com</p>
        <hr>
        <a href="https://wa.me/?text=Merhaba%2C%20Lisans%20hakkinda%20bilgi%20almak%20istiyorum." target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 10px 15px; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; display: flex; align-items: center; justify-content: center; gap: 5px; margin-bottom: 20px;">
                <img src="https://cdn-icons-png.flaticon.com/512/1384/1384007.png" width="16" style="filter: brightness(0) invert(1);">
                WhatsApp ile İletişime Geç
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.mode == "result":
    st.balloons()
    st.markdown("## 🏆 SINAV TAMAMLANDI!")
    total = len(st.session_state.questions)
    score = st.session_state.score
    percent = int((score / total) * 100) if total > 0 else 0
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Doğru", score)
    col2.metric("❌ Yanlış", total - score)
    col3.metric("📊 Başarı", f"%{percent}")
    if percent >= 80:
        st.success("🎉 Mükemmel! Harika bir performans!")
    elif percent >= 60:
        st.info("👍 İyi! Biraz daha çalışarak daha iyi olabilirsin.")
    else:
        st.warning("📚 Daha fazla çalışman gerekiyor.")
    if st.button("🏠 Ana Menüye Dön", use_container_width=True):
        go_home()
        st.rerun()