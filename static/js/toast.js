let toastTimer;

function showToast(title, message, type = "normal", duration = 3000) {
    const toastComponent = document.getElementById("toast-component");
    const toastTitle = document.getElementById("toast-title");
    const toastMessage = document.getElementById("toast-message");

    if (!toastComponent) {
        return;
    }

    // Hapus class tipe sebelumnya agar styling tidak bertumpuk.
    toastComponent.classList.remove(
        "toast-success",
        "toast-error",
        "toast-normal"
    );

    // Terapkan class berdasarkan tipe notifikasi.
    if (type === "success") {
        toastComponent.classList.add("toast-success");
    } else if (type === "error") {
        toastComponent.classList.add("toast-error");
    } else {
        toastComponent.classList.add("toast-normal");
    }

    // Perbarui isi toast dengan textContent agar aman dari HTML injection.
    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // Batalkan timer sebelumnya jika toast sedang aktif.
    clearTimeout(toastTimer);

    // Tampilkan toast di browser top layer.
    if (!toastComponent.matches(":popover-open")) {
        toastComponent.showPopover();

        // Paksa browser menghitung ulang style agar transisi berjalan.
        void toastComponent.offsetHeight;
    }

    // Jalankan animasi masuk.
    toastComponent.classList.remove("toast-hidden");
    toastComponent.classList.add("toast-show");

    // Sembunyikan toast setelah durasi selesai.
    toastTimer = setTimeout(() => {
        toastComponent.classList.remove("toast-show");
        toastComponent.classList.add("toast-hidden");

        // Tunggu animasi keluar selesai sebelum menutup popover.
        toastTimer = setTimeout(() => {
            toastComponent.hidePopover();
        }, 300);
    }, duration);
}