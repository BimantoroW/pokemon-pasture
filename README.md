### Cara pengimplementasian *checklist*
1. Untuk membuat *project* saya, saya menjalankan *command* `django-admin startproject pokemon_pasture`. *Command* ini akan menghasilkan kode awal yang dibutuhkan untuk memulai *project* Django. Setelah itu, di *file* `settings.py`, tambahkan `'*'` pada `ALLOWED_HOSTS`
2. Untuk membuat aplikasi *main*, saya menjalankan *command* `python manage.py startapp main`. *Command* ini akan menghasilkan struktur direktori dasar dari suatu aplikasi. Setelah membuat aplikasi, kita perlu mendaftarkannya ke proyek dengan cara menambahkan `main` ke `INSTALLED_APPS` di `settings.py` dalam `pokemon_pasture`
3. Untuk melakukan *routing* ke aplikasi *main*, buat sebuah file bernama `urls.py` di dalam direktori `main`. Dalam *file* tersebut, import `path` dari `django.urls` dan import fungsi dari `views.py` untuk menampilkan *template* `main.html`. Setelah itu, buat sebuah variabel bernama `urlpatterns` yang akan berupa sebuah *list*, kemudian isi *list* dengan `path('', show_main, name='main')`. Kode ini akan memanggil fungsi `show_main` apabila ada seorang *user* yang mencoba mengakses `https://pokemon-pasture.adaptable.app/main`. Setelah dipanggil, `show_main` akan mengembalikan template `main.html` untuk ditampilkan ke *user*.
4. Buka *file* `main/models.py` dan buat sebuah *class* baru bernama `Item` yang meng-*inherit* dari `models.Model`. Kemudian, buat atribut `name` dengan tipe `CharField` dan `max_length=255`, atribut `amount` dengan tipe `IntegerField`, dan atribut `description` dengan tipe `TextField`. Selain ketiga atribut di atas, saya juga menambahkan atribut `owner` dengan atribut `CharField` dan `max_length=255` untuk merepresentasikan pemilik dari sebuah *pokemon*. Setelah *model* dibuat, kita perlu menjalankan `python manage.py makemigrations` dan `python manage.py migrate` untuk meng-*update* basis data proyek kita.
5. Pada `main/views.py`, import `render` dari `django.shortcuts` dan import `Item` dari `.models`. Kemudian, buat sebuah fungsi dengan nama bebas dan satu argumen `request` yang merepresentasikan HTTP *request* dari *user*, di sini saya menamakan fungsinya `show_main`. Fungsi ini akan mempersiapkan semua data yang diperlukan sebelum memberi data tersebut ke `main.html` sekaligus menampilkannya. Untuk memberi datanya ke *file* html, kita gunakan sebuah *dictionary* yang pada nantinya dapat diakses dari *file* html kita. Setelah membuat *dictionary*-nya, kita dapat me-*render* html-nya dengan mengembalikan `render(request, 'main.html', context)`. Argumen pertama dari `render` merupakan HTTP *request* dari *user*, argumen kedua merupakan *file* html yang ingin ditampilkan, dan argumen terakhir merupakan data yang ingin kita berikan kepada *file* html tersebut.
6. Setelah menambahkan *url* `main/` di level aplikasi, kita perlu menambahkan *url* ini di level proyek. Untuk melakukan hal itu, kita perlu pergi ke *file* `urls.py` di *folder* `pokemon_pasture` dan menambahkan `path('main/', include('main.urls'))` di variabel `urlpatterns`. Jangan lupa untuk meng-*import* `include` dari `django.urls` terlebih dahulu.
7. Untuk men-*deploy* ke Adaptable, kita perlu membuat *repository* di GitHub terlebih dahulu. Setelah membuatnya, kita perlu mem-*push* kode kita ke *repository* itu. Jangan lupa untuk membuat file `.gitignore` agar *file* yang tidak diperlukan tidak ikut di-*push*. Kemudian, *log in* ke Adaptable.io dengan akun GitHub kita. Setelah itu, hubungkan *repository* GitHub kita ke Adaptable dan buat *app* baru di Adaptable dengan memilih proyek GitHub kita. Selanjutnya, pilih *Python App Template* untuk *template*-nya dan PostgreSQL untuk basis datanya. Kemudian, sesuaikan versi Python-nya dengan versi Python yang kita gunakan untuk mengembangkan proyek kita. Terakhir, pada *start command*, gunakan *command* `python manage.py migrate && gunicorn pokemon_pasture.wsgi`. Masukkan nama aplikasi dan centang *HTTP Listener Port* sebelum men-*deploy*.

