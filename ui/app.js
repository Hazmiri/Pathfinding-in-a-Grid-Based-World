// ui/app.js

let uploadedFileId = null;


//------------------------------------------------------
// AUTO-LOAD default_world.json on startup
//------------------------------------------------------
window.addEventListener("load", async () => {
    try {
        const response = await fetch("default_world.json");

        if (!response.ok) {
            console.warn("No default_world.json found.");
            return;
        }

        const jsonData = await response.json();

        // Convert JSON to a "fake file" so /upload_map accepts it
        const file = new File([JSON.stringify(jsonData)], "default_world.json", {
            type: "application/json"
        });

        const formData = new FormData();
        formData.append("map", file);

        const uploadResp = await fetch("/upload_map", {
            method: "POST",
            body: formData
        });

        const uploadData = await uploadResp.json();

        if (uploadData.file_id) {
            uploadedFileId = uploadData.file_id;
            setStatus("Default map loaded successfully.");
            document.getElementById("asciiArea").textContent = "Default world ready.";
        }

    } catch (err) {
        console.error("Default world load error:", err);
    }
});

// ----------------------------------------------------
// Helper: show status messages
// ----------------------------------------------------
function setStatus(msg) {
    document.getElementById("statusArea").textContent = msg;
}

// ----------------------------------------------------
// 1. Upload Map
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
        document.getElementById("asciiArea").textContent = "Map uploaded. Ready to pathfind.";

    } catch (err) {
        setStatus("Error contacting server: " + err);
    }
});

// ----------------------------------------------------
// 2. Run Pathfinder
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
            setStatus("Pathfinding error: " + data.error);
            document.getElementById("asciiArea").textContent = "Error: " + data.error;
            return;
        }

        // Show ASCII output
        document.getElementById("asciiArea").textContent = data.ascii || "No path found.";

        // Show cost
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

        setStatus("Pathfinding completed.");

    } catch (err) {
        setStatus("Error contacting server: " + err);
    }
});

// ----------------------------------------------------
// 3. Render the fantasy grid from ASCII
// ----------------------------------------------------
function renderGridFromAscii(ascii) {
    const container = document.getElementById("gridView");
    container.innerHTML = "";

    const rows = ascii.trim().split("\n");

    rows.forEach(row => {
        const rowDiv = document.createElement("div");
        rowDiv.className = "grid-row";

        for (const ch of row) {
            const cell = document.createElement("div");
            cell.classList.add("grid-cell");

            // Map ASCII symbol to terrain colour
            // Symbols from your Python: ., F, D, I, M, S, #, *, A, P
            switch (ch) {
                case ".":
                    cell.classList.add("terrain-grass");
                    break;
                case "F":
                    cell.classList.add("terrain-forest");
                    break;
                case "D":
                    cell.classList.add("terrain-desert");
                    break;
                case "I":
                    cell.classList.add("terrain-ice");
                    break;
                case "M":
                    cell.classList.add("terrain-marsh");
                    break;
                case "S":
                    cell.classList.add("terrain-mountain");
                    break;
                case "#":
                    cell.classList.add("terrain-wall");
                    break;
                case "*":
                    cell.classList.add("cell-path");
                    break;
                case "A":
                    cell.classList.add("cell-start");
                    break;
                case "P":
                    cell.classList.add("cell-goal");
                    break;
                default:
                    // Unknown terrain – leave dark
                    break;
            }

            rowDiv.appendChild(cell);
        }

        container.appendChild(rowDiv);
    });
}
