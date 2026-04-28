// client-side/static/script_v2.js

class ChatApp {
  constructor() {
    this.chatMessages = document.getElementById("chatMessages");
    this.messageInput = document.getElementById("messageInput");
    this.sendBtn = document.getElementById("sendBtn");
    this.menuBtn = document.getElementById("menuBtn");
    this.menu = document.getElementById("menu");
    this.clearBtn = document.getElementById("clearBtn");
    this.aboutBtn = document.getElementById("aboutBtn");
    this.playBtn = document.getElementById("playBtn");
    this.exportBtn = document.getElementById("exportBtn");

    this.messageHistory = [];
    this.isLoading = false;

    this.userName = null;
    this.pendingGreet = false;
    this.personalizeCount = 3;
    this.lastAssistantQuestionText = "";
    this.lastAssistantQuestionType = "text";

    this.sessionId = this._generateSessionId();
    console.debug("Session ID:", this.sessionId);

    this._initEventListeners();
    this._bootstrapLastAssistantMessage();
  }

  _bootstrapLastAssistantMessage() {
    try {
      const assistantMessages = this.chatMessages.querySelectorAll(
        ".assistant-message .message-content p"
      );
      if (assistantMessages && assistantMessages.length > 0) {
        const last = assistantMessages[assistantMessages.length - 1];
        this.lastAssistantQuestionText = last.innerText || "";
      }
    } catch (e) {
      this.lastAssistantQuestionText = "";
    }
  }

