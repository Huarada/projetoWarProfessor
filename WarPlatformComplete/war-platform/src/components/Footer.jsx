export default function Footer() {
  return (
    <footer className="bg-neutral-800 border-t border-neutral-700">
      <div className="max-w-7xl mx-auto px-4 py-10 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="flex flex-col gap-4">
          <img src="/src/assets/logo.png" alt="logo" className="h-12 w-12" />
          <div className="flex items-center gap-3 opacity-80">
            <span className="i">X</span><span>Instagram</span><span>GitHub</span><span>LinkedIn</span>
          </div>
        </div>

        <div>
          <h3 className="font-semibold mb-3">Aprenda e Pratique</h3>
          <ul className="space-y-2 text-neutral-300">
            <li><span>Tutorial de como jogar WAR</span></li>
            <li><span>Teoria dos Jogos aplicada ao WAR</span></li>
            <li><span>Exercícios de tomada de decisão</span></li>
            <li><span>Estratégias de ataque e defesa</span></li>
          </ul>
        </div>

        <div>
          <h3 className="font-semibold mb-3">Ferramentas e Demonstrações</h3>
          <ul className="space-y-2 text-neutral-300">
            <li>Construção do Algoritmo Genético</li>
            <li>Histórico de partidas simuladas</li>
            <li>Construção do Mapa</li>
          </ul>
        </div>

        <div>
          <h3 className="font-semibold mb-3">Recursos e Comunidade</h3>
          <ul className="space-y-2 text-neutral-300">
            <li>Materiais para professores</li>
            <li>Artigos e tutoriais</li>
            <li>Comunidade (Discord)</li>
            <li>Projeto (GitHub)</li>
            <li>Licença MIT e termos</li>
            <li>Developers</li>
          </ul>
        </div>
      </div>
    </footer>
  )
}
