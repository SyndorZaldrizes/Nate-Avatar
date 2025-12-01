// app.js

// For later: paste your v0.2 boot prompt here if you call an API
const ALTIUS_BOOT_PROMPT_V02 = `
You are ALTIUS — an identity seeded from a human named Nate...
[shortened here in code; in your real file paste the full v0.2 prompt]
`;

const chatLog = document.getElementById("chat-log");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);

  const label = document.createElement("div");
  label.classList.add("message-label");
  label.textContent = sender === "user" ? "You" : "ALTIUS";

  const body = document.createElement("div");
  body.textContent = text;

  msg.appendChild(label);
  msg.appendChild(body);

  chatLog.appendChild(msg);
  chatLog.scrollTop = chatLog.scrollHeight;
}

async function handleSend() {
  const text = userInput.value.trim();
  if (!text) return;

  appendMessage("user", text);
  userInput.value = "";

  sendBtn.disabled = true;

  try {
    // For now, fake a response to test UI wiring
    const reply = await fakeAltiusResponse(text);
    appendMessage("altius", reply);
  } catch (err) {
    console.error(err);
    appendMessage(
      "altius",
      "Something went wrong processing that. Try again or simplify the question."
    );
  } finally {
    sendBtn.disabled = false;
    userInput.focus();
  }
}

// Placeholder logic for now
async function fakeAltiusResponse(userText) {
  // Simple heuristic: if the question sounds big, go a bit deeper.
  const lower = userText.toLowerCase();
  const bigThemes = ["democracy", "meaning", "point", "future", "world", "politics", "nihilism"];

  const isBig = bigThemes.some((kw) => lower.includes(kw));

  if (isBig) {
    return (
      "This sounds like a structural question, not just a mood.\n\n" +
      "Start by separating what you can influence from what you can’t. " +
      "Then, focus on stabilizing one small system in your immediate orbit. " +
      "That’s how you resist decay without burning yourself out."
    );
  }

  return (
    "Short version: make the next step small and concrete.\n\n" +
    "Pick one thing you can finish in under 30 minutes that moves you a little closer " +
    "to the kind of person you want to become. Do that first. Then reassess."
  );
}

sendBtn.addEventListener("click", handleSend);

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
});
