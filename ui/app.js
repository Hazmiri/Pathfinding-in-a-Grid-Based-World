// ui/app.js

let uploadedFileId = null;

// ----------------------------------------------------
// Helper: show status messages
// ----------------------------------------------------

function setStatus(msg) {
    document.getElementById("statusArea").textContent = msg;
}

// ----------------------------------------------------
// Auto-load DEFAULT WORLD on startup
// ----------------------------------------------------

async function loadDefaultMap() {
    try {
        setStatus("Loading default world...");

        // 1. Fetch raw JSON
        const resp = await fetch("/default_world.json");
        const jsonText = await resp.text();

        // 2. Convert to Blob -> File
        const blob = new Blob([jsonText], { type: "application/json" });
        const file = new File([blob], "default_world.json", { type: "application/json" });

        // 3. Upload through API
        const formData = new FormData();
        formData.append("map", file);

        const uploadResp = await fetch("/upload_map", {
            method: "POST",
            body: formData
        });

        const data = await uploadResp.json();

        if (data.error) {
            setStatus("Default map load failed: " + data.error);
            return;
        }

        uploadedFileId = data.file_id;
        setStatus("Default world loaded.");
        document.getElementById("asciiArea").textContent =
            "Default world loaded. Ready to pathfind.";

    } catch (err) {
        setStatus("Error loading default world: " + err);
    }
}

// ----------------------------------------------------
// Manual Upload (user selects file)
// ----------------------------------------------------

document.getElementById("mapUpload").addEventListener("change", async function () {
    const file = this.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("map", file);

    setStatus("Uploading map...");

    try {
        const resp = await fetch("/upload_map", {
            method: "POST",
            body: formData
        });

        const data = await resp.json();

        if (data.error) {
            setStatus("Upload failed: " + data.error);
            return;
        }

        uploadedFileId = data.file_id;
        setStatus("Map uploaded successfully.");
        document.getElementById("asciiArea").textContent = "Map uploaded. Ready.";

    } catch (err) {
        setStatus("Error contacting server: " + err);
    }
});

// ----------------------------------------------------
// Run Pathfinder
// ----------------------------------------------------

document.getElementById("runBtn").addEventListener("click", async function () {

    if (!uploadedFileId) {
        alert("Please upload a map first.");
        return;
    }

    const startX = Number(document.getElementById("startX").value);
    const startY = Number(document.getElementById("startY").value);
    const goalX = Number(document.getElementById("goalX").value);
    const goalY = Number(document.getElementById("goalY").value);
    const mode = document.getElementById("mode").value;

    const payload = {
        file_id: uploadedFileId,
        start: { x: startX, y: startY },
        goal: { x: goalX, y: goalY },
        mode: mode
    };

    setStatus("Running Saladin_Pathfinder...");

    try {
        const resp = await fetch("/pathfind", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await resp.json();

        if (data.error) {
            setStatus("Error: " + data.error);
            document.getElementById("asciiArea").textContent = "Error: " + data.error;
            return;
        }

        // Show ASCII map
        document.getElementById("asciiArea").textContent =
            data.ascii || "No path found.";

        // Show cost & steps
        if (data.cost === null || data.path === null) {
            document.getElementById("costArea").textContent = "No path found.";
        } else {
            document.getElementById("costArea").textContent =
                `Total cost: ${data.cost} | Steps: ${data.path.length - 1}`;
        }

        // Draw coloured grid
        if (data.ascii) {
            renderGridFromAscii(data.ascii);
        }

        setStatus("Pathfinding complete.");

    } catch (err) {
        setStatus("Error contacting server: " + err);
    }
});

// ----------------------------------------------------
// Render the grid visually
// ----------------------------------------------------

function renderGridFromAscii(ascii) {
    const container = document.getElementById("gridView");
    if (!container) {
        console.error("gridView element not found in HTML.");
        return;
    }

    container.innerHTML = "";

    const rows = ascii.trim().split("\n");

    rows.forEach(row => {
        const rowDiv = document.createElement("div");
        rowDiv.className = "grid-row";

        for (const ch of row) {
            const cell = document.createElement("div");
            cell.classList.add("grid-cell");

            switch (ch) {
                case ".": cell.classList.add("terrain-grass"); break;
                case "F": cell.classList.add("terrain-forest"); break;
                case "D": cell.classList.add("terrain-desert"); break;
                case "I": cell.classList.add("terrain-ice"); break;
                case "M": cell.classList.add("terrain-marsh"); break;
                case "S": cell.classList.add("terrain-mountain"); break;
                case "#": cell.classList.add("terrain-wall"); break;
                case "*": cell.classList.add("cell-path"); break;
                case "A": cell.classList.add("cell-start"); break;
                case "P": cell.classList.add("cell-goal"); break;
            }

            rowDiv.appendChild(cell);
        }

        container.appendChild(rowDiv);
    });
}

// ----------------------------------------------------
// AUTO START
// ----------------------------------------------------

window.addEventListener("DOMContentLoaded", loadDefaultMap);
