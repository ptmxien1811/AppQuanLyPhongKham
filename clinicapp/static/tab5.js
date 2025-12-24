document.addEventListener("DOMContentLoaded", function () {

    const dataEl = document.getElementById("chart-data");
    if (!dataEl) return;

    const labels = JSON.parse(dataEl.dataset.labels || "[]");
    const values = JSON.parse(dataEl.dataset.values || "[]");

    if (labels.length === 0) return;

    const ctx = document.getElementById("revenueChart");
    if (!ctx) return;

    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Doanh thu (VNĐ)",
                data: values,
                borderWidth: 2,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            plugins: {
                legend: { display: true }
            }
        }
    });
});
