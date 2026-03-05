export interface MessageResult {
    success: boolean;
    message?: string;
}

export default function showMessage(
    result: MessageResult,
    form: HTMLFormElement,
    messageId: string
): void {
    const content = document.getElementById("content");
    if (!content) return;

    // Remove old message if exists
    const oldMessage = document.getElementById(messageId);
    if (oldMessage) {
        oldMessage.remove();
    }

    const messageBox = document.createElement("div");
    messageBox.id = messageId;
    messageBox.textContent = result.message ?? "";

    if (result.success) {
        messageBox.classList.add("msg_success");
        form.reset();
    } else {
        messageBox.classList.add("msg_failure");
    }

    content.appendChild(messageBox);
}