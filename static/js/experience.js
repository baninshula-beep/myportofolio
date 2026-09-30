const experienceConfig = window.experienceConfig;

let experiencesAbortController = null;
let searchDebounceTimer = null;

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

            return;
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

    } catch (error) {

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
 * Mengambil nilai cookie berdasarkan nama cookie.
 *
 * Cookie csrftoken digunakan sebagai header
 * X-CSRFToken untuk request POST melalui Fetch API.
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