### Bagan *request-response* Django
![Django Request-Response Diagram](django_diagram.jpg)
1. HTTP *request* dari *user* akan ditangkap oleh `urls.py`
2. Kemudian, fungsi `show_view` yang kita masukkan dalam `path('path/', show_view, name='view')` akan dipanggil
3. Apabila diperlukan, dalam fungsi itu, kita dapat mengambil data dari basis data kita melalui kelas-kelas dalam `models.py`.
4. Data-data ini kemudian dapat kita tampilkan dalam *file* html `template` kita dengan cara membuat sebuah *dicrionary* `context`.
5. Setelah semua persiapan selesai, `show_view` akan mengembalikan `render(request, '<filename>.html', context)` untuk menampilkan *file* html yang sudah sesuai kepada *user*.

### Mengapa kita perlu *virtual environment*?
*Virtual environment* merupakan suatu cara untuk mengisolasi proyek Python kita dari instalasi Python global dan dari proyek Python yang lainnya. Dalam setiap *virtual environment*, kita dapat memiliki versi Python yang berbeda serta memiliki *package* dan *dependencies* yang berbeda juga. Karena kita seringkali ingin membuat banyak proyek Django dalam satu komputer yang membutuhkan versi Python dan *package/dependencies* yang berbeda-beda, penggunaan *virtual environment* sangat direkomendasikan apabila kita ingin mengembangkan proyek Django. Walaupun demikian, kita tetap saja dapat membuat proyek Django tanpa *virtual environment*. Namun, ini sangat tidak disarankan karena alasan-alasan yang telah disebut di atas. Tanpa *virtual environment*, kita tidak bisa memisahkan tiap proyek Django kita ke dalam lingkungannya masing-masing yang rapi dan bersih. Selain itu, jika kita ingin membuat proyek baru yang menggunakan versi Python atau *package/dependencies* yang berbeda dengan proyek kita yang terakhir, itu akan menjadi sangat rumit karena kita harus meng-*uninstall* versi yang lama terlebih dahulu baru meng-*install* versi yang baru. Dengan *virtual environment*, kedua versi tersebut dapat hidup di lingkungannya masing-masing tanpa mengganggu satu sama lain.

### Pengertian MVC, MVT, dan MVVM, serta perbedaannya
MVC (Model-View-Controller), MVT (Model-View-Template), dan MVVM (Model-View-ViewModel) merupakan pola arsitektur pengenmbangan *software*. Pola arsitektur ini berguna untuk memisahkan logika bisnis dengan tampilan pengguna. Pola arsitektur memberikan modularitas pada *file* proyek dan memastikan bahwa semua kode tercakup dalam *unit testing*. Hal ini memudahkan seorang *developer* untuk memelihara aplikasi dan memperluas fitur aplikasi di masa depan.
1. MVC (Model-View-Controller)
   1. Model
   Komponen ini menyimpan data aplikasi. Komponen ini tidak memiliki pengetahuan mengenai tampilan pengguna. Komponen ini bertanggungjawab atas penanganan *domain logic* dan komunikasi dengan *database*
   2. View
   Komponen ini adalah komponen *user interface*. Komponen ini menyediakan visualisasi data yang disimpan dalam model dan menawarkan interaksi kepada pengguna.
   3. Controller
   Komponen ini adalah komponen yang menjembatani *model* dan *view*. Komponen ini mengendalikan aliran data ke *model* dan memperbarui *view* apabila ada data yang berubah.
2. MVT
   1. Model
   Sama seperti *model* di MVC, *model* di MVT berguna untuk menyimpan data aplikasi. Komponen ini juga menangani komunikasi dengan *database*
   2. View
   *View* dalam MVT mirip dengan *controller* di MVC. *View* menjalankan logika bisnis, berinteraksi dengan *model*, dan merender template. *View* merupakan jembatan antara *model* dengan *template*. *View* menerima permintaan HTTP dan kemudian mengembalikan respons HTTP.
   3. Template
   *Template* adalah komponen yang membuat MVT berbeda dari MVC. *Template* bertindak sebagai lapisan presentasi dan pada dasarnya adalah kode HTML yang merender data. Konten dalam *file* ini dapat bersifat statis atau dinamis.
3. MVVM
   1. Model
   Sama seperti MVC dan MVT, komponen *model* berguna untuk menyimpan data aplikasi. Dalam MVVM, *model* dan *viewmodel* bekerja sama untuk mendapatkan dan menyimpan data.
   2. View
   Komponen *user interface*. *View* akan memberitahukan *ViewModel* mengenai tindakan-tindakan yang dilakukan *user* agar data aplikasi dapat di-*update* apabila ada perubahan.
   3. ViewModel
   *ViewModel* mengekspos data-data yang relevan bagi *view*. Selain itu, jika *user* melakukan sesuatu seperti meng-input data, *ViewModel* akan meng-*update* komponen model. *ViewModel* mirip dengan komponen *controller* di MVC dan *view* di MVT.