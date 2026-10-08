document
  .getElementById("predictionForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const submitBtn = document.getElementById("submitBtn");
    const spinner = document.getElementById("spinner");
    const resultCard = document.getElementById("resultCard");
    const scoreDisplay = document.getElementById("scoreDisplay");
    const scoreMessage = document.getElementById("scoreMessage");

    // Show Loading State
    spinner.style.display = "block";
    submitBtn.disabled = true;

    // Collect Form Data matching FastAPI StudentData schema
    const formData = {
      age: parseInt(document.getElementById("age").value),
      gender: document.getElementById("gender").value,
      country: document.getElementById("country").value,
      academic_level: document.getElementById("academic_level").value,
      most_used_platform: document.getElementById("most_used_platform").value,
      purpose_of_use: document.getElementById("purpose_of_use").value,
      avg_daily_usage_hours: parseFloat(
        document.getElementById("avg_daily_usage_hours").value,
      ),
      daily_unlocks: parseInt(document.getElementById("daily_unlocks").value),
      study_hours: parseFloat(document.getElementById("study_hours").value),
      physical_activity_hours: parseFloat(
        document.getElementById("physical_activity_hours").value,
      ),
      sleep_hours_per_night: parseFloat(
        document.getElementById("sleep_hours_per_night").value,
      ),
      stress_level: document.getElementById("stress_level").value,
    };

    try {
      // FastAPI local backend endpoint
      const response = await fetch("http://127.0.0.1:2200/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const result = await response.json();
      const score = result.predicted_mental_health_score;

      // Display Score
      scoreDisplay.textContent = score;

      if (score >= 7.5) {
        scoreMessage.textContent =
          "Your metrics indicate strong well-being and high lifestyle balance.";
        scoreDisplay.style.color = "#4ade80"; // Green
      } else if (score >= 4.5) {
        scoreMessage.textContent =
          "Your mental health score is moderate. Consider tuning sleep and screen habits.";
        scoreDisplay.style.color = "#facc15"; // Yellow
      } else {
        scoreMessage.textContent =
          "Your score indicates higher stress levels or digital fatigue. Focus on rest and physical activity.";
        scoreDisplay.style.color = "#f87171"; // Red
      }

      resultCard.classList.remove("hidden");
    } catch (error) {
      alert(
        "Failed to connect to backend server. Make sure Uvicorn is running on port 2200.",
      );
      console.error("Prediction Error:", error);
    } finally {
      // Hide Loading State
      spinner.style.display = "none";
      submitBtn.disabled = false;
    }
  });
