Nama : Banin Shula Afiqah Aradena
NPM  : 2506604794
Kelas: C
Program studi : Sistem Informasi

### AI Disclosure

Beberapa hal yang saya diskusikan dengan ChatGPT antara lain penggunaan elemen semantik HTML5, penerapan CSS Grid dan media query, serta pengembangan tampilan seperti pemilihan warna, layout, dan efek hover pada foto profil. Saya juga menggunakan ChatGPT untuk mengecek dan memberikan saran terhadap kode HTML dan CSS yang saya buat.

Meskipun menggunakan AI sebagai bantuan, saya tetap menentukan sendiri isi, data, dan tampilan portfolio yang digunakan. Kode yang diberikan atau disarankan oleh AI juga saya sesuaikan kembali dengan kebutuhan website dan saya pahami sebelum digunakan.

### Tugas 1

1. Saya menggunakan beberapa elemen semantik HTML5 seperti `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, dan `<footer>` untuk menyusun halaman. Penggunaannya saya sesuaikan dengan fungsinya masing-masing, misalnya `<section>` untuk memisahkan bagian Profile dan Experience, lalu `<article>` untuk penjabaran setiap experience-nya. Dengan menggunakan elemen semantik, struktur HTML menjadi lebih terorganisasi dan mudah dipahami karena membantu memberikan informasi yang lebih jelas mengenai struktur halaman.

2. Tantangan utama dalam membuat layout responsive adalah memastikan tampilan tetap rapi ketika ukuran layar berubah terutama saat berpindah dari desktop ke mobile. Pada tampilan desktop, saya menggunakan CSS Grid untuk menempatkan informasi profil dan foto dalam dua kolom. Sementara itu, pada layar yang lebih kecil, layout tersebut diubah menjadi satu kolom menggunakan media query agar konten tidak terlalu sempit. Saya juga membatasi ukuran foto pada mobile dan mengatur ulang posisi foto, nama, serta informasi profil agar tetap nyaman dilihat dan dibaca. Dari proses ini, saya belajar bahwa responsive design bukan hanya mengecilkan ukuran elemen, tetapi juga menyesuaikan struktur dan posisi elemen dengan ukuran layar.

3. Website yang saya buat saat ini masih berupa static web, sehingga kontennya masih ditulis langsung di dalam HTML dan belum dapat berubah berdasarkan interaksi pengguna. Ke depannya, saya ingin menambahkan fitur guestbook atau comment, sehingga pengunjung dapat meninggalkan pesan atau komentar yang kemudian ditampilkan pada halaman website. Dengan adanya fitur tersebut, website memiliki fitur interaksi antara saya sebagai pemilik website dengan pengunjung.


### Tugas 2

1. Alur request dari browser sampai halaman ditampilkan dimulai ketika pengguna mengakses URL tertentu pada website. Request tersebut diarahkan oleh `urls.py` pada level project ke URL yang dimiliki oleh aplikasi `main`. Setelah itu, `main/urls.py` menentukan view yang sesuai berdasarkan URL yang diakses. View kemudian mengambil data dari model `Education` melalui database dan memasukkannya ke dalam context. Context tersebut dikirim ke template `education.html`, kemudian Django Template Language digunakan untuk melakukan perulangan terhadap data pendidikan dan menampilkannya menjadi HTML. Setelah proses rendering selesai, hasil HTML dikirim kembali ke browser dan ditampilkan kepada pengguna. Dalam proses tersebut, `urls.py` pada level project berfungsi mengarahkan request ke aplikasi yang sesuai, sedangkan `main/urls.py` menentukan view berdasarkan URL yang diakses. View berfungsi sebagai penghubung antara request, model, dan template. Model digunakan untuk merepresentasikan data dan mengambil data dari database, sedangkan template bertugas menampilkan data tersebut dalam bentuk halaman HTML.

2. Data portfolio sebaiknya disimpan dalam model daripada ditulis langsung di template karena model memungkinkan data dikelola secara terpisah dari tampilan website. Pada implementasi ini, data pendidikan seperti nama institusi, jenjang pendidikan, dan tahun disimpan dalam model `Education`, sedangkan template hanya bertugas menampilkan data yang diberikan oleh view menggunakan Django Template Language. Dengan cara ini, apabila terdapat perubahan atau penambahan data pendidikan, saya tidak perlu mengubah struktur HTML. Data cukup diperbarui melalui database dan halaman akan menampilkan data tersebut secara otomatis. Pemisahan antara data dan tampilan juga membuat kode lebih mudah dipelihara dan dikembangkan. Selain itu, data yang tersimpan dalam model dapat digunakan kembali oleh bagian website lain apabila dibutuhkan.

3. `makemigrations` dan `migrate` memiliki fungsi yang berbeda. `makemigrations` digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model Django. File migration tersebut berisi instruksi mengenai perubahan struktur database yang perlu dilakukan. Sementara itu, `migrate` digunakan untuk menerapkan migration tersebut ke database. Sebagai contoh, setelah saya menambahkan model `Education` ke dalam `main/models.py`, saya menjalankan `python manage.py makemigrations` dan Django membuat file `0002_education.py`. Setelah itu, saya menjalankan `python manage.py migrate` untuk menerapkan perubahan tersebut sehingga tabel `Education` tersedia pada database dan dapat digunakan oleh aplikasi.



### AI Disclosure Tugas 2

Pada Tugas 2, saya menggunakan ChatGPT sebagai bantuan dalam memahami dan mengimplementasikan konsep Model-View-Template (MVT) pada Django. Bantuan yang digunakan meliputi pemahaman mengenai model, migration, view, URL routing, Django Template Language, serta unit testing. Saya juga menggunakan ChatGPT untuk memeriksa struktur kode dan membantu mengidentifikasi kemungkinan kesalahan pada implementasi.

Dalam menggunakan AI, saya menyadari bahwa jawaban yang diberikan tidak selalu dapat langsung diterapkan pada project saya. Salah satu keterbatasannya adalah AI tidak selalu mengetahui kondisi terbaru dari project, seperti struktur file, kode yang sudah ada, atau data yang tersimpan di database. Karena itu, saya tetap memeriksa kode yang diberikan dengan membandingkannya dengan struktur project saya dan menjalankannya secara langsung untuk memastikan kode tersebut bekerja. Contohnya, ketika terdapat data `Education` yang muncul lebih dari satu kali, saya memeriksa data pada database dan tidak langsung menganggap bahwa masalah tersebut berasal dari template.

Strategi prompting yang saya gunakan adalah memberikan konteks project dan kode yang sedang saya kerjakan terlebih dahulu, kemudian menanyakan satu permasalahan atau konsep secara spesifik. Saya juga memberikan pesan error atau hasil terminal ketika membutuhkan bantuan debugging. Setelah mendapatkan saran dari AI, saya menjalankan dan menguji kembali perubahan tersebut secara mandiri. Dengan cara ini, AI saya gunakan sebagai alat bantu belajar dan debugging, bukan sebagai pengganti proses pemahaman dan pengujian kode.

### Tugas 3

1. ModelForm memungkinkan form dibuat berdasarkan model Django sehingga field dan validasi dapat disesuaikan dengan model yang digunakan. Pada implementasi ini, `EducationForm` dibuat menggunakan `ModelForm` dengan model `Education`, sehingga field seperti `institution`, `degree`, `year`, dan `graduation_year` dapat digunakan langsung pada form. ModelForm juga membantu mengurangi penulisan kode HTML secara manual dan mempermudah proses menyimpan atau memperbarui data ke database.

   Jika form dibuat menggunakan HTML secara manual, setiap input harus dibuat dan diproses secara terpisah di dalam view. Dengan ModelForm, proses pengambilan input, validasi, dan penyimpanan data dapat lebih terintegrasi dengan model.

   `csrf_token` diperlukan untuk melindungi form dari serangan Cross-Site Request Forgery (CSRF). Token tersebut digunakan Django untuk memastikan bahwa request POST yang dikirim melalui form berasal dari halaman yang sah dari aplikasi. Pada implementasi form Education, `{% csrf_token %}` ditambahkan di dalam form sehingga request untuk menambah dan memperbarui data dapat diproses oleh Django dengan aman.

2. JSON dan XML sama-sama dapat digunakan untuk menyimpan atau bertukar data dalam format terstruktur. JSON menggunakan pasangan key-value dan struktur yang lebih ringkas, sedangkan XML menggunakan tag untuk merepresentasikan data.

   Pada implementasi ini, JSON digunakan untuk menyediakan data `Education` melalui endpoint `/api/education/`. Django melakukan serialisasi queryset `Education` menjadi JSON sehingga data dapat dikirim dalam format yang terstruktur. JSON dipilih karena formatnya lebih ringkas dan mudah digunakan untuk pertukaran data pada aplikasi web.

3. Alur pengambilan data JSON dimulai ketika pengguna mengakses endpoint `/api/education/`. Request tersebut diarahkan oleh `main/urls.py` ke view `get_education_json`. View kemudian mengambil data `Education` dari database dan melakukan filtering berdasarkan parameter `institution` jika parameter tersebut diberikan.

   Data yang masih berupa queryset Django kemudian diserialisasi menggunakan `serializers.serialize("json", education_list)`. Hasil serialisasi tersebut dikembalikan menggunakan `HttpResponse` dengan `content_type="application/json"`.

   Serialisasi diperlukan karena object atau queryset Django tidak dapat langsung dikirim sebagai data JSON. Melalui proses serialisasi, data dari object Django diubah menjadi format JSON yang dapat dikirim dan diproses oleh client.

   Pada halaman Education, data juga diambil melalui proses serialisasi dan kemudian dideserialisasi kembali menjadi object Django sebelum dikirim ke template. Proses tersebut dilakukan untuk memenuhi alur pengambilan data melalui JSON sekaligus tetap memungkinkan template menggunakan object `Education` untuk menampilkan data.

### AI Disclosure Tugas 3

Pada Tugas 3, saya menggunakan ChatGPT sebagai bantuan dalam memahami dan mengimplementasikan `ModelForm`, fitur CRUD, endpoint JSON, serta proses serialisasi dan deserialisasi pada Django. Saya juga menggunakannya untuk membantu mengecek kode dan testing.

Saya menyadari bahwa AI tidak selalu mengetahui kondisi terbaru dari project saya, seperti struktur file dan perubahan kode yang sudah dilakukan. Karena itu, saya tetap memeriksa saran AI dengan membandingkannya dengan kode project dan menjalankan testing untuk memastikan hasilnya sesuai.

Strategi prompting yang saya gunakan adalah memberikan konteks project, potongan kode, serta error atau hasil yang saya temukan. Setelah mendapatkan saran, saya menerapkannya secara bertahap dan menguji kembali hasilnya. Dengan demikian, AI saya gunakan sebagai alat bantu memahami konsep dan debugging, bukan sebagai pengganti proses pemahaman dan pengujian kode.


### AI Disclosure Tugas 4

Pada Tugas 4, saya menggunakan ChatGPT sebagai bantuan dalam memahami dan mengimplementasikan fitur autentikasi dan otorisasi pada Django, khususnya penerapan role Editor menggunakan Django Group, pembatasan akses berdasarkan role, serta fitur star pada data Experience. Saya juga menggunakannya untuk membantu mengecek kode, memahami error, dan melakukan testing terhadap fitur yang telah diimplementasikan.

Saya menyadari bahwa AI tidak selalu mengetahui kondisi terbaru dari project saya, seperti struktur file, perubahan kode, dan hasil implementasi yang sudah dilakukan. Karena itu, saya tetap memeriksa saran AI dengan membandingkannya dengan kode project, requirement tugas, serta menjalankan testing untuk memastikan hasilnya sesuai.

Strategi prompting yang saya gunakan adalah memberikan konteks project, potongan kode, requirement tugas, serta error atau hasil testing yang saya temukan. Setelah mendapatkan saran, saya menerapkannya secara bertahap dan menguji kembali hasilnya, termasuk melakukan pengecekan terhadap hak akses Guest, Normal User, Editor, dan Superuser. Dengan demikian, AI saya gunakan sebagai alat bantu memahami konsep, debugging, dan code review, bukan sebagai pengganti proses pemahaman dan pengujian kode.

### Tugas 5

**1. Apa itu debouncing dan mengapa berguna pada AJAX search?**

Debouncing adalah teknik untuk menunda eksekusi suatu fungsi sampai pengguna berhenti melakukan input selama waktu tertentu. Pada AJAX search, debouncing berguna agar request tidak dikirim pada setiap perubahan karakter yang diketik pengguna. Dengan demikian, jumlah request ke server dapat dikurangi dan penggunaan resource menjadi lebih efisien. Hasilnya, fitur search menjadi lebih responsif dan server tidak menerima terlalu banyak request yang sebenarnya tidak diperlukan.

**2. Apa yang dilakukan `await` ketika digunakan bersama `fetch()` dan apa yang terjadi jika tidak menggunakan `await`?**

`fetch()` mengembalikan sebuah `Promise` yang merepresentasikan proses asynchronous untuk melakukan HTTP request. `await` digunakan untuk menunggu sampai Promise tersebut selesai sebelum hasilnya digunakan pada baris kode berikutnya.

Contohnya, ketika menggunakan `await fetch(...)`, program akan menunggu response dari server sebelum melanjutkan proses untuk membaca response tersebut. Jika `await` tidak digunakan, kode dapat langsung melanjutkan eksekusi tanpa menunggu Promise selesai. Akibatnya, program dapat mencoba menggunakan hasil request sebelum data tersedia, atau harus menangani Promise tersebut menggunakan mekanisme asynchronous lainnya seperti `.then()`.

**3. Apa itu XSS dan mengapa data yang dirender melalui AJAX/JavaScript lebih rentan dibandingkan output langsung dari Django template?**

XSS atau Cross-Site Scripting adalah serangan ketika input yang tidak aman dapat diperlakukan sebagai HTML atau JavaScript oleh browser sehingga script berbahaya dapat dijalankan dalam konteks halaman web.

Data yang dirender melalui AJAX/JavaScript perlu mendapat perhatian khusus karena data dari server kemudian dimasukkan secara dinamis ke DOM menggunakan JavaScript. Jika data yang tidak terpercaya langsung dimasukkan sebagai HTML, misalnya melalui `innerHTML`, browser dapat menginterpretasikan tag atau atribut berbahaya sebagai bagian dari halaman.

Pada Django template, output dapat di-escape oleh template engine secara otomatis dalam kondisi penggunaan normal. Namun, ketika data dimasukkan secara manual melalui JavaScript, developer harus memastikan proses escaping dilakukan dengan benar. Pada implementasi ini, data yang akan dimasukkan ke HTML di-escape menggunakan `escapeHtml`, sementara input juga divalidasi dan dibersihkan di server menggunakan `strip_tags`.

---

### AI Disclosure Tugas 5

Dalam pengerjaan Tugas 5, saya menggunakan **ChatGPT** sebagai AI assistant untuk membantu proses analisis requirement, code review, debugging, pengembangan implementasi, testing, dan dokumentasi.

AI digunakan sebagai alat bantu, bukan sebagai pengganti proses pemahaman dan verifikasi. Beberapa bagian yang dibantu oleh AI meliputi:

* Menganalisis requirement Tutorial 05 dan menghubungkannya dengan implementasi portfolio.
* Melakukan audit terhadap struktur dan kode yang sudah ada sebelum perubahan dilakukan.
* Mengidentifikasi kebutuhan penggunaan `ModelForm`, AJAX endpoint, authorization, CSRF protection, dan XSS protection.
* Membantu merencanakan tahapan implementasi secara bertahap.
* Membantu mengidentifikasi dan memperbaiki error pada automated tests.
* Membantu melakukan review terhadap status code dan error handling pada endpoint AJAX.
* Membantu menyusun dan memperbaiki dokumentasi serta komentar pada kode.

Setiap saran dari AI tetap diperiksa dan disesuaikan dengan kondisi project. Implementasi kemudian diverifikasi secara manual melalui automated tests, browser testing, pemeriksaan Git diff, dan pengujian functionality pada aplikasi.

#### AI Limitations and Manual Improvements

AI tidak selalu mengetahui kondisi terbaru dari repository dan tidak dapat mengasumsikan bahwa struktur project sesuai dengan contoh umum Django. Oleh karena itu, kode yang sudah ada diperiksa terlebih dahulu sebelum perubahan diterapkan.

Beberapa keputusan dan perbaikan dilakukan secara manual berdasarkan kondisi project dan requirement tugas, termasuk menyesuaikan endpoint dengan struktur URL yang digunakan, memastikan authorization dilakukan di server, menyesuaikan `ModelForm` dengan model yang digunakan, menambahkan validasi sanitasi pada field, memperbaiki automated tests, serta melakukan pengujian langsung pada browser.

Dengan demikian, AI digunakan terutama untuk membantu analisis dan problem solving, sedangkan keputusan akhir mengenai implementasi dan hasil testing dilakukan berdasarkan project yang sebenarnya.

#### AI Working Log / Prompting Log

Dokumentasi percakapan yang digunakan sebagai AI working log dan prompting log selama pengerjaan Tugas 5 dapat diakses melalui:

**[AI Working Log - Audit T05 Bertahap](https://chatgpt.com/share/6ac204ff-29b8-83ec-a496-9c08cc2c25fe)**

Percakapan tersebut mendokumentasikan proses pengerjaan secara bertahap, mulai dari audit kode dan requirement, perencanaan perubahan, implementasi, testing, debugging, hingga penyempurnaan dokumentasi.

**Prompting approach:**
Saya memberikan requirement tugas dan kondisi kode terbaru kepada AI, kemudian meminta AI melakukan audit terhadap implementasi yang sudah ada sebelum perubahan diterapkan. Proses dilakukan secara bertahap berdasarkan milestone. Setiap perubahan diverifikasi melalui automated testing dan/atau browser testing sebelum melanjutkan ke tahap berikutnya. Ketika ditemukan error atau ketidaksesuaian, hasil testing digunakan sebagai dasar untuk menentukan perubahan berikutnya.

**### Tugas 6**

1. REST (Representational State Transfer) merupakan gaya arsitektur yang digunakan untuk mengatur komunikasi antara client dan server melalui resource. Dalam REST, setiap resource memiliki identitas berupa URI dan dapat diakses atau dimanipulasi menggunakan HTTP method yang sesuai. REST juga menerapkan prinsip seperti pemisahan client dan server, komunikasi yang stateless, serta penggunaan interface yang konsisten.

   Mengembalikan data dalam format JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful. JSON hanya merupakan format representasi data, sedangkan REST mengatur bagaimana resource diidentifikasi dan bagaimana client berkomunikasi dengan server. Sebuah API perlu menerapkan prinsip REST, misalnya menggunakan URI untuk mengidentifikasi resource, HTTP method sesuai dengan operasi yang dilakukan, serta status code yang menggambarkan hasil request.

   Pada implementasi ini, Education API menggunakan endpoint `/api/v1/education/` untuk mengakses daftar data pendidikan dan `/api/v1/education/<id>/` untuk mengakses data pendidikan tertentu. API menggunakan `GET` untuk membaca data, `POST` untuk membuat data baru, `PUT` dan `PATCH` untuk memperbarui data, serta `DELETE` untuk menghapus data.

   `PUT` dan `PATCH` sama-sama digunakan untuk memperbarui resource, tetapi memiliki perbedaan pada cakupan perubahan datanya. `PUT` digunakan untuk memperbarui representasi resource secara keseluruhan, sehingga client perlu mengirimkan seluruh field yang diperlukan. Sementara itu, `PATCH` digunakan untuk memperbarui sebagian field saja tanpa harus mengirimkan seluruh data.

   Sebagai contoh, ketika Editor ingin memperbarui seluruh informasi pendidikan, seperti institusi, gelar, tahun pendidikan, dan tahun kelulusan, Editor dapat menggunakan `PUT`. Namun, jika Editor hanya ingin mengubah nama gelar tanpa mengubah informasi lainnya, `PATCH` lebih sesuai karena hanya field `degree` yang perlu dikirimkan. Pada Education API yang saya implementasikan, `PATCH` menggunakan parameter `partial=True` pada serializer sehingga field lain yang tidak dikirimkan tidak wajib disertakan.

2. Serializer pada Django REST Framework berfungsi untuk mengubah data dari model Django menjadi representasi yang dapat dikirim melalui API, seperti JSON. Serializer juga menangani proses validasi dan deserialisasi data yang diterima dari client sebelum data tersebut digunakan untuk membuat atau memperbarui object pada database.

   Pada implementasi ini, saya menggunakan `EducationSerializer` yang dibuat berdasarkan `ModelSerializer`. Field yang digunakan ditentukan secara eksplisit, yaitu `id`, `institution`, `degree`, `year`, `graduation_year`, `star_count`, dan `is_starred`. Selain itu, serializer juga menangani validasi input, termasuk membersihkan tag HTML pada field teks menggunakan `strip_tags` dan memastikan hasil input tidak kosong.

   Keuntungan menggunakan serializer dibandingkan merakit dictionary secara manual dengan `JsonResponse` seperti pada Tutorial 05 adalah proses konversi data, validasi, dan penyimpanan menjadi lebih terstruktur dan terintegrasi dengan model. Jika menggunakan dictionary secara manual, developer perlu menentukan sendiri setiap field yang akan dikirim dan menangani validasi input secara terpisah. Sementara itu, serializer menyediakan mekanisme yang lebih terorganisasi melalui `.data`, `.is_valid()`, dan `.save()`.

   Dengan menggunakan serializer, struktur representasi data juga lebih mudah dipelihara karena field dan aturan validasinya dikelola dalam satu tempat. Pada Education API, serializer juga digunakan untuk menghasilkan informasi tambahan seperti jumlah star dan status apakah pengguna yang sedang login sudah memberikan star pada suatu data Education.

3. Autentikasi dan otorisasi merupakan dua konsep yang berbeda dalam Django REST Framework. Autentikasi merupakan proses untuk mengidentifikasi pengguna yang melakukan request, misalnya dengan memeriksa session pengguna yang sedang login. Sementara itu, otorisasi merupakan proses untuk menentukan apakah pengguna tersebut memiliki hak akses untuk melakukan suatu tindakan berdasarkan identitas dan role yang dimilikinya.

   Pada implementasi Education API, autentikasi dilakukan menggunakan `SessionAuthentication`, sedangkan otorisasi diatur menggunakan permission class `IsPortfolioOwnerOrEditorOrReadOnly`. Permission tersebut menentukan hak akses berdasarkan role pengguna. Visitor dapat melihat data Education, Normal User dapat melihat serta melakukan star dan unstar, Editor dapat melihat, melakukan star, serta memperbarui data, sedangkan Superuser memiliki akses penuh untuk melakukan operasi CRUD dan star.

   Pemeriksaan hak akses harus dilakukan pada server melalui permission class karena menyembunyikan tombol pada template hanya membatasi tampilan antarmuka, bukan benar-benar melindungi API. Pengguna masih dapat mengirimkan HTTP request secara langsung melalui browser Developer Tools, Postman, atau tools lainnya tanpa menggunakan tombol pada halaman website. Jika pembatasan hanya dilakukan pada frontend, pengguna yang tidak memiliki izin masih berpotensi mengakses endpoint secara langsung.

   Dengan menerapkan permission class pada server, setiap request tetap diperiksa berdasarkan hak akses pengguna sebelum operasi dijalankan. Dengan demikian, keamanan API tidak hanya bergantung pada tampilan frontend, tetapi juga pada aturan akses yang diterapkan di sisi server.

4. Request yang mengubah data tetap memerlukan token CSRF ketika API menggunakan `SessionAuthentication` karena autentikasi berbasis session memanfaatkan cookie yang disimpan oleh browser. Browser dapat mengirimkan cookie session secara otomatis ketika melakukan request ke website yang bersangkutan. Kondisi ini dapat dimanfaatkan dalam serangan Cross-Site Request Forgery (CSRF), yaitu ketika pengguna yang sudah login tanpa sadar diarahkan untuk mengirimkan request yang tidak diinginkan.

   Token CSRF digunakan untuk memastikan bahwa request yang mengubah data berasal dari halaman aplikasi yang sah. Pada implementasi Education API, token CSRF dikirimkan melalui header `X-CSRFToken` pada setiap request yang melakukan perubahan data, seperti `POST`, `PATCH`, `PUT`, dan `DELETE`. Dengan demikian, server dapat memeriksa token tersebut sebelum memproses request.

   Pengujian menggunakan `force_authenticate` saja tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan karena metode tersebut secara langsung menetapkan pengguna yang terautentikasi pada request untuk keperluan testing. Proses tersebut melewati mekanisme autentikasi session normal sehingga tidak menguji pengiriman cookie session dan pemeriksaan CSRF sebagaimana yang terjadi pada request dari browser.

   Oleh karena itu, pada pengujian CSRF Education API, saya menggunakan `APIClient(enforce_csrf_checks=True)` dan melakukan login menggunakan session. Setelah memperoleh token CSRF, saya menguji request perubahan data tanpa token dan memastikan request ditolak. Saya juga menguji request dengan token yang valid untuk memastikan operasi yang diizinkan dapat berhasil. Dengan cara tersebut, pengujian dapat membuktikan bahwa perlindungan CSRF benar-benar berjalan pada mekanisme autentikasi session.

**### AI Disclosure Tugas 6**

Dalam pengerjaan Tugas 6, saya menggunakan **ChatGPT dan Codex** sebagai AI assistant dengan peran yang berbeda. ChatGPT saya gunakan untuk membantu memahami konsep Django REST Framework, menganalisis requirement tugas, menyusun tahapan implementasi, melakukan code review, debugging, serta menyusun dokumentasi. Sementara itu, Codex saya gunakan untuk membantu mengimplementasikan perubahan secara langsung pada repository project dan memeriksa hasil implementasinya.

Beberapa bagian yang dibantu oleh AI meliputi:

* Menganalisis requirement Tugas 6 dan menentukan model `Education` sebagai model yang digunakan untuk implementasi REST API.
* Membantu memahami konsep REST, HTTP method, serializer, autentikasi, otorisasi, permission class, dan CSRF protection.
* Membantu merancang struktur REST API, termasuk endpoint, serializer, permission, API views, dan URL routing.
* Membantu mengimplementasikan fitur star menggunakan relasi ManyToMany antara model `Education` dan pengguna.
* Membantu mengintegrasikan frontend halaman Education dengan REST API, termasuk fitur search, create, edit, star, dan delete tanpa reload halaman.
* Membantu menyusun serta memeriksa automated tests untuk menguji akses berdasarkan role, validasi data, operasi CRUD, fitur star, dan perlindungan CSRF.
* Membantu melakukan audit terhadap komentar dan docstring agar kode lebih mudah dipahami dan dipelihara.
* Membantu menyusun jawaban refleksi dan dokumentasi pengerjaan Tugas 6.

**#### AI Limitations and Manual Improvements**

Saya menyadari bahwa AI tidak selalu mengetahui kondisi terbaru dari repository dan tidak dapat langsung mengasumsikan bahwa struktur project sesuai dengan contoh umum Django. Karena itu, implementasi dilakukan dengan tetap mempertahankan struktur dan fitur yang sudah ada, khususnya REST API Experience dari Tutorial 07 dan halaman Education yang telah dibuat pada tugas sebelumnya.

Salah satu hal yang perlu diperhatikan selama pengerjaan adalah bahwa implementasi frontend dan backend harus memiliki aturan akses yang konsisten. Tombol yang ditampilkan pada frontend tidak dapat dijadikan satu-satunya mekanisme pembatasan akses. Oleh karena itu, permission tetap diperiksa pada server untuk memastikan setiap pengguna hanya dapat melakukan tindakan sesuai dengan role-nya.

Selain itu, pada proses integrasi fitur search, ditemukan kemungkinan hasil request yang lebih lama ditampilkan setelah pengguna melakukan pencarian baru. Hal tersebut diperbaiki dengan menggunakan penanda urutan request sehingga hanya hasil dari request terbaru yang digunakan. Perbaikan ini dilakukan agar hasil pencarian tetap sesuai dengan input terakhir pengguna.

Setiap perubahan dari AI tetap diperiksa dengan membandingkannya terhadap requirement tugas dan kode project yang sebenarnya. Saya juga melakukan pengujian menggunakan automated tests dan browser testing untuk memeriksa perilaku aplikasi dari sisi pengguna. Pengujian tersebut mencakup hak akses Visitor, Normal User, Editor, dan Superuser, serta memastikan fitur-fitur pada Tutorial 07 tetap berfungsi.

Dengan demikian, AI digunakan sebagai alat bantu untuk memahami konsep, mempercepat proses implementasi, dan membantu menemukan masalah. Keputusan akhir mengenai perubahan kode, kesesuaian requirement, dan hasil pengujian tetap didasarkan pada pemeriksaan terhadap project yang dikerjakan.

**#### AI Working Log / Prompting Log**

Dokumentasi percakapan yang digunakan sebagai AI working log dan prompting log selama pengerjaan Tugas 6 dapat diakses melalui:

https://chatgpt.com/share/6af1df66-6bd8-83ec-a9f2-68864ecf120a

Proses pengerjaan dilakukan secara bertahap, mulai dari memahami requirement, menentukan rancangan REST API, mengimplementasikan backend, mengintegrasikan frontend, melakukan testing, hingga menyempurnakan komentar dan dokumentasi.

**Prompting approach:**

Saya memberikan konteks project, requirement tugas, struktur file, serta kondisi implementasi terbaru kepada AI sebelum meminta bantuan. Saya menggunakan pendekatan bertahap dengan memisahkan pembahasan konsep, perencanaan implementasi, code review, dan debugging. Untuk perubahan kode yang dilakukan menggunakan Codex, saya memberikan instruksi yang spesifik mengenai file yang boleh diubah, fitur yang harus dipertahankan, serta batasan perubahan agar implementasi tidak merusak fitur sebelumnya.

Setelah perubahan dilakukan, saya memeriksa hasilnya melalui code review, automated tests, dan browser testing. Ketika ditemukan error atau ketidaksesuaian, saya memberikan hasil error atau testing tersebut sebagai konteks untuk proses debugging berikutnya. Dengan pendekatan ini, penggunaan AI tetap terarah dan setiap hasil implementasi diverifikasi berdasarkan kondisi project yang sebenarnya.