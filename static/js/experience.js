const experienceConfig = window.experienceConfig;

let experiencesAbortController = null;
let searchDebounceTimer = null;
const pendingStarExperienceIds = new Set();

const SEARCH_DEBOUNCE_DELAY = 300;

const loadingState = document.getElementById("loading");
const errorState = document.getElementById("error");
const emptyState = document.getElementById("empty");
const gridContainer = document.getElementById("grid");

const searchForm = document.getElementById(
    "experience-search-form"
);

const searchInput = document.getElementById(
    "search-input"
);

const csrfInput = document.querySelector(
    "#csrf-form input[name='csrfmiddlewaretoken']"
);

const CSRF_TOKEN = csrfInput
    ? csrfInput.value
    : "";


/*
 * Menampilkan state halaman sesuai kondisi request AJAX.
 *
 * Hanya satu state utama yang ditampilkan pada satu waktu:
 * loading, error, empty, atau grid.
 */
function displayPageSection({
    showLoading = false,
    showError = false,
    showEmpty = false,
    showGrid = false,
}) {
    loadingState.classList.toggle(
        "hide",
        !showLoading
    );

    errorState.classList.toggle(
        "hide",
        !showError
    );

    emptyState.classList.toggle(
        "hide",
        !showEmpty
    );

    gridContainer.classList.toggle(
        "hide",
        !showGrid
    );
}


/*
 * Escape HTML sebelum data dari server dimasukkan
 * ke dalam innerHTML.
 */

// Escape nilai dari server sebelum dimasukkan ke innerHTML
// untuk mencegah eksekusi HTML atau script yang berasal dari data pengguna.
function escapeHtml(value) {
    const div = document.createElement("div");

    div.textContent = value ?? "";

    return div.innerHTML;
}


/*
 * Membuat URL berdasarkan URL template Django
 * yang memiliki placeholder UUID.
 */
function buildExperienceUrl(baseUrl, experienceId) {
    return baseUrl.replace(
        "00000000-0000-0000-0000-000000000000",
        experienceId
    );
}


/*
 * Membuat satu Experience card dari object JSON.
 */
