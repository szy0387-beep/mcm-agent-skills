for (const copyButton of document.querySelectorAll(".copy-button[aria-controls]")) {
  const promptText = document.getElementById(copyButton.getAttribute("aria-controls"));
  const copyStatus = copyButton.closest(".prompt-option").querySelector(".copy-status");
  copyButton.hidden = false;
  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(promptText.textContent.trim());
      copyStatus.textContent = "已复制到剪贴板。";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(promptText);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      copyStatus.textContent = "指令已选中，请手动复制。";
    }
  });
}
