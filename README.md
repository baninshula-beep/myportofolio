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
