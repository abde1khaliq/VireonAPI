
document.addEventListener("DOMContentLoaded", function () {
    const sidebarLinks = document.querySelectorAll(".sidebar-link");
    const panels = document.querySelectorAll(".content-panel");

    sidebarLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            sidebarLinks.forEach((l) => l.classList.remove("active"));
            panels.forEach((p) => p.classList.remove("active"));
            this.classList.add("active");
            const panelId = this.getAttribute("data-panel") + "-panel";
            document.getElementById(panelId).classList.add("active");
        });
    });

    // Modal functionality
    const newKeyModal = document.getElementById("newKeyModal");
    const createKeyBtn = document.getElementById("createKeyBtn");
    const closeModal = document.getElementById("closeModal");
    const cancelModal = document.getElementById("cancelModal");

    function closeModalFunc() {
        newKeyModal.classList.remove("active");
        document.getElementById("keyNameInput").value = "";
        document.getElementById("keyResponse").style.display = "none";
        document.getElementById("keyResponse").innerHTML = "";
    }

    if (createKeyBtn) {
        createKeyBtn.addEventListener("click", function () {
            newKeyModal.classList.add("active");
        });
    }
    if (closeModal) closeModal.addEventListener("click", closeModalFunc);
    if (cancelModal) cancelModal.addEventListener("click", closeModalFunc);
    newKeyModal.addEventListener("click", function (e) {
        if (e.target === newKeyModal) closeModalFunc();
    });

    // Submit key creation
    const submitBtn = document.getElementById("submitKeyBtn");
    submitBtn.addEventListener("click", async () => {
        const keyName = document.getElementById("keyNameInput").value.trim();
        const responseBox = document.getElementById("keyResponse");

        if (!keyName) {
            responseBox.textContent = "Please enter a key name.";
            responseBox.style.display = "block";
            return;
        }

        // Simulate API call
        setTimeout(() => {
            responseBox.innerHTML = `
            <strong>API Key created:</strong>
            <code>vi_2x4y6z8a0b2c4e6g8i0k2m4o6q8s0u2w</code>
            <button class="btn" onclick="navigator.clipboard.writeText('vi_2x4y6z8a0b2c4e6g8i0k2m4o6q8s0u2w')">Copy</button>
            <small style="display:block;margin-top:4px;">Store this key now—it won’t be shown again.</small>
          `;
            responseBox.style.display = "block";
        }, 500);
    });
});
