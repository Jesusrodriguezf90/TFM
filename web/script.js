// script.js
// Manejo del formulario de predicción de diabetes

// Campos que deben ser float
const floatFields = ["EXEROFT1", "_FRUTSUM", "_VEGESUM"];

// Campos que deben ser int (todos los demás)
const intFields = [
  "BPHIGH4","_RACE","BPMEDS","BLOODCHO","HAVARTH3","QLACTLM2","USEEQUIP",
  "BLIND","DECIDE","DIFFWALK","DIFFALON","DIFFDRES","SMOKE100","ADDEPEV2",
  "SEX","GENHLTH","_PACAT1","_AGEG5YR","_BMI5CAT"
];

// Obtener referencias al formulario y al contenedor de resultados
const form = document.getElementById("prediction-form");
const result = document.getElementById("prediction");

// Escuchar el evento submit del formulario
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const inputData = {};

    formData.forEach((value, key) => {
        if (value === "") {
            inputData[key] = null; // Evitar enviar ""
        } else if (floatFields.includes(key)) {
            inputData[key] = parseFloat(value);
        } else if (intFields.includes(key)) {
            inputData[key] = parseInt(value);
        } else {
            inputData[key] = value; // por seguridad, aunque no debería haber
        }
    });

    // Threshold
    const thresholdSelect = document.getElementById("threshold");
    const thresholdValue = parseFloat(thresholdSelect.value);

    const payload = {
        input_data: inputData,
        config: { threshold: thresholdValue }
    };

    console.log("Payload a enviar a la API:", payload);

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const error = await response.json();
            console.error("Error completo de la API:", error);

            if (error.detail) {
                if (Array.isArray(error.detail)) {
                    result.textContent = "Error de validación:\n" +
                        error.detail.map(d => `${d.msg} (campo: ${d.loc.join(" > ")})`).join("\n");
                } else {
                    result.textContent = "Error: " + error.detail;
                }
            } else {
                result.textContent = "Error desconocido";
            }

            result.classList.remove("positivo", "negativo");
            return;
        }

        const prediction = await response.json();
        console.log("Respuesta de la API:", prediction);

        result.textContent = `Decisión: ${prediction.decision} ` +
                             `(${prediction.probability}%) ` +
                             `umbral usado: ${prediction.threshold_used}`;

        if (prediction.decision.toLowerCase().includes("no")) {
            result.classList.remove("positivo");
            result.classList.add("negativo");
        } else {
            result.classList.remove("negativo");
            result.classList.add("positivo");
        }

    } catch (err) {
        console.error("Error al llamar a la API:", err);
        result.textContent = `Error de comunicación con el servidor: ${err}`;
        result.classList.remove("positivo", "negativo");
    }
});