function buildExperienceCard(experience) {
    const { pk, fields } = experience;

    const editUrl = buildExperienceUrl(
        experienceConfig.editUrl,
        pk
    );

    const deleteUrl = buildExperienceUrl(
        experienceConfig.deleteUrl,
        pk
    );

    const starUrl = buildExperienceUrl(
        experienceConfig.starUrl,
        pk
    );

    const starApiUrl = buildExperienceUrl(
        experienceConfig.starApiUrl,
        pk
    );

    const modalId = `delete-experience-${pk}`;
    const modalTitleId = `delete-experience-title-${pk}`;

    const dateRange = fields.ended_at
        ? `${escapeHtml(fields.started_at)} - ${escapeHtml(fields.ended_at)}`
        : `${escapeHtml(fields.started_at)} - Present`;

    const status = fields.is_ongoing
        ? "<span>· Sedang berlangsung</span>"
        : "<span>· Selesai</span>";

    const thumbnail = fields.thumbnail_url
        ? `
            <div class="experience-image">
                <img
                    src="${escapeHtml(fields.thumbnail_url)}"
                    alt="${escapeHtml(fields.title)}"
                >
            </div>
        `
        : "";

    const editButton = (
        experienceConfig.isSuperuser ||
        experienceConfig.isEditor
    )
        ? `
            <a
                href="${editUrl}"
                class="button"
            >
                Edit
            </a>
        `
        : "";

    const deleteButton = experienceConfig.isSuperuser
        ? `
            <button
                type="button"
                class="button button-danger"
                popovertarget="${modalId}"
            >
                Hapus
            </button>
        `
        : "";

    const deleteModal = experienceConfig.isSuperuser
        ? `
            <div
                id="${modalId}"
                class="education-delete-modal"
                popover="auto"
                role="dialog"
                aria-modal="true"
                aria-labelledby="${modalTitleId}"
            >
                <button
                    type="button"
                    class="education-delete-modal__backdrop"
                    popovertarget="${modalId}"
                    popovertargetaction="hide"
                    aria-label="Tutup konfirmasi hapus"
                ></button>

                <div class="education-delete-modal__content">

                    <button
                        type="button"
                        class="education-delete-modal__close"
                        popovertarget="${modalId}"
                        popovertargetaction="hide"
                        aria-label="Tutup konfirmasi hapus"
                    >
                        ×
                    </button>

                    <h2 id="${modalTitleId}">
                        Hapus Experience?
                    </h2>

                    <p>
                        Apakah kamu yakin ingin menghapus
                        <strong>
                            ${escapeHtml(fields.title)}
                        </strong>?
                    </p>

                    <div class="education-delete-modal__actions">

                        <button
                            type="button"
                            class="button button-secondary"
                            popovertarget="${modalId}"
                            popovertargetaction="hide"
                        >
                            Batal
                        </button>

                        <form
                            method="post"
                            action="${deleteUrl}"
                        >
                            <input
                                type="hidden"
                                name="csrfmiddlewaretoken"
                                value="${escapeHtml(CSRF_TOKEN)}"
                            >

                            <button
                                type="submit"
                                class="button button-danger"
                            >
                                Ya, Hapus
                            </button>
                        </form>

                    </div>

                </div>

            </div>
        `
        : "";

    const starLabel = fields.is_starred
        ? "★ Unstar"
        : "☆ Star";
    const isStarPending = pendingStarExperienceIds.has(String(pk));

    const starControl = experienceConfig.isAuthenticated
        ? `
            <form
                method="post"
                action="${starUrl}"
                class="experience-star-form"
                data-experience-id="${escapeHtml(pk)}"
                data-api-url="${escapeHtml(starApiUrl)}"
            >
                <input
                    type="hidden"
                    name="csrfmiddlewaretoken"
                    value="${escapeHtml(CSRF_TOKEN)}"
                >

                <button
                    type="submit"
                    class="button"
                    data-star-button
                    data-star-label="${escapeHtml(starLabel)}"
                    data-star-count="${escapeHtml(fields.star_count)}"
                    aria-pressed="${fields.is_starred}"
                    ${isStarPending ? "disabled aria-busy=\"true\"" : ""}
                >
                    ${isStarPending
                        ? `Memproses Star... (${fields.star_count})`
                        : `${starLabel} (${fields.star_count})`}
                </button>

            </form>
        `
        : `
            <a
                href="${escapeHtml(experienceConfig.loginUrl)}"
                class="button"
            >
                Login untuk memberi Star (${fields.star_count})
            </a>
        `;

    return `
        <article class="experience-card">

            ${thumbnail}

            <div class="experience-card-content">

                <p class="experience-date">
                    ${dateRange}
                    ${status}
                </p>

                <h2>
                    ${escapeHtml(fields.title)}
                </h2>

                <p class="experience-role">
                    ${escapeHtml(fields.category)}
                </p>

                <p class="experience-description">
                    ${escapeHtml(fields.description)
                        .replace(/\n/g, "<br>")}
                </p>

                <div class="project-actions">

                    ${editButton}

                    ${deleteButton}

                    ${starControl}

                </div>

            </div>

            ${deleteModal}

        </article>
    `;
}


/*
 * Mengambil data Experience dari endpoint Django
 * menggunakan Fetch API.
 */

// Request pencarian sebelumnya dibatalkan ketika query baru dikirim
// agar hasil response yang sudah tidak relevan tidak menggantikan hasil terbaru.
async function fetchExperiences(query = "") {
    if (experiencesAbortController) {
        experiencesAbortController.abort();
    }

    experiencesAbortController = new AbortController();

    displayPageSection({
        showLoading: true,
    });

    try {
        const url = new URL(
            experienceConfig.endpoint,
            window.location.origin
        );

        if (query) {
            url.searchParams.set(
                "title",
                query
            );
        }

        const response = await fetch(
            url,
            {
                method: "GET",
                signal: experiencesAbortController.signal,
            }
        );

        if (!response.ok) {
            throw new Error(
                `HTTP error: ${response.status}`
            );
        }

        const experiences = await response.json();

        gridContainer.innerHTML = "";

        if (experiences.length === 0) {
            displayPageSection({
                showEmpty: true,
            });

            return true;
        }

        experiences.forEach((experience) => {
            gridContainer.insertAdjacentHTML(
                "beforeend",
                buildExperienceCard(experience)
            );
        });

        displayPageSection({
            showGrid: true,
        });
        return true;

    } catch (error) {

        if (error.name === "AbortError") {
            return "aborted";
        }

        console.error(
            "Failed to fetch experiences:",
            error
        );

        displayPageSection({
            showError: true,
        });
        return false;
    }
}




