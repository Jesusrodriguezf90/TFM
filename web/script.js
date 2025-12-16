const form = document.getElementById("prediction-form");
const result = document.getElementById("prediction");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Se recogen los datos del formulario
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        // Se convierte a número si es posible
        data[key] = isNaN(value) ? value : Number(value);
    });

    try {
        const response = await fetch("http://127.0.0.1:8001/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            result.textContent = `Error: ${error.detail}`;
            return;
        }

        const prediction = await response.json();
        result.textContent = `Predicción: ${prediction.prediction === 1 ? "Diabetes" : "No Diabetes"}`;
    } catch (err) {
        result.textContent = `Error: ${err}`;
    }
});