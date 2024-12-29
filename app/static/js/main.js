/// Função para criar gráficos usando Plotly
function createChart(elementId, data, title, customConfig = {}) {
    const trace = {
        x: data.dates,
        y: data.values,
        type: 'scatter',
        mode: 'lines',
        name: data.label,
        line: {
            color: '#2980b9',
            width: 2.5,
            shape: 'spline'
        },
        hovertemplate: '%{y:.2f}<br>%{x}<extra></extra>'
    };
    
    // Configurações padrão para o eixo x
    const defaultXAxisConfig = {
        title: 'Período',
        tickangle: -45,
        gridcolor: '#f7f7f7',
        showgrid: true,
        zeroline: false,
        dtick: 'M48', //determina o intervalo de 4 anos (48 meses)
        tickformat: '%m/%Y',
        tickfont: { family: 'Arial', size: 11 }
    };

    // Configurações específicas para desocupação
    const desocupacaoXAxisConfig = title.includes('Desocupação') ? {
        ...defaultXAxisConfig,
        dtick: 'M3', // Intervalo de 3 meses (trimestral)
        tickformat: '%Y-Q%q' // Formato para mostrar trimestres
    } : defaultXAxisConfig;

    const layout = {
        title: {
            text: title,
            font: {
                size: 24
            }
        },
        xaxis: customConfig.xaxis || desocupacaoXAxisConfig,
        yaxis: {
            title: data.unit,
            gridcolor: '#eee'
        },
        paper_bgcolor: 'white',
        plot_bgcolor: 'white',
        margin: {
            l: 60,
            r: 30,
            b: 60,
            t: 80,
            pad: 4
        },
        showlegend: false
    };

    const config = {
        responsive: true,
        displayModeBar: false
    };

    Plotly.newPlot(elementId, [trace], layout, config);
}

// Função para carregar dados do PIB
function loadPIBData() {
    fetch('/api/pib')
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.error(data.message);
                return;
            }
            // Criar gráfico na página inicial
            if (document.getElementById('pib-chart')) {
                createChart('pib-chart', data, 'PIB Trimestral');
            }
            // Criar gráfico no dashboard
            if (document.getElementById('pib-chart-full')) {
                createChart('pib-chart-full', data, 'PIB Trimestral - Visão Detalhada');
            }
        })
        .catch(error => console.error('Erro ao carregar dados do PIB:', error));
}

// Função para carregar dados do IPCA
function loadIPCAData() {
    //linhas adicionadas para o cache
    const cacheKey = 'ipca_data';
    const cachedData = localStorage.getItem(cacheKey);
    const cacheExpiry = localStorage.getItem(cacheKey + '_expiry');
    
    if (cachedData && cacheExpiry && Date.now() < parseInt(cacheExpiry)) {
        createChart('ipca-chart', JSON.parse(cachedData), 'IPCA - Variação Mensal');
        return;
    }
    // fim das linhas adicionadas
    fetch('/api/ipca')
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.error(data.message);
                return;
            }
            if (document.getElementById('ipca-chart')) {
                createChart('ipca-chart', data, 'IPCA');
            }
            if (document.getElementById('ipca-chart-full')) {
                createChart('ipca-chart-full', data, 'IPCA - Visão Detalhada');
            }
        })
        .catch(error => console.error('Erro ao carregar dados do IPCA:', error));
}

// Função para carregar dados da SELIC
function loadSELICData() {
    fetch('/api/selic')
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.error(data.message);
                return;
            }
            if (document.getElementById('selic-chart')) {
                createChart('selic-chart', data, 'Taxa SELIC');
            }
            if (document.getElementById('selic-chart-full')) {
                createChart('selic-chart-full', data, 'Taxa SELIC - Visão Detalhada');
            }
        })
        .catch(error => console.error('Erro ao carregar dados da SELIC:', error));
}


// Função para carregar dados do câmbio
function loadCambioData() {
    fetch('/api/cambio')
        .then(response => response.json())
        .then(data => {
            createChart('cambio-chart', data, 'Taxa de Câmbio - PTAX');
        })
        .catch(error => {
            console.error('Erro ao carregar dados do câmbio:', error);
        });
}

// Função para carregar dados de Desocupação
function loadDesocupacaoData() {
    fetch('/api/desocupacao')
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.error(data.message);
                return;
            }
            // Criar gráfico na página inicial
            if (document.getElementById('desocupacao-chart')) {
                createChart('desocupacao-chart', data, 'Taxa de Desocupação - Trimestral');
            }
            // Criar gráfico no dashboard
            if (document.getElementById('desocupacao-chart-full')) {
                createChart('desocupacao-chart-full', data, 'Taxa de Desocupação - Visão Detalhada');
            }
        })
        .catch(error => console.error('Erro ao carregar dados de Desocupacao:', error));
}


// Carregar dados quando a página carregar
document.addEventListener('DOMContentLoaded',
    function() {
        //limpa cache local
        localStorage.clear();
        loadPIBData();
        loadIPCAData();
        loadSELICData();
        loadCambioData();
        loadDesocupacaoData();
    });