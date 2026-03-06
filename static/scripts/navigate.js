var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function routeToPartial(pathname) {
    if (pathname === "/")
        return "/partials/home";
    return "/partials" + pathname;
}
export default function navigate(e) {
    return __awaiter(this, void 0, void 0, function* () {
        let url;
        if (e) {
            const target = e.target;
            if (!(target instanceof Element))
                return;
            const anchor = target.closest("a");
            if (!anchor)
                return;
            const href = anchor.getAttribute("href");
            if (!href)
                return;
            url = href;
            history.pushState({}, "", url);
        }
        else {
            url = window.location.pathname;
        }
        const partialUrl = routeToPartial(url);
        try {
            const token = localStorage.getItem("token");
            const headers = token ? { "Authorization": "Bearer " + token } : {};
            const response = yield fetch(partialUrl, { headers });
            if (!response.ok) {
                throw new Error("Failed to fetch: " + response.status);
            }
            const html = yield response.text();
            const content = document.getElementById("content");
            if (!content)
                return;
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
        }
        catch (error) {
            console.error("Navigation error:", error);
        }
    });
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
        if (signUp)
            signUp.style.display = "none";
        if (login)
            login.style.display = "none";
        if (profile)
            profile.style.display = "";
        if (logout)
            logout.style.display = "";
    }
    else {
        // Not logged in
        if (signUp)
            signUp.style.display = "";
        if (login)
            login.style.display = "";
        if (profile)
            profile.style.display = "none";
        if (logout)
            logout.style.display = "none";
    }
}
// Check login token and toggle Add Destination form
export function checkAddDestinationAccess() {
    const token = localStorage.getItem("token");
    const form = document.getElementById("addDestinationForm");
    const guestMessage = document.getElementById("guestMessage");
    if (token) {
        // Logged in → show form, hide guest message
        if (form)
            form.style.display = "";
        if (guestMessage)
            guestMessage.style.display = "none";
    }
    else {
        // Guest → hide form, show message
        if (form)
            form.style.display = "none";
        if (guestMessage)
            guestMessage.style.display = "";
    }
}
export function checkSignupAccess() {
    const token = localStorage.getItem("token");
    const form = document.getElementById("signupForm");
    const message = document.getElementById("alreadyLoggedMessage");
    if (token) {
        // logged in → hide signup form
        if (form)
            form.style.display = "none";
        if (message)
            message.style.display = "";
    }
    else {
        // guest → allow signup
        if (form)
            form.style.display = "";
        if (message)
            message.style.display = "none";
    }
}
//# sourceMappingURL=navigate.js.map