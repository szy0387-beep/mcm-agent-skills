const copyButton = document.querySelector("#copy-prompt");
const promptText = document.querySelector("#prompt-text");
const copyStatus = document.querySelector("#copy-status");

if (navigator.clipboard) {
  copyButton.hidden = false;
  copyButton.addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText(promptText.textContent.trim());
      copyStatus.textContent = "已复制到剪贴板。";
    } catch {
      copyStatus.textContent = "复制失败，请手动选中并复制上方指令。";
    }
  });
}
