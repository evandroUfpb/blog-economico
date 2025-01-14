const normalizeData = (values, title) => {
    console.group(`🔍 Normalização de Dados para ${title}`);
    console.log('Valores originais:', values);
    
    // Tratamento específico para SELIC
    if (title.toLowerCase().includes('selic')) {
        const numericValues = values.map((v, index) => {
            let num = typeof v === 'string' ? parseFloat(v) : v;
            
            // Log detalhado para diagnóstico
            console.log(`Valor original [${index}]: ${v}, Valor numérico: ${num}`);
            
            // Conversão para porcentagem se for decimal muito pequeno
            if (num < 0.1) {  // Ajuste este limite conforme necessário
                const percentValue = parseFloat((num * 100).toFixed(2));
                console.log(`Convertido para %: ${percentValue}`);
                return percentValue;
            }
            
            return num;
        });

        console.log('Valores SELIC após normalização:', numericValues);
        console.groupEnd();
        return numericValues;
    }

    // Tratamento específico para IPCA
    if (title.toLowerCase().includes('ipca')) {
        const numericValues = values.map((v, index) => {
            let num = typeof v === 'string' ? parseFloat(v) : v;
            
            // Log detalhado para diagnóstico
            console.log(`Valor original [${index}]: ${v}, Valor numérico: ${num}`);
            
            // Conversão para porcentagem se for decimal muito pequeno
            if (num < 0.1) {  // Ajuste este limite conforme necessário
                const percentValue = parseFloat((num * 100).toFixed(2));
                console.log(`Convertido para %: ${percentValue}`);
                return percentValue;
            }
            
            return num;
        });

        console.log('Valores IPCA após normalização:', numericValues);
        console.groupEnd();
        return numericValues;
    }

    console.groupEnd();
    return values;
};

// Função para calcular range do eixo y
const calculateYRange = (values, title) => {
    console.group(`📊 Cálculo de Range para ${title}`);
    
    const normalizedValues = normalizeData(values, title);
    
    const yMin = Math.min(...normalizedValues);
    const yMax = Math.max(...normalizedValues);
    
    console.log(`Valores normalizados - Min: ${yMin}, Max: ${yMax}`);

    // Tratamentos específicos por tipo de gráfico
    if (title.toLowerCase().includes('selic') || title.toLowerCase().includes('ipca')) {
        // Ajuste mais preciso para SELIC e IPCA
        const range = yMax - yMin;
        const dynamicPadding = range > 0 ? range * 0.2 : 0.5;
        
        const calculatedRange = [
            Math.max(0, yMin - dynamicPadding), 
            yMax + dynamicPadding
        ];
        
        console.log(`Range calculado: [${calculatedRange[0]}, ${calculatedRange[1]}]`);
        console.groupEnd();
        return calculatedRange;
    }

    // Para outros gráficos
    const yPadding = (yMax - yMin) * 0.1;
    const calculatedRange = [yMin - yPadding, yMax + yPadding];
    
    console.log(`Range padrão: [${calculatedRange[0]}, ${calculatedRange[1]}]`);
    console.groupEnd();
    return calculatedRange;
};

  // Processamento de datas específico para Desocupação
let processedDates = data.dates;
let processedValues = data.values;

if (title.includes('Desocupação')) {
    const filteredDates = [];
    const filteredValues = [];

    data.dates.forEach((dateStr, index) => {
        // Manter o formato original 'YYYYMM'
        if (parseInt(dateStr.substring(0, 4)) >= 2012 && parseInt(dateStr.substring(4, 6)) % 3 === 1) {
            filteredDates.push(dateStr);
            filteredValues.push(data.values[index]);
        }
    });

    // Usar dados filtrados se houver resultados
    if (filteredDates.length > 0) {
        processedDates = filteredDates;
        processedValues = filteredValues;
    }

    console.log('🗓️ Processed Dates:', processedDates);
    console.log('📈 Processed Values:', processedValues);
}

