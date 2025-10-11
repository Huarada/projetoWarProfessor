import { useState } from "react"
import { startGame } from '@/services/gameApi'

export default function NavBar({ onStart, disabled }) {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <header className="sticky top-0 z-50 bg-neutral-800/90 backdrop-blur border-b border-neutral-700">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        
        {/* Logo */}
        <div className="flex items-center gap-3">
          <img src="/src/assets/logo.png" alt="WAR Professor" className="h-10 w-10" />
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
          <span className="hover:text-white/90 cursor-default">Home</span>
          <button
            onClick={async () => {
              const { game_id, state } = await startGame()
              onStart(game_id, state)
            }}
            disabled={disabled}
            className="px-3 py-1 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
          >
            Iniciar jogo
          </button>
          <span className="hover:text-white/90 cursor-default">Aprenda Estratégia</span>
          <span className="hover:text-white/90 cursor-default">Comunidade</span>
          <span className="hover:text-white/90 cursor-default">Sobre</span>
          <span className="hover:text-white/90 cursor-default">Contato</span>
        </nav>

        {/* Botões Sign in / Register (desktop) */}
        <div className="hidden md:flex items-center gap-2">
          <button className="px-3 py-1 rounded-md border border-neutral-600 hover:bg-neutral-700">Sign in</button>
          <button className="px-3 py-1 rounded-md bg-neutral-100 text-neutral-900 hover:bg-white">Register</button>
        </div>


        {/* Botão fixo no mobile (sempre visível) */}
        <div className="flex md:hidden">
          <button
            onClick={async () => {
              const { game_id, state } = await startGame()
              onStart(game_id, state)
            }}
            disabled={disabled}
            className="px-3 py-1 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
          >
            Iniciar jogo
          </button>
        </div>


        {/* Botão hamburguer (apenas mobile) */}
        <button
          className="md:hidden px-3 py-2 rounded-md text-white hover:bg-neutral-700"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? "✖" : "☰"}
        </button>
      </div>

      {/* Menu mobile */}
      {menuOpen && (
        <div className="md:hidden flex flex-col items-center gap-3 p-4 bg-neutral-900 text-sm border-t border-neutral-700">
          <a
            className="px-3 py-1 rounded-full bg-orange-500/90 hover:bg-orange-500 font-medium"
            href="https://patreon.com/Huarada"
            target="_blank"
            rel="noreferrer"
          >
            Patreon
          </a>
          <span className="hover:text-white/90 cursor-default">Home</span>
          <button
            onClick={async () => {
              const { game_id, state } = await startGame()
              onStart(game_id, state)
            }}
            disabled={disabled}
            className="px-3 py-1 rounded-md bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50"
          >
            Iniciar jogo
          </button>
          <span className="hover:text-white/90 cursor-default">Aprenda Estratégia</span>
          <span className="hover:text-white/90 cursor-default">Comunidade</span>
          <span className="hover:text-white/90 cursor-default">Sobre</span>
          <span className="hover:text-white/90 cursor-default">Contato</span>
          <div className="flex gap-2 mt-2">
            <button className="px-3 py-1 rounded-md border border-neutral-600 hover:bg-neutral-700">Sign in</button>
            <button className="px-3 py-1 rounded-md bg-neutral-100 text-neutral-900 hover:bg-white">Register</button>
          </div>
        </div>
      )}
    </header>
  )
}

