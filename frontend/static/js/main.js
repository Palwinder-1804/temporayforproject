function switchTab(id) {
  document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".input-section").forEach(s => s.classList.remove("active"));

  document.querySelector(`button[onclick="switchTab('${id}')"]`).classList.add("active");
  document.getElementById(id).classList.add("active");
}

function showLoader(show) {
  document.getElementById("loader").classList.toggle("hidden", !show);
  if (show) {
    document.getElementById("output").classList.add("hidden");
  }
}

/* ===============================
   RENDER RESULT (SAFE)
================================ */
function renderResult(data) {
  // Handle backend error payload
  if (data?.error) {
    document.getElementById("summary").textContent = "Error: " + data.error;
    document.getElementById("output").classList.remove("hidden");
    return;
  }

  // SUMMARY
  document.getElementById("summary").textContent = data?.summary || "No summary generated.";

  // INSIGHTS / KEYWORDS
  const insights = document.getElementById("insights");
  insights.innerHTML = "";
  (data?.insights?.keywords || []).forEach(k => {
    const li = document.createElement("li");
    li.textContent = k;
    insights.appendChild(li);
  });

  // FLASHCARDS
  const flashcards = document.getElementById("flashcards");
  flashcards.innerHTML = "";
  (data?.flashcards || []).forEach(card => {
    const div = document.createElement("div");
    div.className = "flashcard";
    div.innerHTML = `
      ❓ ${card.question || ""}
      <div class="flashcard-answer">${card.answer || ""}</div>
    `;
    div.onclick = () => {
      const ans = div.querySelector(".flashcard-answer");
      ans.style.display = ans.style.display === "block" ? "none" : "block";
    };
    flashcards.appendChild(div);
  });

  // FLOWCHART
  const flow = document.getElementById("flowchart");
  flow.innerHTML = "";
  (data?.flowchart || "")
    .split("\n")
    .forEach(step => {
      if (step.trim()) {
        const li = document.createElement("li");
        li.textContent = step.replace(/^[A-Z]\[|\]$/g, "");
        flow.appendChild(li);
      }
    });

  document.getElementById("output").classList.remove("hidden");
}

/* ===============================
   TEXT SUBMIT
================================ */
async function submitText() {
  showLoader(true);
  try {
    const res = await fetch("/api/text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text: document.getElementById("textInput").value.trim()
      })
    });

    const data = await res.json();
    renderResult(data);

  } catch (err) {
    document.getElementById("summary").textContent = "Error: " + err.message;
    document.getElementById("output").classList.remove("hidden");
  } finally {
    showLoader(false);
  }
}

/* ===============================
   FILE SUBMIT (PDF / IMAGE)
================================ */
async function submitFile(endpoint, inputId) {
  showLoader(true);
  try {
    const input = document.getElementById(inputId);
    if (!input.files.length) {
      throw new Error("Please select a file first.");
    }

    const formData = new FormData();
    formData.append("file", input.files[0]);

    const res = await fetch(endpoint, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    renderResult(data);

  } catch (err) {
    document.getElementById("summary").textContent = "Error: " + err.message;
    document.getElementById("output").classList.remove("hidden");
  } finally {
    showLoader(false);
  }
}

/* ===============================
   VIDEO SUBMIT
================================ */
async function submitVideo() {
  showLoader(true);
  try {
    const url = document.getElementById("videoInput").value.trim();
    if (!url) {
      throw new Error("Please enter a video URL.");
    }

    const res = await fetch("/api/video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });

    const data = await res.json();
    renderResult(data);

  } catch (err) {
    document.getElementById("summary").textContent = "Error: " + err.message;
    document.getElementById("output").classList.remove("hidden");
  } finally {
    showLoader(false);
  }
}
