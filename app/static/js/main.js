function normalizeData(values) {
    return values.map(v => {
        let num = typeof v === 'string' ? parseFloat(v) : v;
        return isNaN(num) ? 0 : num;
    });
}

function createChart(elementId, data, title) {
    console.log(`Criando gráfico para ${title}`);
    console.log('Dados recebidos:', {
        dates: data.dates,
        values: data.values,
        length: data.dates.length
    });

    const trace = {
        x: data.dates,
        y: normalizeData(data.values),
        type: 'scatter',
        mode: 'lines',
        name: title,
        line: { color: '#2980b9', width: 2.5 }
    };

    // Estratégia para selecionar ticks com base no título
    let selectedTicks;
    if (title === 'IPCA') {
        // Para IPCA, selecione ticks em intervalos maiores
        selectedTicks = data.dates.filter((_, index) => index % 12 === 0);
    } else {
        // Para outros gráficos, mantenha o intervalo de 4
        selectedTicks = data.dates.filter((_, index) => index % 4 === 0);
    }
    
    console.log('Ticks selecionados para ' + title + ':', {
        selectedTicks: selectedTicks,
        totalTicks: selectedTicks.length,
        firstTick: selectedTicks[0],
        lastTick: selectedTicks[selectedTicks.length - 1]
    });

    const layout = {
        title: {
            text: title,
            font: { size: 14 }  // Reduzir tamanho do título para telas menores
        },
        xaxis: { 
            title: 'Período', 
            type: 'category',
            tickmode: 'array',
            tickvals: selectedTicks,
            ticktext: selectedTicks,
            tickangle: 45,
            tickfont: { size: 8 }  // Reduzir tamanho da fonte dos ticks
        },
        yaxis: { 
            title: data.unit || '',
            tickformat: '.2f',
            tickfont: { size: 10 }
        },
        margin: {
            l: 40,  // Reduzir margem esquerda
            r: 20,  // Reduzir margem direita
            b: 80,  // Aumentar margem inferior para rótulos
            t: 30   // Reduzir margem superior
        },
        responsive: true,
        autosize: true
    };

    console.log('Layout configurado para ' + title + ':', layout);

    const config = {
        responsive: true,
        displayModeBar: false  // Ocultar barra de ferramentas do Plotly
    };

    Plotly.newPlot(elementId, [trace], layout, config);
}





function loadChartData(endpoint, elementId, title) {
    console.log(`Carregando dados de ${title} do endpoint: ${endpoint}`);
    fetch(endpoint)
        .then(response => {
            console.log(`Resposta do ${title}:`, response);
            if (!response.ok) {
                console.error(`Erro na requisição de ${title}: ${response.status}`);
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(`Dados recebidos para ${title}:`, data);
            
            if (data && data.dates && data.values && data.dates.length > 0) {
                console.log(`Dados válidos para ${title}. Criando gráfico...`);
                console.log('Detalhes dos dados:', {
                    dates: data.dates,
                    values: data.values,
                    label: data.label,
                    unit: data.unit
                });
                createChart(elementId, data, title);
            } else {
                console.error(`Dados inválidos para ${title}:`, data);
            }
        })
        .catch(error => {
            console.error(`Erro completo ao carregar ${title}:`, error);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    loadChartData('/api/pib', 'pib-chart', 'PIB do Brasil (R$ Trilhôes)');
    loadChartData('/api/desocupacao', 'desocupacao-chart', 'Taxa de Desocupação');
    loadChartData('/api/ipca', 'ipca-chart', 'IPCA');
});