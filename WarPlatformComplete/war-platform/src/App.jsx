// src/App.jsx
import { useState } from 'react'
import Button from '@/components/ui/button.jsx'
import { Twitter, Instagram, Linkedin, Github } from 'lucide-react'
import warLogo from './assets/war-logo.png'
import worldMap from './assets/world-map.png'
import openSourceLogo from './assets/open-source-logo.png'
import './App.css'
import GameBoard from '@/components/GameBoard.jsx'
import { startGame } from '@/services/gameApi'
import NavBar from '@/components/NavBar'


function App() {
  const [gameId, setGameId] = useState(null)
  const [gameState, setGameState] = useState(null)

  // quando o jogo está rolando, mostramos o GameBoard
  if (gameId) {
    return (
      <div className="min-h-screen bg-neutral-900 text-neutral-100">
        <header className="bg-neutral-800 border-b border-neutral-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center gap-3">
            <img src={warLogo} alt="WAR Logo" className="h-10 w-10" />
            <span className="font-semibold">WAR Professor</span>
          </div>
        </header>
        <GameBoard
          gameId={gameId}
          gameState={gameState}
          setGameState={setGameState}
          onExit={() => { setGameId(null); setGameState(null) }}
        />
      </div>
    )
  }

  // Home (estrutura e links exatos)
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <NavBar
        onStart={(game_id, state) => {
          setGameId(game_id)
          setGameState(state)
        }}
        disabled={!!gameId}
      />

      {/* World Map Section */}
      <section className="bg-black py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <img id="mapaMundial" src={worldMap} alt="Mapa Mundial WAR" className="w-full h-auto" />
        </div>
      </section>

      {/* Footer Navigation */}
      <footer className="bg-gray-200 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Aprenda e Pratique */}
            <div>
              <h3 className="font-bold text-gray-900 mb-4">Aprenda e Pratique</h3>
              <ul className="space-y-2 text-gray-700">
                <li><a href="https://www.youtube.com/watch?v=gOH3lXcDrEA" className="hover:text-gray-900">Tutorial de como jogar WAR</a></li>
                <li><a href="https://pt.khanacademy.org/economics-finance-domain/microeconomics/perfect-competition-topic/game-theory/e/game-theory" className="hover:text-gray-900">Exercícios de tomada de decisão</a></li>
                <li><a href="https://github.com/Huarada/JupyterNotebookAlgoritmoWar" className="hover:text-gray-900">Estratégias de ataque e defesa</a></li>
              </ul>
            </div>

            {/* Ferramentas e Demonstrações */}
            <div>
              <h3 className="font-bold text-gray-900 mb-4">Ferramentas e Demonstrações</h3>
              <ul className="space-y-2 text-gray-700">
                <li><a href="https://github.com/Huarada/JupyterNotebookAlgoritmoWar" className="hover:text-gray-900">Construção do Algoritmo Genético</a></li>
                <li><a href="#" className="hover:text-gray-900">Histórico de partidas simuladas</a></li>
                <li><a href="#" className="hover:text-gray-900">Construção do Mapa</a></li>
              </ul>
            </div>

            {/* Recursos e Comunidade */}
            <div className="md:col-start-3">
              <h3 className="font-bold text-gray-900 mb-4">Recursos e Comunidade</h3>
              <ul className="space-y-2 text-gray-700">
                <li><a href="https://www.britannica.com/science/game-theory/Two-person-constant-sum-games" className="hover:text-gray-900">Materiais para professores e educadores</a></li>
                <li><a href="https://www.britannica.com/science/game-theory/Two-person-constant-sum-games" className="hover:text-gray-900">Artigos e tutoriais sobre Teoria dos Jogos</a></li>
                <li><a href="https://discord.gg/jztUsSA9wX" className="hover:text-gray-900">Comunidade (Discord)</a></li>
                <li><a href="https://github.com/Huarada/projetoWarProfessor" className="hover:text-gray-900">Projeto (GitHub)</a></li>
                <li><a href="#licenseForOpenSource" className="hover:text-gray-900">Licença MIT e termos de uso</a></li>
                <li><a href="https://www.linkedin.com/in/eng-lucas-harada/" className="hover:text-gray-900">Developers</a></li>
                <li><a href="mailto:lucasharada@usp.br" className="hover:text-gray-900">Contato/Suporte oficial</a></li>
              </ul>
            </div>
          </div>

          {/* Social Media Icons */}
          <div className="flex space-x-4 mt-8">
            <a href="https://x.com/LucasHarada5?t=UBWFBRSfWdpvMI72sj9Zsg&s=08"><Twitter className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
            <a href="https://www.instagram.com/lucas.harada.94?utm_source=qr&igsh=MTkxdjFrZ2N6bW1qcQ=="><Instagram className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
            <a href="https://github.com/Huarada"><Github className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
            <a href="https://www.linkedin.com/in/eng-lucas-harada/"><Linkedin className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
          </div>
        </div>
      </footer>

      {/* Sobre a Plataforma */}
      <section className="bg-gray-100 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 id="sobrePlataforma" className="text-4xl font-bold text-gray-900 mb-8">Sobre a Plataforma</h2>
          <div className="text-gray-700 space-y-4 text-left">
            <p>Este site é parte do Trabalho de Conclusão de Curso (TCC) de Lucas Harada na POLI-USP, orientado pelo Prof. Márcio Lobo Neto. O objetivo do projeto é tornar o ensino de estratégia e Teoria dos Jogos mais acessível, prático e divertido, utilizando o jogo WAR como ferramenta.</p>
            <p>O projeto nasceu a partir da falta de recursos lúdicos para explicar conceitos estratégicos de forma aplicada. A plataforma permite que estudantes, professores e entusiastas do jogo tenham acesso a um agente autônomo de IA, que utiliza Algoritmos Genéticos para treinar sua estratégia ao longo do tempo.</p>
            <p>Além da experiência de jogo, o agente explica suas jogadas e escolhas utilizando processamento de linguagem natural (NLP), tornando o aprendizado mais transparente e interativo.</p>
            <p>O código do agente será disponibilizado como open-source sob licença MIT, permitindo liberdade de uso e adaptação, sem responsabilidade do autor por usos indevidos.</p>
            <p>Este site é gratuito para uso educacional, com possibilidade de planos premium para funcionalidades avançadas. Acreditamos que o ensino de estratégia deve ser acessível, lúdico e envolvente para todos.</p>
          </div>
        </div>
      </section>

      {/* Como Jogar WAR */}
      <section className="bg-gray-200 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold text-gray-900 mb-8 text-center">Como Jogar WAR</h2>
          <div className="text-gray-700 space-y-6">
            <div>
              <h3 className="text-xl font-bold mb-2">1. Objetivo do Jogo</h3>
              <p>Cada jogador recebe uma missão secreta (como conquistar certos continentes ou eliminar um adversário). Quem cumprir sua missão primeiro, ou tiver mais territórios até a última rodada, vence.</p>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-2">2. Preparando o Tabuleiro</h3>
              <ul className="list-disc list-inside space-y-1 ml-4">
                <li>Cada jogador escolhe uma cor e pega seus exércitos.</li>
                <li>Os territórios são sorteados e distribuídos entre os jogadores.</li>
                <li>Cada jogador coloca uma tropa em cada território que ganhou.</li>
                <li>Depois, distribua o resto das tropas como quiser nos seus territórios.</li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-2">3. Como Funciona o Seu Turno</h3>
              <p>Seu turno tem três partes:</p>
              <div className="ml-4 space-y-2">
                <div>
                  <strong>a) Receber Novas Tropas</strong>
                  <p className="ml-4">No começo do turno, conte quantos territórios você tem. Divida por 2 (arredonde pra baixo) para saber quantas tropas novas recebe. Exemplo: 11 territórios → ganha 5 tropas.</p>
                </div>
                <div>
                  <strong>b) Colocar Tropas</strong>
                  <p className="ml-4">Coloque suas novas tropas em qualquer território que já seja seu.</p>
                </div>
                <div>
                  <strong>c) Atacar (opcional)</strong>
                  <p className="ml-4">Você pode atacar territórios vizinhos que pertencem a outros jogadores.</p>
                  <ul className="list-disc list-inside ml-8 space-y-1">
                    <li>Para atacar, escolha de onde vai atacar e para onde.</li>
                    <li>Use dados: quem ataca usa até 3 dados, quem defende até 2.</li>
                    <li>Quem tirar o maior número no dado ganha (empate é do defensor).</li>
                    <li>Se o atacante vencer, o defensor perde uma tropa.</li>
                    <li>Se o defensor perder todas as tropas, o atacante toma o território.</li>
                  </ul>
                </div>
                <div>
                  <strong>d) Mover Tropas</strong>
                  <p className="ml-4">No fim do seu turno, você pode mover tropas de um território para outro seu, desde que estejam conectados.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Comunidade */}
      <section className="bg-gray-300 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-8">COMUNIDADE</h2>
          <p className="text-gray-700 mb-4">Interaja com outros entusiastas de WAR, e com contribuidores do código Open-Source em nossa comunidade do Discord</p>
          <p className="text-gray-700"><a href="https://discord.gg/jztUsSA9wX" className="text-blue-600 hover:underline">link: https://discord.gg/jztUsSA9wX</a></p>
        </div>
      </section>

      {/* Projeto */}
      <section className="bg-gray-200 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-8">Projeto</h2>
          <p className="text-gray-700 mb-4">Gostaria de aprender mais sobre Algoritmos Genéticos e contribuir com nosso projeto Open-Source junto de outros desenvolvedores? Acesse nosso link do github</p>
          <p className="text-gray-700"><a href="https://github.com/Huarada/projetoWarProfessor" className="text-blue-600 hover:underline">Link: https://github.com/Huarada/projetoWarProfessor</a></p>
        </div>
      </section>

      {/* Algoritmo Genético */}
      <section className="bg-gray-300 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-8">Algoritmo Genético Implementado</h2>
          <p className="text-gray-700 mb-4">O código do algoritmo genético usado para os agentes autônomos jogarem WAR podem ser encontrado no seguinte repositório do Github</p>
          <p className="text-gray-700"><a href="https://github.com/Huarada/JupyterNotebookAlgoritmoWar" className="text-blue-600 hover:underline">Link: https://github.com/Huarada/JupyterNotebookAlgoritmoWar</a></p>
        </div>
      </section>

      {/* Licença OpenSource */}
      <section className="bg-gray-200 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-8">Licença OpenSource</h2>
          <p className="text-gray-700 mb-8">A licença usada no projeto de War usando algoritmo genético é a MIT License abaixo</p>
          <div id="licenseForOpenSource" className="bg-white p-8 rounded-lg shadow-lg text-left">
            <p className="text-center font-bold mb-4">Copyright 2025 Lucas Harada</p>
            <p className="text-sm text-gray-600 leading-relaxed">Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>
            <p className="text-sm text-gray-600 leading-relaxed mt-4">The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>
            <p className="text-sm text-gray-600 leading-relaxed mt-4">THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p>
          </div>
          <div className="mt-8">
            <img src={openSourceLogo} alt="Open Source Initiative" className="mx-auto h-32 w-32" />
          </div>
        </div>
      </section>

      {/* Contatos */}
      <section className="bg-gray-300 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-8">Contatos</h2>
          <div className="flex justify-center space-x-8">
            <a href="https://x.com/LucasHarada5?t=UBWFBRSfWdpvMI72sj9Zsg&s=08"><Twitter className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
            <a href="https://www.instagram.com/lucas.harada.94?utm_source=qr&igsh=MTkxdjFrZ2N6bW1qcQ=="><Instagram className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
            <a href="https://github.com/Huarada"><Github className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
            <a href="https://www.linkedin.com/in/eng-lucas-harada/"><Linkedin className="h-6 w-6 text-gray-600 hover:text-gray-900 cursor-pointer" /></a>
          </div>
        </div>
      </section>
    </div>
  )
}

export default App


