function routeToPartial(pathname: string): string {
    if (pathname === "/") return "/partials/home";
    return "/partials" + pathname;
}

export default async function navigate(e?: Event): Promise<void> {
    let url: string;

    if (e) {
        const target = e.target as HTMLElement | null;
        if (!target) return;

        const anchor = target.closest("a") as HTMLAnchorElement | null;
        if (!anchor) return;

        const href = anchor.getAttribute("href");
        if (!href) return;

        url = href;
        history.pushState({}, "", url);
    } else {
        url = window.location.pathname;
    }

    const partialUrl = routeToPartial(url);

    try {
        const token = localStorage.getItem("token");
        const headers: HeadersInit = token ? { "Authorization": "Bearer " + token } : {};

        const response = await fetch(partialUrl, { headers });

        if (!response.ok) {
            throw new Error("Failed to fetch: " + response.status );
        }

        const html: string = await response.text();

        const content = document.getElementById("content");
        if (!content) return;

        content.innerHTML = html;

        // Update menu after navigation
        updateMainMenu();

        // Page-specific checks
        if (url === "/add_destination") {
            checkAddDestinationAccess();
        }

        if (url === "/signup") {
            checkSignupAccess();
        }

    } catch (error) {
        console.error("Navigation error:", error);
    }
}

// Update main menu based on login status
export function updateMainMenu() {
    const token = localStorage.getItem("token");

    const signUp = document.getElementById("authSignUp");
    const login = document.getElementById("authLogin");
    const profile = document.getElementById("authProfile");
    const logout = document.getElementById("authLogout");

    if (token) {
        // Logged in
        if (signUp) signUp.style.display = "none";
        if (login) login.style.display = "none";
        if (profile) profile.style.display = "";
        if (logout) logout.style.display = "";
    } else {
        // Not logged in
        if (signUp) signUp.style.display = "";
        if (login) login.style.display = "";
        if (profile) profile.style.display = "none";
        if (logout) logout.style.display = "none";
    }
}

// Check login token and toggle Add Destination form
export function checkAddDestinationAccess() {
    const token = localStorage.getItem("token");
    const form = document.getElementById("addDestinationForm") as HTMLFormElement | null;
    const guestMessage = document.getElementById("guestMessage");

    if (token) {
        // Logged in → show form, hide guest message
        if (form) form.style.display = "";
        if (guestMessage) guestMessage.style.display = "none";
    } else {
        // Guest → hide form, show message
        if (form) form.style.display = "none";
        if (guestMessage) guestMessage.style.display = "";
    }
}

export function checkSignupAccess() {
    const token = localStorage.getItem("token");

    const form = document.getElementById("signupForm");
    const message = document.getElementById("alreadyLoggedMessage");

    if (token) {
        // logged in → hide signup form
        if (form) form.style.display = "none";
        if (message) message.style.display = "";
    } else {
        // guest → allow signup
        if (form) form.style.display = "";
        if (message) message.style.display = "none";
    }
}