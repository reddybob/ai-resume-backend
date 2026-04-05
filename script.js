/* Show selected file name */
document.getElementById("resume").addEventListener("change", function() {
    let fileName = this.files[0]?.name || "No file chosen";
    document.getElementById("file-name").innerText = fileName;
});

/* Upload + Analyze */
function uploadResume() {
    let file = document.getElementById("resume").files[0];
    let job = document.getElementById("job").value;

    if (!file) {
        alert("Please upload resume");
        return;
    }

    if (!job) {
        alert("Please select role");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);
    formData.append("job", job);

    fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        let match = data.match;

        // Match text
        document.getElementById("match").innerText = "Match %: " + match + "%";

        // Progress bar
        document.getElementById("bar").style.width = match + "%";

        // 🔥 Resume PDF Preview
        let fileURL = URL.createObjectURL(file);
        document.getElementById("preview").src = fileURL;
    })
    .catch(err => {
        console.error(err);
        alert("Error connecting to server");
    });
}

/* Dark mode toggle */
function toggleMode() {
    document.body.classList.toggle("dark");
}