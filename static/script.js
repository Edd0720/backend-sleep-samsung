document.getElementById("predictionForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = {
        Age: parseInt(document.getElementById("Age").value),
        Gender: parseInt(document.getElementById("Gender").value),
        Sleep_duration: parseFloat(document.getElementById("Sleep_duration").value),
        REM_sleep_percentage: parseFloat(document.getElementById("REM_sleep_percentage").value),
        Deep_sleep_percentage: parseFloat(document.getElementById("Deep_sleep_percentage").value),
        Light_sleep_percentage: parseFloat(document.getElementById("Light_sleep_percentage").value),
        Awakenings: parseInt(document.getElementById("Awakenings").value),
        Caffeine_consumption: parseInt(document.getElementById("Caffeine_consumption").value),
        Alcohol_consumption: parseInt(document.getElementById("Alcohol_consumption").value),
        Smoking_status: parseInt(document.getElementById("Smoking_status").value),
        Exercise_frequency: parseInt(document.getElementById("Exercise_frequency").value),
    };

    try {
        const response = await fetch("/predict/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
        });

        const result = await response.json();
        if (result.prediction) {
            document.getElementById("result").innerText = `Predicción: ${result.prediction}`;
        } else {
            document.getElementById("result").innerText = `Error: ${result.error}`;
        }
    } catch (error) {
        document.getElementById("result").innerText = `Error: ${error.message}`;
    }
});