/*
 * Mengambil nilai cookie berdasarkan nama cookie.
 *
 * Cookie csrftoken digunakan sebagai header
 * X-CSRFToken untuk request yang mengubah data melalui Fetch API.
 */
function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const trimmedCookie = cookie.trim();

        if (trimmedCookie.startsWith(`${name}=`)) {
            return decodeURIComponent(
                trimmedCookie.substring(name.length + 1)
            );
        }
    }

    return null;
}


/*
 * Toggle Star melalui API. Tombol dikunci selama request berlangsung,
 * lalu daftar di-refresh dari endpoint JSON legacy setelah sukses.
 */
async function updateExperienceStar(event) {
    const starForm = event.target.closest(
        ".experience-star-form"
    );

    if (!starForm || !gridContainer.contains(starForm)) {
        return;
    }

    event.preventDefault();

    const experienceId = starForm.dataset.experienceId;
    if (pendingStarExperienceIds.has(experienceId)) {
        return;
    }

    const button = starForm.querySelector("[data-star-button]");

    if (!button) {
        return;
    }

    const csrfToken = getCookie("csrftoken") || CSRF_TOKEN;

    pendingStarExperienceIds.add(experienceId);
    setStarPendingUI(experienceId, true);
    const requestController = new AbortController();
    const timeoutId = setTimeout(
        () => requestController.abort(),
        15000
    );

    try {
        const response = await fetch(
            starForm.dataset.apiUrl,
            {
                method: "POST",
                credentials: "same-origin",
                signal: requestController.signal,
                headers: {
                    "Accept": "application/json",
                    "X-CSRFToken": csrfToken,
                },
            }
        );

        if (!response.ok) {
            let result = {};
            try {
                result = await response.json();
            } catch (error) {
                // The response body may be unavailable; reconcile from the list below.
            }
            throw new Error(response.status === 403
                ? "Sesi login atau token keamanan tidak valid. Silakan login kembali."
                : result.detail || "Star tidak dapat diperbarui. Silakan coba lagi.");
        }

        const result = await response.json();
        if (
            typeof result.star_count !== "number" ||
            typeof result.is_starred !== "boolean"
        ) {
            throw new Error("Respons Star tidak dapat dibaca dengan benar.");
        }

        const refreshResult = await refreshExperiencesForCurrentSearch();
        if (refreshResult === false) {
            showToast(
                "Star berhasil diperbarui",
                "Daftar Experience gagal disegarkan. Muat ulang daftar untuk melihat status terbaru.",
                "error"
            );
        }

    } catch (error) {
        console.error("Failed to update experience star:", error);
        const refreshResult = await refreshExperiencesForCurrentSearch();
        const message = error.name === "AbortError"
            ? "Request Star melewati batas waktu; status server sedang disinkronkan."
            : error.message || "Terjadi kesalahan saat menghubungi server.";
        const refreshMessage = refreshResult === true
            ? "Daftar telah disegarkan dari server."
            : refreshResult === "aborted"
                ? "Penyegaran daftar terbaru masih berjalan."
                : "Refresh daftar juga gagal; coba muat ulang halaman.";
        showToast(
            refreshResult === false
                ? "Status Star belum dapat disinkronkan"
                : "Gagal mengonfirmasi perubahan Star",
            `${message} ${refreshMessage}`,
            "error"
        );

    } finally {
        clearTimeout(timeoutId);
        pendingStarExperienceIds.delete(experienceId);
        setStarPendingUI(experienceId, false);
    }
}


function setStarPendingUI(experienceId, isPending) {
    gridContainer
        .querySelectorAll(".experience-star-form[data-experience-id]")
        .forEach((form) => {
            if (form.dataset.experienceId !== experienceId) {
                return;
            }

            const button = form.querySelector("[data-star-button]");
            if (!button) {
                return;
            }

            button.disabled = isPending;
            if (isPending) {
                button.setAttribute("aria-busy", "true");
                button.textContent = `Memproses Star... (${button.dataset.starCount})`;
            } else {
                button.removeAttribute("aria-busy");
                button.textContent = `${button.dataset.starLabel} (${button.dataset.starCount})`;
            }
        });
}


