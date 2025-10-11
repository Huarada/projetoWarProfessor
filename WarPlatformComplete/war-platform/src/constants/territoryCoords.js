// src/constants/territoryCoords.js
// Coordenadas relativas (em %) sobre a imagem worldMap.png.
// Ajuste livremente para o seu mapa. Use o "Dev mode" do GameBoard para pegar coordenadas.
const COORDS = {
  // América do Norte
  'Ottawa' : { x: 22.4, y: 34.6 },
  'Mackenzie' : { x: 11.4, y: 24.6 },
  'Alasca': { x: 6, y: 23 },
  'Vancouver': { x: 11, y: 32 },
  'Labrador': { x: 25.6, y: 30.9 },
  'Groenlândia': { x: 35.6, y: 19.2 },
  'México': { x: 14.4, y: 52.5 },
  'Nova York': { x: 24.1, y: 39.3 },
  'Califórnia': { x: 11.0, y: 43.0 },

  // América do Sul
  'Venezuela': { x: 26.3, y: 61.2 },
  'Peru': { x: 23.2, y: 70.2 },
  'Brasil': { x: 30.7, y: 70.4},
  'Argentina': { x: 27.7, y: 78.6 },

  // Europa
  'Suécia' : { x: 49.5, y: 28.1 },
  'Polônia' : { x: 50.3, y: 34.8 },
  'Alemanha': { x: 47.5, y: 35.2 },
  'Islândia': { x: 41, y: 23 },
  'Inglaterra': { x: 44.8, y: 33.4 },
  'França' : { x: 46.3, y: 38.3 },

  // África
  'Sudão' : { x: 56.8, y: 57.3 },
  'Egito': { x: 54.7, y: 49.8 },
  'Congo': { x: 52.9, y: 61.8 },
  'África do Sul': { x: 52.2, y: 79.2 },
  'Madagascar': { x: 60.3, y: 73.6 },
  'Argélia' : { x: 43.3, y: 53.3 },

  // Ásia
  'Moscou' : { x: 53.9, y: 35.4 },
  'Vladivostok' : { x: 84.0, y: 20.8 },
  'Tchita' : { x: 70.9, y: 30.4 },
  'Omsk' : { x: 56.7, y: 30.1 },
  'Dudinka' : { x: 65.1, y: 27.4 },
  'Aral': { x: 63.9, y: 40.8 },
  'Oriente Médio': { x: 60.2, y: 50.5 },
  'Sibéria': { x: 77.5, y: 22.9 },
  'Mongólia': { x: 76.8, y: 36.1 },
  'China': { x: 79.0, y: 43.1 },
  'Japão': { x: 87.9, y: 43.9 },
  'Índia': { x: 70.0, y: 53.9 },
  'Vietnã' : { x: 80.5, y: 51.1 },

  // Oceania
  'Sumatra': { x: 78.3, y: 65.7 },
  'Nova Guiné': { x: 91.2, y: 67.1 },
  'Austrália' :  { x: 89.0, y: 78.9 },
  'Bornéu' : { x: 83.5, y: 61.6 },
};

// ⚠️ Qualquer território que não estiver aqui será mostrado na lista "Sem posição"
// dentro do painel lateral, pra você clicar no mapa (Dev mode) e anotar as coords.
export default COORDS;
