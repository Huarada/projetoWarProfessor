import { useState } from "react"
import { startGame } from '@/services/gameApi'
import warLogo from '@/assets/war-logo.png'

export default function NavBar({ onStart, disabled }) {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-gray-400 border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center gap-3">
          <img src={warLogo} alt="WAR Professor" className="h-10 w-10" />
          <span className="sr-only">WAR Professor</span>
        </div>

        {/* Links (visíveis no desktop) */}
        <nav className="hidden md:flex items-center gap-6 text-sm">
          <a
            className="px-3 py-1 rounded-full bg-orange-500/90 hover:bg-orange-500 font-medium"
            href="https://patreon.com/Huarada"
            target="_blank"
            rel="noreferrer"
          >
            Patreon
          </a>
          <a href="/" className="hover:text-white/90">Home</a>
          <a href="https://pt.khanacademy.org/economics-finance-domain/microeconomics/perfect-competition-topic/game-theory/v/prisoners-dilemma-and-nash-equilibrium" className="hover:text-white/90">Aprenda Estratégia</a>
          <a href="https://discord.gg/jztUsSA9wX" className="hover:text-white/90">Comunidade</a>
          <a href="#sobrePlataforma" className="hover:text-white/90">Sobre</a>
          <a href="mailto:lucasharada@usp.br" className="hover:text-white/90">Contato</a>

          {/* assistir bots jogando (só bots) */}
          <button
            onClick={async () => {
              const { game_id, state } = await startGame()
              onStart(game_id, state)
            }}
            disabled={disabled}
            className="px-3 py-1 rounded-md bg-blue-600 hover:bg-blue-500 disabled:opacity-50"
          >
            Assistir Bots
          </button>

          {/* Novo botão: modo jogador humano */}
          <button
            onClick={async () => {
              const { game_id, state } = await startGame({ include_human: true })
              onStart(game_id, state)
            }}
            disabled={disabled}
            className="px-3 py-1 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
            title="Jogue controlando o primeiro jogador humano"
          >
            🎮 Iniciar Jogo
          </button>
        </nav>

        {/* Botões Sign in / Register (desktop) */}
        <div className="hidden md:flex items-center gap-2">
          <button className="px-3 py-1 rounded-md border border-neutral-600 hover:bg-neutral-700">Sign in</button>
          <button className="px-3 py-1 rounded-md bg-neutral-100 text-neutral-900 hover:bg-white">Register</button>
        </div>


        {/* Botão fixo no mobile (sempre visível) */}
        <div className="flex md:hidden">
        {/* assistir bots jogando (só bots) */}
        <button
          onClick={async () => {
            const { game_id, state } = await startGame()
            onStart(game_id, state)
          }}
          disabled={disabled}
          className="px-3 py-1 rounded-md bg-blue-600 hover:bg-blue-500 disabled:opacity-50"
        >
          Assistir Bots
        </button>

        {/* Novo botão: modo jogador humano */}
        <button
          onClick={async () => {
            const { game_id, state } = await startGame({ include_human: true })
            onStart(game_id, state)
          }}
          disabled={disabled}
          className="px-3 py-1 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
          title="Jogue controlando o primeiro jogador humano"
        >
          🎮 Iniciar Jogo
        </button>

        </div>


        {/* Botão hamburguer (apenas mobile) */}
        <button
          className="md:hidden px-3 py-2 rounded-md text-white bg-silver-500/90 hover:bg-neutral-700"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? "✖" : "☰"}
        </button>
      </div>

      {/* Menu mobile */}
      {menuOpen && (
          <div className="md:hidden fixed top-16 left-0 w-full flex flex-col items-center gap-3 p-4 bg-neutral-900 text-white border-t border-neutral-700 shadow-lg z-40 overflow-x-hidden">

          <a
            className="px-3 py-1 rounded-full bg-orange-500/90 hover:bg-orange-500 font-medium"
            href="https://patreon.com/Huarada"
            target="_blank"
            rel="noreferrer"
          >
            Patreon
          </a>
          <span className="hover:text-orange-400 cursor-default">Home</span>

          <button
            onClick={async () => {
              const { game_id, state } = await startGame()
              onStart(game_id, state)
            }}
            disabled={disabled}
            className="px-3 py-1 rounded-md bg-blue-600 hover:bg-blue-500 disabled:opacity-50"
          >
            Assistir Bots
          </button>

          <button
            onClick={async () => {
              const { game_id, state } = await startGame({ include_human: true })
              onStart(game_id, state)
            }}
            disabled={disabled}
            className="px-3 py-1 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
          >
            🎮 Iniciar Jogo
          </button>

          <span className="hover:text-orange-400 cursor-default">Aprenda Estratégia</span>
          <span className="hover:text-orange-400 cursor-default">Comunidade</span>
          <span className="hover:text-orange-400 cursor-default">Sobre</span>
          <span className="hover:text-orange-400 cursor-default">Contato</span>

          <div className="flex gap-2 mt-2">
            <button className="px-3 py-1 rounded-md border border-neutral-500 hover:bg-neutral-800">
              Sign in
            </button>
            <button className="px-3 py-1 rounded-md bg-neutral-200 text-neutral-900 hover:bg-neutral-300">
              Register
            </button>
          </div>
        </div>
      )}

    </header>
  )
}

