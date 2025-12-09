// ui/app.js

let uploadedFileId = null;

// ---------------------------
// 1. Upload Map
// ---------------------------
document.getElementById("mapUpload").addEventListener("change", async function () {

    const file = this.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("map", file);

    const resp = await fetch("/upload_map", {
        method: "POST",
        body: formData
    });

    const data = await resp.json();

    if (data.error) {
        alert("Upload failed: " + data.error);
        return;
    }

    uploadedFileId = data.file_id;
    alert("Map uploaded successfully!");
});

// ---------------------------
// 2. Run Pathfinder
// ---------------------------
document.getElementById("runBtn").addEventListener("click", async function () {

    if (!uploadedFileId) {
        alert("Please upload a map first.");
        return;
    }

    const payload = {
        file_id: uploadedFileId,
        start: {
            x: Number(document.getElementById("startX").value),
            y: Number(document.getElementById("startY").value)
        },
        goal: {
            x: Number(document.getElementById("goalX").value),
            y: Number(document.getElementById("goalY").value)
        },
        mode: document.getElementById("mode").value
    };

    const resp = await fetch("/pathfind", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const data = await resp.json();

    document.getElementById("asciiArea").textContent = data.ascii ?? "No path found.";
    document.getElementById("costArea").textContent = data.cost === null ? "-" : data.cost;
});
