function switchTab(id) {
  document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".input-section").forEach(s => s.classList.remove("active"));

  document.querySelector(`button[onclick="switchTab('${id}')"]`).classList.add("active");
  document.getElementById(id).classList.add("active");
}

function showLoader(show) {
  document.getElementById("loader").classList.toggle("hidden", !show);
  document.getElementById("output").classList.add("hidden");
}

function renderResult(data) {
  document.getElementById("summary").textContent = data.summary || "";

  const insights = document.getElementById("insights");
  insights.innerHTML = "";
  (data.insights?.keywords || []).forEach(k => {
    const li = document.createElement("li");
    li.textContent = k;
    insights.appendChild(li);
  });

  const flashcards = document.getElementById("flashcards");
  flashcards.innerHTML = "";
  (data.flashcards || []).forEach(card => {
    const div = document.createElement("div");
    div.className = "flashcard";
    div.innerHTML = `❓ ${card.question}<div class="flashcard-answer">${card.answer}</div>`;
    div.onclick = () => {
      const ans = div.querySelector(".flashcard-answer");
      ans.style.display = ans.style.display === "block" ? "none" : "block";
    };
    flashcards.appendChild(div);
  });

  const flow = document.getElementById("flowchart");
  flow.innerHTML = "";
  (data.flowchart || "").split("\n").forEach(step => {
    if (step.trim()) {
      const li = document.createElement("li");
      li.textContent = step.replace(/^[A-Z]\[|\]$/g, "");
      flow.appendChild(li);
    }
  });

  document.getElementById("output").classList.remove("hidden");
}

async function submitText() {
  showLoader(true);
  try {
    const res = await fetch("/api/text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: document.getElementById("textInput").value })
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || `HTTP ${res.status}`);
    }
    const data = await res.json();
    renderResult(data);
  } catch (err) {
    document.getElementById("summary").textContent = "Error: " + (err.message || err);
    document.getElementById("output").classList.remove("hidden");
  } finally {
    showLoader(false);
  }
}

async function submitFile(endpoint, inputId) {
  showLoader(true);
  try {
    const formData = new FormData();
    formData.append("file", document.getElementById(inputId).files[0]);

    const res = await fetch(endpoint, { method: "POST", body: formData });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || `HTTP ${res.status}`);
    }
    const data = await res.json();
    renderResult(data);
  } catch (err) {
    document.getElementById("summary").textContent = "Error: " + (err.message || err);
    document.getElementById("output").classList.remove("hidden");
  } finally {
    showLoader(false);
  }
}

async function submitVideo() {
  showLoader(true);
  try {
    const res = await fetch("/api/video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: document.getElementById("videoInput").value })
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(txt || `HTTP ${res.status}`);
    }
    const data = await res.json();
    renderResult(data);
  } catch (err) {
    document.getElementById("summary").textContent = "Error: " + (err.message || err);
    document.getElementById("output").classList.remove("hidden");
  } finally {
    showLoader(false);
  }
}
