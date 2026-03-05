export default function showMessage(result, form, messageId) {
    var _a;
    const content = document.getElementById("content");
    if (!content)
        return;
    // Remove old message if exists
    const oldMessage = document.getElementById(messageId);
    if (oldMessage) {
        oldMessage.remove();
    }
    const messageBox = document.createElement("div");
    messageBox.id = messageId;
    messageBox.textContent = (_a = result.message) !== null && _a !== void 0 ? _a : "";
    if (result.success) {
        messageBox.classList.add("msg_success");
        form.reset();
    }
    else {
        messageBox.classList.add("msg_failure");
    }
    content.appendChild(messageBox);
}
//# sourceMappingURL=showMessage.js.map