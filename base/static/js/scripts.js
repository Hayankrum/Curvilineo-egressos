const ctx = document.getElementById('salaChart').getContext('2d');
const salaChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: JSON.parse(document.getElementById('salaChart').dataset.labels),
        datasets: [
            {
                label: 'Tópicos',
                data: JSON.parse(document.getElementById('salaChart').dataset.topics),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            },
            {
                label: 'Respostas',
                data: JSON.parse(document.getElementById('salaChart').dataset.replies),
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});