  _initEventListeners() {
    this.sendBtn.addEventListener("click", () => this.sendMessage());

    this.messageInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });

    this.messageInput.addEventListener("input", () => {
      this.messageInput.style.height = "auto";
      this.messageInput.style.height =
        Math.min(this.messageInput.scrollHeight, 120) + "px";
    });

    this.menuBtn.addEventListener("click", () => {
      this.menu.classList.toggle("active");
    });

    this.clearBtn.addEventListener("click", () => {
      this.clearChat();
      this.menu.classList.remove("active");
    });

    this.aboutBtn.addEventListener("click", () => {
      alert(
        "Chat Assistant\n\nA ChatGPT-like web interface built with Python Flask and vanilla JavaScript.\n\nVersion 2.0 (Game Gen)"
      );
      this.menu.classList.remove("active");
    });

    this.playBtn.addEventListener("click", () => {
      alert("Play feature is now handled directly in the chat!");
    });

    this.exportBtn.addEventListener("click", () => {
      alert("Export Game feature coming soon!");
    });

    document.addEventListener("click", (e) => {
      if (!e.target.closest(".chat-header") && !e.target.closest(".menu")) {
        this.menu.classList.remove("active");
      }
    });
  }

  onUserSend(_message) {}

  // הפונקציה המשודרגת שמזהה מתי המשחק מוכן
  async sendMessage() {
    const message = this.messageInput.value.trim();
    console.debug("sendMessage:", message);

    if (!message || this.isLoading) return;

    this.isLoading = true;
    this.sendBtn.disabled = true;

    this.addMessage(message, "user");
    this.messageHistory.push({ role: "user", content: message });

    this._captureNameIfNeeded(message);

    try {
      if (typeof this.onUserSend === "function") this.onUserSend(message);
    } catch (err) {
      console.error("onUserSend hook error:", err);
    }

    this.messageInput.value = "";
    this.messageInput.style.height = "auto";

    this.addTypingIndicator();

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Session-ID": this.sessionId,
        },
        body: JSON.stringify({
          message,
          history: this.messageHistory,
          extract_structure: this._shouldExtractGameStructure(message),
        }),
      });

      const data = await response.json();
      this.removeTypingIndicator();

      if (!data.success) {
        this.addMessage(`Error: ${data.error || "Unknown error"}`, "assistant");
        return;
      }

      let assistantText = data.response || "";
      assistantText = this._maybePersonalize(assistantText);

      // --- handle server response types ---
      if (data.type === "game_ready" && data.game_url) {
        this.addMessage(assistantText, "assistant");
        this.messageHistory.push({ role: "assistant", content: assistantText });
        this.renderPlayButton(data.game_url);

      } else {
        this.addMessage(assistantText, "assistant");
        this.messageHistory.push({ role: "assistant", content: assistantText });

        if (data.game_structure) {
          this.showGameStructure(data.game_structure);
        }
      }

      this.lastAssistantQuestionText = data.response || "";
      this.lastAssistantQuestionType = data.type || "text";

      if (Array.isArray(data.options) && data.options.length > 0) {
        this.renderOptions(data.options);
      }

      if (data.type === "text_or_image") {
        this.renderUploadUI();
      }
    } catch (error) {
      this.removeTypingIndicator();
      this.addMessage(`Error: ${error.message}`, "assistant");
      console.error("Request error:", error);
    } finally {
      this.isLoading = false;
      this.sendBtn.disabled = false;
      this.messageInput.focus();
    }
  }

  _captureNameIfNeeded(message) {
    try {
      if (
        !this.userName &&
        this.lastAssistantQuestionText &&
        this.lastAssistantQuestionText.toLowerCase().includes("name")
      ) {
        this.userName = message.split("\n")[0].trim();
        this.pendingGreet = true;
        this.personalizeCount = 3;
        console.debug("Captured userName:", this.userName);
      }
    } catch (_) {}
  }

  _maybePersonalize(text) {
    if (this.pendingGreet && this.userName) {
      this.pendingGreet = false;
      if (this.personalizeCount > 0) this.personalizeCount -= 1;
      return `Nice to meet you, ${this.userName}! ${text}`;
    }

    if (this.userName && this.personalizeCount > 0) {
      this.personalizeCount -= 1;
      return `${this.userName}, ${text}`;
    }

    return text;
  }

  _shouldExtractGameStructure(message) {
    const keywords = [
      "create",
      "build",
      "make",
      "generate",
      "design game",
      "platformer",
      "level",
      "game",
      "new game",
      "design",
    ];
    const lower = message.toLowerCase();
    return keywords.some((k) => lower.includes(k));
  }

  showGameStructure(gameStructure) {
    const game = gameStructure.game || {};
    const levels = gameStructure.levels || [];
    const mechanics = gameStructure.mechanics || {};

    let text = `\n🎮 GAME STRUCTURE CREATED:\n\n`;
    text += `Title: ${game.title}\n`;
    text += `Description: ${game.description}\n`;
    text += `Difficulty: ${game.difficulty}\n\n`;
    text += `Levels: ${levels.length}\n`;
    text += `Mechanics: Double Jump=${mechanics.has_double_jump}, Dash=${mechanics.has_dash}\n\n`;
    text += `✅ Ready to export and build!`;

    this.addMessage(text, "assistant");
    this.messageHistory.push({ role: "assistant", content: text });
  }

  _generateSessionId() {
    return (
      "session-" +
      Math.random().toString(36).substring(2, 15) +
      Math.random().toString(36).substring(2, 15)
    );
  }

  addMessage(content, role) {
    console.debug("addMessage:", role, content);

    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", `${role}-message`);

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");

    const isImageUrl = (value) => {
      const s = String(value || "").toLowerCase();
      const looksLikeUrl = s.startsWith("http") || s.startsWith("/static/");
      const isImageExt = /\.(png|jpe?g|gif|webp|svg)(\?|$)/.test(s);
      return looksLikeUrl && isImageExt;
    };

    if (isImageUrl(content)) {
      const img = document.createElement("img");
      img.src = content;
      img.alt = "image";
      img.style.maxWidth = "520px";
      img.style.width = "100%";
      img.style.borderRadius = "8px";
      img.style.imageRendering = "pixelated";
      img.loading = "lazy";
      contentDiv.appendChild(img);
    } else {
      const p = document.createElement("p");
      p.innerHTML = String(content).replace(/\n/g, "<br>");
      contentDiv.appendChild(p);
    }

    messageDiv.appendChild(contentDiv);
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
    return messageDiv;
  }

  renderOptions(options) {
    const assistantMessages = this.chatMessages.querySelectorAll(".assistant-message");
    if (!assistantMessages.length) return;

    const lastAssistant = assistantMessages[assistantMessages.length - 1];
    const container = document.createElement("div");
    container.classList.add("options-container");

    options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.classList.add("choice-btn");
      btn.textContent = opt;
      btn.addEventListener("click", () => {
        container.remove();
        this.messageInput.value = opt;
        this.sendMessage();
      });
      container.appendChild(btn);
    });

    lastAssistant.appendChild(container);
    this.scrollToBottom();
  }

  // --- הפונקציה החדשה שמציירת את כפתור המשחק ---
  renderPlayButton(gameUrl) {
    const assistantMessages = this.chatMessages.querySelectorAll(".assistant-message");
    if (!assistantMessages.length) return;

    const lastAssistant = assistantMessages[assistantMessages.length - 1];
    const container = document.createElement("div");
    container.classList.add("play-container");
    container.style.marginTop = "15px";
    container.style.textAlign = "center";

    const btn = document.createElement("button");
    btn.textContent = "🎮 Play Game!";

    // קצת עיצוב UX משודרג לכפתור
    btn.style.background = "linear-gradient(45deg, #FF512F 0%, #DD2476 100%)";
    btn.style.color = "#FFF";
    btn.style.border = "none";
    btn.style.padding = "14px 28px";
    btn.style.borderRadius = "30px";
    btn.style.fontSize = "18px";
    btn.style.fontWeight = "bold";
    btn.style.cursor = "pointer";
    btn.style.boxShadow = "0 4px 15px rgba(221, 36, 118, 0.4)";
    btn.style.transition = "all 0.2s ease";

    btn.addEventListener("mouseover", () => {
      btn.style.transform = "scale(1.05)";
      btn.style.boxShadow = "0 6px 20px rgba(221, 36, 118, 0.6)";
    });
    btn.addEventListener("mouseout", () => {
      btn.style.transform = "scale(1)";
      btn.style.boxShadow = "0 4px 15px rgba(221, 36, 118, 0.4)";
    });

    btn.addEventListener("click", () => {
      window.open(gameUrl, "_blank");
    });

    container.appendChild(btn);
    lastAssistant.appendChild(container);
    this.scrollToBottom();
  }
  // ----------------------------------------------

  renderUploadUI() {
    const assistantMessages = this.chatMessages.querySelectorAll(".assistant-message");
    if (!assistantMessages.length) return;

    const lastAssistant = assistantMessages[assistantMessages.length - 1];
    const container = document.createElement("div");
    container.classList.add("upload-container");

    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.classList.add("upload-input");

    const uploadBtn = document.createElement("button");
    uploadBtn.type = "button";
    uploadBtn.classList.add("upload-btn");
    uploadBtn.textContent = "Upload Image";

    const urlRow = document.createElement("div");
    urlRow.classList.add("url-input-row");

    const urlInput = document.createElement("input");
    urlInput.type = "text";
    urlInput.placeholder = "Or paste an image URL here";
    urlInput.classList.add("url-input");

    const urlSend = document.createElement("button");
    urlSend.type = "button";
    urlSend.classList.add("url-send-btn");
    urlSend.textContent = "Send URL";

    urlRow.appendChild(urlInput);
    urlRow.appendChild(urlSend);

    container.appendChild(fileInput);
    container.appendChild(uploadBtn);
    container.appendChild(urlRow);

    uploadBtn.addEventListener("click", async () => {
      if (!fileInput.files || fileInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
      }

      const file = fileInput.files[0];
      try {
        const form = new FormData();
        form.append("file", file);

        const resp = await fetch("/api/upload", {
          method: "POST",
          headers: { "X-Session-ID": this.sessionId },
          body: form,
        });

        const j = await resp.json();
        if (j.url) {
          this.messageInput.value = j.url;
          container.remove();
          this.sendMessage();
        } else {
          alert("Upload failed: " + (j.error || "Unknown error"));
        }
      } catch (err) {
        console.error("Upload error:", err);
        alert("Upload failed. See console for details.");
      }
    });

    urlSend.addEventListener("click", () => {
      const val = urlInput.value.trim();
      if (!val) return alert("Enter an image URL first.");
      this.messageInput.value = val;
      container.remove();
      this.sendMessage();
    });

    lastAssistant.appendChild(container);
    this.scrollToBottom();
  }

  addTypingIndicator() {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "assistant-message");
    messageDiv.id = "typingIndicator";

    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content", "typing-indicator");

    for (let i = 0; i < 3; i++) {
      const dot = document.createElement("div");
      dot.classList.add("typing-dot");
      contentDiv.appendChild(dot);
    }

    messageDiv.appendChild(contentDiv);
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
  }

  removeTypingIndicator() {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) indicator.remove();
  }

  scrollToBottom() {
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  clearChat() {
    if (!confirm("Are you sure you want to clear the chat history?")) return;

    this.chatMessages.innerHTML = `
      <div class="message assistant-message">
        <div class="message-content">
          <p>Chat cleared. How can I help you?</p>
        </div>
      </div>
    `;

    this.messageHistory = [];
    this.messageInput.focus();

    this.userName = null;
    this.pendingGreet = false;
    this.personalizeCount = 3;
    this.lastAssistantQuestionText = "Chat cleared. How can I help you?";
    this.lastAssistantQuestionType = "text";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.chatApp = new ChatApp();
});