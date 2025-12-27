document.addEventListener("DOMContentLoaded", function () {

    // Vẽ biểu đồ doanh thu
    const dataEl = document.getElementById("chart-data");
    if (dataEl) {
        const labels = JSON.parse(dataEl.dataset.labels || "[]");
        const values = JSON.parse(dataEl.dataset.values || "[]");

        if (labels.length > 0) {
            const ctx = document.getElementById("revenueChart");
            if (ctx) {
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
            }
        }
    }

});