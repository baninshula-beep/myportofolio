const experienceConfig = window.experienceConfig;

let experiencesAbortController = null;
let searchDebounceTimer = null;

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
 *
 * Hal ini penting agar data Experience yang berasal
 * dari database tidak dapat menyisipkan HTML atau script.
 */
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

    const modalId = `delete-experience-${pk}`;
    const modalTitleId = `delete-experience-title-${pk}`;

    /*
     * Jika Experience memiliki ended_at,
     * tampilkan rentang tanggal lengkap.
     *
     * Jika tidak, Experience dianggap masih berlangsung.
     */
    const dateRange = fields.ended_at
        ? `${escapeHtml(fields.started_at)} - ${escapeHtml(fields.ended_at)}`
        : `${escapeHtml(fields.started_at)} - Present`;

    const status = fields.is_ongoing
        ? "<span>· Sedang berlangsung</span>"
        : "<span>· Selesai</span>";

    /*
     * Thumbnail hanya dibuat jika endpoint
     * mengembalikan thumbnail_url.
     */
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

    /*
     * Editor dan superuser dapat melihat tombol Edit.
     */
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

    /*
     * Hanya superuser yang dapat menghapus Experience.
     */
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

    /*
     * Modal konfirmasi delete hanya dibuat
     * untuk superuser.
     */
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

    /*
     * Label star berubah berdasarkan status
     * Experience untuk user saat ini.
     */
    const starLabel = fields.is_starred
        ? "★ Unstar"
        : "☆ Star";

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

                    <form
                        method="post"
                        action="${starUrl}"
                    >
                        <input
                            type="hidden"
                            name="csrfmiddlewaretoken"
                            value="${escapeHtml(CSRF_TOKEN)}"
                        >

                        <button
                            type="submit"
                            class="button"
                        >
                            ${starLabel}
                            (${fields.star_count})
                        </button>
                    </form>

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
async function fetchExperiences(query = "") {
    /*
     * Batalkan request sebelumnya jika user
     * mengetik pencarian baru sebelum request
     * sebelumnya selesai.
     */
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

        /*
         * Search query hanya dikirim jika tidak kosong.
         */
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

        /*
         * Bersihkan hasil rendering sebelumnya.
         */
        gridContainer.innerHTML = "";

        /*
         * Jika tidak ada data, tampilkan empty state.
         */
        if (experiences.length === 0) {
            displayPageSection({
                showEmpty: true,
            });

            return;
        }

        /*
         * Render setiap Experience ke dalam grid.
         */
        experiences.forEach((experience) => {
            gridContainer.insertAdjacentHTML(
                "beforeend",
                buildExperienceCard(experience)
            );
        });

        /*
         * Setelah data berhasil dirender,
         * tampilkan grid.
         */
        displayPageSection({
            showGrid: true,
        });

    } catch (error) {

        /*
         * AbortError bukan error sebenarnya.
         * Request tersebut memang sengaja dibatalkan
         * karena ada request baru.
         */
        if (error.name === "AbortError") {
            return;
        }

        console.error(
            "Failed to fetch experiences:",
            error
        );

        displayPageSection({
            showError: true,
        });
    }
}


/*
 * Search melalui tombol Cari.
 */
searchForm.addEventListener(
    "submit",
    (event) => {
        event.preventDefault();

        fetchExperiences(
            searchInput.value.trim()
        );
    }
);


/*
 * Debounce search.
 *
 * Request baru hanya dikirim 300 ms setelah
 * user berhenti mengetik.
 */
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
            300
        );
    }
);


/*
 * Load seluruh Experience ketika halaman
 * pertama kali dibuka.
 */
fetchExperiences(
    searchInput.value.trim()
);