// Configuração do eixo x
xaxis: {
    title: 'Período',
    type: 'date',
    tickformat: '%Y%m'
},

    // Normalizar valores
    const normalizedValues = normalizeData(processedValues, title);

    const trace = {
        x: processedDates,
        y: normalizedValues,
        type: 'scatter',
        mode: 'lines',
        name: data.label || title,
        line: {
            color: '#2980b9',
            width: 2.5
        }
    };

    const layout = {
        title: {
            text: title,
            font: { 
                size: 18, 
                color: '#333' 
            }
        },
        xaxis: {
            title: 'Período',
            type: 'date',
            tickformat: title.includes('Desocupação') ? '%Y-Q%q' : '%Y-%m',
            range: title.includes('Desocupação') 
                ? [new Date('2012-01-01'), new Date('2025-12-31')]
                : [new Date('2000-01-01'), new Date('2025-12-31')]
        },
        yaxis: {
            title: title.includes('IPCA') || title.includes('SELIC') 
                ? `${data.unit || 'Valor'} (%)` 
                : data.unit || 'Valor',
            range: calculateYRange(processedValues, title),
            tickformat: '.2f'
        },
        responsive: true
    };

    const config = {
        displayModeBar: false
    };

    try {
        Plotly.newPlot(elementId, [trace], layout, config);
    } catch (error) {
        console.error(`Erro ao renderizar gráfico ${elementId}:`, error);
    }

//
// Para cima foi modificado


/function loadChartData(endpoint, elementId, title) {
    console.log(`🔍 Carregando dados para ${elementId}`);
    console.log(`📡 Endpoint: ${endpoint}, Título: ${title}`);
    
    fetch(endpoint)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(`📦 Dados recebidos para ${elementId}:`, data);
            const chartElement = document.getElementById(elementId);
            
            if (chartElement) {
                console.log('🎯 Elemento do gráfico encontrado:', chartElement);
                
                // Verificar se os dados são válidos antes de criar o gráfico
                if (data && data.dates && data.dates.length > 0 && data.values && data.values.length > 0) {
                    console.log('✅ Dados válidos, criando gráfico...');
                    console.log('📊 Detalhes dos dados:', {
                        dates: data.dates,
                        values: data.values,
                        label: data.label,
                        unit: data.unit
                    });
                    
                    // Adicionar log para verificar a função createChart
                    console.log('🤔 Verificando createChart:', typeof createChart);
                    
                    createChart(elementId, data, title);
                } else {
                    console.warn(`❌ Dados inválidos para ${elementId}:`, data);
                    chartElement.innerHTML = `<p>Não foi possível carregar os dados para ${title}</p>`;
                }
            } else {
                console.warn(`🚨 Elemento ${elementId} não encontrado`);
            }
        })
        .catch(error => {
            console.error(`🔥 Erro ao carregar dados para ${elementId}:`, error);
            const chartElement = document.getElementById(elementId);
            if (chartElement) {
                chartElement.innerHTML = `<p>Erro ao carregar dados: ${error.message}</p>`;
            }
        });
}



// Funções de carregamento de dados individuais
function loadPIBData() {
    loadChartData('/api/pib', 'pib-chart-full', 'PIB Trimestral - Visão Detalhada');
}

function loadIPCAData() {
    loadChartData('/api/ipca', 'ipca-chart-full', 'IPCA - Visão Detalhada');
}

function loadSELICData() {
    loadChartData('/api/selic', 'selic-chart-full', 'Taxa SELIC - Visão Detalhada');
}

function loadDesocupacaoData() {
    loadChartData('/api/desocupacao', 'desocupacao-chart-full', 'Taxa de Desocupação - Visão Detalhada');
}

// Funções de carregamento de dados para página inicial
function loadPIBDataIndex() {
    loadChartData('/api/pib', 'pib-chart', 'PIB Trimestral');
}

function loadIPCADataIndex() {
    loadChartData('/api/ipca', 'ipca-chart', 'IPCA');
}

function loadSELICDataIndex() {
    loadChartData('/api/selic', 'selic-chart', 'Taxa SELIC');
}

function loadDesocupacaoDataIndex() {
    loadChartData('/api/desocupacao', 'desocupacao-chart', 'Taxa de Desocupação - Trimestral');
}

// Carregar dados quando a página inicial carregar
document.addEventListener('DOMContentLoaded', function() {
    console.log('Iniciando carregamento de dados');
    
    // Dados para dashboard
    loadPIBData();
    loadIPCAData();
    loadSELICData();
    loadDesocupacaoData();

    // Dados para página inicial
    loadPIBDataIndex();
    loadIPCADataIndex();
    loadSELICDataIndex();
    loadDesocupacaoDataIndex();
});