function refreshExperiencesForCurrentSearch() {
    return fetchExperiences(
        searchInput ? searchInput.value.trim() : ""
    );
}


/*
 * Menampilkan error validasi dari response AJAX
 * ke dalam form tambah Experience.
 */
function displayCreateExperienceErrors(errors) {
    const errorContainer = document.getElementById(
        "create-experience-errors"
    );

    if (!errorContainer) {
        return;
    }

    const messages = [];

    Object.entries(errors).forEach(
        ([fieldName, fieldErrors]) => {
            fieldErrors.forEach((error) => {
                messages.push(
                    `${fieldName}: ${error.message}`
                );
            });
        }
    );

    errorContainer.innerHTML = messages
        .map(
            (message) =>
                `<p>${escapeHtml(message)}</p>`
        )
        .join("");

    errorContainer.classList.remove("hide");
}


/*
 * Menghapus error validasi sebelum submit baru.
 */
function clearCreateExperienceErrors() {
    const errorContainer = document.getElementById(
        "create-experience-errors"
    );

    if (!errorContainer) {
        return;
    }

    errorContainer.innerHTML = "";
    errorContainer.classList.add("hide");
}


/*
 * Menutup modal tambah Experience setelah
 * request berhasil diproses.
 */
function closeExperienceModal() {
    const modal = document.getElementById(
        "add-experience-modal"
    );

    if (
        modal &&
        modal.matches(":popover-open")
    ) {
        modal.hidePopover();
    }
}


/*
 * Mengirim form tambah Experience melalui AJAX.
 */
async function addExperience(event) {
    event.preventDefault();

    const experienceForm = document.getElementById(
        "experience-form"
    );

    if (!experienceForm) {
        return;
    }

    const submitButton = experienceForm.querySelector(
        "button[type='submit']"
    );

    clearCreateExperienceErrors();

    if (submitButton) {
        submitButton.disabled = true;
    }

    try {
        const response = await fetch(
            experienceConfig.createEndpoint,
            {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: new FormData(experienceForm),
            }
        );

        const result = await response
            .json()
            .catch(() => ({}));

        if (response.ok) {
            experienceForm.reset();

            closeExperienceModal();

            showToast(
                "Berhasil",
                "Experience baru berhasil ditambahkan!",
                "success"
            );

            await fetchExperiences(
                searchInput.value.trim()
            );

            return;
        }

        if (result.errors) {
            displayCreateExperienceErrors(
                result.errors
            );

            const errorMessages = [];

            Object.values(result.errors).forEach(
                (fieldErrors) => {
                    fieldErrors.forEach((error) => {
                        errorMessages.push(
                            error.message
                        );
                    });
                }
            );

            showToast(
                "Gagal menambahkan experience",
                errorMessages.join(" "),
                "error"
            );

            return;
        }

        showToast(
            "Gagal menambahkan experience",
            result.message ||
                "Terjadi kesalahan saat menambahkan experience.",
            "error"
        );

    } catch (error) {

        console.error(
            "Failed to create experience:",
            error
        );

        showToast(
            "Gagal menambahkan experience",
            "Terjadi kesalahan saat menghubungi server.",
            "error"
        );

    } finally {

        if (submitButton) {
            submitButton.disabled = false;
        }
    }
}


if (searchForm) {
    searchForm.addEventListener(
        "submit",
        (event) => {
            event.preventDefault();

            fetchExperiences(
                searchInput.value.trim()
            );
        }
    );
}


if (gridContainer) {
    gridContainer.addEventListener(
        "submit",
        updateExperienceStar
    );
}


if (searchInput) {
    searchInput.addEventListener(
        "input",
        () => {
            clearTimeout(searchDebounceTimer);

            searchDebounceTimer = setTimeout(
                () => {
                    fetchExperiences(
                        searchInput.value.trim()
                    );
                },
                SEARCH_DEBOUNCE_DELAY
            );
        }
    );
}


const experienceForm = document.getElementById(
    "experience-form"
);

if (experienceForm) {
    experienceForm.addEventListener(
        "submit",
        addExperience
    );
}


fetchExperiences(
    searchInput
        ? searchInput.value.trim()
        : ""
);
