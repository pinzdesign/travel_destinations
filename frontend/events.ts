import navigate from "./scripts/navigate.js";
import updateMainMenu from "./scripts/navigate.js";
import checkAddDestinationAccess from "./scripts/navigate.js";
import checkSignupAccess from "./scripts/navigate.js";
import showMessage from "./scripts/showMessage.js";

// Call on page load
document.addEventListener("DOMContentLoaded", updateMainMenu);
document.addEventListener("DOMContentLoaded", checkAddDestinationAccess);
document.addEventListener("DOMContentLoaded", checkSignupAccess);

// Also call after login/signup
function onLoginOrLogout() {
    updateMainMenu();
}

document.addEventListener("click", (e: MouseEvent) => {
    const target = e.target as HTMLElement | null;
    if (!target) return;

    const link = target.closest(".hreflink") as HTMLElement | null;
    if (!link) return;

    e.preventDefault();
    navigate(e);
});

window.addEventListener("popstate", () => {
    navigate();
});

document.addEventListener("DOMContentLoaded", () => {
    navigate();
});

// listen to submit, then check for which form it is by form id
document.addEventListener("submit", async (e: SubmitEvent) => {
    const form = e.target as HTMLFormElement | null;
    if (!form) return;

    // sign up
    if (form.id === "signupForm") {
        e.preventDefault();

        const formData = new FormData(form);

        const data = {
            username: formData.get("new_username") as string | null,
            email: formData.get("new_email") as string | null,
            password: formData.get("new_password") as string | null,
            password_confirm: formData.get("new_passwordConfirm") as string | null
        };

        const response = await fetch("/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result: { success: boolean; message: string } = await response.json();

        showMessage(result, form, "signupMessage");
    }

    // login
    if (form.id === "loginForm") {
        e.preventDefault();

        const formData = new FormData(form);

        const data = {
            username: formData.get("login_username") as string | null,
            password: formData.get("login_password") as string | null
        };

        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const result: { success: boolean; message?: string; token?: string } = await response.json();

        if (result.success && result.token) {
            localStorage.setItem("token", result.token);
            loadProfile();
            onLoginOrLogout();
        }

        showMessage(result, form, "loginMessage");
    }

    // add destination form
    if (form.id === "addDestinationForm") {
        //console.log("add destination runs");
        e.preventDefault();

        const formData = new FormData(form);

        const data = {
            name: formData.get("destination_name") as string | null,
            country: formData.get("destination_country") as string | null,
            description: formData.get("destination_desc") as string | null
        };

        //console.log("Sending data:", data);

        const token = localStorage.getItem("token");

        const response = await fetch("/add_destination", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify(data)
        });

        const result: { success: boolean; message: string } = await response.json();

        showMessage(result, form, "destinationMessage");
    }
});

// Delete destination button
document.addEventListener("click", async (e: MouseEvent) => {
    const target = e.target as HTMLElement | null;
    if (!target) return;

    if (target.classList.contains("delete-destination")) {
        const destId = target.dataset.id;
        if (!destId) return;

        const confirmDelete = confirm("Are you sure you want to delete this destination?");
        if (!confirmDelete) return;

        const token = localStorage.getItem("token");

        try {
            const response = await fetch(`/destination/${destId}`, {
                method: "DELETE",
                headers: {
                    "Authorization": "Bearer " + token
                }
            });

            const result: { success: boolean; message: string } = await response.json();

            if (result.success) {
                // remove card from DOM
                const card = target.closest(".destination-card");
                if (card) card.remove();
            } else {
                alert(result.message);
            }

        } catch (error) {
            console.error("Delete error:", error);
        }
    }
});

// Open Edit form when clicking Edit button
document.addEventListener("click", async (e: MouseEvent) => {
    const target = e.target as HTMLElement | null;
    if (!target) return;

    if (target.classList.contains("edit-destination")) {
        const destId = target.dataset.id;
        if (!destId) return;

        const token = localStorage.getItem("token");

        try {
            const response = await fetch(`/partials/edit_destination/${destId}`, {
                headers: {
                    "Authorization": "Bearer " + token
                }
            });

            if (!response.ok) {
                alert("Cannot edit this destination");
                return;
            }

            const html = await response.text();
            const content = document.getElementById("content");
            if (!content) return;

            content.innerHTML = html;

        } catch (error) {
            console.error("Load edit form error:", error);
        }
    }
});

// Save edited destination
document.addEventListener("submit", async (e: SubmitEvent) => {
    const form = e.target as HTMLFormElement | null;
    if (!form) return;

    if (form.id === "editDestinationForm") {
        e.preventDefault();

        const destId = form.dataset.id;
        if (!destId) return;

        const formData = new FormData(form);
        const data = {
            name: String(formData.get("destination_name") || ""),
            country: String(formData.get("destination_country") || ""),
            description: String(formData.get("destination_desc") || "")
        };

        const token = localStorage.getItem("token");

        try {
            const response = await fetch(`/destination/${destId}`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify(data)
            });

            const result: { success: boolean; message: string } = await response.json();

            showMessage(result, form, "editDestinationMessage");

            if (result.success) {
                // Optionally reload home partial
                navigate(); // will reload home and updated list
            }

        } catch (error) {
            console.error("Save edit error:", error);
        }
    }
});

document.addEventListener("click", (e: MouseEvent) => {
    const target = e.target as HTMLElement | null;
    if (!target) return;

    if (target.id === "logoutBtn") {
        e.preventDefault();
        localStorage.removeItem("token");
        onLoginOrLogout(); // update menu immediately
        navigate(); // redirect to home
    }
});

async function loadProfile() {
    const token = localStorage.getItem("token");
    if (!token) return;

    const response = await fetch("/partials/profile", {
        headers: { "Authorization": "Bearer " + token }
    });

    const html = await response.text();

    const content = document.getElementById("content");
    if (!content) return;

    content.innerHTML = html;  // insert the partial
}